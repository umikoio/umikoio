"""
    Author: Umiko (https://github.com/umikoio)
    Project: SVG Generator (https://github.com/umikoio/umikoio)

    This script was built specifically for the following workflow: https://github.com/umikoio/umikoio/blob/main/.github/workflows/update-readme.yml
"""

import base64, os, html, datetime, requests

BG   = "#0b0f14"
TXT  = "#c0cad3"
ACC  = "#7ee787"
VAL  = "#e6edf3"
DATE = "#8b949e"
GRID = "#132029"

pad    = 24
gap    = 20
line_h = 22
logo_w = 220
font   = "DejaVu Sans Mono, Menlo, Consolas, monospace"

def get__readme_header_txt() -> list[str]:
    nf_txt = open("_readme_header.txt", "r", encoding="utf-8").read().rstrip("\n")
    lines = nf_txt.splitlines()
    return lines

def main():
    parsed = []

    for line in get__readme_header_txt():
        if ": " in line:
            lab, val = line.split(": ", 1)
        else:
            lab, val = "", line
        parsed.append((lab, val))

    text_h = len(parsed) * line_h
    canvas_h = max(text_h + pad * 2, 240)
    canvas_w = logo_w + 560 + pad * 2

    x0 = pad + logo_w + gap
    y0 = pad + 24
    text_elems = []
    y = y0

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    text_elems.append(f'<text x="{x0}" y="{y}" font-family="{font}" font-size="16" fill="{DATE}">Last update: {html.escape(ts)}</text>')
    y += line_h + 6

    text_elems.append(f'<rect x="{x0}" y="{y - 18}" width="{canvas_w-x0 - pad}" height="1" fill="{GRID}" />')

    for lab, val in parsed:
        if lab:
            text_elems.append(
                f'<text x="{x0}" y="{y}" font-family="{font}" font-size="16">'
                f'<tspan fill="{ACC}">{html.escape(lab)}:</tspan>'
                f'<tspan fill="{TXT}"> </tspan>'
                f'<tspan fill="{VAL}">{html.escape(val)}</tspan>'
                f'</text>'
            )
        else:
            text_elems.append(f'<text x="{x0}" y="{y}" font-family="{font}" font-size="16" fill="{VAL}">{html.escape(val)}</text>')

        y += line_h

    with open("readme.jpg", "wb") as f:
        f.write(requests.get("https://avatars.githubusercontent.com/u/231703339", timeout=10).content)

    if os.path.exists("readme.jpg"):
        b = base64.b64encode(open("readme.jpg", "rb").read()).decode()

    svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" role="img" aria-label="umikoio">
        <defs>
            <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
            <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000" flood-opacity="0.35"/>
            </filter>
        </defs>
        <rect width="100%" height="100%" rx="14" ry="14" fill="{BG}" filter="url(#shadow)"/>
        <image href="data:image/jpg;base64,{b}" x="{pad}" y="{pad}" height="{canvas_h - pad * 2}" preserveAspectRatio="xMidYMid meet"/>
        {''.join(text_elems)}
    </svg>
    '''

    open("readme_header.svg","w",encoding="utf-8").write(svg)

if __name__ == '__main__':
    main()
