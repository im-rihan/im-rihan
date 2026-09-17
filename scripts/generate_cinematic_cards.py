"""Generate cinematic isometric SVG cards + animated stack for the GitHub profile README."""
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
    # Centered title + bidirectional accent line (was left-aligned)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="56" viewBox="0 0 900 56" role="img">
  <defs>
    <linearGradient id="lineL" x1="100%" y1="0%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6"/>
      <stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="lineR" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6"/>
      <stop offset="70%" stop-color="#14b8a6" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="40" y="27" width="280" height="2" fill="url(#lineL)"/>
  <rect x="580" y="27" width="280" height="2" fill="url(#lineR)"/>
  <circle cx="328" cy="28" r="3" fill="#14b8a6">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="2.8s" repeatCount="indefinite"/>
  </circle>
  <circle cx="572" cy="28" r="3" fill="#f59e0b">
    <animate attributeName="opacity" values="1;0.4;1" dur="2.8s" repeatCount="indefinite"/>
  </circle>
  <text x="450" y="34" text-anchor="middle" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="18" font-weight="800" fill="#e2e8f0" letter-spacing="4">{escape(label.upper())}</text>
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
    delay: float = 0,
) -> None:
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
    <linearGradient id="sheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.18"/>
      <stop offset="55%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
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
  <ellipse cx="90" cy="50" rx="130" ry="70" fill="url(#glow)">
    <animate attributeName="opacity" values="0.7;1;0.7" dur="4s" begin="{delay}s" repeatCount="indefinite"/>
  </ellipse>
  <path d="M30 205 L210 185 L370 205 L190 225 Z" fill="#14b8a6" opacity="0.08"/>
  <g filter="url(#shadow)">
    <animateTransform attributeName="transform" type="translate" values="0 0; 0 -3; 0 0" dur="5s" begin="{delay}s" repeatCount="indefinite"/>
    <path d="M340 42 L370 58 L370 188 L340 172 Z" fill="url(#side)"/>
    <path d="M40 42 L70 26 L370 58 L340 42 Z" fill="url(#top)"/>
    <path d="M40 42 L340 42 L340 172 L40 172 Z" fill="url(#face)" stroke="{accent}" stroke-opacity="0.45"/>
    <rect x="40" y="42" width="300" height="130" fill="url(#sheen)">
      <animate attributeName="x" values="-260;340" dur="6s" begin="{delay}s" repeatCount="indefinite"/>
    </rect>
  </g>
  <rect x="40" y="42" width="300" height="3" fill="{accent}" opacity="0.85">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="3s" begin="{delay}s" repeatCount="indefinite"/>
  </rect>
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
    delay: float = 0,
) -> None:
    lines = ""
    y = 116
    for b in bullets[:3]:
        lines += f'<circle cx="58" cy="{y - 3}" r="2.6" fill="{accent}"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" begin="{delay}s" repeatCount="indefinite"/></circle>\n'
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
    <linearGradient id="sheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="48%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.16"/>
      <stop offset="52%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
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
  <ellipse cx="500" cy="36" rx="120" ry="70" fill="url(#orb)">
    <animate attributeName="opacity" values="0.65;1;0.65" dur="4.5s" begin="{delay}s" repeatCount="indefinite"/>
  </ellipse>
  <path d="M40 198 L290 180 L520 198 L270 216 Z" fill="{accent}" opacity="0.08"/>
  <g filter="url(#shadow)">
    <animateTransform attributeName="transform" type="translate" values="0 0; 0 -2; 0 0" dur="5.5s" begin="{delay}s" repeatCount="indefinite"/>
    <path d="M480 36 L520 54 L520 184 L480 166 Z" fill="url(#side)"/>
    <path d="M40 36 L80 18 L520 54 L480 36 Z" fill="url(#top)"/>
    <path d="M40 36 L480 36 L480 166 L40 166 Z" fill="url(#face)" stroke="{accent}" stroke-opacity="0.4"/>
    <rect x="40" y="36" width="440" height="130" fill="url(#sheen)">
      <animate attributeName="x" values="-400;480" dur="7s" begin="{delay}s" repeatCount="indefinite"/>
    </rect>
  </g>
  <rect x="40" y="36" width="8" height="130" fill="{accent}">
    <animate attributeName="opacity" values="0.55;1;0.55" dur="2.8s" begin="{delay}s" repeatCount="indefinite"/>
  </rect>
  <text x="64" y="58" font-family="JetBrains Mono, Consolas, monospace" font-size="10" font-weight="700" fill="{accent}" letter-spacing="2">EXPERIENCE</text>
  <text x="64" y="84" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="20" font-weight="800" fill="#f8fafc">{escape(role)}</text>
  <text x="64" y="104" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="13" font-weight="600" fill="#f59e0b">{escape(company)}  ·  {escape(period)}</text>
  {lines}
