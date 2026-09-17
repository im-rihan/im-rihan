"""Generate cinematic SVGs: hero, stack with icons, more-systems, cards."""
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
    """HUD section header with aurora panel background."""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="64" viewBox="0 0 900 64" role="img">
  <title>{escape(label)}</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/><stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <radialGradient id="wash" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rim" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0"/>
      <stop offset="50%" stop-color="#14b8a6"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="lineL" x1="100%" y1="0%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6"/><stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="lineR" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6"/>
      <stop offset="70%" stop-color="#14b8a6" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="900" height="64" rx="14" fill="url(#void)" stroke="rgba(20,184,166,0.22)"/>
  <ellipse cx="450" cy="32" rx="220" ry="40" fill="url(#wash)">
    <animate attributeName="opacity" values="0.55;1;0.55" dur="4.5s" repeatCount="indefinite"/>
  </ellipse>
  <rect x="1" y="1" width="898" height="2" fill="url(#rim)">
    <animate attributeName="opacity" values="0.35;1;0.35" dur="3.2s" repeatCount="indefinite"/>
  </rect>
  <g stroke="#14b8a6" stroke-width="1.1" fill="none" opacity="0.4">
    <path d="M14 14 H28 V28"/><path d="M886 14 H872 V28"/><path d="M14 50 H28 V36"/><path d="M886 50 H872 V36"/>
  </g>
  <rect x="48" y="31" width="250" height="2" fill="url(#lineL)"/>
  <rect x="602" y="31" width="250" height="2" fill="url(#lineR)"/>
  <circle cx="312" cy="32" r="3" fill="#14b8a6">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="2.8s" repeatCount="indefinite"/>
  </circle>
  <circle cx="588" cy="32" r="3" fill="#f59e0b">
    <animate attributeName="opacity" values="1;0.4;1" dur="2.8s" repeatCount="indefinite"/>
  </circle>
  <text x="450" y="38" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="800" fill="#e2e8f0" letter-spacing="4">{escape(label.upper())}</text>
</svg>
"""
    (ASSETS / filename).write_text(svg, encoding="utf-8", newline="\n")
    print("wrote", filename)


# Minimal brand-mark icons (self-contained paths) for stack tiles
ICONS = {
    "react": '<circle cx="0" cy="0" r="3" fill="#61dafb"/><ellipse cx="0" cy="0" rx="12" ry="4.5" fill="none" stroke="#61dafb" stroke-width="1.4" transform="rotate(0)"/><ellipse cx="0" cy="0" rx="12" ry="4.5" fill="none" stroke="#61dafb" stroke-width="1.4" transform="rotate(60)"/><ellipse cx="0" cy="0" rx="12" ry="4.5" fill="none" stroke="#61dafb" stroke-width="1.4" transform="rotate(120)"/>',
    "next": '<path d="M-8 8 V-8 H-4 L8 6 V-8 H12 V8 H8 L-4 -6 V8 Z" fill="#e2e8f0"/>',
    "ts": '<rect x="-10" y="-10" width="20" height="20" rx="3" fill="#3178c6"/><text x="0" y="4" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" font-weight="800" fill="#fff">TS</text>',
    "nest": '<path d="M0 -11 C6 -11 10 -6 10 0 C10 7 4 11 0 11 C-2 11 -4 10 -5 8 C-2 10 2 8 2 3 C2 -2 -2 -4 -5 -2 C-7 -6 -4 -11 0 -11 Z" fill="#e0234e"/>',
    "node": '<path d="M0 -12 L10 -6 V6 L0 12 L-10 6 V-6 Z" fill="none" stroke="#68a063" stroke-width="2"/><text x="0" y="4" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" font-weight="800" fill="#68a063">JS</text>',
    "php": '<ellipse cx="0" cy="0" rx="13" ry="8" fill="#777bb4"/><text x="0" y="3.5" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" font-weight="800" fill="#fff">php</text>',
    "py": '<path d="M-2 -10 H2 C8 -10 10 -6 10 -2 V2 H2 C-4 2 -6 6 -6 10 H-10 C-10 2 -6 -2 -2 -2 H6 V-6 H-2 C-6 -6 -6 -10 -2 -10 Z" fill="#3776ab"/><circle cx="-4" cy="-6" r="1.2" fill="#ffd43b"/><circle cx="4" cy="6" r="1.2" fill="#3776ab"/>',
    "mysql": '<path d="M-10 6 Q-10 -8 0 -8 Q10 -8 10 6" fill="none" stroke="#00758f" stroke-width="2.2"/><ellipse cx="0" cy="6" rx="10" ry="3.5" fill="#f29111"/>',
    "redis": '<path d="M-12 2 L0 -8 L12 2 L0 10 Z" fill="#dc382d"/><path d="M-12 2 L0 6 L12 2" fill="none" stroke="#fff" stroke-width="1" opacity="0.5"/>',
    "aws": '<path d="M-11 4 Q0 12 11 4" fill="none" stroke="#ff9900" stroke-width="2.2" stroke-linecap="round"/><text x="0" y="-1" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" font-weight="800" fill="#e2e8f0">aws</text>',
    "docker": '<rect x="-9" y="-2" width="5" height="5" fill="#2496ed"/><rect x="-3" y="-2" width="5" height="5" fill="#2496ed"/><rect x="3" y="-2" width="5" height="5" fill="#2496ed"/><rect x="-3" y="-8" width="5" height="5" fill="#2496ed"/><path d="M-12 4 H12" stroke="#2496ed" stroke-width="2"/>',
    "vercel": '<path d="M0 -9 L10 9 H-10 Z" fill="#e2e8f0"/>',
    "cf": '<path d="M-12 2 H4 C8 2 10 0 10 -3 C10 -7 6 -9 2 -8 C1 -12 -5 -12 -8 -9 C-12 -9 -13 -4 -12 2 Z" fill="#f38020"/>',
    "langchain": '<circle cx="-5" cy="0" r="5" fill="none" stroke="#1c3c3c" stroke-width="2"/><circle cx="5" cy="0" r="5" fill="none" stroke="#14b8a6" stroke-width="2"/><path d="M-1 0 H1" stroke="#f59e0b" stroke-width="2"/>',
    "fastapi": '<circle cx="0" cy="0" r="10" fill="#009688"/><path d="M-2 -6 L6 0 L-2 6 Z" fill="#fff"/>',
    "puppeteer": '<circle cx="0" cy="-2" r="7" fill="none" stroke="#00d8a2" stroke-width="2"/><circle cx="-2.5" cy="-3" r="1.3" fill="#00d8a2"/><circle cx="2.5" cy="-3" r="1.3" fill="#00d8a2"/><path d="M-4 6 Q0 10 4 6" fill="none" stroke="#00d8a2" stroke-width="1.5"/>',
    "leaflet": '<path d="M0 -10 C6 -10 10 -4 10 0 C10 6 0 12 0 12 C0 12 -10 6 -10 0 C-10 -4 -6 -10 0 -10 Z" fill="#199900"/><circle cx="0" cy="-1" r="3" fill="#fff"/>',
    "typesense": '<circle cx="-2" cy="-2" r="7" fill="none" stroke="#d4ff52" stroke-width="2.2"/><path d="M3 3 L9 9" stroke="#d4ff52" stroke-width="2.4" stroke-linecap="round"/><circle cx="-2" cy="-2" r="2" fill="#d4ff52"/>',
    "catboost": '<rect x="-10" y="-10" width="20" height="20" rx="4" fill="#ffcc00"/><path d="M-6 4 L0 -6 L6 4 Z" fill="#1a1a1a"/>',
    "mcp": '<rect x="-11" y="-8" width="22" height="16" rx="3" fill="none" stroke="#22d3ee" stroke-width="1.8"/><circle cx="-4" cy="0" r="2.2" fill="#22d3ee"/><circle cx="4" cy="0" r="2.2" fill="#22d3ee"/><path d="M-2 0 H2" stroke="#f59e0b" stroke-width="1.6"/>',
}


def isometric_tile(cx: float, cy: float, label: str, icon_key: str, accent: str, delay: float, size: float = 36) -> str:
    hx, hy = size * 0.95, size * 0.55
    top = f"M{cx} {cy - hy} L{cx + hx} {cy} L{cx} {cy + hy} L{cx - hx} {cy} Z"
    left = f"M{cx - hx} {cy} L{cx} {cy + hy} L{cx} {cy + hy + size * 0.55} L{cx - hx} {cy + size * 0.55} Z"
    right = f"M{cx + hx} {cy} L{cx} {cy + hy} L{cx} {cy + hy + size * 0.55} L{cx + hx} {cy + size * 0.55} Z"
    icon = ICONS.get(icon_key, f'<text text-anchor="middle" y="4" font-size="9" fill="#e2e8f0">{escape(label[:2])}</text>')
    return f"""<g>
  <animateTransform attributeName="transform" type="translate" values="0 0; 0 -5; 0 0" dur="3.8s" begin="{delay}s" repeatCount="indefinite"/>
  <path d="{left}" fill="{accent}" fill-opacity="0.3"/>
  <path d="{right}" fill="{accent}" fill-opacity="0.48"/>
  <path d="{top}" fill="#0b1220" stroke="{accent}" stroke-width="1.2" stroke-opacity="0.9"/>
  <path d="{top}" fill="{accent}" fill-opacity="0.14">
    <animate attributeName="fill-opacity" values="0.1;0.28;0.1" dur="3.8s" begin="{delay}s" repeatCount="indefinite"/>
  </path>
  <g transform="translate({cx}, {cy - 2}) scale(0.85)">{icon}</g>
  <text x="{cx}" y="{cy + hy + size * 0.55 + 14}" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="10" font-weight="700" fill="#cbd5e1">{escape(label)}</text>
