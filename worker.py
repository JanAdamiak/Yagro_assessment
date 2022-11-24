from enum import Enum
from conveyor_belt import FactoryItem


class WorkerState(Enum):
    LOOKING_FOR_PARTS = 0
    ASSEMBLING = 1
    WAITING_TO_DROP_ITEM = 2


class Worker:
    def __init__(self) -> None:
        self.current_state = WorkerState.LOOKING_FOR_PARTS
        self.inventory = set()
        self.time_until_completion = 0


    def attempt_to_pick_up_part(self, item: FactoryItem) -> None:
        if item not in self.inventory:
            self.inventory.add(item)

        

    def continue_assembling(self, item: FactoryItem) -> None:
        self.time_until_completion =- 1

        if self.time_until_completion == 0:
            self.current_state = WorkerState.WAITING_TO_DROP_ITEM
            self.

    def attempt_to_pick_up_part(self, item: FactoryItem) -> None:
        pass
