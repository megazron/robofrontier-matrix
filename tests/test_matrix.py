import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import opmatrix                                                    # noqa: E402
from opmatrix.model import MatrixError, STATUSES                  # noqa: E402
from opmatrix.render import to_html, to_json, to_markdown         # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")


def test_loads_and_validates():
    m = opmatrix.load()
    assert m.validate() is True
    assert sum(1 for _ in m.items()) >= 15


def test_every_item_cites_a_defined_source():
    m = opmatrix.load()
    for it in m.items():
        assert it.source in m.sources, it.id


def test_no_orphan_sources():
    # every source is cited by at least one item
    assert opmatrix.load().orphan_sources() == []


def test_statuses_are_legal():
    m = opmatrix.load()
    for it in m.items():
        assert it.status in STATUSES


def test_item_ids_unique():
    m = opmatrix.load()
    ids = [it.id for it in m.items()]
    assert len(ids) == len(set(ids))


def test_counts_sum_to_total():
    m = opmatrix.load()
    c = m.counts()
    assert sum(c.values()) == sum(1 for _ in m.items())


def test_bad_status_rejected(tmp_path):
    (tmp_path / "sources.yaml").write_text(
        "sources:\n  s1:\n    label: x\n    verify: y\n")
    (tmp_path / "matrix.yaml").write_text(
        "version: 1\ncompiled: 2026\nwindow: w\nareas:\n"
        "  - id: a\n    title: A\n    items:\n"
        "      - id: i1\n        problem: p\n        status: nonsense\n"
        "        evidence_level: consensus\n        source: s1\n")
    with pytest.raises(MatrixError):
        opmatrix.load(str(tmp_path))


def test_undefined_source_rejected(tmp_path):
    (tmp_path / "sources.yaml").write_text("sources:\n  s1:\n    label: x\n")
    (tmp_path / "matrix.yaml").write_text(
        "version: 1\ncompiled: 2026\nwindow: w\nareas:\n"
        "  - id: a\n    title: A\n    items:\n"
        "      - id: i1\n        problem: p\n        status: open\n"
        "        evidence_level: consensus\n        source: ghost\n")
    with pytest.raises(MatrixError):
        opmatrix.load(str(tmp_path))


def test_duplicate_ids_rejected(tmp_path):
    (tmp_path / "sources.yaml").write_text("sources:\n  s1:\n    label: x\n")
    (tmp_path / "matrix.yaml").write_text(
        "version: 1\ncompiled: 2026\nwindow: w\nareas:\n"
        "  - id: a\n    title: A\n    items:\n"
        "      - id: dup\n        problem: p\n        status: open\n"
        "        evidence_level: consensus\n        source: s1\n"
        "      - id: dup\n        problem: q\n        status: open\n"
        "        evidence_level: consensus\n        source: s1\n")
    with pytest.raises(MatrixError):
        opmatrix.load(str(tmp_path))


def test_markdown_has_every_area():
    m = opmatrix.load()
    md = to_markdown(m)
    for a in m.areas:
        assert a.title in md


def test_json_round_trips():
    import json
    m = opmatrix.load()
    d = json.loads(to_json(m))
    assert sum(len(a["items"]) for a in d["areas"]) == sum(1 for _ in m.items())


def test_html_is_self_contained():
    h = to_html(opmatrix.load())
    assert h.startswith("<!doctype html>")
    assert "<script" not in h.lower()   # no external anything
    assert "http://" not in h and "https://" not in h


def test_cli_validate_ok():
    r = subprocess.run([sys.executable, "-m", "opmatrix.cli", "validate"],
                       cwd=ROOT, env=dict(os.environ, PYTHONPATH="src"),
                       capture_output=True, text=True)
    assert r.returncode == 0 and "OK" in r.stdout


def test_cli_filter_open():
    r = subprocess.run([sys.executable, "-m", "opmatrix.cli", "filter",
                        "--status", "open"], cwd=ROOT,
                       env=dict(os.environ, PYTHONPATH="src"),
                       capture_output=True, text=True)
    assert r.returncode == 0 and "[open]" in r.stdout


def test_no_solved_overclaim():
    # these are open problems; nothing should be marked solved without evidence.
    m = opmatrix.load()
    assert m.counts()["solved"] == 0
