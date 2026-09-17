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
    report: dict = {"sha": sha}

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # --- Local asset truth (no CDN cache) ---
        local = browser.new_page(viewport={"width": 1100, "height": 900}, color_scheme="dark")
        assets = [
            ("hero", ROOT / "assets" / "hero-aurora.svg"),
            ("intro", ROOT / "assets" / "intro-signal.svg"),
            ("more", ROOT / "assets" / "more-systems.svg"),
            ("stack", ROOT / "assets" / "stack-cinematic.svg"),
            ("metrics", ROOT / "assets" / "metrics-strip.svg"),
            ("card-ziffy", ROOT / "assets" / "card-ziffy.svg"),
            ("exp-ziffy", ROOT / "assets" / "exp-ziffy.svg"),
            ("cta-portfolio", ROOT / "assets" / "cta-portfolio.svg"),
        ]
        for name, path in assets:
            url = path.as_uri()
            local.goto(url, wait_until="load", timeout=30000)
            local.wait_for_timeout(400)
            local.screenshot(path=str(OUT / f"local-{name}.png"))
            # OCR-ish: extract visible text nodes from SVG
            texts = local.evaluate(
                """() => [...document.querySelectorAll('text')]
                  .map(t => (t.textContent || '').trim())
                  .filter(Boolean)"""
            )
            report.setdefault("localTexts", {})[name] = texts

        # Truncation heuristic: title texts longer than ~14 chars in more cards
        more_titles = [
            t
            for t in report["localTexts"].get("more", [])
            if t not in {"MORE SYSTEMS", "SYSTEM"} and len(t) < 40
        ]
        report["moreTitles"] = more_titles
        report["suspectLongTitles"] = [t for t in more_titles if len(t) > 14]

        # --- Live GitHub (cache-bust raw SVG URLs) ---
        page = browser.new_page(viewport={"width": 1280, "height": 2200}, color_scheme="dark")
        page.goto("https://github.com/im-rihan", wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(8000)

        page.evaluate(
            """(sha) => {
              const article = document.querySelector('article');
              if (!article) return;
              article.querySelectorAll('img').forEach(img => {
                const src = img.getAttribute('src') || '';
                if (!/im-rihan\\/im-rihan.*assets\\/.*\\.svg/i.test(src)
                    && !/raw\\.githubusercontent\\.com\\/im-rihan\\/im-rihan/i.test(src)
                    && !src.includes('/assets/')) return;
                // rewrite to raw + bust
                let file = src;
                const m = src.match(/assets\\/[^?#\"']+\\.svg/);
                if (m) {
                  file = `https://raw.githubusercontent.com/im-rihan/im-rihan/main/${m[0]}?v=${sha}`;
                  img.src = file;
                }
              });
            }""",
            sha,
        )
        page.wait_for_timeout(4000)

        details = page.locator("article details").first
        if details.count():
            details.click()
            page.wait_for_timeout(1200)

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
                  src: (img.currentSrc || img.src || '').slice(0, 160),
                  naturalW: img.naturalWidth,
                  naturalH: img.naturalHeight,
                  displayW: Math.round(r.width),
                  displayH: Math.round(r.height),
                  broken: img.complete && img.naturalWidth === 0,
                  loading: !img.complete,
                  visible: r.width > 0 && r.height > 0,
                };
              });
              return {
                imgCount: imgs.length,
                broken: imgs.filter(x => x.broken).map(x => x.alt),
                zeroSize: imgs.filter(x => x.naturalW === 0 || x.displayW === 0).map(x => x.alt),
                stillLoading: imgs.filter(x => x.loading).map(x => x.alt),
                alts: imgs.map(x => x.alt),
                imgs,
              };
            }"""
        )
        report["live"] = live

        shots = [
            ("hero", 'article img[alt="Rihan Mohammed — Full Stack Developer"]'),
            ("intro", 'article img[alt*="fintech"]'),
            ("stack", 'article img[alt="Cinematic tech stack matrix with skill icons"]'),
            ("more", 'article img[alt="More production systems"]'),
            ("metrics", 'article img[alt*="years"]'),
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
                    report.setdefault("shotErrors", []).append(f"{name}: {exc}")
            else:
                report.setdefault("shotErrors", []).append(f"{name}: not found ({sel})")

        browser.close()

    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in report if k != "live"}, indent=2))
    live = report.get("live", {})
    print(
        json.dumps(
            {
                "broken": live.get("broken"),
                "zeroSize": live.get("zeroSize"),
                "stillLoading": live.get("stillLoading"),
                "imgCount": live.get("imgCount"),
                "alts": live.get("alts"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
