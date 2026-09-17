"""Generate cinematic teal-aurora SVG cards for the GitHub profile README."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def wrap_text(text: str, width: int = 52) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if len(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:3]


def featured_card(
    *,
    filename: str,
    eyebrow: str,
    title: str,
    stack: str,
    blurb: str,
    accent: str = "#14b8a6",
) -> None:
    blurb_lines = wrap_text(blurb, 50)
    blurb_svg = "\n".join(
        f'<text x="34" y="{138 + i * 18}" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="12" fill="#94a3b8">{escape(line)}</text>'
        for i, line in enumerate(blurb_lines)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="380" height="210" viewBox="0 0 380 210" role="img">
  <title>{escape(title)}</title>
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="55%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#0b1220"/>
    </linearGradient>
    <linearGradient id="glass" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.02"/>
    </linearGradient>
    <radialGradient id="glow" cx="18%" cy="20%" r="55%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="edge" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0"/>
      <stop offset="40%" stop-color="{accent}"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.7"/>
    </linearGradient>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>
  <rect width="380" height="210" rx="18" fill="url(#bg)"/>
  <ellipse cx="70" cy="40" rx="120" ry="70" fill="url(#glow)" filter="url(#soft)"/>
  <path d="M24 168 L190 148 L356 168 L190 188 Z" fill="#14b8a6" opacity="0.08"/>
  <path d="M24 168 L190 148 L356 168" fill="none" stroke="{accent}" stroke-opacity="0.35" stroke-width="1"/>
  <rect x="14" y="14" width="352" height="182" rx="14" fill="url(#glass)" stroke="rgba(20,184,166,0.35)" stroke-width="1"/>
  <rect x="14" y="14" width="352" height="3" rx="1.5" fill="url(#edge)"/>
  <g stroke="{accent}" stroke-width="1.4" fill="none" opacity="0.55">
    <path d="M26 42 L26 28 L40 28"/>
    <path d="M340 28 L354 28 L354 42"/>
    <path d="M26 168 L26 182 L40 182"/>
    <path d="M340 182 L354 182 L354 168"/>
  </g>
  <text x="34" y="52" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="700" fill="{accent}" letter-spacing="1.8">{escape(eyebrow.upper())}</text>
  <text x="34" y="84" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="20" font-weight="800" fill="#f1f5f9">{escape(title)}</text>
  <text x="34" y="108" font-family="JetBrains Mono, Consolas, monospace" font-size="10" fill="#f59e0b">{escape(stack)}</text>
  {blurb_svg}
</svg>
"""
    (ASSETS / filename).write_text(svg, encoding="utf-8", newline="\n")
    print("wrote", filename)


def experience_card(
    *,
    filename: str,
    role: str,
    company: str,
    period: str,
    bullets: list[str],
    accent: str = "#14b8a6",
) -> None:
    lines = ""
    y = 118
    for b in bullets[:3]:
        lines += f'<circle cx="42" cy="{y - 3}" r="2.5" fill="{accent}"/>\n'
        lines += f'<text x="54" y="{y}" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="12" fill="#cbd5e1">{escape(b)}</text>\n'
        y += 22

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="560" height="200" viewBox="0 0 560 200" role="img">
  <title>{escape(role)} - {escape(company)}</title>
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="panel" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.05"/>
    </linearGradient>
    <radialGradient id="orb" cx="88%" cy="18%" r="40%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <filter id="blur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>
  </defs>
  <rect width="560" height="200" rx="18" fill="url(#bg)"/>
  <ellipse cx="480" cy="40" rx="110" ry="70" fill="url(#orb)" filter="url(#blur)"/>
  <!-- perspective plate -->
  <path d="M28 176 L280 156 L532 176 L280 196 Z" fill="#14b8a6" opacity="0.07"/>
  <rect x="16" y="16" width="528" height="168" rx="14" fill="url(#panel)" stroke="rgba(20,184,166,0.32)"/>
  <rect x="16" y="16" width="6" height="168" rx="3" fill="{accent}"/>
  <text x="40" y="48" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="700" fill="{accent}" letter-spacing="1.6">EXPERIENCE</text>
  <text x="40" y="78" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="20" font-weight="800" fill="#f8fafc">{escape(role)}</text>
  <text x="40" y="100" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="13" font-weight="600" fill="#f59e0b">{escape(company)}  ·  {escape(period)}</text>
  {lines}
</svg>
"""
    (ASSETS / filename).write_text(svg, encoding="utf-8", newline="\n")
    print("wrote", filename)


def section_label(filename: str, label: str) -> None:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="48" viewBox="0 0 900 48" role="img">
  <defs>
    <linearGradient id="line" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6"/>
      <stop offset="70%" stop-color="#14b8a6" stop-opacity="0"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="900" height="48" fill="transparent"/>
  <text x="0" y="30" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="18" font-weight="800" fill="#e2e8f0" letter-spacing="2">{escape(label.upper())}</text>
  <rect x="160" y="24" width="720" height="2" fill="url(#line)"/>
</svg>
"""
    (ASSETS / filename).write_text(svg, encoding="utf-8", newline="\n")
    print("wrote", filename)


if __name__ == "__main__":
    section_label("label-featured.svg", "Featured")
    section_label("label-experience.svg", "Experience")

    featured_card(
        filename="card-ziffy.svg",
        eyebrow="Live product",
        title="Ziffy.ai",
        stack="Next.js 15 · React 19 · SSE · Vercel",
        blurb="AI investor platform with streaming NLP search, ISR SEO listings, and DSCR / pre-approval flows.",
        accent="#14b8a6",
    )
    featured_card(
        filename="card-appi.svg",
        eyebrow="Core API",
        title="appi",
        stack="NestJS · Redis · LangGraph · Typesense",
        blurb="Production REST API for auth, property search, loans, CRM sync, and MCP-ready AI tooling.",
        accent="#22d3ee",
    )
    featured_card(
        filename="card-integrations.svg",
        eyebrow="Integrations",
        title="Hub + Pricer",
        stack="PHP 8.3 · Puppeteer · AWS Lambda",
        blurb="60+ webhooks, 12+ AI agent tools, and live rates from 11 Non-QM / DSCR lender portals.",
        accent="#f59e0b",
    )

    experience_card(
        filename="exp-ziffy.svg",
        role="Full Stack Engineer",
        company="Ziffy.ai",
        period="Jan 2025 - Present · Remote",
        bullets=[
            "Next.js 15 / React 19 dual-brand frontend on Vercel",
            "AI property search with SSE streaming + Typesense",
            "SEO listings, DSCR calculators, pre-approval portal",
        ],
        accent="#14b8a6",
    )
    experience_card(
        filename="exp-homeabroad.svg",
        role="Full Stack Developer",
        company="HomeAbroad Inc.",
        period="Apr 2022 - Present · Remote",
        bullets=[
            "NestJS API - auth, search, loans, CRM, LangGraph/MCP",
            "PHP 8.3 hub - 60+ webhooks and 12+ AI agent tools",
            "Lambda pricer, CatBoost AVM, AWS to Hetzner cutover",
        ],
        accent="#f59e0b",
    )
