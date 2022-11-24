from worker import Worker
from enums import WorkerState

def test_initialising_worker():
    worker = Worker()

    assert worker.current_state == WorkerState.LOOKING_FOR_PARTS
    assert worker.inventory == set()


def test_pick_up_part():
    