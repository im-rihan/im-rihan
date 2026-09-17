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


def isometric_tile(
    cx: float,
    cy: float,
    label: str,
    icon_key: str,
    accent: str,
    delay: float,
    size: float = 42,
    uid: str = "t",
) -> str:
    """Premium isometric cube with soft shadow, lit faces, and hover float."""
    hx, hy = size * 0.98, size * 0.56
    depth = size * 0.58
    top = f"M{cx} {cy - hy} L{cx + hx} {cy} L{cx} {cy + hy} L{cx - hx} {cy} Z"
    left = f"M{cx - hx} {cy} L{cx} {cy + hy} L{cx} {cy + hy + depth} L{cx - hx} {cy + depth} Z"
    right = f"M{cx + hx} {cy} L{cx} {cy + hy} L{cx} {cy + hy + depth} L{cx + hx} {cy + depth} Z"
    icon = ICONS.get(icon_key, f'<text text-anchor="middle" y="4" font-size="9" fill="#e2e8f0">{escape(label[:2])}</text>')
    shadow_cy = cy + hy + depth + 6
    return f"""<g>
  <defs>
    <linearGradient id="L{uid}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.18"/>
    </linearGradient>
    <linearGradient id="R{uid}" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.28"/>
    </linearGradient>
    <linearGradient id="T{uid}" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0b1220"/>
      <stop offset="55%" stop-color="#122033"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.35"/>
    </linearGradient>
    <radialGradient id="S{uid}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <ellipse cx="{cx}" cy="{shadow_cy}" rx="{hx * 0.95}" ry="7" fill="url(#S{uid})">
    <animate attributeName="rx" values="{hx * 0.95};{hx * 0.75};{hx * 0.95}" dur="4.2s" begin="{delay}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.9;0.45;0.9" dur="4.2s" begin="{delay}s" repeatCount="indefinite"/>
  </ellipse>
  <g>
    <animateTransform attributeName="transform" type="translate" values="0 0; 0 -8; 0 0" dur="4.2s" begin="{delay}s" repeatCount="indefinite"/>
    <path d="{left}" fill="url(#L{uid})"/>
    <path d="{right}" fill="url(#R{uid})"/>
    <path d="{top}" fill="url(#T{uid})" stroke="{accent}" stroke-width="1.35" stroke-opacity="0.95"/>
    <path d="{top}" fill="{accent}" fill-opacity="0.12">
      <animate attributeName="fill-opacity" values="0.08;0.3;0.08" dur="3.6s" begin="{delay}s" repeatCount="indefinite"/>
    </path>
    <g transform="translate({cx}, {cy - 1}) scale(0.92)">{icon}</g>
  </g>
  <text x="{cx}" y="{cy + hy + depth + 18}" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="11" font-weight="700" fill="#e2e8f0">{escape(label)}</text>
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
  <rect width="400" height="240" rx="16" fill="url(#void)" stroke="rgba(20,184,166,0.18)"/>
  <ellipse cx="90" cy="50" rx="130" ry="70" fill="url(#glow)"><animate attributeName="opacity" values="0.7;1;0.7" dur="4s" begin="{delay}s" repeatCount="indefinite"/></ellipse>
  <path d="M30 205 L210 185 L370 205 L190 225 Z" fill="#14b8a6" opacity="0.1">
    <animate attributeName="opacity" values="0.06;0.14;0.06" dur="5s" begin="{delay}s" repeatCount="indefinite"/>
  </path>
  <g filter="url(#shadow)">
    <animateTransform attributeName="transform" type="translate" values="0 0; 0 -8; 0 0" dur="4.2s" begin="{delay}s" repeatCount="indefinite"/>
    <path d="M340 42 L376 62 L376 192 L340 172 Z" fill="url(#side)"/>
    <path d="M40 42 L76 22 L376 62 L340 42 Z" fill="url(#top)"/>
    <path d="M40 42 L340 42 L340 172 L40 172 Z" fill="url(#face)" stroke="{accent}" stroke-opacity="0.5"/>
    <rect x="40" y="42" width="300" height="130" fill="url(#sheen)"><animate attributeName="x" values="-260;340" dur="5.5s" begin="{delay}s" repeatCount="indefinite"/></rect>
  </g>
  <rect x="40" y="42" width="300" height="3" fill="{accent}" opacity="0.85"><animate attributeName="opacity" values="0.45;1;0.45" dur="2.6s" begin="{delay}s" repeatCount="indefinite"/></rect>
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
  <rect width="560" height="220" rx="16" fill="url(#void)" stroke="rgba(20,184,166,0.18)"/>
  <ellipse cx="500" cy="36" rx="120" ry="70" fill="url(#orb)"><animate attributeName="opacity" values="0.65;1;0.65" dur="4.5s" begin="{delay}s" repeatCount="indefinite"/></ellipse>
  <path d="M40 198 L290 180 L520 198 L270 216 Z" fill="{accent}" opacity="0.1">
    <animate attributeName="opacity" values="0.06;0.14;0.06" dur="5s" begin="{delay}s" repeatCount="indefinite"/>
  </path>
  <g filter="url(#shadow)">
    <animateTransform attributeName="transform" type="translate" values="0 0; 0 -7; 0 0" dur="4.6s" begin="{delay}s" repeatCount="indefinite"/>
    <path d="M480 36 L524 58 L524 188 L480 166 Z" fill="url(#side)"/>
    <path d="M40 36 L84 16 L524 58 L480 36 Z" fill="url(#top)"/>
    <path d="M40 36 L480 36 L480 166 L40 166 Z" fill="url(#face)" stroke="{accent}" stroke-opacity="0.45"/>
    <rect x="40" y="36" width="440" height="130" fill="url(#sheen)"><animate attributeName="x" values="-400;480" dur="6s" begin="{delay}s" repeatCount="indefinite"/></rect>
  </g>
  <rect x="40" y="36" width="8" height="130" fill="{accent}"><animate attributeName="opacity" values="0.55;1;0.55" dur="2.4s" begin="{delay}s" repeatCount="indefinite"/></rect>
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
    gap = 12
    w = 160
    total = len(items) * w + (len(items) - 1) * gap
    start = (900 - total) / 2
    for i, (title, line1, line2, accent) in enumerate(items):
        x = start + i * (w + gap)
        cards.append(
            f"""<g>
  <ellipse cx="{x + (w-12)/2}" cy="186" rx="{(w-12)/2 * 0.85}" ry="6" fill="#000" opacity="0.35">
    <animate attributeName="rx" values="{(w-12)/2 * 0.85};{(w-12)/2 * 0.65};{(w-12)/2 * 0.85}" dur="3.6s" begin="{i * 0.18}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.4;0.18;0.4" dur="3.6s" begin="{i * 0.18}s" repeatCount="indefinite"/>
  </ellipse>
  <g>
  <animateTransform attributeName="transform" type="translate" values="0 0; 0 -7; 0 0" dur="3.6s" begin="{i * 0.18}s" repeatCount="indefinite"/>
  <path d="M{x+w-12} 52 L{x+w+6} 64 L{x+w+6} 178 L{x+w-12} 166 Z" fill="{accent}" fill-opacity="0.4"/>
  <path d="M{x} 52 L{x+14} 40 L{x+w+6} 64 L{x+w-12} 52 Z" fill="{accent}" fill-opacity="0.28"/>
  <rect x="{x}" y="52" width="{w-12}" height="114" rx="12" fill="#0f172a" stroke="{accent}" stroke-opacity="0.6"/>
  <rect x="{x}" y="52" width="{w-12}" height="3" fill="{accent}">
    <animate attributeName="opacity" values="0.5;1;0.5" dur="2.8s" begin="{i * 0.18}s" repeatCount="indefinite"/>
  </rect>
  <text x="{x + (w-12)/2}" y="78" text-anchor="middle" font-family="JetBrains Mono,Consolas,monospace" font-size="9" font-weight="700" fill="{accent}" letter-spacing="1.5">SYSTEM</text>
  <text x="{x + (w-12)/2}" y="104" text-anchor="middle" font-family="Inter,Segoe UI,sans-serif" font-size="13" font-weight="800" fill="#f1f5f9">{escape(title)}</text>
  <text x="{x + (w-12)/2}" y="128" text-anchor="middle" font-family="Inter,Segoe UI,sans-serif" font-size="10" fill="#94a3b8">{escape(line1)}</text>
  <text x="{x + (w-12)/2}" y="144" text-anchor="middle" font-family="Inter,Segoe UI,sans-serif" font-size="10" fill="#94a3b8">{escape(line2)}</text>
  </g>
