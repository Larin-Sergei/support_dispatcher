
from ticket import Ticket
from bst import BinarySearchTree


tree = BinarySearchTree()

tickets = [
    Ticket(50, "Ошибка сервера", 5),
    Ticket(30, "Не работает принтер", 2),
    Ticket(70, "Сбой базы данных", 5),
    Ticket(20, "Сброс пароля", 1),
    Ticket(40, "Проблема с почтой", 3),
    Ticket(60, "Не работает API", 4),
    Ticket(80, "Ошибка авторизации", 3),
]

for ticket in tickets:
    tree.insert(ticket)

print("=== ОБХОДЫ ДЕРЕВА ===")

print("Прямой:",
      [t.id for t in tree.preorder()])

print("Симметричный:",
      [t.id for t in tree.inorder()])

print("Обратный:",
      [t.id for t in tree.postorder()])

print("Уровневый:",
      [t.id for t in tree.level_order()])

print("\n=== ХАРАКТЕРИСТИКИ ===")

print("Количество узлов:", tree.count_nodes())
print("Количество листьев:", tree.count_leaves())
print("Высота дерева:", tree.height())
print("Минимальный ID:", tree.min_ticket().id)
print("Максимальный ID:", tree.max_ticket().id)
print("Корректное BST:", tree.is_valid_bst())

print("\n=== ПОИСК ===")
print(tree.search(40))
print("Поиск 999:", tree.search(999))

print("\n=== ПРОВЕРКА УДАЛЕНИЯ ===")

print("Удаление листа 20:", tree.delete(20))
print("Удаление узла с одним потомком 30:",
      tree.delete(30))
print("Удаление узла с двумя потомками 70:",
      tree.delete(70))

print("Оставшиеся ID:",
      [t.id for t in tree.inorder()])

print("BST корректно:", tree.is_valid_bst())
