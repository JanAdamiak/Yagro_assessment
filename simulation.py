from typing import Dict, List

from conveyor_belt import ConveyorBelt
from worker import Worker


class Simulation:
    def __init__(self, length_of_conveyor_belt: int, steps: int, workers: Dict[int, List[Worker]]) -> None:
        self.conveyor_belt = ConveyorBelt(length_of_conveyor_belt)
        self.steps = steps
        self.workers = workers
        self.basket = {}

    def resolve_one_step_of_time(self) -> None:
        """Resolve actions equal to one unit of time (movement of the conveyor belt and worker actions)."""
        self.resolve_belt_action()
        self.resolve_worker_actions()

    def resolve_belt_action(self) -> None:
        dropped_item = self.conveyor_belt.move()
        if dropped_item:
            self.basket[dropped_item] = self.basket[dropped_item] + 1
        
    def resolve_worker_actions(self) -> None:
        for belt_index, worker in self.workers.items():
            


    def run_simulation(self) -> None:
        while self.steps > 0:
            self.resolve_actions()
            self.steps =- 1
    
    def worker_method_dispatcher(self) -> callable:
        return {

        }

    def execute_worker_command(self, worker: Worker) -> None:
        pass