from pathlib import Path
from msight_base import TrajectoryManager, RoadObject
import json
from datetime import datetime


def get_timestamp_from_filename(file_name: str) -> datetime:
    # file name is like "2023-09-05 10-00-00-039784.json"
    stem = file_name.split(".")[0]
    return datetime.strptime(stem, "%Y-%m-%d %H-%M-%S-%f")


def read_msight_json_data(file_path: Path) -> TrajectoryManager:
    tm = TrajectoryManager()
    step = 0
    for frame_file in file_path.iterdir():
        if frame_file.suffix != ".json":
            continue
        timestamp = get_timestamp_from_filename(frame_file.stem)
        with open(frame_file, "r") as f:
            frame_data = json.load(f)
            for obj_data in frame_data['fusion']:
                obj = RoadObject(
                    obj_data['lat'],
                    obj_data['lon'],
                    heading=obj_data['heading'],
                    width=obj_data['width'],
                    length=obj_data['length'],
                )
                tm.add_object(obj, obj_data['id'], step, timestamp=timestamp)
        step += 1
    return tm
