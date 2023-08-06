from ovirt_python_sdk.exceptions import TooManyItemsException, ItemNotFoundException


def find_one_in_list_by_name(items_list: list, name: str):
    """
    Поиск ровно одного элемента в списке

    .list(search="...") не работает :(

    :param items_list: Список
    :param name: Искомое название
    :return: Найденный элемент
    """
    result = []

    for item in items_list:
        if item.name == name:
            result.append(item)

        if len(result) > 1:
            raise TooManyItemsException(len(result))

    if len(result) == 0:
        raise ItemNotFoundException(name)

    return result[0]
