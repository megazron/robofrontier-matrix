"""Render the matrix to Markdown, JSON and a self-contained HTML page."""
from __future__ import annotations

import html
import json

from .model import STATUSES

_BADGE = {"solved": "✅ solved", "partial": "🟡 partial", "open": "🔴 open"}


def to_json(m):
    return json.dumps({
        "version": m.version, "compiled": m.compiled, "window": m.window,
        "counts": m.counts(),
        "areas": [
            {"id": a.id, "title": a.title,
             "items": [{"id": it.id, "problem": it.problem, "status": it.status,
                        "evidence_level": it.evidence_level, "source": it.source,
                        "notes": it.notes} for it in a.items]}
            for a in m.areas],
        "sources": {sid: vars(s) for sid, s in m.sources.items()},
    }, indent=2)


def _src_short(m, sid):
    s = m.sources.get(sid)
    if not s:
        return sid
    yr = ("%s" % s.year) if s.year else ""
    return "%s%s" % (s.label, (" (%s)" % yr if yr else ""))


def to_markdown(m):
    out = []
    out.append("# Open-problems matrix\n")
    c = m.counts()
    out.append("_%d problems across %d areas, window %s, compiled %s._\n"
               % (sum(c.values()), len(m.areas), m.window, m.compiled))
    out.append("**%d open · %d partial · %d solved.** Status is the field's, "
               "not this repo's.\n" % (c["open"], c["partial"], c["solved"]))
    for a in m.areas:
        out.append("\n## %s\n" % a.title)
        out.append("| Problem | Status | Evidence | Source |")
        out.append("|---|---|---|---|")
        for it in a.items:
            prob = it.problem.strip().replace("\n", " ")
            out.append("| %s | %s | %s | %s |"
                       % (prob, _BADGE[it.status], it.evidence_level,
                          _src_short(m, it.source)))
    return "\n".join(out) + "\n"


def to_html(m):
    col = {"solved": "#2b8a3e", "partial": "#b25a00", "open": "#b02a37"}
    c = m.counts()
    rows = []
    for a in m.areas:
        rows.append('<tr class="area"><td colspan="4">%s</td></tr>'
                    % html.escape(a.title))
        for it in a.items:
            rows.append(
                '<tr><td>%s%s</td><td style="color:%s;font-weight:600">%s</td>'
                '<td>%s</td><td>%s</td></tr>' % (
                    html.escape(it.problem.strip()),
                    ('<div class="note">%s</div>' % html.escape(it.notes)) if it.notes else "",
                    col[it.status], it.status, it.evidence_level,
                    html.escape(_src_short(m, it.source))))
    bars = "".join(
        '<span class="seg %s" style="flex:%d"></span>' % (s, c[s]) for s in STATUSES if c[s])
    return _HTML.replace("{{ROWS}}", "\n".join(rows)).replace(
        "{{BARS}}", bars).replace("{{WINDOW}}", m.window).replace(
        "{{COMPILED}}", m.compiled).replace(
        "{{OPEN}}", str(c["open"])).replace(
        "{{PARTIAL}}", str(c["partial"])).replace("{{SOLVED}}", str(c["solved"]))


_HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Robotics open-problems matrix</title>
<style>
:root{--ink:#1f2933;--mute:#6b7580;--line:#e1e6ea;--bg:#fff}
body{font-family:'Segoe UI',Helvetica,Arial,sans-serif;color:var(--ink);
background:var(--bg);margin:0;padding:2rem 1rem;line-height:1.5}
main{max-width:1000px;margin:0 auto}
h1{margin:0 0 .3rem} .sub{color:var(--mute);margin:0 0 1rem}
.bar{display:flex;height:14px;border-radius:7px;overflow:hidden;margin:.6rem 0 1.4rem}
.seg.open{background:#b02a37}.seg.partial{background:#b25a00}.seg.solved{background:#2b8a3e}
table{border-collapse:collapse;width:100%;font-size:14px}
td{border-bottom:1px solid var(--line);padding:.55rem .6rem;vertical-align:top}
tr.area td{background:#0b728510;font-weight:700;color:#0b7285;font-size:15px;
border-bottom:2px solid #0b7285}
.note{color:var(--mute);font-size:12.5px;margin-top:.25rem}
@media(prefers-color-scheme:dark){:root{--ink:#e6eaee;--mute:#9aa4ae;--line:#2b3440;--bg:#0d1420}
tr.area td{background:#0b728522}}
</style></head><body><main>
<h1>Robotics open-problems matrix</h1>
<p class="sub">Window {{WINDOW}} · compiled {{COMPILED}} · {{OPEN}} open, {{PARTIAL}} partial, {{SOLVED}} solved. Status is the field's, not this page's.</p>
<div class="bar">{{BARS}}</div>
<table>{{ROWS}}</table>
</main></body></html>"""