</svg>
"""
    (ASSETS / filename).write_text(svg, encoding="utf-8", newline="\n")
    print("wrote", filename)


def isometric_tile(cx: float, cy: float, label: str, accent: str, delay: float, size: float = 34) -> str:
    """Draw one isometric cube tile with floating animation."""
    hx, hy = size * 0.9, size * 0.52
    # diamond top
    top = f"M{cx} {cy - hy} L{cx + hx} {cy} L{cx} {cy + hy} L{cx - hx} {cy} Z"
    # left face
    left = f"M{cx - hx} {cy} L{cx} {cy + hy} L{cx} {cy + hy + size * 0.55} L{cx - hx} {cy + size * 0.55} Z"
    # right face
    right = f"M{cx + hx} {cy} L{cx} {cy + hy} L{cx} {cy + hy + size * 0.55} L{cx + hx} {cy + size * 0.55} Z"
    return f"""<g>
  <animateTransform attributeName="transform" type="translate" values="0 0; 0 -4; 0 0" dur="3.6s" begin="{delay}s" repeatCount="indefinite"/>
  <path d="{left}" fill="{accent}" fill-opacity="0.28"/>
  <path d="{right}" fill="{accent}" fill-opacity="0.45"/>
  <path d="{top}" fill="#0f172a" stroke="{accent}" stroke-width="1.2" stroke-opacity="0.85"/>
  <path d="{top}" fill="{accent}" fill-opacity="0.18">
    <animate attributeName="fill-opacity" values="0.12;0.32;0.12" dur="3.6s" begin="{delay}s" repeatCount="indefinite"/>
  </path>
  <text x="{cx}" y="{cy + 4}" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="9" font-weight="700" fill="#e2e8f0">{escape(label)}</text>
</g>"""


def stack_panel() -> None:
    # Centered cinematic stack: isometric tech lattice + fluent chips
    tiles = [
        (150, 95, "React", "#14b8a6", 0.0),
        (250, 95, "Next", "#22d3ee", 0.25),
        (350, 95, "TS", "#38bdf8", 0.5),
        (450, 95, "Nest", "#2dd4bf", 0.75),
        (550, 95, "Node", "#34d399", 1.0),
        (650, 95, "PHP", "#f59e0b", 1.25),
        (750, 95, "Py", "#a3e635", 1.5),
        (200, 155, "MySQL", "#14b8a6", 0.35),
        (300, 155, "Redis", "#f43f5e", 0.6),
        (400, 155, "AWS", "#f59e0b", 0.85),
        (500, 155, "Docker", "#22d3ee", 1.1),
        (600, 155, "Vercel", "#e2e8f0", 1.35),
        (700, 155, "CF", "#f97316", 1.6),
    ]
    tile_svg = "\n".join(isometric_tile(*t) for t in tiles)
    fluent = [
        "LangChain",
        "LangGraph",
        "MCP",
        "Typesense",
        "BullMQ",
        "FastAPI",
        "CatBoost",
        "Puppeteer",
        "Leaflet",
    ]
    chip_w = 86
    start_x = (900 - len(fluent) * (chip_w + 8) + 8) / 2
    chips = []
    for i, name in enumerate(fluent):
        x = start_x + i * (chip_w + 8)
        chips.append(
            f"""<g>
  <rect x="{x}" y="212" width="{chip_w}" height="26" rx="8" fill="rgba(20,184,166,0.12)" stroke="#14b8a6" stroke-opacity="0.45">
    <animate attributeName="stroke-opacity" values="0.3;0.85;0.3" dur="3s" begin="{i * 0.15}s" repeatCount="indefinite"/>
  </rect>
  <text x="{x + chip_w / 2}" y="229" text-anchor="middle" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="10" font-weight="600" fill="#99f6e4">{escape(name)}</text>
</g>"""
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="260" viewBox="0 0 900 260" role="img">
  <title>Tech stack</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="rim" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0"/>
      <stop offset="50%" stop-color="#14b8a6"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="wash" cx="50%" cy="35%" r="55%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="900" height="260" rx="18" fill="url(#void)"/>
  <ellipse cx="450" cy="100" rx="280" ry="90" fill="url(#wash)">
    <animate attributeName="opacity" values="0.6;1;0.6" dur="5s" repeatCount="indefinite"/>
  </ellipse>
  <rect x="1" y="1" width="898" height="3" rx="1.5" fill="url(#rim)">
    <animate attributeName="opacity" values="0.45;1;0.45" dur="3.5s" repeatCount="indefinite"/>
  </rect>
  <!-- perspective grid floor -->
  <g stroke="#14b8a6" stroke-opacity="0.15" fill="none">
    <path d="M80 190 L450 150 L820 190"/>
    <path d="M140 210 L450 160 L760 210"/>
    <path d="M220 230 L450 170 L680 230"/>
  </g>
  <text x="450" y="36" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="700" fill="#14b8a6" letter-spacing="3">STACK MATRIX</text>
  {tile_svg}
  <text x="450" y="205" text-anchor="middle" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="10" font-weight="600" fill="#64748b" letter-spacing="1.5">FLUENT SYSTEMS</text>
  {''.join(chips)}
</svg>
"""
    (ASSETS / "stack-cinematic.svg").write_text(svg, encoding="utf-8", newline="\n")
    print("wrote stack-cinematic.svg")