</g>"""
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="220" viewBox="0 0 900 220" role="img">
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
  <rect width="900" height="220" rx="16" fill="url(#void)" stroke="rgba(20,184,166,0.22)"/>
  <ellipse cx="450" cy="90" rx="280" ry="70" fill="url(#wash)">
    <animate attributeName="opacity" values="0.55;1;0.55" dur="5s" repeatCount="indefinite"/>
  </ellipse>
  <rect x="1" y="1" width="898" height="3" fill="url(#rim)">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="3s" repeatCount="indefinite"/>
  </rect>
  <g stroke="#14b8a6" stroke-width="1.1" fill="none" opacity="0.35">
    <path d="M14 14 H30 V30"/><path d="M886 14 H870 V30"/><path d="M14 206 H30 V190"/><path d="M886 206 H870 V190"/>
  </g>
  <text x="450" y="32" text-anchor="middle" font-family="JetBrains Mono,Consolas,monospace" font-size="11" font-weight="700" fill="#14b8a6" letter-spacing="3">MORE SYSTEMS</text>
  <path d="M60 200 L450 182 L840 200" fill="none" stroke="#14b8a6" stroke-opacity="0.2"/>
  {''.join(cards)}
</svg>
"""
    (ASSETS / "more-systems.svg").write_text(svg, encoding="utf-8", newline="\n")
    print("wrote more-systems.svg")


