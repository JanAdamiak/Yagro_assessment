import pytest

from worker import Worker
from enums import WorkerState, FactoryItem


def test_initialising_worker():
    worker = Worker()

    assert worker.current_state == WorkerState.LOOKING_FOR_PARTS
    assert worker.inventory == set()


@pytest.mark.parametrize(
    "part",
    [FactoryItem.COMPONENT_A, FactoryItem.COMPONENT_B],
)
def test_pick_up_part(part):
    worker = Worker()
    assert len(worker.inventory) == 0

    worker.pick_up_part(part)
    assert len(worker.inventory) == 1


def test_pick_up_part_both_parts_inventory():
    worker = Worker()

    assert not worker.pick_up_part(FactoryItem.COMPONENT_A)
    assert worker.time_until_completion == 0
    assert worker.new_state is None

    assert worker.pick_up_part(FactoryItem.COMPONENT_B)
    assert worker.time_until_completion == 3
    assert worker.new_state == WorkerState.ASSEMBLING


@pytest.mark.parametrize(
    "timer, expected",
    [(3, False), (2, False), (1, True)],
)
def test_continue_assembling(timer, expected):
    worker = Worker()
    worker.current_state = WorkerState.ASSEMBLING
    worker.time_until_completion = timer

    assert worker.continue_assembling() == expected


def test_drop_completed_item():
    worker = Worker()
    worker.current_state = WorkerState.WAITING_TO_DROP_ITEM
    worker.inventory = {FactoryItem.FINISHED_PRODUCT}

    assert worker.drop_completed_item()
    assert len(worker.inventory) == 0
    assert worker.new_state == WorkerState.LOOKING_FOR_PARTS


@pytest.mark.parametrize(
    "inventory, part, expected",
    [
        (
            {FactoryItem.COMPONENT_A, FactoryItem.COMPONENT_B},
            FactoryItem.COMPONENT_A,
            False,
        ),
        (
            {FactoryItem.COMPONENT_A},
            FactoryItem.COMPONENT_A,
            False,
        ),
        (
            {FactoryItem.COMPONENT_B},
            FactoryItem.COMPONENT_A,
            True,
        ),
        (
            set(),
            FactoryItem.COMPONENT_B,
            True,
        ),
    ],
)
def test_is_part_desired_by_worker(inventory, part, expected):
    worker = Worker()
    worker.inventory = inventory

    assert worker.is_part_desired_by_worker(part) == expected


@pytest.mark.parametrize(
    "current_state, new_state",
    [
        (WorkerState.LOOKING_FOR_PARTS, WorkerState.ASSEMBLING),
        (WorkerState.ASSEMBLING, WorkerState.WAITING_TO_DROP_ITEM),
        (WorkerState.WAITING_TO_DROP_ITEM, WorkerState.LOOKING_FOR_PARTS),
        (
            WorkerState.LOOKING_FOR_PARTS,
            WorkerState.LOOKING_FOR_PARTS,
        ),  # currently accepted even though this state change should not happen
        (
            WorkerState.LOOKING_FOR_PARTS,
            WorkerState.WAITING_TO_DROP_ITEM,
        ),  # currently accepted even though this state change should not happen
        (
            WorkerState.ASSEMBLING,
            WorkerState.WAITING_TO_DROP_ITEM,
        ),  # currently accepted even though this state change should not happen
    ],
)
def test_set_new_state(current_state, new_state):
    worker = Worker()
    worker.current_state = current_state
    worker.new_state = new_state

    worker.set_new_state()
    assert worker.current_state == new_state
    assert worker.new_state is None
