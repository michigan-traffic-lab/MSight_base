from enum import Enum


class RoadUserPoint:
    def __init__(self,
                 timestamp=None,
                 frame_step=None,
                 traj_id=None,
                 x=None,
                 y=None,
                 speed=None,
                 acceleration=None,
                 heading=None,
                 width=None,
                 length=None,
                 poly_box=None,
                 category=None,
                 confidence=None,
                 turning_signal=None,
                 map_info=None,
                 sensor_data={},
                 behaviors=[],):
        self._timestamp = timestamp
        self._frame_step = frame_step
        self.x = x
        self.y = y
        self.speed = speed
        self.acceleration = acceleration
        self.heading = heading
        self.width = width
        self.length = length
        self.poly_box = poly_box
        self.category = category
        self.traj = None
        self.frame = None
        self.prev = None
        self.next = None
        self.sensor_data = sensor_data # sensor id to sensor data map
        self.confidence = confidence
        self.turning_signal = turning_signal
        self.map_info = map_info
        self.behaviors = behaviors
        self.pred_trajectory = None

        ## this is used to store the id when the object's trajectory is not yet created or assigned
        self._traj_id = traj_id

        ## this is also used to store the id when the object's trajectory is not yet created or assigned
        ## for some use cases, we need a uuid instead of a trajectory id (that increments from 0)
        self._traj_uuid = None

    @property
    def traj_id(self):
        if self.traj is not None:
            return self.traj.id
        return self._traj_id

    @traj_id.setter
    def traj_id(self, value):
        if self.traj is not None:
            raise AttributeError("Cannot set traj_id directly when traj is assigned.")
        self._traj_id = value

    @property
    def frame_step(self):
        if self.frame is None:
            return None
        return self.frame.step
    
    @frame_step.setter
    def frame_step(self, value):
        if self.frame is not None:
            raise AttributeError("Cannot set frame_step directly when frame is assigned.")
        self._frame_step = value

    @property
    def timestamp(self):
        if self.frame is None:
            return None
        return self.frame.timestamp
    
    @timestamp.setter
    def timestamp(self, value):
        if self.frame is not None:
            raise AttributeError("Cannot set timestamp directly when frame is assigned.")
        self._timestamp = value

    @staticmethod
    def from_dict(object_dict):
        return RoadUserPoint(
            object_dict['x'],
            object_dict['y'],
            speed=object_dict['speed'],
            acceleration=object_dict['acceleration'],
            source=object_dict['source'],
            heading=object_dict['heading'],
            width=object_dict['width'],
            length=object_dict['length'],
            id=object_dict['id'],
        )

    def to_dict(self):
        return {
            'source': self.source,
            'traj_id': self.traj_id,
            'frame_step': self.frame_step,
            'timestamp': self.timestamp,
            'x': self.x,
            'y': self.y,
            'speed': self.speed,
            'acceleration': self.acceleration,
            'heading': self.heading,
            'width': self.width,
            'length': self.length,
            'map_info': self.map_info.to_dict() if self.map_info else None,
            'behaviors': self.behaviors,
            'sensor_data': self.sensor_data
        }

    def __repr__(self):
        return f"RoadUserPoint(x={self.x}, y={self.y}, heading={self.heading}, width={self.width}, length={self.length})"


class RoadUserCategory(Enum):
    """
    Enum for road user categories.
    """
    UNKNOWN = -1
    CAR = 0
    TRUCK = 1
    BUS = 2
    PEDESTRIAN = 3
    BICYCLE = 4
    MOTORCYCLE = 5

    def __str__(self):
        return self.name.lower()
