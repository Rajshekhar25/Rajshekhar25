"""
Builds the full profile.sh --live banner: terminal chrome + dot-path portrait
(from the approved dot_pattern.npy / foreground_mask.npy) + SYSTEM.INFO panel
with programmatically-computed dotted leaders. Static (no animation yet) —
that's layered on once this geometry is confirmed correct.

Two outputs: dark.svg (dark-mode UI chrome/background) and light.svg
(light-mode chrome/background), portrait treatment identical in both (it
already lives on a near-black panel per the approved design).
"""

import os
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import io
import numpy as np
from scipy import ndimage

ASSETS = os.path.join(_REPO, "assets")
OUT = os.path.join(_REPO, "scripts", "_build")

# ---------- palette (from the Master Prompt spec) ----------
PORTRAIT_DARK  = "#A78BFA"
PORTRAIT_LIGHT = "#7C3AED"
CHROME_DARK    = "#22D3EE"
CHROME_LIGHT   = "#0891B2"
ACCENT         = "#10B981"
BG             = "#0A101F"

# ---------- geometry ----------
W, H = 1180, 610
TITLEBAR_H = 32
PORTRAIT_X, PORTRAIT_Y = 34, 76
PORTRAIT_W, PORTRAIT_H = 380, 431
INFO_X = 478
INFO_RIGHT = 1150

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))

# ---------- portrait path data (reused from svg_portrait.py's logic) ----------
def runs_to_spans(row_bool):
    spans, x, w = [], 0, len(row_bool)
    while x < w:
        if row_bool[x]:
            s = x
            while x < w and row_bool[x]:
                x += 1
            spans.append((s, x))
        else:
            x += 1
    return spans

def grid_path(bool_grid, ox, oy, sx, sy):
    h, w = bool_grid.shape
    parts = []
    for y in range(h):
        row = bool_grid[y]
        if not row.any():
            continue
        py = oy + (y + 0.5) * sy
        for (x0, x1) in runs_to_spans(row):
            parts.append("M%.2f,%.2fH%.2f" % (ox + x0*sx, py, ox + x1*sx))
    return "".join(parts)

dots = np.load(ASSETS + r"\dot_pattern.npy").astype(bool)
fg = np.load(ASSETS + r"\foreground_mask.npy").astype(bool)
edge = (fg.astype(np.uint8) ^ ndimage.binary_erosion(fg, iterations=1).astype(np.uint8)).astype(bool)

GH, GW = dots.shape
SX, SY = PORTRAIT_W / GW, PORTRAIT_H / GH
edge_d = grid_path(edge, PORTRAIT_X, PORTRAIT_Y, SX, SY)
intro_svg = io.open(OUT + r"\intro_layer.svg", encoding="utf-8").read()
loop_svg = io.open(OUT + r"\loop_layer.svg", encoding="utf-8").read()
traveler_svg = io.open(OUT + r"\traveler_layer.svg", encoding="utf-8").read()
print("animated layers loaded: intro=%d chars, loop=%d chars, traveler=%d chars, edge=%d chars" % (len(intro_svg), len(loop_svg), len(traveler_svg), len(edge_d)))

# ---------- info panel rows ----------
ROWS = [
    ("Subject",   "Rajshekhar Das"),
    ("Role",      "Software Engineer, Systems & AI"),
    ("Origin",    "Agartala, India"),
    ("Education", "B.Tech CSE, NIT Durgapur"),
    ("Status",    "Open to SDE Internships"),
    ("ToolChain", "VS Code, Git, Docker, Postman"),
    ("Core.Lang",     "JavaScript/TS, Python, C, C++"),
    ("Core.Frontend", "React, Next.js, Tailwind"),
    ("Core.Backend",  "Node.js, Express, Socket.io"),
    ("Core.Database", "MongoDB, PostgreSQL"),
    ("Core.Infra",    "Docker, Vercel, GH Actions"),
    ("Grid.Mail",       "rajshekhardas85@gmail.com"),
    ("Grid.LinkedIn",   "linkedin.com/in/rajshekhar25"),
    ("Grid.GitHub",     "github.com/Rajshekhar25"),
    ("Grid.LeetCode",   "leetcode.com/u/0xRajshekhar"),
    ("Grid.Codeforces", "codeforces.com/profile/0xRajshekhar"),
]

ROW_FONT_SIZE = 14
ROW_CHAR_W = 7.6      # monospace-equivalent width we lock every glyph run to
ROW_SPACING = 23
ROWS_TOP = 172
LEADER_GAP = 6         # gap between label/value text and the dotted leader
MIN_LEADER = 14

def build_rows(color_label, color_value, color_leader):
    out = []
    max_label_w = max(len(l) for l, v in ROWS) * ROW_CHAR_W
    label_x = INFO_X
    value_right_x = INFO_RIGHT
    for i, (label, value) in enumerate(ROWS):
        y = ROWS_TOP + i * ROW_SPACING
        label_tl = len(label) * ROW_CHAR_W
        value_tl = len(value) * ROW_CHAR_W
        value_left_x = value_right_x - value_tl
        leader_x0 = label_x + label_tl + LEADER_GAP
        leader_x1 = value_left_x - LEADER_GAP
        # if a long value would crowd the leader below the minimum, that's a
        # real overflow -- shrink this row's char width rather than silently
        # overlapping label and value
        if leader_x1 - leader_x0 < MIN_LEADER:
            scale = (value_right_x - label_x - 2*LEADER_GAP - MIN_LEADER) / (label_tl + value_tl)
            label_tl *= scale
            value_tl *= scale
            value_left_x = value_right_x - value_tl
            leader_x0 = label_x + label_tl + LEADER_GAP
            leader_x1 = value_left_x - LEADER_GAP
        out.append(
            '<text x="%.1f" y="%.1f" font-size="%d" fill="%s" '
            'textLength="%.1f" lengthAdjust="spacingAndGlyphs">%s</text>\n'
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
            'stroke-width="1.4" stroke-dasharray="1.6,3.4" stroke-linecap="round"/>\n'
            '<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="end" '
            'textLength="%.1f" lengthAdjust="spacingAndGlyphs">%s</text>'
            % (label_x, y, ROW_FONT_SIZE, color_label, label_tl, esc(label),
               leader_x0, y-4, leader_x1, y-4, color_leader,
               value_right_x, y, ROW_FONT_SIZE, color_value, value_tl, esc(value))
        )
    return "\n".join(out)