</g>"""


def featured_card(*, filename, eyebrow, title, stack, blurb, accent, delay=0.0):
    lines = wrap_text(blurb, 40)
    text = "\n".join(
        f'<text x="48" y="{132 + i * 17}" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="11.5" fill="#94a3b8">{escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="240" viewBox="0 0 400 240" role="img">
  <title>{escape(title)}</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#020617"/><stop offset="100%" stop-color="#0b1220"/></linearGradient>
    <linearGradient id="face" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#122033"/><stop offset="100%" stop-color="#0b1524"/></linearGradient>
    <linearGradient id="side" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{accent}" stop-opacity="0.55"/><stop offset="100%" stop-color="#0f766e" stop-opacity="0.25"/></linearGradient>
    <linearGradient id="top" x1="0%" y1="100%" x2="100%" y2="0%"><stop offset="0%" stop-color="{accent}" stop-opacity="0.22"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0.12"/></linearGradient>
    <linearGradient id="sheen" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#fff" stop-opacity="0"/><stop offset="50%" stop-color="#fff" stop-opacity="0.16"/><stop offset="100%" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <radialGradient id="glow" cx="20%" cy="18%" r="50%"><stop offset="0%" stop-color="{accent}" stop-opacity="0.45"/><stop offset="100%" stop-color="{accent}" stop-opacity="0"/></radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="14" stdDeviation="10" flood-color="#000" flood-opacity="0.55"/></filter>
  </defs>
  <rect width="400" height="240" fill="url(#void)"/>
  <ellipse cx="90" cy="50" rx="130" ry="70" fill="url(#glow)"><animate attributeName="opacity" values="0.7;1;0.7" dur="4s" begin="{delay}s" repeatCount="indefinite"/></ellipse>
  <path d="M30 205 L210 185 L370 205 L190 225 Z" fill="#14b8a6" opacity="0.08"/>
  <g filter="url(#shadow)">
    <animateTransform attributeName="transform" type="translate" values="0 0; 0 -3; 0 0" dur="5s" begin="{delay}s" repeatCount="indefinite"/>
    <path d="M340 42 L370 58 L370 188 L340 172 Z" fill="url(#side)"/>
    <path d="M40 42 L70 26 L370 58 L340 42 Z" fill="url(#top)"/>
    <path d="M40 42 L340 42 L340 172 L40 172 Z" fill="url(#face)" stroke="{accent}" stroke-opacity="0.45"/>
    <rect x="40" y="42" width="300" height="130" fill="url(#sheen)"><animate attributeName="x" values="-260;340" dur="6s" begin="{delay}s" repeatCount="indefinite"/></rect>
  </g>
  <rect x="40" y="42" width="300" height="3" fill="{accent}" opacity="0.85"><animate attributeName="opacity" values="0.5;1;0.5" dur="3s" begin="{delay}s" repeatCount="indefinite"/></rect>
  <text x="58" y="72" font-family="JetBrains Mono, Consolas, monospace" font-size="10" font-weight="700" fill="{accent}" letter-spacing="2">{escape(eyebrow.upper())}</text>
  <text x="58" y="100" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="22" font-weight="800" fill="#f8fafc">{escape(title)}</text>
  <text x="58" y="120" font-family="JetBrains Mono, Consolas, monospace" font-size="10" fill="#f59e0b">{escape(stack)}</text>
  {text}
</svg>
"""
    (ASSETS / filename).write_text(svg, encoding="utf-8", newline="\n")
    print("wrote", filename)


