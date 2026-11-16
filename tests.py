import unittest

from ticket import Ticket
from bst import BinarySearchTree
from heap import MaxHeap
from heap_sort import heap_sort
from main import SupportDispatcher


class TestBinarySearchTree(unittest.TestCase):
    """Тестирование бинарного дерева поиска."""

    def setUp(self):
        self.tree = BinarySearchTree()

        self.tickets = [
            Ticket(50, "Ошибка сервера", 5),
            Ticket(30, "Принтер", 2),
            Ticket(70, "База данных", 5),
            Ticket(20, "Сброс пароля", 1),
            Ticket(40, "Почта", 3),
            Ticket(60, "API", 4),
            Ticket(80, "Авторизация", 3),
        ]

        for ticket in self.tickets:
            self.tree.insert(ticket)

    def test_insert(self):
        """Проверка добавления узлов."""
        self.assertEqual(self.tree.count_nodes(), 7)
        self.assertTrue(self.tree.insert(Ticket(90, "Новая", 5)))
        self.assertEqual(self.tree.count_nodes(), 8)

    def test_duplicate_id(self):
        """Повторяющийся ID запрещён."""
        result = self.tree.insert(Ticket(50, "Дубликат", 10))

        self.assertFalse(result)
        self.assertEqual(self.tree.count_nodes(), 7)
        self.assertEqual(self.tree.search(50).priority, 5)

    def test_search_existing(self):
        """Поиск существующей заявки."""
        ticket = self.tree.search(40)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.title, "Почта")

    def test_search_missing(self):
        """Поиск несуществующей заявки."""
        self.assertIsNone(self.tree.search(999))

    def test_delete_leaf(self):
        """Удаление листа."""
        self.assertTrue(self.tree.delete(20))
        self.assertIsNone(self.tree.search(20))
        self.assertEqual(self.tree.count_nodes(), 6)
        self.assertTrue(self.tree.is_valid_bst())

    def test_delete_one_child(self):
        """Удаление узла с одним потомком."""
        self.tree.delete(20)
        self.assertTrue(self.tree.delete(30))

        self.assertIsNone(self.tree.search(30))
        self.assertIsNotNone(self.tree.search(40))
        self.assertTrue(self.tree.is_valid_bst())

    def test_delete_two_children(self):
        """Удаление узла с двумя потомками."""
        self.assertTrue(self.tree.delete(70))

        self.assertIsNone(self.tree.search(70))
        self.assertEqual(self.tree.count_nodes(), 6)
        self.assertTrue(self.tree.is_valid_bst())

    def test_delete_root(self):
        """Удаление корневого узла."""
        self.assertTrue(self.tree.delete(50))

        self.assertIsNone(self.tree.search(50))
        self.assertEqual(self.tree.count_nodes(), 6)
        self.assertTrue(self.tree.is_valid_bst())

    def test_delete_missing(self):
        """Удаление отсутствующего ID."""
        self.assertFalse(self.tree.delete(999))
        self.assertEqual(self.tree.count_nodes(), 7)

    def test_preorder(self):
        """Прямой обход."""
        ids = [t.id for t in self.tree.preorder()]

        self.assertEqual(
            ids,
            [50, 30, 20, 40, 70, 60, 80]
        )

    def test_inorder(self):
        """Симметричный обход."""
        ids = [t.id for t in self.tree.inorder()]

        self.assertEqual(
            ids,
            [20, 30, 40, 50, 60, 70, 80]
        )

    def test_postorder(self):
        """Обратный обход."""
        ids = [t.id for t in self.tree.postorder()]

        self.assertEqual(
            ids,
            [20, 40, 30, 60, 80, 70, 50]
        )

    def test_level_order(self):
        """Уровневый обход."""
        ids = [t.id for t in self.tree.level_order()]

        self.assertEqual(
            ids,
            [50, 30, 70, 20, 40, 60, 80]
        )

    def test_tree_characteristics(self):
        """Характеристики дерева."""
        self.assertEqual(self.tree.count_nodes(), 7)
        self.assertEqual(self.tree.count_leaves(), 4)
        self.assertEqual(self.tree.height(), 3)
        self.assertEqual(self.tree.min_ticket().id, 20)
        self.assertEqual(self.tree.max_ticket().id, 80)

    def test_valid_bst(self):
        """Проверка корректного BST."""
        self.assertTrue(self.tree.is_valid_bst())

    def test_invalid_bst(self):
        """Обнаружение нарушения свойства BST."""
        self.tree.root.left.ticket = Ticket(
            100, "Неправильный узел", 1
        )

        self.assertFalse(self.tree.is_valid_bst())

    def test_empty_tree(self):
        """Операции с пустым деревом."""
        empty = BinarySearchTree()

        self.assertEqual(empty.count_nodes(), 0)
        self.assertEqual(empty.count_leaves(), 0)
        self.assertEqual(empty.height(), 0)

        self.assertEqual(empty.preorder(), [])
        self.assertEqual(empty.inorder(), [])
        self.assertEqual(empty.postorder(), [])
        self.assertEqual(empty.level_order(), [])

        self.assertIsNone(empty.search(10))
        self.assertIsNone(empty.min_ticket())
        self.assertIsNone(empty.max_ticket())

        self.assertFalse(empty.delete(10))
        self.assertTrue(empty.is_valid_bst())