# ---------- assemble one theme ----------
def build_svg(theme):
    if theme == "dark":
        chrome = CHROME_DARK
        page_bg = "#05070C"
        panel_bg = "#0D1220"
        titlebar_bg = "#0A0E18"
        text_dim = "#5B7083"
        label_col = chrome
        value_col = "#E7F6FB"
        leader_col = "#2A3B47"
        portrait_ink = PORTRAIT_DARK
    else:
        chrome = CHROME_LIGHT
        page_bg = "#EAF6FA"
        panel_bg = "#F4FBFD"
        titlebar_bg = "#DCEEF3"
        text_dim = "#4B6672"
        label_col = "#0E7490"
        value_col = "#0B1220"
        leader_col = "#AFD8E2"
        portrait_ink = PORTRAIT_LIGHT

    portrait_edge_col = portrait_ink  # edge stroke reuses portrait ink at reduced opacity below

    rows_svg = build_rows(label_col, value_col, leader_col)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="'JetBrains Mono','Fira Code',ui-monospace,Consolas,monospace">
<defs>
  <clipPath id="portraitClip-{theme}"><rect x="{PORTRAIT_X}" y="{PORTRAIT_Y}" width="{PORTRAIT_W}" height="{PORTRAIT_H}" rx="6"/></clipPath>
</defs>
<rect width="{W}" height="{H}" rx="14" fill="{page_bg}"/>
<rect width="{W}" height="{TITLEBAR_H}" rx="14" fill="{titlebar_bg}"/>
<rect y="{TITLEBAR_H-14}" width="{W}" height="14" fill="{titlebar_bg}"/>
<circle cx="18" cy="16" r="5" fill="#FF5F57"/>
<circle cx="36" cy="16" r="5" fill="#FEBC2E"/>
<circle cx="54" cy="16" r="5" fill="#28C840"/>
<text x="{W/2}" y="20.5" font-size="12.5" fill="{text_dim}" text-anchor="middle">profile.sh --live</text>

<rect x="{PORTRAIT_X-10}" y="{PORTRAIT_Y-30}" width="{PORTRAIT_W+20}" height="{PORTRAIT_H+50}" rx="10" fill="{panel_bg}" stroke="{leader_col}" stroke-width="1"/>
<text x="{PORTRAIT_X}" y="{PORTRAIT_Y-12}" font-size="12" letter-spacing="2.5" fill="{chrome}">VISUAL.MAP</text>
<rect x="{PORTRAIT_X}" y="{PORTRAIT_Y}" width="{PORTRAIT_W}" height="{PORTRAIT_H}" rx="6" fill="{BG}"/>
<g clip-path="url(#portraitClip-{theme})">
  <path d="{edge_d}" stroke="{portrait_edge_col}" stroke-opacity="0.55" stroke-width="{SY:.3f}" fill="none" shape-rendering="crispEdges"/>
  <g style="--portrait-ink:{portrait_ink}">
{intro_svg}
{loop_svg}
{traveler_svg}
  </g>
</g>
<rect x="{PORTRAIT_X}" y="{PORTRAIT_Y}" width="{PORTRAIT_W}" height="{PORTRAIT_H}" rx="6" fill="none" stroke="{leader_col}" stroke-width="1"/>

<text x="{INFO_X}" y="60" font-size="13" letter-spacing="2.5" fill="{chrome}">SYSTEM.INFO</text>
<circle cx="{INFO_RIGHT-192}" cy="56" r="4" fill="#F43F5E">
  <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>
</circle>
<text x="{INFO_RIGHT-182}" y="60.5" font-size="12" letter-spacing="1.5" fill="#F43F5E">LIVE</text>
<rect x="{INFO_RIGHT-148}" y="47" width="148" height="18" rx="9" fill="{ACCENT}"/>
<text x="{INFO_RIGHT-74}" y="60" font-size="11" fill="{BG}" text-anchor="middle" font-weight="700">&#64;Rajshekhar25</text>

<line x1="{INFO_X}" y1="76" x2="{INFO_RIGHT}" y2="76" stroke="{leader_col}" stroke-width="1"/>

<rect x="{INFO_X}" y="96" width="{INFO_RIGHT-INFO_X}" height="52" rx="6" fill="{panel_bg}" stroke="{leader_col}" stroke-width="1"/>
<text x="{INFO_X+16}" y="118" font-size="14" font-weight="700" fill="{value_col}">RAJSHEKHAR DAS</text>
<text x="{INFO_X+16}" y="136" font-size="11.5" fill="{text_dim}">Software Engineer &#183; Systems, Backends and Applied AI</text>

{rows_svg}

</svg>'''
    return svg

for theme in ("dark", "light"):
    svg = build_svg(theme)
    path = OUT + f"\\banner_{theme}.svg"
    io.open(path, "w", encoding="utf-8").write(svg)
    print(theme, "bytes:", len(svg))
