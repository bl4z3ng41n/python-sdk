from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Relay:
    fingerprint: str
    nickname: Optional[str] = None

@dataclass
class Circuit:
    id: str
    status: str
    path: List[Relay]
    purpose: Optional[str] = None
    time_created: Optional[datetime] = None
