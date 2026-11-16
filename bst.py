from collections import deque
from ticket import Ticket


class TreeNode:
    """Узел бинарного дерева поиска."""

    def __init__(self, ticket: Ticket):
        self.ticket = ticket
        self.left = None
        self.right = None


class BinarySearchTree:
    """Бинарное дерево поиска заявок по ID."""

    def __init__(self):
        self.root = None

    def insert(self, ticket: Ticket) -> bool:
        """Добавить заявку. Возвращает False при повторном ID."""

        if self.root is None:
            self.root = TreeNode(ticket)
            return True

        current = self.root

        while True:
            if ticket.id == current.ticket.id:
                return False

            if ticket.id < current.ticket.id:
                if current.left is None:
                    current.left = TreeNode(ticket)
                    return True
                current = current.left
            else:
                if current.right is None:
                    current.right = TreeNode(ticket)
                    return True
                current = current.right

    def search(self, ticket_id: int):
        """Найти заявку по идентификатору."""

        current = self.root

        while current is not None:
            if ticket_id == current.ticket.id:
                return current.ticket

            if ticket_id < current.ticket.id:
                current = current.left
            else:
                current = current.right

        return None

    def delete(self, ticket_id: int) -> bool:
        """Удалить заявку по ID."""

        if self.search(ticket_id) is None:
            return False

        self.root = self._delete_recursive(self.root, ticket_id)
        return True

    def _delete_recursive(self, node, ticket_id):
        if node is None:
            return None

        if ticket_id < node.ticket.id:
            node.left = self._delete_recursive(node.left, ticket_id)

        elif ticket_id > node.ticket.id:
            node.right = self._delete_recursive(node.right, ticket_id)

        else:
            # Случай 1: нет левого потомка
            if node.left is None:
                return node.right

            # Случай 2: нет правого потомка
            if node.right is None:
                return node.left

            # Случай 3: два потомка
            successor = self._find_min_node(node.right)
            node.ticket = successor.ticket

            node.right = self._delete_recursive(
                node.right,
                successor.ticket.id
            )

        return node

    def _find_min_node(self, node):
        while node.left is not None:
            node = node.left

        return node

    def preorder(self):
        """Прямой обход: корень -> левый -> правый."""
        result = []

        def traverse(node):
            if node is not None:
                result.append(node.ticket)
                traverse(node.left)
                traverse(node.right)

        traverse(self.root)
        return result

    def inorder(self):
        """Симметричный обход: левый -> корень -> правый."""
        result = []

        def traverse(node):
            if node is not None:
                traverse(node.left)
                result.append(node.ticket)
                traverse(node.right)

        traverse(self.root)
        return result

    def postorder(self):
        """Обратный обход: левый -> правый -> корень."""
        result = []

        def traverse(node):
            if node is not None:
                traverse(node.left)
                traverse(node.right)
                result.append(node.ticket)

        traverse(self.root)
        return result

    def level_order(self):
        """Уровневый обход с использованием очереди."""
        if self.root is None:
            return []

        result = []
        queue = deque([self.root])

        while queue:
            node = queue.popleft()
            result.append(node.ticket)

            if node.left is not None:
                queue.append(node.left)

            if node.right is not None:
                queue.append(node.right)

        return result

    def count_nodes(self):
        """Общее количество узлов."""

        def count(node):
            if node is None:
                return 0

            return 1 + count(node.left) + count(node.right)

        return count(self.root)

    def count_leaves(self):
        """Количество листьев."""

        def count(node):
            if node is None:
                return 0

            if node.left is None and node.right is None:
                return 1

            return count(node.left) + count(node.right)

        return count(self.root)

    def height(self):
        """Высота дерева в количестве уровней."""

        def calculate(node):
            if node is None:
                return 0

            return 1 + max(
                calculate(node.left),
                calculate(node.right)
            )

        return calculate(self.root)

    def min_ticket(self):
        """Заявка с минимальным ID."""
        if self.root is None:
            return None

        return self._find_min_node(self.root).ticket

    def max_ticket(self):
        """Заявка с максимальным ID."""
        if self.root is None:
            return None

        current = self.root

        while current.right is not None:
            current = current.right

        return current.ticket

    def is_valid_bst(self):
        """Проверить соблюдение свойства BST."""

        def validate(node, min_id, max_id):
            if node is None:
                return True

            ticket_id = node.ticket.id

            if min_id is not None and ticket_id <= min_id:
                return False

            if max_id is not None and ticket_id >= max_id:
                return False

            return (
                validate(node.left, min_id, ticket_id)
                and validate(node.right, ticket_id, max_id)
            )

        return validate(self.root, None, None)
