"""Preview connect strip locally."""
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "debug"
OUT.mkdir(parents=True, exist_ok=True)


def uri(name: str) -> str:
    return (ROOT / "assets" / name).as_uri()


def main() -> None:
    html = f"""<!doctype html>
<html><body style="margin:0;background:#0b1220;display:flex;flex-direction:column;align-items:center;gap:14px;padding:24px;font-family:sans-serif">
  <img src="{uri("intro-signal.svg")}" width="900"/>
  <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center">
    <img src="{uri("cta-portfolio.svg")}" height="68"/>
    <img src="{uri("cta-linkedin.svg")}" height="68"/>
    <img src="{uri("cta-email.svg")}" height="68"/>
    <img src="{uri("cta-available.svg")}" height="68"/>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center">
    <img src="{uri("chip-casestudy.svg")}" height="34"/>
    <img src="{uri("chip-live.svg")}" height="34"/>
    <img src="{uri("chip-appi.svg")}" height="34"/>
    <img src="{uri("chip-pricer.svg")}" height="34"/>
  </div>
</body></html>"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1100, "height": 500}, color_scheme="dark")
        page.set_content(html)
        page.wait_for_timeout(900)
        page.screenshot(path=str(OUT / "connect-preview.png"), full_page=True)
        browser.close()
    print("wrote assets/debug/connect-preview.png")


if __name__ == "__main__":
    main()
