from dataclasses import dataclass
from typing import List

from utils import spawn_random_item
from enums import FactoryItem, COMPONENTS
from exceptions import TriedToPickUpNonComponentItem, NotAnEmptySpace


class ConveyorBelt:
    def __init__(self, length: int) -> None:
        # self.length = length
        self.contents = [FactoryItem.EMPTY_SPACE] * length

    def move_belt(self) -> FactoryItem:
        new_item = spawn_random_item()
        self.contents.insert(0, new_item)

        return self.contents.pop()

    def pick_up_item(self, index: int) -> None:
        if not self.contents[index] in COMPONENTS:
            raise TriedToPickUpNonComponentItem

        self.contents[index] = FactoryItem.EMPTY_SPACE

    def place_completed_item(self, index: int) -> None:
        if self.contents[index] != FactoryItem.EMPTY_SPACE:
            raise NotAnEmptySpace

        self.contents[index] = FactoryItem.FINISHED_PRODUCT
