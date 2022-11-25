import itertools

from conveyor_belt import FactoryItem
from enums import WorkerState, COMPONENTS


class Worker:
    id_iter = itertools.count()

    def __init__(self) -> None:
        self.id = next(self.id_iter)
        self.current_state = WorkerState.LOOKING_FOR_PARTS
        self.inventory = set()
        self.time_until_completion = 0
        self.new_state: WorkerState = None

    def pick_up_part(self, item: FactoryItem) -> bool:
        if self.current_state != WorkerState.LOOKING_FOR_PARTS:
            raise BaseException(f"pick_up_part:: something went wrong, state: {self.current_state}")
        
        self.inventory.add(item)

        if self.inventory == COMPONENTS:
            self.new_state = WorkerState.ASSEMBLING
            self.time_until_completion = 3
            return True
        return False

    def continue_assembling(self) -> bool:
        if self.current_state != WorkerState.ASSEMBLING or self.time_until_completion < 0:
            raise BaseException(f"continue_assembling:: something went wrong, state: {self.current_state}, timer: {self.time_until_completion}")

        self.time_until_completion = self.time_until_completion - 1

        if self.time_until_completion == 0:
            self.new_state = WorkerState.WAITING_TO_DROP_ITEM
            self.inventory = {FactoryItem.FINISHED_PRODUCT}
            return True
        return False

    def drop_completed_item(self) -> bool:
        if self.current_state != WorkerState.WAITING_TO_DROP_ITEM:
            raise BaseException(f"drop_completed_item:: something went wrong, state: {self.current_state}")

        if self.time_until_completion == 0:
            self.new_state = WorkerState.LOOKING_FOR_PARTS
            self.inventory = set()
            return True
        return False

    def is_part_desired_by_worker(self, item: FactoryItem) -> bool:
        if item in COMPONENTS and item not in self.inventory:
            return True
        return False

    def set_new_state(self) -> None:
        self.current_state = self.new_state
        self.new_state = None