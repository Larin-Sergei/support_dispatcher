from ticket import Ticket
from heap import MaxHeap
from heap_sort import heap_sort


tickets = [
    Ticket(50, "Ошибка сервера", 5),
    Ticket(30, "Не работает принтер", 2),
    Ticket(70, "Сбой базы данных", 5),
    Ticket(20, "Сброс пароля", 1),
    Ticket(40, "Проблема с почтой", 3),
    Ticket(60, "Не работает API", 4),
    Ticket(80, "Ошибка авторизации", 3),
]

print("=== ПОСТРОЕНИЕ МАКСИМАЛЬНОЙ КУЧИ ===")

heap = MaxHeap(tickets)

print("Массив кучи:")
print([(t.id, t.priority) for t in heap.get_array()])

print("Количество заявок:", heap.size())
print("Корректность кучи:", heap.is_valid_heap())
print("Самая срочная заявка:", heap.peek())

print("\n=== ДОБАВЛЕНИЕ ЗАЯВКИ ===")

new_ticket = Ticket(90, "Критическая ошибка", 10)
heap.insert(new_ticket)

print("Добавлена:", new_ticket)
print("Самая срочная:", heap.peek())
print("Корректность кучи:", heap.is_valid_heap())

print("\n=== ИЗВЛЕЧЕНИЕ МАКСИМУМА ===")

extracted = heap.extract_max()

print("Извлечена:", extracted)
print("Следующая заявка:", heap.peek())
print("Корректность кучи:", heap.is_valid_heap())

print("\n=== ОБРАБОТКА ВСЕХ ЗАЯВОК ===")

while not heap.is_empty():
    ticket = heap.extract_max()
    print(f"ID: {ticket.id}, приоритет: {ticket.priority}")

print("\n=== СОРТИРОВКА КУЧЕЙ ===")

sorted_tickets = heap_sort(tickets)

for ticket in sorted_tickets:
    print(
        f"ID: {ticket.id}, "
        f"приоритет: {ticket.priority}, "
        f"название: {ticket.title}"
    )

print("\n=== АВТОМАТИЧЕСКИЕ ПРОВЕРКИ ===")

assert [t.id for t in sorted_tickets] == [
    50, 70, 60, 40, 80, 30, 20
]

assert [t.id for t in tickets] == [
    50, 30, 70, 20, 40, 60, 80
]

assert heap.is_empty()

print("Все проверки пройдены!")
