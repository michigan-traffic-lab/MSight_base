from typing import List
from .utils.cls import get_class_path, import_class_from_path

class DetectedObjectBase:
    def __init__(self):
        pass

    def to_dict(self):
        raise NotImplementedError("Subclasses should implement this!")

class DetectionResultBase:
    def __init__(self, object_list: List[DetectedObjectBase], timestamp: int, sensor_id: str, sensor_type: str, frame_id: str):
        self.object_list = object_list
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.frame_id = frame_id

    def to_dict(self):
        object_data_type = get_class_path(self.object_list[0].__class__) if len(self.object_list) > 0 else None
        return {
            'object_list': [obj.to_dict() for obj in self.object_list],
            'timestamp': self.timestamp,
            'sensor_id': self.sensor_id,
            'sensor_type': self.sensor_type,
            'object_data_type': object_data_type,
            'frame_id': self.frame_id,
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'DetectionResultBase':
        object_data_type = data.get("object_data_type")
        if object_data_type is None:
            raise ValueError(f"Missing 'object_data_type' in data: {data}")

        obj_cls = import_class_from_path(object_data_type)
        object_list = [obj_cls.from_dict(obj_data) for obj_data in data['object_list']]

        return DetectionResultBase(
            object_list=object_list,
            timestamp=data['timestamp'],
            sensor_id=data['sensor_id'],
            sensor_type=data['sensor_type'],
            frame_id=data['frame_id'],
        )
