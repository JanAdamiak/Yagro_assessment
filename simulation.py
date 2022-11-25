from typing import Dict, List

from conveyor_belt import ConveyorBelt
from worker import Worker
from enums import WorkerState, FactoryItem, COMPONENTS
from exceptions import TooManyWorkersAtBelt


class Simulation:
    """
    Simulation object takes in 3 integer parameters length_of_conveyor_belt, steps, pairs_of_workers.
    If length_of_conveyor_belt < pairs_of_workers it will raise a custom exception.

    It tries to assign all of the workers to the conveyor belt.
    """

    def __init__(
        self, length_of_conveyor_belt: int, steps: int, pairs_of_workers: int
    ) -> None:
        if length_of_conveyor_belt < pairs_of_workers:
            raise TooManyWorkersAtBelt()

        self.conveyor_belt = ConveyorBelt(length_of_conveyor_belt)
        self.steps = steps
        self.workers = self.place_workers_along_the_belt(pairs_of_workers)

        self.basket = {}
        self.workers_requiring_cleanup = []

    def resolve_one_step_of_time(self) -> None:
        """Resolve actions equal to one unit of time (movement of the conveyor belt and worker actions)."""
        self.resolve_belt_action()
        self.resolve_worker_actions()

        self.cleanup_workers()
        self.steps = self.steps - 1

    def place_workers_along_the_belt(self, pairs_of_workers) -> Dict[int, List[Worker]]:
        """This method places all pairs of workers along the belt"""

        return {n: [Worker(), Worker()] for n in range(0, pairs_of_workers)}

    def resolve_belt_action(self) -> None:
        """This method goes through one movement of conveyor belt and records what fell off it"""
        dropped_item = self.conveyor_belt.move_belt()

        if dropped_item != FactoryItem.EMPTY_SPACE:
            self.basket[dropped_item] = self.basket.get(dropped_item, 0) + 1

    def resolve_worker_actions(self) -> None:
        """
        This method is really ugly and should be broken into smaller parts and/or fully rethought.

        It's responsible for iterating through all of the worker pairs,
        checking if any of them have workers in the assembling state.
        Then going through flow matching assembling state.

        Then it checks for other states matching the item on the conveyor belt.
        If it's done by one worker the other worker skips their action (as item disappears is placed).

        Any workers that should change state are added to a list and are iterated later over to change their state.
        """
        for belt_index, workers in self.workers.items():
            item = self.conveyor_belt.contents[belt_index]

            for worker in workers:
                if worker.current_state == WorkerState.ASSEMBLING:
                    is_worker_changing_state = worker.continue_assembling()
                    if is_worker_changing_state:
                        self.workers_requiring_cleanup.append(worker)

            if item in COMPONENTS:
                for worker in workers:
                    if (
                        worker.current_state == WorkerState.LOOKING_FOR_PARTS
                        and worker.is_part_desired_by_worker(item)
                    ):
                        self.conveyor_belt.pick_up_item(belt_index)
                        is_worker_changing_state = worker.pick_up_part(item)
                        if is_worker_changing_state:
                            self.workers_requiring_cleanup.append(worker)
                        break

            elif item == FactoryItem.EMPTY_SPACE:
                for worker in workers:
                    if worker.current_state == WorkerState.WAITING_TO_DROP_ITEM:
                        self.conveyor_belt.place_completed_item(belt_index)
                        is_worker_changing_state = worker.drop_completed_item()
                        if is_worker_changing_state:
                            self.workers_requiring_cleanup.append(worker)
                        break

    def cleanup_workers(self) -> None:
        """
        This method iterates through workers awaiting new state applying it to them,
        then assigns a new empty list.
        """
        for worker in self.workers_requiring_cleanup:
            worker.set_new_state()

        self.workers_requiring_cleanup = []

    def run_simulation(self) -> None:
        """This method makes it simpler to use Simulation object as an API."""
        while self.steps > 0:
            self.resolve_one_step_of_time()

            # print(self.conveyor_belt.contents)

        print(self.basket)
