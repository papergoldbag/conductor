from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    username: str
    chat_id: str
    id: str