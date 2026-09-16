#!/usr/bin/env python3
"""Regenerate docs/img/ for the open-problems matrix.

    python3 docs/make_figures.py

A status-by-area stacked bar (matplotlib) and a legend-only SVG key. Reads the
matrix through the package so the figure cannot drift from the data.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(HERE, "img")
os.makedirs(IMG, exist_ok=True)
sys.path.insert(0, os.path.join(ROOT, "src"))

import opmatrix                                                   # noqa: E402

OPEN, PARTIAL, SOLVED = "#b02a37", "#b25a00", "#2b8a3e"


def status_by_area():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    m = opmatrix.load()
    by = m.counts_by_area()
    titles = {a.id: a.title for a in m.areas}
    ids = [a.id for a in m.areas]
    op = [by[i]["open"] for i in ids]
    pa = [by[i]["partial"] for i in ids]
    so = [by[i]["solved"] for i in ids]
    labels = [titles[i].replace(" (ROS 2 and friends)", "") for i in ids]

    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=150)
    y = range(len(ids))
    ax.barh(y, op, color=OPEN, label="open")
    ax.barh(y, pa, left=op, color=PARTIAL, label="partial")
    ax.barh(y, so, left=[o + p for o, p in zip(op, pa)], color=SOLVED, label="solved")
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("number of catalogued problems")
    c = m.counts()
    ax.set_title("Open problems by area, %s  (%d open, %d partial, %d solved)"
                 % (m.window, c["open"], c["partial"], c["solved"]))
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(IMG, "status_by_area.png"))
    plt.close(fig)
    print("wrote status_by_area.png")


def coverage_map():
    """An SVG map of which sibling repo addresses which area."""
    m = opmatrix.load()
    addressed = {
        "vla": ("skill-package-spec", "skill portability slice"),
        "eval": ("robobench-harness", "the evaluation infrastructure"),
        "world-models": ("world-model-eval", "long-horizon / trust metrics"),
        "safety": ("vla-scene-redteam", "threat taxonomy + defenses"),
        "ros2": ("ros2-interaction-lint", "the cheap-to-detect bug classes"),
        "cross-cutting": ("", ""),
    }
    W, rowh = 940, 62
    rows = list(m.areas)
    H = 90 + rowh * len(rows)
    b = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Segoe UI,Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="30" y="42" font-size="22" font-weight="700" fill="#1f2933">'
         'What this project set out to move</text>',
         '<text x="30" y="66" font-size="13" fill="#6b7580">Each area of the matrix, '
         'and the sibling repo that ships a runnable slice of it. The frontier itself stays open.</text>']
    y = 92
    for a in rows:
        repo, what = addressed[a.id]
        b.append(f'<rect x="30" y="{y}" width="360" height="{rowh-12}" rx="8" '
                 f'fill="#0b728510" stroke="#0b7285" stroke-width="1.5"/>')
        b.append(f'<text x="46" y="{y+27}" font-size="15" font-weight="600" fill="#1f2933">{a.title}</text>')
        if repo:
            b.append(f'<line x1="390" y1="{y+19}" x2="470" y2="{y+19}" stroke="#6b7580" '
                     f'stroke-width="1.6" marker-end="url(#a)"/>')
            b.append(f'<rect x="470" y="{y}" width="440" height="{rowh-12}" rx="8" '
                     f'fill="#e8f5ec" stroke="#2b8a3e" stroke-width="1.5"/>')
            b.append(f'<text x="486" y="{y+22}" font-size="14" font-weight="700" '
                     f'fill="#2b8a3e" font-family="monospace">{repo}</text>')
            b.append(f'<text x="486" y="{y+40}" font-size="12" fill="#6b7580">{what}</text>')
        else:
            b.append(f'<text x="486" y="{y+27}" font-size="13" fill="#9aa4ae" '
                     f'font-style="italic">recurs across areas; no single-repo slice</text>')
        y += rowh
    b.insert(1, '<defs><marker id="a" markerWidth="9" markerHeight="9" refX="7" refY="3" '
                'orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#6b7580"/></marker></defs>')
    b.append("</svg>")
    open(os.path.join(IMG, "coverage_map.svg"), "w").write("\n".join(b))
    print("wrote coverage_map.svg")


if __name__ == "__main__":
    try:
        status_by_area()
    except Exception as e:                                        # noqa: BLE001
        print("skipped status_by_area.png:", e)
    coverage_map()
