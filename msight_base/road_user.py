from enum import IntEnum
from msight_base.map import MapInfo
from msight_base.behavior import BehaviorType


class RoadUserPoint:
    def __init__(self,
                 x=None,
                 y=None,
                 speed=None,
                 acceleration=None,
                 heading=None,
                 width=None,
                 length=None,
                 height=None,
                 poly_box=None,
                 category=None,
                 confidence=None,
                 turning_signal=None,
                 map_info=None,
                 timestamp=None,
                 frame_step=None,
                 traj_id=None,
                 sensor_data={},
                 behaviors=[],
                 conf_int_2sigma=None,
                 conf_int_vel_2sigma=None,
                 heading_confidence=None,
                 yaw_rate=None):
        self._timestamp = timestamp
        self._frame_step = frame_step
        self.x = x
        self.y = y
        self.speed = speed
        self.acceleration = acceleration
        self.heading = heading
        self.width = width
        self.length = length
        self.height = height
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
        self.conf_int_2sigma = conf_int_2sigma
        self.conf_int_vel_2sigma = conf_int_vel_2sigma
        self.heading_confidence = heading_confidence
        self.yaw_rate = yaw_rate

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
            timestamp=object_dict.get('timestamp', None),
            frame_step=object_dict.get('frame_step', None),
            traj_id=object_dict.get('traj_id', None),
            x=object_dict.get('x', None),
            y=object_dict.get('y', None),
            speed=object_dict.get('speed', None),
            acceleration=object_dict.get('acceleration', None),
            heading=object_dict.get('heading', None),
            width=object_dict.get('width', None),
            length=object_dict.get('length', None),
            height=object_dict.get('height', None),
            poly_box=object_dict.get('poly_box', None),
            category=RoadUserCategory(int(object_dict['category'])) if object_dict.get('category') is not None else None,
            confidence=object_dict.get('confidence', None),
            turning_signal=object_dict.get('turning_signal', None),
            map_info=MapInfo.from_dict(object_dict['map_info']) if object_dict.get('map_info') else None,
            sensor_data=object_dict.get('sensor_data', {}),
            behaviors=[BehaviorType[behavior] for behavior in object_dict.get('behaviors', [])],
            conf_int_2sigma=object_dict.get('conf_int_2sigma', None),
            conf_int_vel_2sigma=object_dict.get('conf_int_vel_2sigma', None),
            heading_confidence=object_dict.get('heading_confidence', None),
            yaw_rate=object_dict.get('yaw_rate', None)
        )

    def to_dict(self):
        return {
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
            'height': self.height,
            'category': RoadUserCategory(int(self.category)) if self.category is not None else None,
            'confidence': self.confidence,
            'turning_signal': self.turning_signal,
            'poly_box': self.poly_box,
            'map_info': self.map_info.to_dict() if self.map_info else None,
            'behaviors': [str(behavior) for behavior in self.behaviors],
            'sensor_data': self.sensor_data,
            'conf_int_2sigma': self.conf_int_2sigma,
            'conf_int_vel_2sigma': self.conf_int_vel_2sigma,
            'heading_confidence': self.heading_confidence,
            'yaw_rate': self.yaw_rate,
        }

    def __repr__(self):
        return f"RoadUserPoint(x={self.x}, y={self.y}, heading={self.heading}, width={self.width}, length={self.length}, category={self.category})"


class RoadUserCategory(IntEnum):
    """
    Enum for road user categories.
    """
    UNKNOWN = -1
    SEDAN = 0
    SUV = 1
    TRUCK = 2
    BUS = 3
    PEDESTRIAN = 4
    BICYCLE = 5
    MOTORCYCLE = 6
    TRAILER = 7
    VAN = 8
    PICKUP = 9

    def __str__(self):
        return self.name.lower()
    
    @classmethod
    def from_name(cls, name: str):
        try:
            return cls[name.upper()]
        except KeyError:
            # Fall back to UNKNOWN
            return cls.UNKNOWN