def experience_card(*, filename, role, company, period, bullets, accent, delay=0.0):
    lines = ""
    y = 116
    for b in bullets[:3]:
        lines += f'<circle cx="58" cy="{y-3}" r="2.6" fill="{accent}"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.4s" begin="{delay}s" repeatCount="indefinite"/></circle>\n'
        lines += f'<text x="70" y="{y}" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="12" fill="#cbd5e1">{escape(b)}</text>\n'
        y += 22
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="560" height="220" viewBox="0 0 560 220" role="img">
  <title>{escape(role)} - {escape(company)}</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#020617"/><stop offset="100%" stop-color="#0b1220"/></linearGradient>
    <linearGradient id="face" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#132033"/><stop offset="100%" stop-color="#0f172a"/></linearGradient>
    <linearGradient id="side" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{accent}" stop-opacity="0.6"/><stop offset="100%" stop-color="{accent}" stop-opacity="0.2"/></linearGradient>
    <linearGradient id="top" x1="0%" y1="100%" x2="100%" y2="0%"><stop offset="0%" stop-color="{accent}" stop-opacity="0.28"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0.1"/></linearGradient>
    <linearGradient id="sheen" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#fff" stop-opacity="0"/><stop offset="50%" stop-color="#fff" stop-opacity="0.14"/><stop offset="100%" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <radialGradient id="orb" cx="90%" cy="12%" r="35%"><stop offset="0%" stop-color="{accent}" stop-opacity="0.5"/><stop offset="100%" stop-color="{accent}" stop-opacity="0"/></radialGradient>
    <filter id="shadow" x="-15%" y="-15%" width="140%" height="160%"><feDropShadow dx="0" dy="12" stdDeviation="9" flood-color="#000" flood-opacity="0.5"/></filter>
  </defs>
  <rect width="560" height="220" fill="url(#void)"/>
  <ellipse cx="500" cy="36" rx="120" ry="70" fill="url(#orb)"><animate attributeName="opacity" values="0.65;1;0.65" dur="4.5s" begin="{delay}s" repeatCount="indefinite"/></ellipse>
  <path d="M40 198 L290 180 L520 198 L270 216 Z" fill="{accent}" opacity="0.08"/>
  <g filter="url(#shadow)">
    <animateTransform attributeName="transform" type="translate" values="0 0; 0 -2; 0 0" dur="5.5s" begin="{delay}s" repeatCount="indefinite"/>
    <path d="M480 36 L520 54 L520 184 L480 166 Z" fill="url(#side)"/>
    <path d="M40 36 L80 18 L520 54 L480 36 Z" fill="url(#top)"/>
    <path d="M40 36 L480 36 L480 166 L40 166 Z" fill="url(#face)" stroke="{accent}" stroke-opacity="0.4"/>
    <rect x="40" y="36" width="440" height="130" fill="url(#sheen)"><animate attributeName="x" values="-400;480" dur="7s" begin="{delay}s" repeatCount="indefinite"/></rect>
  </g>
  <rect x="40" y="36" width="8" height="130" fill="{accent}"><animate attributeName="opacity" values="0.55;1;0.55" dur="2.8s" begin="{delay}s" repeatCount="indefinite"/></rect>
  <text x="64" y="58" font-family="JetBrains Mono, Consolas, monospace" font-size="10" font-weight="700" fill="{accent}" letter-spacing="2">EXPERIENCE</text>
  <text x="64" y="84" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="20" font-weight="800" fill="#f8fafc">{escape(role)}</text>
  <text x="64" y="104" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="13" font-weight="600" fill="#f59e0b">{escape(company)}  ·  {escape(period)}</text>
  {lines}
</svg>
"""
    (ASSETS / filename).write_text(svg, encoding="utf-8", newline="\n")
    print("wrote", filename)


def more_systems() -> None:
    """Cinematic expanded 'more systems' panel — replaces ugly markdown table."""
    items = [
        ("ha-realtor", "Agent / MLO dashboards", "Leaflet maps", "#14b8a6"),
        ("pipelines", "Multi-source scrape", "MySQL / Typesense", "#22d3ee"),
        ("Rental AVM", "CatBoost rent model", "FastAPI · DuckDB", "#f59e0b"),
        ("estimate-lib", "Shared DSCR / fees", "liquidity library", "#a78bfa"),
        ("portfolio", "Case studies · status", "blog · R3F", "#34d399"),
    ]
    cards = []
    gap = 14
    w = 164
    total = len(items) * w + (len(items) - 1) * gap
    start = (920 - total) / 2
    for i, (title, line1, line2, accent) in enumerate(items):
        x = start + i * (w + gap)
        cards.append(
            f"""<g>
  <animateTransform attributeName="transform" type="translate" values="0 0; 0 -3; 0 0" dur="4s" begin="{i * 0.2}s" repeatCount="indefinite"/>
  <path d="M{x+w-12} 52 L{x+w+6} 64 L{x+w+6} 178 L{x+w-12} 166 Z" fill="{accent}" fill-opacity="0.35"/>
  <path d="M{x} 52 L{x+14} 40 L{x+w+6} 64 L{x+w-12} 52 Z" fill="{accent}" fill-opacity="0.22"/>
  <rect x="{x}" y="52" width="{w-12}" height="114" rx="12" fill="#0f172a" stroke="{accent}" stroke-opacity="0.55"/>
  <rect x="{x}" y="52" width="{w-12}" height="3" fill="{accent}">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="2.8s" begin="{i * 0.2}s" repeatCount="indefinite"/>
  </rect>
  <text x="{x + (w-12)/2}" y="78" text-anchor="middle" font-family="JetBrains Mono,Consolas,monospace" font-size="9" font-weight="700" fill="{accent}" letter-spacing="1.5">SYSTEM</text>
  <text x="{x + (w-12)/2}" y="104" text-anchor="middle" font-family="Inter,Segoe UI,sans-serif" font-size="13" font-weight="800" fill="#f1f5f9">{escape(title)}</text>
  <text x="{x + (w-12)/2}" y="128" text-anchor="middle" font-family="Inter,Segoe UI,sans-serif" font-size="10" fill="#94a3b8">{escape(line1)}</text>
  <text x="{x + (w-12)/2}" y="144" text-anchor="middle" font-family="Inter,Segoe UI,sans-serif" font-size="10" fill="#94a3b8">{escape(line2)}</text>
