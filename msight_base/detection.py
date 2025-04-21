from typing import List

class DetectedObjectBase:
    def __init__(self):
        pass

    def to_dict(self):
        raise NotImplementedError("Subclasses should implement this!")

class DetectionResultBase:
    def __init__(self, object_list: List[DetectedObjectBase], timestamp: int, sensor_id: str, sensor_type: str):
        self.object_list = object_list
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type

    def to_dict(self):
        return {
            'object_list': [obj.to_dict() for obj in self.object_list],
            'timestamp': self.timestamp,
            'sensor_id': self.sensor_id,
            'sensor_type': self.sensor_type
        }
