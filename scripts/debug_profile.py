"""Screenshot GitHub profile README and local SVGs; report image/layout bugs."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "debug"
OUT.mkdir(parents=True, exist_ok=True)


def git_sha() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT)
            .decode()
            .strip()
        )
    except Exception:  # noqa: BLE001
        return "local"


def main() -> None:
    sha = git_sha()
    report: dict = {"sha": sha, "gaps": [], "shotErrors": []}

    with sync_playwright() as p:
        browser = p.chromium.launch()

        local = browser.new_page(viewport={"width": 1100, "height": 900}, color_scheme="dark")
        assets = [
            ("hero", "hero-aurora.svg"),
            ("signal-deck", "signal-deck.svg"),
            ("metrics", "metrics-strip.svg"),
            ("intro", "intro-signal.svg"),
            ("label-featured", "label-featured.svg"),
            ("label-stack", "label-stack.svg"),
            ("more", "more-systems.svg"),
            ("stack", "stack-cinematic.svg"),
            ("card-ziffy", "card-ziffy.svg"),
            ("exp-ziffy", "exp-ziffy.svg"),
            ("cta-portfolio", "cta-portfolio.svg"),
        ]
        for name, file in assets:
            path = ROOT / "assets" / file
            if not path.exists():
                report["shotErrors"].append(f"missing:{file}")
                continue
            local.goto(path.as_uri(), wait_until="load", timeout=30000)
            local.wait_for_timeout(350)
            local.screenshot(path=str(OUT / f"local-{name}.png"))
            texts = local.evaluate(
                """() => [...document.querySelectorAll('text')]
                  .map(t => (t.textContent || '').trim())
                  .filter(Boolean)"""
            )
            report.setdefault("localTexts", {})[name] = texts

        # Local composite: signal deck alone is the mission+metrics unit
        more_titles = [
            t
            for t in report.get("localTexts", {}).get("more", [])
            if t not in {"MORE SYSTEMS", "SYSTEM"} and len(t) < 40
        ]
        report["moreTitles"] = more_titles
        report["suspectLongTitles"] = [t for t in more_titles if len(t) > 14]

        page = browser.new_page(viewport={"width": 1280, "height": 2600}, color_scheme="dark")
        page.goto("https://github.com/im-rihan", wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(9000)

        page.evaluate(
            """(sha) => {
              const article = document.querySelector('article');
              if (!article) return;
              article.querySelectorAll('img').forEach(img => {
                const src = img.getAttribute('src') || '';
                if (!/im-rihan\\/im-rihan.*assets\\/.*\\.svg/i.test(src)
                    && !/raw\\.githubusercontent\\.com\\/im-rihan\\/im-rihan/i.test(src)
                    && !src.includes('/assets/')) return;
                const m = src.match(/assets\\/[^?#\"']+\\.svg/);
                if (m) {
                  img.src = `https://raw.githubusercontent.com/im-rihan/im-rihan/main/${m[0]}?v=${sha}`;
                }
              });
            }""",
            sha,
        )
        page.wait_for_timeout(4500)

        details = page.locator("article details").first
        if details.count():
            details.click()
            page.wait_for_timeout(1000)

        page.screenshot(path=str(OUT / "full.png"), full_page=True)
        article = page.locator("article").first
        if article.count():
            article.screenshot(path=str(OUT / "readme.png"))

        live = page.evaluate(
            """() => {
              const article = document.querySelector('article');
              if (!article) return { error: 'no article' };
              const imgs = [...article.querySelectorAll('img')].map((img, i) => {
                const r = img.getBoundingClientRect();
                return {
                  i,
                  alt: img.alt || '',
                  src: (img.currentSrc || img.src || '').slice(0, 180),
                  naturalW: img.naturalWidth,
                  naturalH: img.naturalHeight,
                  displayW: Math.round(r.width),
                  displayH: Math.round(r.height),
                  top: Math.round(r.top + window.scrollY),
                  broken: img.complete && img.naturalWidth === 0,
                  loading: !img.complete,
                  visible: r.width > 0 && r.height > 0,
                };
              });
              // gap analysis between consecutive visible imgs in article
              const gaps = [];
              for (let i = 1; i < imgs.length; i++) {
                const prev = imgs[i - 1];
                const cur = imgs[i];
                if (!prev.visible || !cur.visible) continue;
                const gap = cur.top - (prev.top + prev.displayH);
                if (gap > 48) {
                  gaps.push({
                    between: [prev.alt.slice(0, 40), cur.alt.slice(0, 40)],
                    gapPx: gap,
                  });
                }
              }
              return {
                imgCount: imgs.length,
                broken: imgs.filter(x => x.broken).map(x => x.alt),
                zeroSize: imgs.filter(x => x.naturalW === 0 || x.displayW === 0).map(x => x.alt),
                stillLoading: imgs.filter(x => x.loading).map(x => x.alt),
                gaps,
                alts: imgs.map(x => x.alt),
                imgs,
              };
            }"""
        )
        report["live"] = live
        report["gaps"] = live.get("gaps", [])

        shots = [
            ("hero", 'article img[alt="Rihan Mohammed — Full Stack Developer"]'),
            ("signal-deck", 'article img[alt*="Mission brief"]'),
            ("stack", 'article img[alt="Cinematic tech stack matrix with skill icons"]'),
            ("more", 'article img[alt="More production systems"]'),
            ("label-featured", 'article img[alt="Featured"]'),
            ("label-stack", 'article img[alt="Stack"]'),
            ("label-experience", 'article img[alt="Experience"]'),
            ("label-activity", 'article img[alt="Activity"]'),
            ("activity-pacman", 'article img[alt*="Pac-Man"]'),
            ("activity-stats", 'article img[alt="GitHub Stats"]'),
            ("activity-streak", 'article img[alt="GitHub Streak"]'),
        ]
        for name, sel in shots:
            loc = page.locator(sel).first
            if loc.count():
                try:
                    loc.screenshot(path=str(OUT / f"{name}.png"))
                except Exception as exc:  # noqa: BLE001
                    report["shotErrors"].append(f"{name}: {exc}")
            else:
                report["shotErrors"].append(f"{name}: not found")

        browser.close()

    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    summary = {
        "sha": sha,
        "broken": report.get("live", {}).get("broken"),
        "zeroSize": report.get("live", {}).get("zeroSize"),
        "gaps": report.get("gaps"),
        "shotErrors": report.get("shotErrors"),
        "suspectLongTitles": report.get("suspectLongTitles"),
        "imgCount": report.get("live", {}).get("imgCount"),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
