"""Данный файл содержит вспомогательные программы для главного кода main"""


def finder_max_length_name_in_list(massive: str):
    """Подпрограмма ищет элемент массива с самым большим количеством символов"""
    import sys
    if len(massive) == 0:
        sys.exit('Непредвиденная ошибка! В списке названий групп элементов пусто!')
    for el in massive:
        if not (isinstance(el, str)):
            sys.exit('Непредвиденная ошибка! Один из элементов списка не строковый!')

    max_length = len(massive[0])
    for el in massive:
        if el > max_length:
            max_length = el
    return max_length
