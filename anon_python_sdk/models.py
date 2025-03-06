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
    CONFLUX_LINKED = 'CONFLUX_LINKED'  # TODO: check if this is correct

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


class Flag(Enum):
    Authority = 'Authority'
    BadExit = 'BadExit'
    BadDirectory = 'BadDirectory'
    Exit = 'Exit'
    Fast = 'Fast'
    Guard = 'Guard'
    HSDir = 'HSDir'
    Named = 'Named'
    NoEdConsensus = 'NoEdConsensus'
    Running = 'Running'
    Stable = 'Stable'
    StaleDesc = 'StaleDesc'
    Unnamed = 'Unnamed'
    Valid = 'Valid'
    V2Dir = 'V2Dir'
    V3Dir = 'V3Dir'

    def __str__(self):
        return self.name


@dataclass
class Relay:
    fingerprint: str
    nickname: str
    address: str
    or_port: int
    flags: List[Flag]
    bandwidth: int  # kilobytes per second
    dir_port: int
    document: object
    published: datetime
    version_line: str
    measured: int
    is_unmeasured: bool  # less than 3 measurements
    digest: Optional[str]
    identifier: str
    identifier_type: str
    or_addresses: object
    version: object
    unrecognized_bandwidth_entries: object
    exit_policy: object
    protocols: object
    microdescriptor_hashes: object


class EventType(Enum):
    ADDRMAP = 'ADDRMAP'
    AUTHDIR_NEWDESCS = 'AUTHDIR_NEWDESCS'
    BUILDTIMEOUT_SET = 'BUILDTIMEOUT_SET'
    BW = 'BW'
    CELL_STATS = 'CELL_STATS'
    CIRC = 'CIRC'
    CIRC_BW = 'CIRC_BW'
    CIRC_MINOR = 'CIRC_MINOR'
    CONF_CHANGED = 'CONF_CHANGED'
    CONN_BW = 'CONN_BW'
    CLIENTS_SEEN = 'CLIENTS_SEEN'
    DEBUG = 'DEBUG'
    DESCCHANGED = 'DESCCHANGED'
    ERR = 'ERR'
    GUARD = 'GUARD'
    HS_DESC = 'HS_DESC'
    HS_DESC_CONTENT = 'HS_DESC_CONTENT'
    INFO = 'INFO'
    NETWORK_LIVENESS = 'NETWORK_LIVENESS'
    NEWCONSENSUS = 'NEWCONSENSUS'
    NEWDESC = 'NEWDESC'
    NOTICE = 'NOTICE'
    NS = 'NS'
    ORCONN = 'ORCONN'
    SIGNAL = 'SIGNAL'
    STATUS_CLIENT = 'STATUS_CLIENT'
    STATUS_GENERAL = 'STATUS_GENERAL'
    STATUS_SERVER = 'STATUS_SERVER'
    STREAM = 'STREAM'
    STREAM_BW = 'STREAM_BW'
    TB_EMPTY = 'TB_EMPTY'
    TRANSPORT_LAUNCHED = 'TRANSPORT_LAUNCHED'
    WARN = 'WARN'


@dataclass
class Event:
    type: EventType
    # other fields are omitted for now


class StreamStatus(Enum):
    NEW = 'NEW'
    NEWRESOLVE = 'NEWRESOLVE'
    REMAP = 'REMAP'
    SENTCONNECT = 'SENTCONNECT'
    SENTRESOLVE = 'SENTRESOLVE'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'
    DETACHED = 'DETACHED'
    CLOSED = 'CLOSED'

    def __str__(self):
        return self.name


class StreamPurpose(Enum):
    DIR_FETCH = 'DIR_FETCH'
    DIR_UPLOAD = 'DIR_UPLOAD'
    DNS_REQUEST = 'DNS_REQUEST'
    DIRPORT_TEST = 'DIRPORT_TEST'
    USER = 'USER'

    def __str__(self):
        return self.name


@dataclass
class Stream(Event):
    id: str
    target: str
    status: StreamStatus
    purpose: Optional[StreamPurpose]
    # other fields are omitted for now


@dataclass
class AddrMap(Event):
    hostname: str
    destination: str
    expiry: datetime
    error: str
    utc_expiry: datetime
    cached: Optional[bool]


@dataclass
class Microdescriptor:
    onion_key: str
    ntor_onion_key: str
    or_addresses: List[str]
    family: List[str]
    exit_policy: object
    exit_policy_v6: object
    identifiers: object
    protocols: object
    digest: object


@dataclass
class VPNRouting:
    target_address: str
    exit_countries: List[str]


@dataclass
class VPNConfig:
    routings: List[VPNRouting]
