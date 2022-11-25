import itertools

from enums import WorkerState, COMPONENTS, FactoryItem


class Worker:
    id_iter = itertools.count()

    def __init__(self) -> None:
        self.worker_id = next(self.id_iter)
        self.current_state = WorkerState.LOOKING_FOR_PARTS
        self.inventory = set()
        self.time_until_completion = 0
        self.new_state: WorkerState = None

    def pick_up_part(self, item: FactoryItem) -> bool:
        """
        Worker attempts to pick up a spare part.
        If 2 different components present, changes state to ASSEMBLING and starts assembling it.
        """
        self.inventory.add(item)

        if self.inventory == COMPONENTS:
            self.new_state = WorkerState.ASSEMBLING
            self.time_until_completion = 3
            return True
        return False

    def continue_assembling(self) -> bool:
        """
        Worker continues assembling the item for 3 units of time.
        If finished, completed item is put in their inventory
        and worker's state changes to WAITING_TO_DROP_ITEM.
        """
        self.time_until_completion = self.time_until_completion - 1

        if self.time_until_completion == 0:
            self.new_state = WorkerState.WAITING_TO_DROP_ITEM
            self.inventory = {FactoryItem.FINISHED_PRODUCT}
            return True
        return False

    def drop_completed_item(self) -> True:
        """
        Worker drops completed item on the belt.
        It empties their inventory and transitions them back to the state LOOKING_FOR_PARTS.
        """
        self.new_state = WorkerState.LOOKING_FOR_PARTS
        self.inventory = set()
        return True

    def is_part_desired_by_worker(self, item: FactoryItem) -> bool:
        """A boolean method to check if worker already has part in their inventory"""
        if item in COMPONENTS and item not in self.inventory:
            return True
        return False

    def set_new_state(self) -> None:
        """A method to change to new state stored in temporary state. Changes temporary state back to None."""
        self.current_state = self.new_state
        self.new_state = None
