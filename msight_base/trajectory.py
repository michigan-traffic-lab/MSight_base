import bisect
from .road_user import RoadUserPoint
from typing import List

class Container:
    def __init__(self, id=None, objects = None):
        self.id = id
        if objects is None:
            objects = []
        self.objects = objects

    def __len__(self):
        return len(self.objects)

    def __iter__(self):
        return iter(self.objects)
    
    def __getitem__(self, item):
        return self.objects[item]


class Trajectory(Container):
    def __init__(self, id=None):
        self.steps = []
        self.step_to_object_map = {}
        super().__init__(id=id, objects=[])

    def add_object(self, obj, step, insort=False):
        if insort:
            index = bisect.bisect_left(self.steps, step)
            if index < len(self.steps) and self.steps[index] == step:
                raise ValueError(f"Step {step} already exists")
            self.steps.insert(index, step)
            self.objects.insert(index, obj)
            self.step_to_object_map[step] = obj
            if index > 0:
                self.objects[index - 1].next = obj
                obj.prev = self.objects[index - 1]
            if index < len(self.objects) - 1:
                obj.next = self.objects[index + 1]
                self.objects[index + 1].prev = obj
        else:
            if len(self.steps) > 0 and step < self.steps[-1]:
                raise ValueError(f"Step {step} is less than the last step {self.steps[-1]}, if you want to insert in between use insort=True")
            self.objects.append(obj)
            self.step_to_object_map[step] = obj
            self.steps.append(step)
            if len(self.objects) > 1:
                self.objects[-2].next = obj
                obj.prev = self.objects[-2]
        obj.traj = self

    def get_object_at_step(self, step):
        return self.step_to_object_map.get(step, None)
    
    def remove_object(self, step):
        if step not in self.steps:
            raise ValueError(f"Step {step} does not exist in the trajectory")
        obj = self.get_object_at_step(step)
        self.objects.remove(obj)
        self.steps.remove(step)
        del self.step_to_object_map[step]
        obj.traj = None
        next_obj = obj.next
        prev_obj = obj.prev
        if next_obj is not None:
            next_obj.prev = prev_obj
        if prev_obj is not None:
            prev_obj.next = next_obj


class Frame(Container):
    def __init__(self, step, timestamp=None):
        self.step = step
        self.timestamp = timestamp
        self.traj_ids = set()
        self.traj_id_to_obj_map = {}
        super().__init__(None, objects=[])

    def add_object(self, obj):
        if obj.traj_id in self.traj_ids:
            raise ValueError(f"Object with id {obj.traj_id} already exists in the frame")
        self.objects.append(obj)
        self.traj_id_to_obj_map[obj.traj_id] = obj
        self.traj_ids.add(obj.traj_id)
        obj.frame = self

    def remove_object(self, obj):
        if obj.traj_id not in self.traj_ids:
            raise ValueError(f"Object with id {obj.traj_id} does not exist in the frame")
        self.objects.remove(obj)
        del self.traj_id_to_obj_map[obj.traj_id]
        self.traj_ids.remove(obj.traj_id)
        obj.frame = None


class TrajectoryManager:
    def __init__(self, max_frames=None):
        self.trajectories = []
        self.traj_ids = set()
        self.traj_id_to_traj_map = {}
        self.frames = []
        self.steps = []
        self.timestamps = []
        self.step_to_frame_map = {}
        self.timestamp_to_frame_map = {}
        self.max_frames = max_frames

    @property
    def last_step(self):
        return self.steps[-1] if len(self.steps)>0 else -1
    
    @property
    def earliest_step(self):
        return self.steps[0] if len(self.steps)>0 else -1

    @property
    def last_frame(self):
        return self.frames[-1]
    
    def delete_earliest_frame(self):
        if not self.frames:
            raise ValueError("No frames to delete")
        step = self.frames[0].step
        for obj in self.frames[0].objects:
            # print(obj.traj, obj.traj_id)
            if obj.traj is not None:
                obj.traj.remove_object(step)
        if self.frames[0].timestamp is not None:
            del self.timestamp_to_frame_map[self.frames[0].timestamp]
            self.timestamps.remove(self.frames[0].timestamp)
        del self.step_to_frame_map[step]
        self.steps.remove(step)

        for traj in self.trajectories:
            if len(traj.objects) == 0:
                self.remove_traj(traj)
        self.frames.pop(0)

    def add_object(self, obj, traj_id, step, timestamp=None, insort=False):
        if traj_id not in self.traj_ids:
            traj = Trajectory(traj_id)
            self.trajectories.append(traj)
            self.traj_ids.add(traj_id)
            self.traj_id_to_traj_map[traj_id] = traj
        else:
            traj = self.traj_id_to_traj_map[traj_id]

        if step == self.last_step + 1:
            frame = Frame(step, timestamp)
            self.frames.append(frame)
            self.steps.append(step)
            self.step_to_frame_map[step] = frame
            if timestamp is not None:
                self.timestamps.append(timestamp)
                self.timestamp_to_frame_map[timestamp] = frame
            
        elif step <= self.last_step and step >= self.earliest_step:
            frame = self.step_to_frame_map[step]
        else:
            raise ValueError(f"Step {step} is not a valid step, valid steps are from 0 to {self.last_step+1}")

        traj.add_object(obj, step, insort=insort)
        frame.add_object(obj)
        while self.max_frames is not None and len(self.frames) > self.max_frames:
            # print(len(self.frames), self.max_frames)
            self.delete_earliest_frame()

    def add_list_as_new_frame(self, object_list: List[RoadUserPoint], timestamp=None):
        # use this method to push a list of objects as the last frame, this is very useful when you have a list of objects that are already tracked with id assigned
        step = self.last_step + 1
        for obj in object_list:
            if obj.traj_id is None:
                raise ValueError("Object must have a traj_id to be added to a trajectory manager")
            self.add_object(obj, obj.traj_id, step, timestamp=obj.timestamp)


    def remove_traj(self, traj: Trajectory):
        # print(f"Removing trajectory with id {traj.id}")
        tid = traj.id
        self.trajectories.remove(traj)
        self.traj_ids.remove(tid)
        del self.traj_id_to_traj_map[tid]
        for obj in traj:
            obj.frame.remove_object(obj)