</g>"""
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="220" viewBox="0 0 920 220" role="img">
  <title>More systems</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <radialGradient id="wash" cx="50%" cy="35%" r="55%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rim" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0"/>
      <stop offset="50%" stop-color="#14b8a6"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="920" height="220" rx="16" fill="url(#void)" stroke="rgba(20,184,166,0.22)"/>
  <ellipse cx="460" cy="90" rx="280" ry="70" fill="url(#wash)">
    <animate attributeName="opacity" values="0.55;1;0.55" dur="5s" repeatCount="indefinite"/>
  </ellipse>
  <rect x="1" y="1" width="918" height="3" fill="url(#rim)">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="3s" repeatCount="indefinite"/>
  </rect>
  <g stroke="#14b8a6" stroke-width="1.1" fill="none" opacity="0.35">
    <path d="M14 14 H30 V30"/><path d="M906 14 H890 V30"/><path d="M14 206 H30 V190"/><path d="M906 206 H890 V190"/>
  </g>
  <text x="460" y="32" text-anchor="middle" font-family="JetBrains Mono,Consolas,monospace" font-size="11" font-weight="700" fill="#14b8a6" letter-spacing="3">MORE SYSTEMS</text>
  <path d="M60 200 L460 182 L860 200" fill="none" stroke="#14b8a6" stroke-opacity="0.2"/>
  {''.join(cards)}
</svg>
"""
    (ASSETS / "more-systems.svg").write_text(svg, encoding="utf-8", newline="\n")
    print("wrote more-systems.svg")


