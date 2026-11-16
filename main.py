from ticket import Ticket
from bst import BinarySearchTree
from heap import MaxHeap
from heap_sort import heap_sort


class SupportDispatcher:
    """Консольный диспетчер заявок службы поддержки."""

    def __init__(self):
        self.tree = BinarySearchTree()

    # ---------- ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ----------

    @staticmethod
    def read_int(message, min_value=None):
        """Безопасный ввод целого числа."""

        while True:
            try:
                value = int(input(message))

                if min_value is not None and value < min_value:
                    print(
                        f"Ошибка: число должно быть "
                        f"не меньше {min_value}."
                    )
                    continue

                return value

            except ValueError:
                print("Ошибка: введите целое число.")

    @staticmethod
    def print_tickets(tickets):
        """Вывести список заявок."""

        if not tickets:
            print("Список заявок пуст.")
            return

        print("-" * 75)
        print(
            f"{'ID':<8} "
            f"{'Название':<45} "
            f"{'Приоритет':<10}"
        )
        print("-" * 75)

        for ticket in tickets:
            print(
                f"{ticket.id:<8} "
                f"{ticket.title[:44]:<45} "
                f"{ticket.priority:<10}"
            )

        print("-" * 75)
        print(f"Всего заявок: {len(tickets)}")

    def get_all_tickets(self):
        """Получить актуальные заявки из BST."""
        return self.tree.inorder()

    def create_heap(self):
        """Создать максимальную кучу из текущих заявок."""
        return MaxHeap(self.get_all_tickets())

    # ---------- РАБОТА С ЗАЯВКАМИ ----------

    def add_ticket(self):
        """Добавление новой заявки."""

        print("\n=== ДОБАВЛЕНИЕ ЗАЯВКИ ===")

        ticket_id = self.read_int(
            "Введите ID заявки: ", min_value=1
        )

        if self.tree.search(ticket_id) is not None:
            print("Ошибка: заявка с таким ID уже существует.")
            return

        while True:
            title = input("Введите название заявки: ").strip()

            if title:
                break

            print("Ошибка: название не может быть пустым.")

        priority = self.read_int(
            "Введите приоритет (от 1 до 10): ",
            min_value=1
        )

        if priority > 10:
            print("Ошибка: приоритет не может превышать 10.")
            return

        ticket = Ticket(ticket_id, title, priority)

        if self.tree.insert(ticket):
            print("Заявка успешно добавлена.")
            print(ticket)
        else:
            print("Ошибка при добавлении заявки.")

    def find_ticket(self):
        """Поиск заявки по идентификатору."""

        print("\n=== ПОИСК ЗАЯВКИ ===")

        ticket_id = self.read_int(
            "Введите ID заявки: ", min_value=1
        )

        ticket = self.tree.search(ticket_id)

        if ticket is None:
            print("Заявка не найдена.")
        else:
            print("Найдена заявка:")
            print(ticket)

    def delete_ticket(self):
        """Удаление заявки по идентификатору."""

        print("\n=== УДАЛЕНИЕ ЗАЯВКИ ===")

        ticket_id = self.read_int(
            "Введите ID заявки: ", min_value=1
        )

        ticket = self.tree.search(ticket_id)

        if ticket is None:
            print("Заявка не найдена.")
            return

        print("Удаляемая заявка:")
        print(ticket)

        confirmation = input(
            "Подтвердить удаление? (да/нет): "
        ).strip().lower()

        if confirmation not in ("да", "д", "yes", "y"):
            print("Удаление отменено.")
            return

        if self.tree.delete(ticket_id):
            print("Заявка успешно удалена.")
        else:
            print("Ошибка при удалении заявки.")

    def show_all_tickets(self):
        """Просмотр всех заявок в порядке ID."""

        print("\n=== ВСЕ ЗАЯВКИ (ПО ID) ===")
        self.print_tickets(self.get_all_tickets())

    # ---------- БИНАРНОЕ ДЕРЕВО ----------

    def show_traversals(self):
        """Вывод всех четырёх обходов дерева."""

        print("\n=== ОБХОДЫ БИНАРНОГО ДЕРЕВА ===")

        if self.tree.root is None:
            print("Дерево пустое.")
            return

        traversals = [
            ("Прямой (NLR)", self.tree.preorder()),
            ("Симметричный (LNR)", self.tree.inorder()),
            ("Обратный (LRN)", self.tree.postorder()),
            ("Уровневый (BFS)", self.tree.level_order()),
        ]

        for name, tickets in traversals:
            ids = [ticket.id for ticket in tickets]

            print(f"\n{name}:")
            print(" -> ".join(map(str, ids)))

    def show_tree_stats(self):
        """Вывод характеристик BST."""

        print("\n=== ХАРАКТЕРИСТИКИ ДЕРЕВА ===")

        count = self.tree.count_nodes()
        leaves = self.tree.count_leaves()
        height = self.tree.height()

        print(f"Количество узлов: {count}")
        print(f"Количество листьев: {leaves}")
        print(f"Высота дерева (в уровнях): {height}")

        min_ticket = self.tree.min_ticket()
        max_ticket = self.tree.max_ticket()

        if min_ticket is not None:
            print(f"Минимальный ID: {min_ticket.id}")
            print(f"Максимальный ID: {max_ticket.id}")
        else:
            print("Дерево пустое.")

    def validate_tree(self):
        """Проверка свойств бинарного дерева поиска."""

        print("\n=== ПРОВЕРКА СВОЙСТВ BST ===")

        if self.tree.is_valid_bst():
            print("Дерево удовлетворяет свойствам BST.")
        else:
            print("Ошибка: нарушены свойства BST.")

    # ---------- ДВОИЧНАЯ КУЧА ----------

    def show_heap(self):
        """Построить и показать максимальную кучу."""

        print("\n=== МАКСИМАЛЬНАЯ ДВОИЧНАЯ КУЧА ===")

        heap = self.create_heap()

        if heap.is_empty():
            print("Нет заявок для построения кучи.")
            return

        print("Представление кучи массивом:")
        print()

        for index, ticket in enumerate(heap.get_array()):
            print(
                f"[{index}] "
                f"ID={ticket.id}, "
                f"priority={ticket.priority}, "
                f"title={ticket.title}"
            )

        print()
        print(f"Количество элементов: {heap.size()}")

        if heap.is_valid_heap():
            print("Свойство максимальной кучи соблюдается.")
        else:
            print("Ошибка: свойство кучи нарушено.")

        print("\nНаиболее срочная заявка:")
        print(heap.peek())

    def process_ticket(self):
        """Обработать наиболее срочную заявку."""

        print("\n=== ОБРАБОТКА СРОЧНОЙ ЗАЯВКИ ===")

        heap = self.create_heap()

        if heap.is_empty():
            print("Нет заявок для обработки.")
            return

        ticket = heap.extract_max()

        print("Выбрана наиболее срочная заявка:")
        print(ticket)

        confirmation = input(
            "Обработать заявку? (да/нет): "
        ).strip().lower()

        if confirmation not in ("да", "д", "yes", "y"):
            print("Обработка отменена.")
            return

        if self.tree.delete(ticket.id):
            print(
                f"Заявка #{ticket.id} успешно обработана "
                f"и удалена из списка активных заявок."
            )
        else:
            print("Ошибка при обработке заявки.")

    # ---------- СОРТИРОВКА КУЧЕЙ ----------

    def show_report(self):
        """Формирование отчёта методом Heap Sort."""

        print("\n=== ИТОГОВЫЙ ОТЧЁТ (HEAP SORT) ===")

        tickets = self.get_all_tickets()

        if not tickets:
            print("Нет заявок для формирования отчёта.")
            return

        sorted_tickets = heap_sort(tickets)

        print("Заявки отсортированы по убыванию приоритета:")
        self.print_tickets(sorted_tickets)

    # ---------- ДЕМОНСТРАЦИОННЫЕ ДАННЫЕ ----------

    def load_demo_data(self):
        """Добавление демонстрационных заявок."""

        print("\n=== ЗАГРУЗКА ДЕМОНСТРАЦИОННЫХ ДАННЫХ ===")

        demo_tickets = [
            Ticket(50, "Ошибка сервера", 5),
            Ticket(30, "Не работает принтер", 2),
            Ticket(70, "Сбой базы данных", 5),
            Ticket(20, "Сброс пароля", 1),
            Ticket(40, "Проблема с почтой", 3),
            Ticket(60, "Не работает API", 4),
            Ticket(80, "Ошибка авторизации", 3),
        ]

        added = 0
        skipped = 0

        for ticket in demo_tickets:
            if self.tree.insert(ticket):
                added += 1
            else:
                skipped += 1

        print(f"Добавлено заявок: {added}")
        print(f"Пропущено повторяющихся ID: {skipped}")

    # ---------- ГЛАВНОЕ МЕНЮ ----------

    @staticmethod
    def show_menu():
        """Отображение главного меню."""

        print("\n" + "=" * 55)
        print("     ДИСПЕТЧЕР ЗАЯВОК СЛУЖБЫ ПОДДЕРЖКИ")
        print("=" * 55)

        print("1. Добавить заявку")
        print("2. Найти заявку по ID")
        print("3. Удалить заявку")
        print("4. Показать все заявки")
        print("5. Обходы бинарного дерева")
        print("6. Характеристики дерева")
        print("7. Проверить свойства BST")
        print("8. Показать максимальную кучу")
        print("9. Обработать самую срочную заявку")
        print("10. Итоговый отчёт (Heap Sort)")
        print("11. Загрузить демонстрационные данные")
        print("0. Выход")

        print("=" * 55)

    def run(self):
        """Основной цикл программы."""

        actions = {
            1: self.add_ticket,
            2: self.find_ticket,
            3: self.delete_ticket,
            4: self.show_all_tickets,
            5: self.show_traversals,
            6: self.show_tree_stats,
            7: self.validate_tree,
            8: self.show_heap,
            9: self.process_ticket,
            10: self.show_report,
            11: self.load_demo_data,
        }

        while True:
            self.show_menu()

            choice = self.read_int("\nВыберите действие: ")

            if choice == 0:
                print("\nРабота программы завершена.")
                break

            action = actions.get(choice)

            if action is None:
                print("Ошибка: неизвестный пункт меню.")
                continue

            action()


if __name__ == "__main__":
    dispatcher = SupportDispatcher()

    try:
        dispatcher.run()
    except (KeyboardInterrupt, EOFError):
        print("\nРабота программы прервана.")