def stack_panel() -> None:
    """3D tech city — larger lit cubes, soft shadows, category rails, AI gems."""
    # Row layout: core / platform / cloud-ops / ai gems
    core = [
        (130, 78, "React", "react", "#61dafb", 0.0),
        (230, 78, "Next.js", "next", "#e2e8f0", 0.15),
        (330, 78, "TS", "ts", "#3178c6", 0.3),
        (430, 78, "NestJS", "nest", "#e0234e", 0.45),
        (530, 78, "Node", "node", "#68a063", 0.6),
        (630, 78, "PHP", "php", "#777bb4", 0.75),
        (730, 78, "Python", "py", "#3776ab", 0.9),
    ]
    data = [
        (180, 168, "MySQL", "mysql", "#00758f", 0.2),
        (280, 168, "Redis", "redis", "#dc382d", 0.35),
        (380, 168, "AWS", "aws", "#ff9900", 0.5),
        (480, 168, "Docker", "docker", "#2496ed", 0.65),
        (580, 168, "Vercel", "vercel", "#e2e8f0", 0.8),
        (680, 168, "CF", "cf", "#f38020", 0.95),
        (780, 168, "FastAPI", "fastapi", "#009688", 1.1),
    ]
    gems = [
        (180, 258, "LangChain", "langchain", "#14b8a6", 0.1),
        (300, 258, "Puppeteer", "puppeteer", "#00d8a2", 0.25),
        (420, 258, "Leaflet", "leaflet", "#199900", 0.4),
        (540, 258, "Typesense", "typesense", "#d4ff52", 0.55),
        (660, 258, "CatBoost", "catboost", "#ffcc00", 0.7),
        (780, 258, "MCP", "mcp", "#22d3ee", 0.85),
    ]

    tiles = []
    for i, t in enumerate(core):
        tiles.append(isometric_tile(*t, size=40, uid=f"c{i}"))
    for i, t in enumerate(data):
        tiles.append(isometric_tile(*t, size=38, uid=f"d{i}"))
    for i, t in enumerate(gems):
        tiles.append(isometric_tile(*t, size=32, uid=f"g{i}"))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="340" viewBox="0 0 900 340" role="img">
  <title>3D tech stack city</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#01040c"/><stop offset="50%" stop-color="#0b1220"/><stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <radialGradient id="wash" cx="50%" cy="28%" r="55%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.22"/><stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="amber" cx="78%" cy="70%" r="40%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.12"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rim" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0"/><stop offset="50%" stop-color="#14b8a6"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="floor" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0"/><stop offset="100%" stop-color="#14b8a6" stop-opacity="0.1"/>
    </linearGradient>
  </defs>
  <rect width="900" height="340" rx="20" fill="url(#void)" stroke="rgba(20,184,166,0.28)"/>
  <ellipse cx="450" cy="100" rx="320" ry="100" fill="url(#wash)">
    <animate attributeName="opacity" values="0.55;1;0.55" dur="5.5s" repeatCount="indefinite"/>
  </ellipse>
  <ellipse cx="720" cy="260" rx="200" ry="70" fill="url(#amber)"/>
  <rect x="0" y="260" width="900" height="80" fill="url(#floor)"/>
  <rect x="1" y="1" width="898" height="2.5" fill="url(#rim)">
    <animate attributeName="opacity" values="0.35;1;0.35" dur="3.2s" repeatCount="indefinite"/>
  </rect>
  <g stroke="#14b8a6" stroke-width="1.2" fill="none" opacity="0.4">
    <path d="M16 16 H36 V36"/><path d="M884 16 H864 V36"/><path d="M16 324 H36 V304"/><path d="M884 324 H864 V304"/>
  </g>
  <!-- perspective city grid -->
  <g stroke="#14b8a6" stroke-opacity="0.16" fill="none">
    <path d="M60 300 L450 250 L840 300"/>
    <path d="M110 320 L450 265 L790 320"/>
    <path d="M180 338 L450 278 L720 338"/>
    <line x1="40" y1="285" x2="860" y2="285"/>
    <line x1="40" y1="310" x2="860" y2="310"/>
  </g>
  <text x="450" y="30" text-anchor="middle" font-family="JetBrains Mono,Consolas,monospace" font-size="11" font-weight="700" fill="#14b8a6" letter-spacing="3">STACK CITY · 3D</text>
  <!-- row captions -->
  <g font-family="JetBrains Mono,Consolas,monospace" font-size="9" font-weight="700" fill="#64748b" letter-spacing="1.2">
    <text x="70" y="48">CORE</text>
    <text x="70" y="138">CLOUD</text>
    <text x="70" y="228">AI / TOOLS</text>
  </g>
  {''.join(tiles)}
