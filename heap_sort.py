from ticket import Ticket


def is_higher(first: Ticket, second: Ticket) -> bool:
    """
    Определить порядок заявок.

    Больший приоритет идёт первым.
    При равных приоритетах меньший ID идёт первым.
    """
    if first.priority != second.priority:
        return first.priority > second.priority

    return first.id < second.id


def heapify(tickets, size, index):
    """
    Восстановить свойство максимальной кучи
    в пределах первых size элементов.
    """
    while True:
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if (
            left < size
            and is_higher(tickets[left], tickets[largest])
        ):
            largest = left

        if (
            right < size
            and is_higher(tickets[right], tickets[largest])
        ):
            largest = right

        if largest == index:
            break

        tickets[index], tickets[largest] = (
            tickets[largest],
            tickets[index]
        )

        index = largest


def heap_sort(tickets):
    """
    Сортировка кучей по убыванию приоритета.

    Исходный список не изменяется.
    """
    result = list(tickets)
    size = len(result)

    for i in range(size // 2 - 1, -1, -1):
        heapify(result, size, i)

    for end in range(size - 1, 0, -1):
        result[0], result[end] = result[end], result[0]
        heapify(result, end, 0)

    result.reverse()

    return result
