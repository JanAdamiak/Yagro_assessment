from random import randint

from enums import FactoryItem


def spawn_random_item() -> FactoryItem:
    """
    Spawns a random component or empty space.
    All 3 are equally distributed and ahve equal chance of happening.
    """
    random_number = randint(0, 2)
    return FactoryItem(random_number)