</svg>
"""
    (ASSETS / "stack-cinematic.svg").write_text(svg, encoding="utf-8", newline="\n")
    print("wrote stack-cinematic.svg")


def _parse_activity_numbers() -> dict:
    """Extract live numbers from cached upstream SVGs (or defaults)."""
    import re

    stats = {
        "commits": "222",
        "prs": "43",
        "stars": "0",
        "rank": "C+",
        "total": "2,838",
        "current": "1",
        "longest": "11",
        "current_range": "Sep 17",
        "total_range": "2021 - Present",
    }
    stats_path = ASSETS / "github-stats.svg"
    streak_path = ASSETS / "github-streak.svg"
    if stats_path.exists():
        text = stats_path.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"Total Stars Earned:\s*([\d,]+).*Total Commits[^:]*:\s*([\d,]+).*Total PRs:\s*([\d,]+)", text, re.I | re.S)
        if m:
            stats["stars"] = m.group(1).strip(",")
            stats["commits"] = m.group(2).strip(",")
            stats["prs"] = m.group(3).strip(",")
        r = re.search(r"Rank:\s*([A-F][+-]?)", text)
        if r:
            stats["rank"] = r.group(1)
    if streak_path.exists():
        text = streak_path.read_text(encoding="utf-8", errors="ignore")
        nums = re.findall(r"font-size='28px'[^>]*>\s*([\d,]+)\s*<", text)
        if len(nums) >= 3:
            stats["total"] = nums[0].strip()
            stats["current"] = nums[1].strip()
            stats["longest"] = nums[2].strip()
        years = re.search(r"(\d{4})\s*-\s*Present", text)
        if years:
            stats["total_range"] = f"{years.group(1)} - Present"
        day = re.search(
            r"Current Streak</text>[\s\S]{0,400}?font-size='12px'[^>]*>\s*([A-Za-z]{3}\s+\d{1,2})\s*<",
            text,
        )
        if day:
            stats["current_range"] = day.group(1).strip()
        else:
            stats["current_range"] = "today"
    return stats


def activity_hud(data: dict | None = None) -> None:
    """Cinematic HUD replacement for flat github-readme-stats + streak cards."""
    d = data or _parse_activity_numbers()
    for key in ("stars", "commits", "prs", "total", "current", "longest"):
        d[key] = str(d[key]).strip().strip(",")
    rank_map = {"S": 0.95, "A+": 0.88, "A": 0.8, "A-": 0.72, "B+": 0.64, "B": 0.55, "B-": 0.48, "C+": 0.4, "C": 0.32}
    fill = rank_map.get(d["rank"], 0.4)
    dash = 163  # 2*pi*26
    offset = int(dash * (1 - fill))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="200" viewBox="0 0 900 200" role="img">
  <title>GitHub activity — {escape(d['commits'])} commits · streak {escape(d['current'])}</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#01040c"/><stop offset="50%" stop-color="#0b1220"/><stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <radialGradient id="washL" cx="22%" cy="40%" r="42%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.28"/><stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="washR" cx="80%" cy="45%" r="38%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.16"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rim" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0"/><stop offset="50%" stop-color="#14b8a6"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="face" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#152033"/><stop offset="100%" stop-color="#0c1524"/>
    </linearGradient>
    <linearGradient id="sideT" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.35"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0.12"/>
    </linearGradient>
    <linearGradient id="sideR" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.55"/><stop offset="100%" stop-color="#0f766e" stop-opacity="0.2"/>
    </linearGradient>
    <linearGradient id="sideRo" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.5"/><stop offset="100%" stop-color="#b45309" stop-opacity="0.2"/>
    </linearGradient>
    <linearGradient id="ink" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f8fafc"/><stop offset="100%" stop-color="#99f6e4"/>
    </linearGradient>
    <filter id="drop" x="-15%" y="-20%" width="140%" height="160%">
      <feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="#000" flood-opacity="0.45"/>
    </filter>
  </defs>
  <rect width="900" height="200" rx="18" fill="url(#void)" stroke="rgba(20,184,166,0.28)"/>
  <ellipse cx="200" cy="80" rx="240" ry="90" fill="url(#washL)">
    <animate attributeName="opacity" values="0.6;1;0.6" dur="6s" repeatCount="indefinite"/>
  </ellipse>
  <ellipse cx="720" cy="120" rx="200" ry="70" fill="url(#washR)"/>
  <rect x="1" y="1" width="898" height="2.5" fill="url(#rim)">
    <animate attributeName="opacity" values="0.35;1;0.35" dur="3.2s" repeatCount="indefinite"/>
  </rect>
  <g stroke="#14b8a6" stroke-width="1.2" fill="none" opacity="0.45">
    <path d="M16 16 H34 V34"/><path d="M884 16 H866 V34"/><path d="M16 184 H34 V166"/><path d="M884 184 H866 V166"/>
  </g>
  <text x="450" y="24" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="10" font-weight="700" fill="#14b8a6" letter-spacing="3.5">ACTIVITY SIGNAL</text>

  <!-- left 3D plate: ops -->
  <g filter="url(#drop)">
    <animateTransform attributeName="transform" type="translate" values="0 0; 0 -6; 0 0" dur="4.8s" repeatCount="indefinite"/>
    <path d="M412 40 L436 54 L436 168 L412 154 Z" fill="url(#sideR)"/>
    <path d="M32 40 L56 28 L436 54 L412 40 Z" fill="url(#sideT)"/>
    <rect x="32" y="40" width="380" height="114" fill="url(#face)" stroke="#14b8a6" stroke-opacity="0.4"/>
    <rect x="32" y="40" width="380" height="3" fill="#14b8a6">
      <animate attributeName="opacity" values="0.45;1;0.45" dur="2.8s" repeatCount="indefinite"/>
    </rect>
    <text x="50" y="60" font-family="JetBrains Mono, Consolas, monospace" font-size="10" font-weight="700" fill="#14b8a6" letter-spacing="1.6">OPS METRICS</text>
    <g text-anchor="middle" font-family="Inter, Segoe UI, sans-serif">
      <g transform="translate(100,105)">
        <text y="0" font-size="28" font-weight="800" fill="#14b8a6">{escape(d['commits'])}</text>
        <rect x="-20" y="8" width="40" height="2" rx="1" fill="#14b8a6" fill-opacity="0.7"/>
        <text y="26" font-family="JetBrains Mono, Consolas, monospace" font-size="10" fill="#94a3b8" letter-spacing="1.2">COMMITS</text>
        <text y="40" font-family="JetBrains Mono, Consolas, monospace" font-size="9" fill="#64748b">last year</text>
      </g>
      <g transform="translate(210,105)">
        <text y="0" font-size="28" font-weight="800" fill="#22d3ee">{escape(d['prs'])}</text>
        <rect x="-16" y="8" width="32" height="2" rx="1" fill="#22d3ee" fill-opacity="0.7"/>
        <text y="26" font-family="JetBrains Mono, Consolas, monospace" font-size="10" fill="#94a3b8" letter-spacing="1.2">PRS</text>
        <text y="40" font-family="JetBrains Mono, Consolas, monospace" font-size="9" fill="#64748b">all time</text>
      </g>
      <g transform="translate(320,105)">
        <text y="0" font-size="28" font-weight="800" fill="#f59e0b">{escape(d['stars'])}</text>
        <rect x="-14" y="8" width="28" height="2" rx="1" fill="#f59e0b" fill-opacity="0.7"/>
        <text y="26" font-family="JetBrains Mono, Consolas, monospace" font-size="10" fill="#94a3b8" letter-spacing="1.2">STARS</text>
        <text y="40" font-family="JetBrains Mono, Consolas, monospace" font-size="9" fill="#64748b">earned</text>
      </g>
    </g>
  </g>

  <!-- right 3D plate: streak -->
  <g filter="url(#drop)">
    <animateTransform attributeName="transform" type="translate" values="0 0; 0 -6; 0 0" dur="5.2s" begin="0.35s" repeatCount="indefinite"/>
    <path d="M848 40 L872 54 L872 168 L848 154 Z" fill="url(#sideRo)"/>
    <path d="M468 40 L492 28 L872 54 L848 40 Z" fill="url(#sideT)"/>
    <rect x="468" y="40" width="380" height="114" fill="url(#face)" stroke="#f59e0b" stroke-opacity="0.35"/>
    <rect x="468" y="40" width="380" height="3" fill="#f59e0b">
      <animate attributeName="opacity" values="0.45;1;0.45" dur="2.8s" begin="0.3s" repeatCount="indefinite"/>
    </rect>
    <text x="486" y="60" font-family="JetBrains Mono, Consolas, monospace" font-size="10" font-weight="700" fill="#f59e0b" letter-spacing="1.6">STREAK CORE</text>

    <g transform="translate(545,108)">
      <circle r="36" fill="none" stroke="#14b8a6" stroke-opacity="0.15" stroke-width="6"/>
      <circle r="36" fill="none" stroke="#14b8a6" stroke-width="6" stroke-linecap="round" stroke-dasharray="170 56">
        <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="16s" repeatCount="indefinite"/>
      </circle>
      <text text-anchor="middle" y="8" font-family="Inter, Segoe UI, sans-serif" font-size="32" font-weight="800" fill="#f8fafc">{escape(d['current'])}</text>
      <text text-anchor="middle" y="56" font-family="JetBrains Mono, Consolas, monospace" font-size="9" font-weight="700" fill="#14b8a6" letter-spacing="1.2">CURRENT</text>
    </g>

    <g transform="translate(680,95)" text-anchor="middle">
      <text y="0" font-family="Inter, Segoe UI, sans-serif" font-size="24" font-weight="800" fill="#f59e0b">{escape(d['longest'])}</text>
      <text y="16" font-family="JetBrains Mono, Consolas, monospace" font-size="10" fill="#94a3b8" letter-spacing="1">LONGEST</text>
      <text y="48" font-family="Inter, Segoe UI, sans-serif" font-size="20" font-weight="800" fill="#e2e8f0">{escape(d['total'])}</text>
      <text y="64" font-family="JetBrains Mono, Consolas, monospace" font-size="10" fill="#94a3b8" letter-spacing="1">TOTAL</text>
    </g>

    <g transform="translate(800,108)">
      <circle r="22" fill="none" stroke="#14b8a6" stroke-opacity="0.2" stroke-width="4"/>
      <circle r="22" fill="none" stroke="#14b8a6" stroke-width="4" stroke-linecap="round"
        stroke-dasharray="{dash}" stroke-dashoffset="{offset}" transform="rotate(-90)"/>
      <text text-anchor="middle" y="5" font-family="Inter, Segoe UI, sans-serif" font-size="13" font-weight="800" fill="url(#ink)">{escape(d['rank'])}</text>
      <text text-anchor="middle" y="38" font-family="JetBrains Mono, Consolas, monospace" font-size="8" fill="#64748b">RANK</text>
    </g>
  </g>

  <text x="450" y="186" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="10" fill="#64748b">streak {escape(d['current_range'])}  ·  contributions {escape(d['total_range'])}</text>
</svg>
"""
    (ASSETS / "activity-hud.svg").write_text(svg, encoding="utf-8", newline="\n")
    print("wrote activity-hud.svg")


