from typing import List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Hop:
    fingerprint: str
    nickname: str


class CircuitStatus(Enum):
    LAUNCHED = 'LAUNCHED'
    BUILT = 'BUILT'
    GUARD_WAIT = 'GUARD_WAIT'
    EXTENDED = 'EXTENDED'
    FAILED = 'FAILED'
    CLOSED = 'CLOSED'

    def __str__(self):
        return self.name


@dataclass
class Circuit:
    id: str
    path: List[Hop]
    created: datetime
    status: CircuitStatus
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
