class RoadUserPoint:
    def __init__(self, x, y, heading=None, width=None, length=None, category=None):
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

    @property
    def traj_id(self):
        if self.traj is None:
            return None
        return self.traj.id

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
    

