from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Color(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    DEFAULT = 39
    RESET = 0


@dataclass
class Project:
    id: Optional[int]
    name: str
    color: Color
    created_at: datetime
    updated_at: datetime