from ticket import Ticket


class MaxHeap:
    """Максимальная двоичная куча заявок."""

    def __init__(self, tickets=None):
        self.heap = []

        if tickets is not None:
            self.build_heap(tickets)

    @staticmethod
    def _is_higher(first: Ticket, second: Ticket) -> bool:
        """
        Сравнить заявки.

        Сначала сравнивается приоритет.
        При равном приоритете меньший ID считается более срочным.
        """
        if first.priority != second.priority:
            return first.priority > second.priority

        return first.id < second.id

    def build_heap(self, tickets):
        """Построить максимальную кучу за O(n)."""
        self.heap = list(tickets)

        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._heapify_down(i)

    def _heapify_down(self, index):
        """Восстановить свойство кучи сверху вниз."""
        size = len(self.heap)

        while True:
            largest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if (
                left < size
                and self._is_higher(
                    self.heap[left],
                    self.heap[largest]
                )
            ):
                largest = left

            if (
                right < size
                and self._is_higher(
                    self.heap[right],
                    self.heap[largest]
                )
            ):
                largest = right

            if largest == index:
                break

            self.heap[index], self.heap[largest] = (
                self.heap[largest],
                self.heap[index]
            )

            index = largest

    def _heapify_up(self, index):
        """Восстановить свойство кучи снизу вверх."""

        while index > 0:
            parent = (index - 1) // 2

            if not self._is_higher(
                self.heap[index],
                self.heap[parent]
            ):
                break

            self.heap[index], self.heap[parent] = (
                self.heap[parent],
                self.heap[index]
            )

            index = parent

    def insert(self, ticket: Ticket):
        """Добавить заявку в кучу."""
        self.heap.append(ticket)
        self._heapify_up(len(self.heap) - 1)

    def peek(self):
        """Получить наиболее срочную заявку без удаления."""
        if not self.heap:
            return None

        return self.heap[0]

    def extract_max(self):
        """Извлечь наиболее срочную заявку."""
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        maximum = self.heap[0]

        self.heap[0] = self.heap.pop()
        self._heapify_down(0)

        return maximum

    def is_valid_heap(self):
        """Проверить соблюдение свойства максимальной кучи."""
        size = len(self.heap)

        for i in range(size):
            left = 2 * i + 1
            right = 2 * i + 2

            if (
                left < size
                and self._is_higher(
                    self.heap[left],
                    self.heap[i]
                )
            ):
                return False

            if (
                right < size
                and self._is_higher(
                    self.heap[right],
                    self.heap[i]
                )
            ):
                return False

        return True

    def size(self):
        """Количество элементов в куче."""
        return len(self.heap)

    def is_empty(self):
        """Проверка кучи на пустоту."""
        return len(self.heap) == 0

    def get_array(self):
        """Получить копию массива кучи."""
        return self.heap.copy()
