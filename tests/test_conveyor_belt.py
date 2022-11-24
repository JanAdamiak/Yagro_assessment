import pytest

from enums import FactoryItem
from conveyor_belt import ConveyorBelt




@pytest.mark.parametrize("length, expected", [(1, [FactoryItem.EMPTY_SPACE]), (2, [FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE]), (4, [FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE])])
def test_initalising_different_length(length, expected):
    new_belt = ConveyorBelt(length)
    assert new_belt.contents == expected


def test_conveyor_belt_item_spawning(monkeypatch):

    def mock_spawn_random_item():
        return FactoryItem.COMPONENT_A

    monkeypatch.setattr('conveyor_belt.spawn_random_item', mock_spawn_random_item)

    new_belt = ConveyorBelt(3)   
    assert new_belt.contents == [FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE]

    ejected_item = new_belt.move_belt()
    assert new_belt.contents == [FactoryItem.COMPONENT_A, FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE]
    assert ejected_item == FactoryItem.EMPTY_SPACE


def test_picking_up_item():
    new_belt = ConveyorBelt(3)
    new_belt.contents = [FactoryItem.COMPONENT_A, FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE]
    assert new_belt.contents == [FactoryItem.COMPONENT_A, FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE]

    new_belt.pick_up_item(0)

    assert new_belt.contents == [FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE]

def test_place_completed_item():
    new_belt = ConveyorBelt(3)   
    assert new_belt.contents == [FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE, FactoryItem.EMPTY_SPACE]

    new_belt.place_completed_item(1)
    assert new_belt.contents == [FactoryItem.EMPTY_SPACE, FactoryItem.FINISHED_PRODUCT, FactoryItem.EMPTY_SPACE]
