from __future__ import annotations
from dataclasses import dataclass

@dataclass
class HashNode:
    key: str
    value: str
    h: int
    v: int
    next: "HashNode | None" = None