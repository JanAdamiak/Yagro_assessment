from dataclasses import dataclass
from enum import Enum

class FactoryItem(Enum):
    EMPTY_SPACE = 0
    COMPONENT_A = 1
    COMPONENT_B = 2
    FINISHED_PRODUCT = 3

@dataclass
class ConveyorBelt:
    length: int

    def move_belt(self):

    def 