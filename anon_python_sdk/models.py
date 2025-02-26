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


class CircuitPurpose(Enum):
    GENERAL = 'GENERAL'
    HS_CLIENT_INTRO = 'HS_CLIENT_INTRO'
    HS_CLIENT_REND = 'HS_CLIENT_REND'
    HS_SERVICE_INTRO = 'HS_SERVICE_INTRO'
    HS_SERVICE_REND = 'HS_SERVICE_REND'
    TESTING = 'TESTING'
    CONTROLLER = 'CONTROLLER'
    MEASURE_TIMEOUT = 'MEASURE_TIMEOUT'
    HS_VANGUARDS = 'HS_VANGUARDS'
    PATH_BIAS_TESTING = 'PATH_BIAS_TESTING'
    CIRCUIT_PADDING = 'CIRCUIT_PADDING'
    CONFLUX_UNLINKED = 'CONFLUX_UNLINKED'  # TODO: check if this is correct

    def __str__(self):
        return self.name


@dataclass
class Circuit:
    id: str
    path: List[Hop]
    created: datetime
    status: CircuitStatus
    purpose: CircuitPurpose
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