def refresh_activity_svgs() -> None:
    """Pull upstream stats, then render cinematic HUD cards from live numbers."""
    import urllib.request

    targets = {
        "github-stats.svg": (
            "https://github-stats-extended.vercel.app/api?username=im-rihan"
            "&show_icons=true&hide_border=true&count_private=true"
            "&title_color=14b8a6&icon_color=f59e0b&text_color=e2e8f0&bg_color=0f172a"
            "&hide=issues,contribs"
        ),
        "github-streak.svg": (
            "https://streak-stats.demolab.com/?user=im-rihan&hide_border=true"
            "&background=0F172A&stroke=0F766E&ring=14B8A6&fire=F59E0B"
            "&currStreakLabel=14B8A6&sideLabels=94A3B8&dates=64748B"
            "&currStreakNum=E2E8F0&sideNums=E2E8F0"
        ),
    }
    headers = {"User-Agent": "Mozilla/5.0 (compatible; im-rihan-profile-bot/1.0)"}
    for name, url in targets.items():
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=40) as resp:
                data = resp.read()
            if b"<svg" not in data[:400].lower() and b"<svg" not in data:
                print("skip", name, "not svg")
                continue
            (ASSETS / name).write_bytes(data)
            print("cached", name, len(data), "bytes")
        except Exception as exc:  # noqa: BLE001
            print("fail", name, exc)
            if (ASSETS / name).exists():
                print("kept existing", name)
    activity_hud(_parse_activity_numbers())


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
      <animateTransform attributeName="transform" type="translate" values="0 0; 0 -8; 0 0" dur="5.4s" repeatCount="indefinite"/>
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
      <animateTransform attributeName="transform" type="translate" values="920 130; 920 120; 920 130" dur="4.6s" repeatCount="indefinite"/>
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
            f"""<g>
  <animateTransform attributeName="transform" type="translate" values="{cx} {y0}; {cx} {y0 - 4}; {cx} {y0}" dur="3.8s" begin="{delay}s" repeatCount="indefinite"/>
  <circle cx="0" cy="32" r="28" fill="{color}" fill-opacity="0.08">
    <animate attributeName="fill-opacity" values="0.05;0.14;0.05" dur="3.6s" begin="{delay}s" repeatCount="indefinite"/>
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
    cells, dividers = _metrics_cells(100)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="188" viewBox="0 0 900 188" role="img">
  <title>Mission brief and profile metrics</title>
  <defs>
    <linearGradient id="void" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/><stop offset="55%" stop-color="#0b1220"/><stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <radialGradient id="auroraA" cx="22%" cy="28%" r="45%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#14b8a6" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="auroraB" cx="78%" cy="72%" r="40%">
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
    <linearGradient id="face" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#152033"/><stop offset="100%" stop-color="#0c1524"/>
    </linearGradient>
    <linearGradient id="sideT" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.32"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0.1"/>
    </linearGradient>
    <linearGradient id="sideR" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.5"/><stop offset="100%" stop-color="#0f766e" stop-opacity="0.18"/>
    </linearGradient>
    <filter id="drop" x="-10%" y="-20%" width="120%" height="150%">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>
  <rect width="900" height="188" rx="18" fill="url(#void)" stroke="rgba(20,184,166,0.3)"/>
  <ellipse cx="200" cy="44" rx="260" ry="80" fill="url(#auroraA)">
    <animate attributeName="opacity" values="0.7;1;0.7" dur="7s" repeatCount="indefinite"/>
  </ellipse>
  <ellipse cx="720" cy="150" rx="220" ry="60" fill="url(#auroraB)"/>
  <rect x="0" y="140" width="900" height="48" fill="url(#floor)"/>
  <g opacity="0.16" stroke="#14b8a6" fill="none" stroke-width="1">
    <path d="M40 176 L450 158 L860 176"/>
    <path d="M80 184 L450 164 L820 184"/>
  </g>
  <rect x="1" y="1" width="898" height="2.5" fill="url(#rim)">
    <animate attributeName="opacity" values="0.35;1;0.35" dur="3.4s" repeatCount="indefinite"/>
  </rect>
  <g stroke="#14b8a6" stroke-width="1.2" fill="none" opacity="0.45">
    <path d="M16 16 H34 V34"/><path d="M884 16 H866 V34"/><path d="M16 172 H34 V154"/><path d="M884 172 H866 V154"/>
  </g>

  <!-- mission -->
  <text x="450" y="26" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="10" font-weight="700" fill="#14b8a6" letter-spacing="3.5">MISSION BRIEF</text>
  <text x="450" y="50" text-anchor="middle" font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif" font-size="18" font-weight="700" fill="url(#ink)">I build production fintech &amp; real-estate platforms</text>
  <text x="450" y="70" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="12" fill="#94a3b8">AI property search  ·  NestJS APIs  ·  data pipelines  ·  cloud infra</text>

  <!-- soft separator -->
  <line x1="80" y1="84" x2="820" y2="84" stroke="#14b8a6" stroke-opacity="0.22"/>
  <circle cx="450" cy="84" r="2.5" fill="#f59e0b">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="2.6s" repeatCount="indefinite"/>
  </circle>

  <!-- floating 3D metrics plate -->
  <g filter="url(#drop)">
    <animateTransform attributeName="transform" type="translate" values="0 0; 0 -3; 0 0" dur="5s" repeatCount="indefinite"/>
    <path d="M848 90 L868 100 L868 174 L848 164 Z" fill="url(#sideR)"/>
    <path d="M32 90 L52 80 L868 100 L848 90 Z" fill="url(#sideT)"/>
    <rect x="32" y="90" width="816" height="78" fill="url(#face)" stroke="#14b8a6" stroke-opacity="0.35"/>
    <rect x="32" y="90" width="816" height="2.5" fill="#14b8a6">
      <animate attributeName="opacity" values="0.4;1;0.4" dur="2.8s" repeatCount="indefinite"/>
    </rect>
    {dividers}
    {cells}
  </g>
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
    <animateTransform attributeName="transform" type="translate" values="0 0; 0 -4; 0 0" dur="3.4s" begin="{delay}s" repeatCount="indefinite"/>
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
    refresh_activity_svgs()

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
