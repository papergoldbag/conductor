from dataclasses import dataclass


@dataclass
class User:
    username: str
    chat_id: str
    id: str
