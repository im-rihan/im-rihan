"""Generate cinematic isometric SVG cards for the GitHub profile README."""
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


def wrap_text(text: str, width: int = 42) -> list[str]:
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


def section_label(filename: str, label: str) -> None:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="52" viewBox="0 0 900 52" role="img">
  <defs>
    <linearGradient id="line" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6"/>
      <stop offset="55%" stop-color="#14b8a6" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <text x="0" y="32" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="18" font-weight="800" fill="#e2e8f0" letter-spacing="3">{escape(label.upper())}</text>
  <rect x="170" y="26" width="700" height="2" fill="url(#line)"/>
  <circle cx="170" cy="27" r="3" fill="#14b8a6"/>
</svg>
"""
    (ASSETS / filename).write_text(svg, encoding="utf-8", newline="\n")
    print("wrote", filename)


def featured_card(
    *,
    filename: str,
    eyebrow: str,
    title: str,
    stack: str,
    blurb: str,
    accent: str,
) -> None:
    # Isometric card: top face + right extrusion + bottom shelf for depth
    lines = wrap_text(blurb, 40)
    text = "\n".join(
        f'<text x="48" y="{132 + i * 17}" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="11.5" fill="#94a3b8">{escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="240" viewBox="0 0 400 240" role="img">
  <title>{escape(title)}</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0b1220"/>
    </linearGradient>
    <linearGradient id="face" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#122033"/>
      <stop offset="55%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#0b1524"/>
    </linearGradient>
    <linearGradient id="side" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#0f766e" stop-opacity="0.25"/>
    </linearGradient>
    <linearGradient id="top" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.12"/>
    </linearGradient>
    <radialGradient id="glow" cx="20%" cy="18%" r="50%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="160%">
      <feDropShadow dx="0" dy="14" stdDeviation="10" flood-color="#000000" flood-opacity="0.55"/>
    </filter>
  </defs>
  <rect width="400" height="240" fill="url(#void)"/>
  <ellipse cx="90" cy="50" rx="130" ry="70" fill="url(#glow)"/>
  <!-- floor plane -->
  <path d="M30 205 L210 185 L370 205 L190 225 Z" fill="{accent}" opacity="0.08"/>
  <g filter="url(#shadow)">
    <!-- right extrusion (depth) -->
    <path d="M340 42 L370 58 L370 188 L340 172 Z" fill="url(#side)"/>
    <!-- top bevel -->
    <path d="M40 42 L70 26 L370 58 L340 42 Z" fill="url(#top)"/>
    <!-- main face -->
    <path d="M40 42 L340 42 L340 172 L40 172 Z" fill="url(#face)" stroke="{accent}" stroke-opacity="0.45"/>
  </g>
  <rect x="40" y="42" width="300" height="3" fill="{accent}" opacity="0.85"/>
  <g stroke="{accent}" stroke-width="1.3" fill="none" opacity="0.65">
    <path d="M52 58 L52 50 L62 50"/>
    <path d="M318 50 L328 50 L328 58"/>
    <path d="M52 156 L52 164 L62 164"/>
    <path d="M318 164 L328 164 L328 156"/>
  </g>
  <text x="58" y="72" font-family="JetBrains Mono, Consolas, monospace" font-size="10" font-weight="700" fill="{accent}" letter-spacing="2">{escape(eyebrow.upper())}</text>
  <text x="58" y="100" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="22" font-weight="800" fill="#f8fafc">{escape(title)}</text>
  <text x="58" y="120" font-family="JetBrains Mono, Consolas, monospace" font-size="10" fill="#f59e0b">{escape(stack)}</text>
  {text}
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
    accent: str,
) -> None:
    lines = ""
    y = 116
    for b in bullets[:3]:
        lines += f'<circle cx="58" cy="{y - 3}" r="2.6" fill="{accent}"/>\n'
        lines += f'<text x="70" y="{y}" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="12" fill="#cbd5e1">{escape(b)}</text>\n'
        y += 22

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="560" height="220" viewBox="0 0 560 220" role="img">
  <title>{escape(role)} - {escape(company)}</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0b1220"/>
    </linearGradient>
    <linearGradient id="face" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#132033"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="side" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.2"/>
    </linearGradient>
    <linearGradient id="top" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.1"/>
    </linearGradient>
    <radialGradient id="orb" cx="90%" cy="12%" r="35%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-15%" y="-15%" width="140%" height="160%">
      <feDropShadow dx="0" dy="12" stdDeviation="9" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
  </defs>
  <rect width="560" height="220" fill="url(#void)"/>
  <ellipse cx="500" cy="36" rx="120" ry="70" fill="url(#orb)"/>
  <path d="M40 198 L290 180 L520 198 L270 216 Z" fill="{accent}" opacity="0.08"/>
  <g filter="url(#shadow)">
    <path d="M480 36 L520 54 L520 184 L480 166 Z" fill="url(#side)"/>
    <path d="M40 36 L80 18 L520 54 L480 36 Z" fill="url(#top)"/>
    <path d="M40 36 L480 36 L480 166 L40 166 Z" fill="url(#face)" stroke="{accent}" stroke-opacity="0.4"/>
  </g>
  <rect x="40" y="36" width="8" height="130" fill="{accent}"/>
  <text x="64" y="58" font-family="JetBrains Mono, Consolas, monospace" font-size="10" font-weight="700" fill="{accent}" letter-spacing="2">EXPERIENCE</text>
  <text x="64" y="84" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="20" font-weight="800" fill="#f8fafc">{escape(role)}</text>
  <text x="64" y="104" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="13" font-weight="600" fill="#f59e0b">{escape(company)}  ·  {escape(period)}</text>
  {lines}
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
