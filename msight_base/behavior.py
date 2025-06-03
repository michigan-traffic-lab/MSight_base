from enum import Enum


class BehaviorType(Enum):
    """
    Enum for different types of behaviors.
    """
    UNKNOWN = 0
    CONSTANT = 1
    ACCELERATE = 2
    DECELERATE = 3
    STOP = 4
    LANE_KEEPING = 5
    LANE_CHANGING = 6
    LANE_DEPARTURE = 7
    TURNING_LEFT = 8
    TURNING_RIGHT = 9

    # Additional behaviors
    U_TURN = 10
    YIELDING = 11
    FOLLOWING = 12
    OVERTAKING = 13
    PARKING = 14
    EMERGENCY_BRAKING = 15
