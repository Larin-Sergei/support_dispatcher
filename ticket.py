from dataclasses import dataclass


@dataclass
class Ticket:
    id: int
    title: str
    priority: int

    def __str__(self):
        return (
            f"Заявка #{self.id} | "
            f"Название: {self.title} | "
            f"Приоритет: {self.priority}"
        )
