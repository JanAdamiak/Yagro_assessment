from random import randint

from enums import FactoryItem


def spawn_random_item() -> FactoryItem:
    random_number = randint(0, 2)
    return FactoryItem(random_number)
