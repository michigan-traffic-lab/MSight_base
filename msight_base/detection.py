from typing import List, Optional
from .utils.cls import get_class_path, import_class_from_path

class DetectedObjectBase:
    def __init__(self):
        pass

    def to_dict(self):
        raise NotImplementedError("Subclasses should implement this!")

class DetectionResultBase:
    def __init__(self, object_list: List[DetectedObjectBase], timestamp: int, sensor_type: Optional[str] = None):
        self.object_list = object_list
        self.timestamp = timestamp
        self.sensor_type = sensor_type

    def to_dict(self):
        object_data_type = get_class_path(self.object_list[0].__class__) if len(self.object_list) > 0 else get_class_path(DetectedObjectBase)
        return {
            'object_list': [obj.to_dict() for obj in self.object_list],
            'timestamp': self.timestamp,
            'sensor_type': self.sensor_type,
            'object_data_type': object_data_type,
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'DetectionResultBase':
        object_data_type = data.get("object_data_type")
        if object_data_type is None:
            raise ValueError(f"Missing 'object_data_type' in data: {data}")

        obj_cls = import_class_from_path(object_data_type)
        if data['object_list'] is not None and len(data['object_list']) > 0:
            object_list = [obj_cls.from_dict(obj_data) for obj_data in data['object_list']]
        else:
            object_list = []

        return DetectionResultBase(
            object_list=object_list,
            timestamp=data['timestamp'],
            sensor_type=data['sensor_type'],
        )