def enhance_metrics() -> None:
    path = ASSETS / "metrics-strip.svg"
    if not path.exists():
        return
    # rewrite with subtle pulse on amber metric
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="96" viewBox="0 0 900 96" role="img" aria-labelledby="mTitle mDesc">
  <title id="mTitle">Profile metrics</title>
  <desc id="mDesc">4+ years, 9+ systems, 60+ webhooks, 2 companies</desc>
  <defs>
    <linearGradient id="panel" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <linearGradient id="accentLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f766e" stop-opacity="0"/>
      <stop offset="50%" stop-color="#14b8a6"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="900" height="96" rx="14" fill="url(#panel)" stroke="rgba(20,184,166,0.28)" stroke-width="1"/>
  <rect x="1" y="1" width="898" height="3" rx="1.5" fill="url(#accentLine)" opacity="0.85">
    <animate attributeName="opacity" values="0.45;1;0.45" dur="3.2s" repeatCount="indefinite"/>
  </rect>
  <g font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" text-anchor="middle">
    <g transform="translate(112.5, 0)">
      <text x="0" y="42" font-size="28" font-weight="800" fill="#14b8a6">4+<animate attributeName="opacity" values="0.75;1;0.75" dur="4s" repeatCount="indefinite"/></text>
      <text x="0" y="66" font-size="11" font-weight="600" fill="#94a3b8" letter-spacing="1.5">YEARS</text>
    </g>
    <line x1="225" y1="24" x2="225" y2="72" stroke="rgba(148,163,184,0.25)" stroke-width="1"/>
    <g transform="translate(337.5, 0)">
      <text x="0" y="42" font-size="28" font-weight="800" fill="#14b8a6">9+</text>
      <text x="0" y="66" font-size="11" font-weight="600" fill="#94a3b8" letter-spacing="1.5">SYSTEMS</text>
    </g>
    <line x1="450" y1="24" x2="450" y2="72" stroke="rgba(148,163,184,0.25)" stroke-width="1"/>
    <g transform="translate(562.5, 0)">
      <text x="0" y="42" font-size="28" font-weight="800" fill="#f59e0b">60+<animate attributeName="opacity" values="0.7;1;0.7" dur="2.4s" repeatCount="indefinite"/></text>
      <text x="0" y="66" font-size="11" font-weight="600" fill="#94a3b8" letter-spacing="1.5">WEBHOOKS</text>
    </g>
    <line x1="675" y1="24" x2="675" y2="72" stroke="rgba(148,163,184,0.25)" stroke-width="1"/>
    <g transform="translate(787.5, 0)">
      <text x="0" y="42" font-size="28" font-weight="800" fill="#14b8a6">2</text>
      <text x="0" y="66" font-size="11" font-weight="600" fill="#94a3b8" letter-spacing="1.5">COMPANIES</text>
    </g>
  </g>
</svg>
"""
    path.write_text(svg, encoding="utf-8", newline="\n")
    print("wrote metrics-strip.svg")


if __name__ == "__main__":
    section_label("label-featured.svg", "Featured")
    section_label("label-experience.svg", "Experience")
    section_label("label-stack.svg", "Stack")

    featured_card(
        filename="card-ziffy.svg",
        eyebrow="Live product",
        title="Ziffy.ai",
        stack="Next.js 15 · React 19 · SSE · Vercel",
        blurb="AI investor platform with streaming NLP search, ISR SEO listings, and DSCR / pre-approval flows.",
        accent="#14b8a6",
        delay=0,
    )
    featured_card(
        filename="card-appi.svg",
        eyebrow="Core API",
        title="appi",
        stack="NestJS · Redis · LangGraph · Typesense",
        blurb="Production REST API for auth, property search, loans, CRM sync, and MCP-ready AI tooling.",
        accent="#22d3ee",
        delay=0.4,
    )
    featured_card(
        filename="card-integrations.svg",
        eyebrow="Integrations",
        title="Hub + Pricer",
        stack="PHP 8.3 · Puppeteer · AWS Lambda",
        blurb="60+ webhooks, 12+ AI agent tools, and live rates from 11 Non-QM / DSCR lender portals.",
        accent="#f59e0b",
        delay=0.8,
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
        delay=0.2,
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
        delay=0.6,
    )

    stack_panel()
    enhance_metrics()
