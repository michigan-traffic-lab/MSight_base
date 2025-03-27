import bisect

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
    def __init__(self):
        self.trajectories = []
        self.traj_ids = set()
        self.traj_id_to_traj_map = {}
        self.frames = []
        self.timestamps = []
        self.timestamp_to_frame_map = {}

    @property
    def last_step(self):
        return len(self.frames) - 1
    
    @property
    def last_frame(self):
        return self.frames[-1]

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
            if timestamp is not None:
                self.timestamps.append(timestamp)
                self.timestamp_to_frame_map[timestamp] = frame
        elif step <= self.last_step:
            frame = self.frames[step]
        else:
            raise ValueError(f"Step {step} is not a valid step, valid steps are from 0 to {self.last_step+1}")

        traj.add_object(obj, step, insort=insort)
        frame.add_object(obj)

    def remove_traj(self, traj: Trajectory):
        # print(f"Removing trajectory with id {traj.id}")
        tid = traj.id
        self.trajectories.remove(traj)
        self.traj_ids.remove(tid)
        del self.traj_id_to_traj_map[tid]
        for obj in traj:
            obj.frame.remove_object(obj)
