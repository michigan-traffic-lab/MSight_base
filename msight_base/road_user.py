class RoadUserPoint:
    def __init__(self, x, y, heading=None, width=None, length=None, category=None, confidence=None):
        self.x = x
        self.y = y
        self.heading = heading
        self.width = width
        self.length = length
        self.category = category
        self.traj = None
        self.frame = None
        self.prev = None
        self.next = None
        self.sensor_data = {} # sensor id to sensor data map
        self.confidence = confidence

        ## this is used to store the id when the object's trajectory is not yet created or assigned
        self._traj_id = None

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

    @property
    def timestamp(self):
        if self.frame is None:
            return None
        return self.frame.timestamp

    @staticmethod
    def from_dict(object_dict):
        return RoadUserPoint(
            object_dict['x'],
            object_dict['y'],
            heading=object_dict['heading'],
            width=object_dict['width'],
            length=object_dict['length'],
            id=object_dict['id'],
        )

    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'heading': self.heading,
            'width': self.width,
            'length': self.length,
            'traj_id': self.traj_id,
            'frame_step': self.frame_step,
            'timestamp': self.timestamp,
        }
    
    def __repr__(self):
        return f"RoadUserPoint(x={self.x}, y={self.y}, heading={self.heading}, width={self.width}, length={self.length})"
    

