from enum import Enum


class FactoryItem(Enum):
    EMPTY_SPACE = 0
    COMPONENT_A = 1
    COMPONENT_B = 2
    FINISHED_PRODUCT = 3


COMPONENTS = {FactoryItem.COMPONENT_A, FactoryItem.COMPONENT_B}


class WorkerState(Enum):
    LOOKING_FOR_PARTS = 0
    ASSEMBLING = 1
    WAITING_TO_DROP_ITEM = 2
