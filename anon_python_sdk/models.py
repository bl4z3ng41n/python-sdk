from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Hop:
    fingerprint: str
    nickname: str


@dataclass
class Circuit:
    id: str
    path: List[Hop]
    created: Optional[datetime] = None
    # other fields are omitted for now


@dataclass
class Relay:
    fingerprint: str
    nickname: str
    address: str
    or_port: int
    flags: List[str]
    bandwidth: int
    # other fields are omitted for now

@dataclass
class Stream:
    id: str
    target: str
    # other fields are omitted for now
