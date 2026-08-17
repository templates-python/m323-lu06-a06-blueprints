from dataclasses import dataclass


@dataclass
class TodoItem:
    item_id: int
    title: str
    is_completed: bool