class TestMaxHeap(unittest.TestCase):
    """Тестирование максимальной двоичной кучи."""

    def setUp(self):
        self.tickets = [
            Ticket(10, "Низкий", 1),
            Ticket(20, "Средний", 3),
            Ticket(30, "Высокий", 5),
            Ticket(40, "Средний 2", 3),
            Ticket(50, "Критический", 10),
        ]

        self.heap = MaxHeap(self.tickets)

    def test_build_heap(self):
        """Построение максимальной кучи."""
        self.assertEqual(self.heap.size(), 5)
        self.assertTrue(self.heap.is_valid_heap())

    def test_peek(self):
        """Просмотр наиболее срочной заявки."""
        self.assertEqual(self.heap.peek().id, 50)
        self.assertEqual(self.heap.size(), 5)

    def test_insert(self):
        """Добавление нового максимума."""
        self.heap.insert(Ticket(60, "Авария", 15))

        self.assertEqual(self.heap.peek().id, 60)
        self.assertEqual(self.heap.size(), 6)
        self.assertTrue(self.heap.is_valid_heap())

    def test_extract_max(self):
        """Извлечение максимального элемента."""
        ticket = self.heap.extract_max()

        self.assertEqual(ticket.id, 50)
        self.assertEqual(self.heap.size(), 4)
        self.assertEqual(self.heap.peek().id, 30)
        self.assertTrue(self.heap.is_valid_heap())

    def test_extract_all(self):
        """Все заявки извлекаются по приоритету."""
        extracted = []

        while not self.heap.is_empty():
            ticket = self.heap.extract_max()
            extracted.append(ticket.priority)
            self.assertTrue(self.heap.is_valid_heap())

        self.assertEqual(extracted, [10, 5, 3, 3, 1])

    def test_equal_priorities(self):
        """При равном приоритете первым идёт меньший ID."""
        heap = MaxHeap([
            Ticket(30, "Третья", 5),
            Ticket(10, "Первая", 5),
            Ticket(20, "Вторая", 5),
        ])

        ids = []

        while not heap.is_empty():
            ids.append(heap.extract_max().id)

        self.assertEqual(ids, [10, 20, 30])

    def test_invalid_heap(self):
        """Обнаружение нарушения свойства кучи."""
        self.heap.heap[0] = Ticket(99, "Ошибка", -100)

        self.assertFalse(self.heap.is_valid_heap())

    def test_empty_heap(self):
        """Операции с пустой кучей."""
        heap = MaxHeap()

        self.assertTrue(heap.is_empty())
        self.assertEqual(heap.size(), 0)
        self.assertIsNone(heap.peek())
        self.assertIsNone(heap.extract_max())
        self.assertTrue(heap.is_valid_heap())

    def test_single_element(self):
        """Куча с одним элементом."""
        heap = MaxHeap([Ticket(1, "Одна заявка", 5)])

        self.assertEqual(heap.peek().id, 1)
        self.assertEqual(heap.extract_max().id, 1)
        self.assertTrue(heap.is_empty())

    def test_array_representation(self):
        """Проверка массивного представления."""
        array = self.heap.get_array()

        self.assertEqual(len(array), 5)

        for i in range(len(array)):
            left = 2 * i + 1
            right = 2 * i + 2

            if left < len(array):
                self.assertGreaterEqual(
                    array[i].priority,
                    array[left].priority
                )

            if right < len(array):
                self.assertGreaterEqual(
                    array[i].priority,
                    array[right].priority
                )