def stack_panel() -> None:
    tiles = [
        (120, 88, "React", "react", "#61dafb", 0.0),
        (220, 88, "Next.js", "next", "#e2e8f0", 0.2),
        (320, 88, "TS", "ts", "#3178c6", 0.4),
        (420, 88, "NestJS", "nest", "#e0234e", 0.6),
        (520, 88, "Node", "node", "#68a063", 0.8),
        (620, 88, "PHP", "php", "#777bb4", 1.0),
        (720, 88, "Python", "py", "#3776ab", 1.2),
        (170, 168, "MySQL", "mysql", "#00758f", 0.3),
        (270, 168, "Redis", "redis", "#dc382d", 0.5),
        (370, 168, "AWS", "aws", "#ff9900", 0.7),
        (470, 168, "Docker", "docker", "#2496ed", 0.9),
        (570, 168, "Vercel", "vercel", "#e2e8f0", 1.1),
        (670, 168, "CF", "cf", "#f38020", 1.3),
        (770, 168, "FastAPI", "fastapi", "#009688", 1.5),
    ]
    # Centered fluent chips: icon above label, both centered in pill
    fluent = [
        ("LangChain", "langchain", "#14b8a6"),
        ("Puppeteer", "puppeteer", "#00d8a2"),
        ("Leaflet", "leaflet", "#199900"),
        ("Typesense", "typesense", "#d4ff52"),
        ("CatBoost", "catboost", "#ffcc00"),
        ("MCP", "mcp", "#22d3ee"),
    ]
    tile_svg = "\n".join(isometric_tile(*t) for t in tiles)
    chip_w = 118
    gap = 12
    total = len(fluent) * chip_w + (len(fluent) - 1) * gap
    start = (900 - total) / 2
    fluent_svg = []
    for i, (label, key, accent) in enumerate(fluent):
        x = start + i * (chip_w + gap) + chip_w / 2
        icon = ICONS.get(key, "")
        fluent_svg.append(
            f"""<g transform="translate({x}, 252)">
  <rect x="{-chip_w/2}" y="-22" width="{chip_w}" height="44" rx="12" fill="rgba(15,23,42,0.95)" stroke="{accent}" stroke-opacity="0.55">
    <animate attributeName="stroke-opacity" values="0.3;0.95;0.3" dur="3s" begin="{i*0.15}s" repeatCount="indefinite"/>
  </rect>
  <g transform="translate(0, -6) scale(0.62)">{icon}</g>
  <text x="0" y="16" text-anchor="middle" font-family="Inter,Segoe UI,sans-serif" font-size="11" font-weight="600" fill="#e2e8f0">{escape(label)}</text>
</g>"""
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300" role="img">
  <title>Tech stack</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#020617"/><stop offset="100%" stop-color="#0f172a"/></linearGradient>
    <linearGradient id="rim" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#14b8a6" stop-opacity="0"/><stop offset="50%" stop-color="#14b8a6"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/></linearGradient>
    <radialGradient id="wash" cx="50%" cy="35%" r="55%"><stop offset="0%" stop-color="#14b8a6" stop-opacity="0.18"/><stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="900" height="300" rx="18" fill="url(#void)" stroke="rgba(20,184,166,0.22)"/>
  <ellipse cx="450" cy="110" rx="300" ry="90" fill="url(#wash)"><animate attributeName="opacity" values="0.55;1;0.55" dur="5s" repeatCount="indefinite"/></ellipse>
  <ellipse cx="180" cy="240" rx="160" ry="50" fill="#f59e0b" fill-opacity="0.05"/>
  <rect x="1" y="1" width="898" height="3" fill="url(#rim)"><animate attributeName="opacity" values="0.4;1;0.4" dur="3.2s" repeatCount="indefinite"/></rect>
  <g stroke="#14b8a6" stroke-width="1.1" fill="none" opacity="0.35">
    <path d="M14 14 H30 V30"/><path d="M886 14 H870 V30"/><path d="M14 286 H30 V270"/><path d="M886 286 H870 V270"/>
  </g>
  <g stroke="#14b8a6" stroke-opacity="0.14" fill="none">
    <path d="M70 210 L450 175 L830 210"/>
    <path d="M140 235 L450 190 L760 235"/>
  </g>
  <text x="450" y="32" text-anchor="middle" font-family="JetBrains Mono,Consolas,monospace" font-size="11" font-weight="700" fill="#14b8a6" letter-spacing="3">STACK MATRIX</text>
  {tile_svg}
  {''.join(fluent_svg)}
</svg>
"""
    (ASSETS / "stack-cinematic.svg").write_text(svg, encoding="utf-8", newline="\n")
    print("wrote stack-cinematic.svg")


def hero_banner() -> None:
    """3D cinematic hero — extruded glass plate, parallax aurora, scanline, particles."""
    particles = []
    for i, (x, y, r, d) in enumerate(
        [
            (180, 70, 1.8, 0),
            (320, 50, 1.2, 0.5),
            (520, 90, 2.0, 1.0),
            (700, 60, 1.4, 1.5),
            (860, 100, 1.6, 0.8),
            (980, 45, 1.3, 2.0),
            (240, 200, 1.5, 1.2),
            (1100, 180, 1.7, 0.3),
        ]
    ):
        particles.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#14b8a6" opacity="0.7"><animate attributeName="cy" values="{y};{y-12};{y}" dur="{4+i*0.3}s" begin="{d}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.25;0.9;0.25" dur="{3+i*0.2}s" begin="{d}s" repeatCount="indefinite"/></circle>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="380" viewBox="0 0 1200 380" role="img">
  <title>Rihan Mohammed - Full Stack Developer</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#01040c"/>
      <stop offset="45%" stop-color="#0b1220"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <radialGradient id="auroraA" cx="22%" cy="35%" r="55%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#0f766e" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="auroraB" cx="78%" cy="28%" r="48%">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="auroraC" cx="50%" cy="90%" r="50%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="plate" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#152033" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#0c1524" stop-opacity="0.88"/>
    </linearGradient>
    <linearGradient id="plateSide" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#0f766e" stop-opacity="0.2"/>
    </linearGradient>
    <linearGradient id="plateTop" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.12"/>
    </linearGradient>
    <linearGradient id="wordmark" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="60%" stop-color="#e2e8f0"/>
      <stop offset="100%" stop-color="#99f6e4"/>
    </linearGradient>
    <linearGradient id="beam" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0"/>
      <stop offset="50%" stop-color="#14b8a6" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#fff" stop-opacity="0"/>
      <stop offset="45%" stop-color="#fff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#fff" stop-opacity="0.2"/>
      <stop offset="55%" stop-color="#fff" stop-opacity="0"/>
      <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="20" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="cardShadow" x="-20%" y="-20%" width="150%" height="160%">
      <feDropShadow dx="0" dy="18" stdDeviation="16" flood-color="#000" flood-opacity="0.55"/>
    </filter>
    <clipPath id="frame"><rect width="1200" height="380" rx="20"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="1200" height="380" fill="url(#void)"/>
    <ellipse cx="260" cy="130" rx="340" ry="170" fill="url(#auroraA)" filter="url(#softGlow)">
      <animate attributeName="cx" values="230;310;230" dur="16s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.75;1;0.75" dur="9s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="940" cy="100" rx="300" ry="150" fill="url(#auroraB)" filter="url(#softGlow)">
      <animate attributeName="cy" values="80;130;80" dur="18s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="620" cy="320" rx="400" ry="110" fill="url(#auroraC)"/>

    <!-- deep perspective city grid -->
    <g opacity="0.22" stroke="#14b8a6" fill="none" stroke-width="1">
      <path d="M0 300 L600 235 L1200 300"/>
      <path d="M40 340 L600 250 L1160 340"/>
      <path d="M120 380 L600 265 L1080 380"/>
      <path d="M220 380 L600 275 L980 380"/>
      <path d="M360 380 L600 285 L840 380"/>
      <line x1="0" y1="310" x2="1200" y2="310"/>
      <line x1="0" y1="335" x2="1200" y2="335"/>
      <line x1="0" y1="360" x2="1200" y2="360"/>
    </g>

    <!-- light beams -->
    <rect x="200" y="0" width="40" height="380" fill="url(#beam)" opacity="0.35">
      <animate attributeName="x" values="120;280;120" dur="12s" repeatCount="indefinite"/>
    </rect>
    <rect x="880" y="0" width="28" height="380" fill="url(#beam)" opacity="0.25">
      <animate attributeName="x" values="820;960;820" dur="14s" repeatCount="indefinite"/>
    </rect>

    {''.join(particles)}

    <!-- HUD corners -->
    <g stroke="#14b8a6" stroke-width="1.6" fill="none" opacity="0.6">
      <path d="M28 60 L28 28 L60 28"/>
      <path d="M1140 28 L1172 28 L1172 60"/>
      <path d="M28 320 L28 352 L60 352"/>
      <path d="M1140 352 L1172 352 L1172 320"/>
    </g>

    <!-- 3D extruded identity plate -->
    <g filter="url(#cardShadow)">
      <animateTransform attributeName="transform" type="translate" values="0 0; 0 -4; 0 0" dur="6s" repeatCount="indefinite"/>
      <path d="M820 88 L880 118 L880 278 L820 248 Z" fill="url(#plateSide)"/>
      <path d="M70 88 L130 58 L880 118 L820 88 Z" fill="url(#plateTop)"/>
      <path d="M70 88 L820 88 L820 248 L70 248 Z" fill="url(#plate)" stroke="#14b8a6" stroke-opacity="0.45"/>
      <rect x="70" y="88" width="750" height="160" fill="url(#sheen)">
        <animate attributeName="x" values="-600;820" dur="8s" repeatCount="indefinite"/>
      </rect>
      <rect x="70" y="88" width="750" height="3" fill="#14b8a6">
        <animate attributeName="opacity" values="0.5;1;0.5" dur="2.8s" repeatCount="indefinite"/>
      </rect>
      <rect x="92" y="118" width="70" height="3" rx="1.5" fill="#f59e0b"/>
      <text x="92" y="168" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="48" font-weight="800" fill="url(#wordmark)" letter-spacing="-0.5">Rihan Mohammed</text>
      <text x="92" y="202" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="700" fill="#14b8a6" letter-spacing="3">FULL STACK DEVELOPER</text>
      <text x="92" y="230" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="14" fill="#94a3b8">Fintech &amp; Real-Estate Systems - HomeAbroad Inc. - Ziffy.ai</text>
    </g>

    <!-- status + signal glass pods -->
    <g transform="translate(92, 300)">
      <rect width="180" height="30" rx="9" fill="rgba(15,118,110,0.28)" stroke="#14b8a6" stroke-opacity="0.5"/>
      <circle cx="18" cy="15" r="4.5" fill="#22c55e"><animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>
      <text x="32" y="19" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700" fill="#e2e8f0">AVAILABLE FOR WORK</text>
    </g>

    <g filter="url(#cardShadow)">
      <animateTransform attributeName="transform" type="translate" values="920 130; 920 124; 920 130" dur="5s" repeatCount="indefinite"/>
      <path d="M200 0 L230 16 L230 140 L200 124 Z" fill="url(#plateSide)"/>
      <path d="M0 0 L30 -14 L230 16 L200 0 Z" fill="url(#plateTop)"/>
      <rect width="200" height="124" fill="url(#plate)" stroke="#14b8a6" stroke-opacity="0.4"/>
      <text x="18" y="28" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="700" fill="#14b8a6">SYSTEM SIGNAL</text>
      <text x="18" y="52" font-family="JetBrains Mono, Consolas, monospace" font-size="12" fill="#e2e8f0">4+ yrs production</text>
      <text x="18" y="72" font-family="JetBrains Mono, Consolas, monospace" font-size="12" fill="#e2e8f0">AI search - pipelines</text>
      <g transform="translate(100, 98)">
        <g transform="translate(-48,0)">
          <g transform="translate(0,-2) scale(0.55)"><path d="M0 -11 C6 -11 10 -6 10 0 C10 7 4 11 0 11 C-2 11 -4 10 -5 8 C-2 10 2 8 2 3 C2 -2 -2 -4 -5 -2 C-7 -6 -4 -11 0 -11 Z" fill="#e0234e"/></g>
          <text x="0" y="16" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="9" fill="#94a3b8">Nest</text>
        </g>
        <g transform="translate(0,0)">
          <g transform="translate(0,-2) scale(0.45)"><path d="M-8 8 V-8 H-4 L8 6 V-8 H12 V8 H8 L-4 -6 V8 Z" fill="#e2e8f0"/></g>
          <text x="0" y="16" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="9" fill="#94a3b8">Next</text>
        </g>
        <g transform="translate(48,0)">
          <g transform="translate(0,-2) scale(0.5)"><path d="M-11 4 Q0 12 11 4" fill="none" stroke="#ff9900" stroke-width="2.2" stroke-linecap="round"/><text x="0" y="-1" text-anchor="middle" font-family="Arial,sans-serif" font-size="8" font-weight="800" fill="#e2e8f0">aws</text></g>
          <text x="0" y="16" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="9" fill="#94a3b8">AWS</text>
        </g>
      </g>
    </g>

    <!-- scanline -->
    <rect x="0" y="0" width="1200" height="3" fill="#14b8a6" opacity="0.15">
      <animate attributeName="y" values="0;380;0" dur="7s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>
"""
    (ASSETS / "hero-aurora.svg").write_text(svg, encoding="utf-8", newline="\n")
    print("wrote hero-aurora.svg")


def metrics() -> None:
    """Clean metrics strip — equal columns, balanced vertical rhythm, soft motion only."""
    # Keep standalone for debug/compat; primary surface is signal_deck().
    _write_metrics_strip(ASSETS / "metrics-strip.svg")


def _metrics_cells(y0: int = 0) -> tuple[str, str]:
    cells = [
        (112.5, "4+", "YEARS", "#14b8a6", 0.0),
        (337.5, "9+", "SYSTEMS", "#14b8a6", 0.2),
        (562.5, "60+", "WEBHOOKS", "#f59e0b", 0.4),
        (787.5, "2", "COMPANIES", "#14b8a6", 0.6),
    ]
    parts = []
    for cx, value, label, color, delay in cells:
        parts.append(
            f"""<g transform="translate({cx},{y0})">
  <circle cx="0" cy="32" r="28" fill="{color}" fill-opacity="0.08">
    <animate attributeName="fill-opacity" values="0.05;0.12;0.05" dur="4s" begin="{delay}s" repeatCount="indefinite"/>
  </circle>
  <text x="0" y="36" text-anchor="middle" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="28" font-weight="800" fill="{color}">{value}</text>
  <rect x="-16" y="44" width="32" height="2" rx="1" fill="{color}" fill-opacity="0.75"/>
  <text x="0" y="64" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="600" fill="#94a3b8" letter-spacing="2">{label}</text>
</g>"""
        )
    dividers = "\n".join(
        f'<line x1="{x}" y1="{y0 + 16}" x2="{x}" y2="{y0 + 68}" stroke="#334155" stroke-opacity="0.5"/>'
        for x in (225, 450, 675)
    )
    return "".join(parts), dividers


def _write_metrics_strip(path: Path) -> None:
    cells, dividers = _metrics_cells(0)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="88" viewBox="0 0 900 88" role="img">
  <title>Profile metrics</title>
  <defs>
    <linearGradient id="panel" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b1220"/><stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <radialGradient id="wash" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rim" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0"/>
      <stop offset="50%" stop-color="#14b8a6"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="900" height="88" rx="16" fill="url(#panel)" stroke="rgba(20,184,166,0.28)"/>
  <ellipse cx="450" cy="40" rx="280" ry="50" fill="url(#wash)">
    <animate attributeName="opacity" values="0.6;1;0.6" dur="5s" repeatCount="indefinite"/>
  </ellipse>
  <rect x="1" y="1" width="898" height="2" fill="url(#rim)">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="3.2s" repeatCount="indefinite"/>
  </rect>
  <g stroke="#14b8a6" stroke-width="1.1" fill="none" opacity="0.4">
    <path d="M14 14 H28 V28"/><path d="M886 14 H872 V28"/><path d="M14 74 H28 V60"/><path d="M886 74 H872 V60"/>
  </g>
  {dividers}
  {cells}
</svg>
"""
    path.write_text(svg, encoding="utf-8", newline="\n")
    print("wrote", path.name)


def signal_deck() -> None:
    """Mission brief + metrics in one panel — removes awkward gap between sections."""
    cells, dividers = _metrics_cells(112)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="200" viewBox="0 0 900 200" role="img">
  <title>Mission brief and profile metrics</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/><stop offset="55%" stop-color="#0b1220"/><stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <radialGradient id="auroraA" cx="22%" cy="30%" r="45%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="auroraB" cx="78%" cy="70%" r="40%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rim" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0"/>
      <stop offset="50%" stop-color="#14b8a6"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ink" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f8fafc"/><stop offset="100%" stop-color="#99f6e4"/>
    </linearGradient>
    <linearGradient id="floor" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0"/>
      <stop offset="100%" stop-color="#14b8a6" stop-opacity="0.08"/>
    </linearGradient>
  </defs>
  <rect width="900" height="200" rx="18" fill="url(#void)" stroke="rgba(20,184,166,0.3)"/>
  <ellipse cx="200" cy="50" rx="260" ry="90" fill="url(#auroraA)">
    <animate attributeName="opacity" values="0.7;1;0.7" dur="7s" repeatCount="indefinite"/>
  </ellipse>
  <ellipse cx="720" cy="160" rx="220" ry="70" fill="url(#auroraB)"/>
  <rect x="0" y="150" width="900" height="50" fill="url(#floor)"/>
  <g opacity="0.18" stroke="#14b8a6" fill="none" stroke-width="1">
    <path d="M40 188 L450 168 L860 188"/>
    <path d="M80 198 L450 176 L820 198"/>
  </g>
  <rect x="1" y="1" width="898" height="2.5" fill="url(#rim)">
    <animate attributeName="opacity" values="0.35;1;0.35" dur="3.4s" repeatCount="indefinite"/>
  </rect>
  <g stroke="#14b8a6" stroke-width="1.2" fill="none" opacity="0.45">
    <path d="M16 16 H34 V34"/><path d="M884 16 H866 V34"/><path d="M16 184 H34 V166"/><path d="M884 184 H866 V166"/>
  </g>

  <!-- mission -->
  <text x="450" y="32" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="10" font-weight="700" fill="#14b8a6" letter-spacing="3.5">MISSION BRIEF</text>
  <text x="450" y="60" text-anchor="middle" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="18" font-weight="700" fill="url(#ink)">I build production fintech &amp; real-estate platforms</text>
  <text x="450" y="84" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="12" fill="#94a3b8">AI property search  ·  NestJS APIs  ·  data pipelines  ·  cloud infra</text>

  <!-- soft separator -->
  <line x1="80" y1="102" x2="820" y2="102" stroke="#14b8a6" stroke-opacity="0.22"/>
  <circle cx="450" cy="102" r="2.5" fill="#f59e0b">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="2.6s" repeatCount="indefinite"/>
  </circle>

  {dividers}
  {cells}
</svg>
"""
    (ASSETS / "signal-deck.svg").write_text(svg, encoding="utf-8", newline="\n")
    print("wrote signal-deck.svg")
    # Keep intro-signal as thin alias for older links / debug
    intro = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="88" viewBox="0 0 900 88" role="img">
  <title>I build production fintech and real-estate platforms</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/><stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <radialGradient id="wash" cx="50%" cy="40%" r="55%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rim" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0"/>
      <stop offset="50%" stop-color="#14b8a6"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ink" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f8fafc"/><stop offset="100%" stop-color="#99f6e4"/>
    </linearGradient>
  </defs>
  <rect width="900" height="88" rx="16" fill="url(#void)" stroke="rgba(20,184,166,0.28)"/>
  <ellipse cx="450" cy="40" rx="260" ry="48" fill="url(#wash)">
    <animate attributeName="opacity" values="0.55;1;0.55" dur="5s" repeatCount="indefinite"/>
  </ellipse>
  <rect x="1" y="1" width="898" height="2" fill="url(#rim)">
    <animate attributeName="opacity" values="0.35;1;0.35" dur="3.4s" repeatCount="indefinite"/>
  </rect>
  <g stroke="#14b8a6" stroke-width="1.1" fill="none" opacity="0.4">
    <path d="M14 14 H28 V28"/><path d="M886 14 H872 V28"/><path d="M14 74 H28 V60"/><path d="M886 74 H872 V60"/>
  </g>
  <text x="450" y="28" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="10" font-weight="700" fill="#14b8a6" letter-spacing="3.5">MISSION BRIEF</text>
  <text x="450" y="52" text-anchor="middle" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="17" font-weight="700" fill="url(#ink)">I build production fintech &amp; real-estate platforms</text>
  <text x="450" y="74" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="11" fill="#94a3b8">AI property search  ·  NestJS APIs  ·  data pipelines  ·  cloud infra</text>
</svg>
"""
    (ASSETS / "intro-signal.svg").write_text(intro, encoding="utf-8", newline="\n")
    print("wrote intro-signal.svg")


def intro_signal() -> None:
    """Deprecated standalone — generated via signal_deck()."""
    pass


def cta_tile(
    *,
    filename: str,
    eyebrow: str,
    title: str,
    hint: str,
    accent: str,
    icon: str,
    delay: float = 0.0,
    width: int = 210,
) -> None:
    """Glass dock tile — each file is a separate clickable <a><img> target."""
    h = 68
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" viewBox="0 0 {width} {h}" role="img">
  <title>{escape(title)} — {escape(hint)}</title>
  <defs>
    <linearGradient id="glass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#132033" stop-opacity="0.96"/>
      <stop offset="100%" stop-color="#0b1220" stop-opacity="0.94"/>
    </linearGradient>
    <linearGradient id="edge" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.15"/>
      <stop offset="50%" stop-color="{accent}" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.15"/>
    </linearGradient>
    <linearGradient id="sheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#fff" stop-opacity="0"/>
      <stop offset="48%" stop-color="#fff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#fff" stop-opacity="0.16"/>
      <stop offset="52%" stop-color="#fff" stop-opacity="0"/>
      <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <filter id="soft" x="-20%" y="-40%" width="140%" height="180%">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>
  <g filter="url(#soft)">
    <rect x="1" y="1" width="{width - 2}" height="{h - 2}" rx="14" fill="url(#glass)" stroke="{accent}" stroke-opacity="0.45">
      <animate attributeName="stroke-opacity" values="0.28;0.75;0.28" dur="3.2s" begin="{delay}s" repeatCount="indefinite"/>
    </rect>
    <rect x="1" y="1" width="{width - 2}" height="2.5" rx="1" fill="url(#edge)">
      <animate attributeName="opacity" values="0.4;1;0.4" dur="2.8s" begin="{delay}s" repeatCount="indefinite"/>
    </rect>
    <rect x="1" y="1" width="{width - 2}" height="{h - 2}" rx="14" fill="url(#sheen)">
      <animate attributeName="x" values="{-width};{width}" dur="7.5s" begin="{delay}s" repeatCount="indefinite"/>
    </rect>
  </g>
  <g transform="translate(18, 34)">
    <circle cx="0" cy="0" r="15" fill="{accent}" fill-opacity="0.14" stroke="{accent}" stroke-opacity="0.45"/>
    <g transform="translate(0,0) scale(0.85)">{icon}</g>
  </g>
  <text x="44" y="28" font-family="JetBrains Mono, Consolas, monospace" font-size="9" font-weight="700" fill="{accent}" letter-spacing="1.6">{escape(eyebrow.upper())}</text>
  <text x="44" y="46" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="14" font-weight="700" fill="#f1f5f9">{escape(title)}</text>
  <text x="44" y="60" font-family="JetBrains Mono, Consolas, monospace" font-size="10" fill="#64748b">{escape(hint)}</text>
</svg>
"""
    (ASSETS / filename).write_text(svg, encoding="utf-8", newline="\n")
    print("wrote", filename)


def link_chip(*, filename: str, label: str, accent: str, delay: float = 0.0) -> None:
    """Compact secondary URL chip for case-study / footer rails."""
    w = max(92, 12 + len(label) * 8)
    h = 34
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
  <title>{escape(label)}</title>
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#020617"/>
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="url(#g)" stroke="{accent}" stroke-opacity="0.5">
    <animate attributeName="stroke-opacity" values="0.3;0.85;0.3" dur="3s" begin="{delay}s" repeatCount="indefinite"/>
  </rect>
  <circle cx="12" cy="17" r="2.4" fill="{accent}">
    <animate attributeName="opacity" values="0.45;1;0.45" dur="2.2s" begin="{delay}s" repeatCount="indefinite"/>
  </circle>
  <text x="{w / 2 + 4}" y="21" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="700" fill="#e2e8f0">{escape(label)}</text>
</svg>
"""
    (ASSETS / filename).write_text(svg, encoding="utf-8", newline="\n")
    print("wrote", filename)


def connect_assets() -> None:
    signal_deck()
    cta_tile(
        filename="cta-portfolio.svg",
        eyebrow="Web",
        title="Portfolio",
        hint="im-rihan.github.io",
        accent="#14b8a6",
        icon='<path d="M-7 -7 H7 V7 H-7 Z" fill="none" stroke="#14b8a6" stroke-width="1.8"/><path d="M-3 0 H3 M0 -3 V3" stroke="#14b8a6" stroke-width="1.8"/>',
        delay=0.0,
        width=216,
    )
    cta_tile(
        filename="cta-linkedin.svg",
        eyebrow="Social",
        title="LinkedIn",
        hint="/in/im-rihan",
        accent="#0A66C2",
        icon='<text x="0" y="5" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" font-weight="800" fill="#0A66C2">in</text>',
        delay=0.15,
        width=216,
    )
    cta_tile(
        filename="cta-email.svg",
        eyebrow="Direct",
        title="Email",
        hint="im.rihan.dev@",
        accent="#EA4335",
        icon='<rect x="-8" y="-5" width="16" height="11" rx="1.5" fill="none" stroke="#EA4335" stroke-width="1.7"/><path d="M-8 -5 L0 2 L8 -5" fill="none" stroke="#EA4335" stroke-width="1.7"/>',
        delay=0.3,
        width=216,
    )
    cta_tile(
        filename="cta-available.svg",
        eyebrow="Status",
        title="Available",
        hint="open to work",
        accent="#22c55e",
        icon='<circle cx="0" cy="0" r="5" fill="#22c55e"><animate attributeName="opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/></circle>',
        delay=0.45,
        width=216,
    )
    chips = [
        ("chip-casestudy.svg", "case study", "#14b8a6", 0.0),
        ("chip-live.svg", "live", "#f59e0b", 0.1),
        ("chip-appi.svg", "appi", "#22d3ee", 0.2),
        ("chip-pricer.svg", "pricer", "#a78bfa", 0.3),
        ("chip-realtor.svg", "ha-realtor", "#14b8a6", 0.0),
        ("chip-pipelines.svg", "pipelines", "#22d3ee", 0.1),
        ("chip-avm.svg", "AVM", "#f59e0b", 0.2),
        ("chip-estimate.svg", "estimate", "#a78bfa", 0.3),
        ("chip-site.svg", "portfolio", "#34d399", 0.4),
        ("chip-footer-portfolio.svg", "portfolio", "#14b8a6", 0.0),
        ("chip-footer-linkedin.svg", "linkedin", "#0A66C2", 0.1),
        ("chip-footer-email.svg", "email", "#EA4335", 0.2),
        ("chip-footer-follow.svg", "follow", "#f59e0b", 0.3),
    ]
    for filename, label, accent, delay in chips:
        link_chip(filename=filename, label=label, accent=accent, delay=delay)


if __name__ == "__main__":
    section_label("label-featured.svg", "Featured")
    section_label("label-stack.svg", "Stack")
    section_label("label-experience.svg", "Experience")
    section_label("label-activity.svg", "Activity")
    hero_banner()
    metrics()
    more_systems()
    stack_panel()
    connect_assets()

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
