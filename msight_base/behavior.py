from enum import Enum


class BehaviorType(Enum):
    """
    Enum for different types of behaviors.
    """
    UNKNOWN = -1
    CONSTANT = 0
    ACCELERATE = 1
    DECELERATE = 2
    STOP = 3
    LANE_KEEPING = 4
    LANE_CHANGING = 5
    LANE_DEPARTURE = 6
    TURNING_LEFT = 7
    TURNING_RIGHT = 8

    # Additional behaviors
    U_TURN = 9
    YIELDING = 10
    FOLLOWING = 11
    OVERTAKING = 12
    PARKING = 13
    EMERGENCY_BRAKING = 14

    def __str__(self):
        return self.name.lower()
