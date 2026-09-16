"""opmatrix CLI: validate the data, render it, and answer simple queries."""
from __future__ import annotations

import argparse
import sys

from .model import STATUSES, load
from .render import to_html, to_json, to_markdown


def _load(a):
    return load(a.data) if a.data else load()


def main(argv=None):
    ap = argparse.ArgumentParser(prog="opmatrix",
                                 description="Sourced open-problems matrix for "
                                             "embodied AI and robotics software.")
    ap.add_argument("--data", help="data directory (default: packaged data/)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate", help="check the data files and exit nonzero on error")
    r = sub.add_parser("render", help="render the matrix")
    r.add_argument("--format", choices=["md", "json", "html"], default="md")
    r.add_argument("-o", "--out", help="write to a file instead of stdout")
    st = sub.add_parser("stats", help="counts by status and area")
    st.add_argument("--json", action="store_true")
    q = sub.add_parser("filter", help="list items by status and/or area")
    q.add_argument("--status", choices=STATUSES)
    q.add_argument("--area")
    sub.add_parser("sources", help="list the sources and their verify notes")

    a = ap.parse_args(argv)

    if a.cmd == "validate":
        try:
            m = _load(a)
        except Exception as e:                                # noqa: BLE001
            print("INVALID:", e)
            return 1
        orph = m.orphan_sources()
        print("OK: %d items, %d areas, %d sources%s"
              % (sum(1 for _ in m.items()), len(m.areas), len(m.sources),
                 ("; orphan sources: " + ", ".join(orph)) if orph else ""))
        return 0

    m = _load(a)
    if a.cmd == "render":
        text = {"md": to_markdown, "json": to_json, "html": to_html}[a.format](m)
        if a.out:
            open(a.out, "w").write(text)
            print("wrote", a.out)
        else:
            print(text)
        return 0
    if a.cmd == "stats":
        if a.json:
            import json
            print(json.dumps({"total": m.counts(), "by_area": m.counts_by_area()},
                             indent=2))
            return 0
        c = m.counts()
        print("total: %d open, %d partial, %d solved" % (c["open"], c["partial"], c["solved"]))
        for aid, cc in m.counts_by_area().items():
            print("  %-14s open %d  partial %d  solved %d"
                  % (aid, cc["open"], cc["partial"], cc["solved"]))
        return 0
    if a.cmd == "filter":
        n = 0
        for it in m.items():
            if a.status and it.status != a.status:
                continue
            if a.area and it.area_id != a.area:
                continue
            n += 1
            print("[%s] %s (%s)\n    %s"
                  % (it.status, it.id, it.area_id, it.problem.strip().replace("\n", " ")))
        if not n:
            print("no items match")
        return 0
    if a.cmd == "sources":
        for sid, s in m.sources.items():
            print("%s  %s%s" % (sid, s.label, (" [%s]" % s.year) if s.year else ""))
            print("    verify: %s" % s.verify)
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
