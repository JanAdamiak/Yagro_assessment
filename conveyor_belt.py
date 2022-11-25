from utils import spawn_random_item
from enums import FactoryItem, COMPONENTS
from exceptions import TriedToPickUpNonComponentItem, NotAnEmptySpace


class ConveyorBelt:
    def __init__(self, length: int) -> None:
        self.contents = [FactoryItem.EMPTY_SPACE] * length

    def move_belt(self) -> FactoryItem:
        """
        Moves belt by one lentgh, adds a new random item to the start of the belt.
        Returns the last item that fell off the conveyor belt.
        """
        new_item = spawn_random_item()
        self.contents.insert(0, new_item)

        return self.contents.pop()

    def pick_up_item(self, index: int) -> None:
        """Replaces a component item on a conveyor belt with empty space."""
        if not self.contents[index] in COMPONENTS:
            raise TriedToPickUpNonComponentItem

        self.contents[index] = FactoryItem.EMPTY_SPACE

    def place_completed_item(self, index: int) -> None:
        """Replaces empty space with a finished product on the conveyor belt."""
        if self.contents[index] != FactoryItem.EMPTY_SPACE:
            raise NotAnEmptySpace

        self.contents[index] = FactoryItem.FINISHED_PRODUCT
