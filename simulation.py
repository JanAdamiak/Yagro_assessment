from typing import Dict, List

from conveyor_belt import ConveyorBelt
from worker import Worker
from enums import WorkerState


class Simulation:
    def __init__(self, length_of_conveyor_belt: int, steps: int, workers: Dict[int, List[Worker]]) -> None:
        self.conveyor_belt = ConveyorBelt(length_of_conveyor_belt)
        self.steps = steps
        self.workers = workers
        self.basket = {}

        self.workers_requiring_cleanup: List[Worker]

    def resolve_one_step_of_time(self) -> None:
        """Resolve actions equal to one unit of time (movement of the conveyor belt and worker actions)."""
        self.resolve_belt_action()
        self.resolve_worker_actions()

    def resolve_belt_action(self) -> None:
        dropped_item = self.conveyor_belt.move_belt()
        if dropped_item:
            self.basket[dropped_item] = self.basket[dropped_item] + 1
        
    def resolve_worker_actions(self) -> None:
        for belt_index, workers in self.workers.items():
            for worker in workers:

                if worker.current_state == WorkerState.ASSEMBLING:
                    worker.continue_assembling()

            item = self.conveyor_belt.contents[belt_index]
            if worker.current_state == WorkerState.LOOKING_FOR_PARTS and worker.is_part_desired_by_worker(item):
                self.conveyor_belt.pick_up_item(belt_index)
                worker.pick_up_part(item)



    def run_simulation(self) -> None:
        while self.steps > 0:
            self.resolve_one_step_of_time()
            self.steps =- 1
