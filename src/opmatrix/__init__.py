"""A sourced, machine-checkable matrix of open problems in embodied AI and
robotics software, 2025 -> Sept 2026. See the data/ directory for the content."""
from .model import Item, Area, Matrix, Source, load, STATUSES, EVIDENCE_LEVELS

__version__ = "0.1.0"
__all__ = ["Item", "Area", "Matrix", "Source", "load",
           "STATUSES", "EVIDENCE_LEVELS"]
