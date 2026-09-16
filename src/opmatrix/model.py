"""Load and validate the matrix. Pure stdlib + PyYAML."""
from __future__ import annotations

import os
from dataclasses import dataclass, field

import yaml

STATUSES = ("solved", "partial", "open")
EVIDENCE_LEVELS = ("consensus", "reported", "inferred")

_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "data")


class MatrixError(ValueError):
    """The data file is malformed; the message says exactly what and where."""


@dataclass
class Source:
    id: str
    label: str
    year: int | None = None
    month: int | None = None
    venue: str = ""
    kind: str = ""
    claim: str = ""
    verify: str = ""
    url: str = ""


@dataclass
class Item:
    id: str
    problem: str
    status: str
    evidence_level: str
    source: str
    notes: str = ""
    area_id: str = ""

    def validate(self, source_ids):
        if self.status not in STATUSES:
            raise MatrixError(
                "item %r has status %r, not one of %s"
                % (self.id, self.status, STATUSES))
        if self.evidence_level not in EVIDENCE_LEVELS:
            raise MatrixError(
                "item %r has evidence_level %r, not one of %s"
                % (self.id, self.evidence_level, EVIDENCE_LEVELS))
        if self.source not in source_ids:
            raise MatrixError(
                "item %r cites source %r, which is not in sources.yaml"
                % (self.id, self.source))
        if not self.problem.strip():
            raise MatrixError("item %r has an empty problem statement" % self.id)


@dataclass
class Area:
    id: str
    title: str
    items: list = field(default_factory=list)


@dataclass
class Matrix:
    version: int
    compiled: str
    window: str
    areas: list
    sources: dict

    def items(self):
        for a in self.areas:
            for it in a.items:
                yield it

    def counts(self):
        """{status: n} over every item."""
        c = {s: 0 for s in STATUSES}
        for it in self.items():
            c[it.status] += 1
        return c

    def counts_by_area(self):
        out = {}
        for a in self.areas:
            c = {s: 0 for s in STATUSES}
            for it in a.items:
                c[it.status] += 1
            out[a.id] = c
        return out

    def orphan_sources(self):
        """Sources defined but cited by no item."""
        cited = {it.source for it in self.items()}
        return sorted(set(self.sources) - cited)

    def validate(self):
        seen = set()
        for it in self.items():
            if it.id in seen:
                raise MatrixError("duplicate item id %r" % it.id)
            seen.add(it.id)
            it.validate(self.sources)
        return True


def load(data_dir=_DATA):
    """Parse data/matrix.yaml + data/sources.yaml into a validated Matrix."""
    with open(os.path.join(data_dir, "matrix.yaml")) as f:
        m = yaml.safe_load(f)
    with open(os.path.join(data_dir, "sources.yaml")) as f:
        srcs = yaml.safe_load(f)["sources"]
    sources = {sid: Source(id=sid, **{k: v for k, v in s.items()})
               for sid, s in srcs.items()}
    areas = []
    for a in m["areas"]:
        items = [Item(area_id=a["id"], **it) for it in a["items"]]
        areas.append(Area(id=a["id"], title=a["title"], items=items))
    mat = Matrix(version=m["version"], compiled=str(m["compiled"]),
                 window=m["window"], areas=areas, sources=sources)
    mat.validate()
    return mat