class TestHeapSort(unittest.TestCase):
    """Тестирование сортировки кучей."""

    def test_sort_by_priority(self):
        """Сортировка по убыванию приоритета."""
        tickets = [
            Ticket(1, "A", 2),
            Ticket(2, "B", 5),
            Ticket(3, "C", 1),
            Ticket(4, "D", 10),
            Ticket(5, "E", 3),
        ]

        result = heap_sort(tickets)

        self.assertEqual(
            [t.priority for t in result],
            [10, 5, 3, 2, 1]
        )

    def test_equal_priorities(self):
        """Сортировка одинаковых приоритетов по ID."""
        tickets = [
            Ticket(30, "A", 5),
            Ticket(10, "B", 5),
            Ticket(20, "C", 5),
        ]

        result = heap_sort(tickets)

        self.assertEqual(
            [t.id for t in result],
            [10, 20, 30]
        )

    def test_empty_list(self):
        """Сортировка пустого списка."""
        self.assertEqual(heap_sort([]), [])

    def test_single_element(self):
        """Сортировка одного элемента."""
        ticket = Ticket(1, "Единственная", 5)

        self.assertEqual(heap_sort([ticket]), [ticket])

    def test_already_sorted(self):
        """Уже отсортированные заявки."""
        tickets = [
            Ticket(1, "A", 10),
            Ticket(2, "B", 5),
            Ticket(3, "C", 1),
        ]

        self.assertEqual(
            [t.id for t in heap_sort(tickets)],
            [1, 2, 3]
        )

    def test_reverse_sorted(self):
        """Обратный исходный порядок."""
        tickets = [
            Ticket(1, "A", 1),
            Ticket(2, "B", 5),
            Ticket(3, "C", 10),
        ]

        self.assertEqual(
            [t.id for t in heap_sort(tickets)],
            [3, 2, 1]
        )

    def test_original_list_unchanged(self):
        """Исходный список не изменяется."""
        tickets = [
            Ticket(1, "A", 1),
            Ticket(2, "B", 10),
        ]

        original_ids = [t.id for t in tickets]

        heap_sort(tickets)

        self.assertEqual(
            [t.id for t in tickets],
            original_ids
        )

    def test_mixed_priorities(self):
        """Проверка большого диапазона приоритетов."""
        tickets = [
            Ticket(i, f"Заявка {i}", (i * 7) % 11)
            for i in range(1, 101)
        ]

        result = heap_sort(tickets)

        actual = [(t.priority, t.id) for t in result]

        for i in range(len(actual) - 1):
            first_priority, first_id = actual[i]
            second_priority, second_id = actual[i + 1]

            self.assertTrue(
                first_priority > second_priority
                or (
                    first_priority == second_priority
                    and first_id < second_id
                )
            )


class TestIntegration(unittest.TestCase):
    """Проверка взаимодействия структур данных."""

    def test_bst_heap_and_sort(self):
        """BST, MaxHeap и Heap Sort работают совместно."""
        dispatcher = SupportDispatcher()

        dispatcher.tree.insert(Ticket(10, "A", 2))
        dispatcher.tree.insert(Ticket(20, "B", 10))
        dispatcher.tree.insert(Ticket(30, "C", 5))

        heap = dispatcher.create_heap()

        self.assertTrue(heap.is_valid_heap())
        self.assertEqual(heap.peek().id, 20)

        sorted_tickets = heap_sort(
            dispatcher.get_all_tickets()
        )

        self.assertEqual(
            [t.id for t in sorted_tickets],
            [20, 30, 10]
        )

        # Обработка заявки через извлечение из кучи
        processed = heap.extract_max()
        dispatcher.tree.delete(processed.id)

        # Новая куча уже не содержит обработанную заявку
        new_heap = dispatcher.create_heap()

        self.assertEqual(new_heap.size(), 2)
        self.assertEqual(new_heap.peek().id, 30)
        self.assertIsNone(dispatcher.tree.search(20))
        self.assertTrue(dispatcher.tree.is_valid_bst())


if __name__ == "__main__":
    unittest.main(verbosity=2)
