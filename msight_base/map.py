from enum import Enum
from typing import List
from commonroad.scenario.lanelet import LaneletType, LaneletNetwork
import matplotlib.pyplot as plt


class LaneShape(Enum):
    """
    Enum for different types of lane shape.
    """
    STRAIGHT = 'straight'
    LEFT_TURN = 'left-turn'
    RIGHT_TURN = 'right-turn'
    U_TURN = 'u-turn'


class LaneSide(Enum):
    """
    Enum for different types of lane side.
    """
    LEFT = 1
    RIGHT = -1
    ONLANE = 0
    UNKNOWN = 'unknown'


class MapInfo:
    def __init__(self, lane_id, lane_point_idx, dis_to_lane_center, side: LaneSide, related_lane_id, related_route, nearest_next_lane_point_idx=None):
        self.lane_id = lane_id
        self.lane_point_idx = lane_point_idx
        self.dis_to_lane_center = dis_to_lane_center
        self.side = side
        self.related_lane_id = related_lane_id
        self.related_route = related_route
        self.nearest_next_lane_point_idx = nearest_next_lane_point_idx

    def __repr__(self):
        return f"MapInfo(lane_id={self.lane_id}, lane_point_idx={self.lane_point_idx})"
    
    def to_dict(self):
        return {
            'lane_id': self.lane_id,
            'lane_point_idx': self.lane_point_idx,
            'dis_to_lane_center': self.dis_to_lane_center,
            'side': self.side.value,
            'related_lane_id': self.related_lane_id,
            'related_route': self.related_route,
            'nearest_next_lane_point_idx': self.nearest_next_lane_point_idx
        }


class MapObject:
    def __init__(self, commonroadObj: LaneletNetwork, center_point, map_lanes, lane_heading, lane_shape: List[LaneShape], lane_seg_length, background_img, corner_coords):
        self.center_point = center_point
        self._map_lanes = map_lanes
        self._lane_heading = lane_heading
        self._lane_shape = lane_shape
        self._lane_seg_length = lane_seg_length
        self.background_img = background_img
        self.corner_coords = corner_coords

        if isinstance(commonroadObj, LaneletNetwork):
            self.map_polylines_ids = [lanelet.lanelet_id for lanelet in commonroadObj.lanelets]
            self._suc_edges = [lanelet.successor for lanelet in commonroadObj.lanelets]
            self._pre_edges = [lanelet.predecessor for lanelet in commonroadObj.lanelets]
            self._left_edges = [lanelet.adj_left for lanelet in commonroadObj.lanelets]
            self._left_edge_directions = [lanelet.adj_left_same_direction for lanelet in commonroadObj.lanelets]
            self._right_edges = [lanelet.adj_right for lanelet in commonroadObj.lanelets]
            self._right_edge_directions = [lanelet.adj_right_same_direction for lanelet in commonroadObj.lanelets]
            self.intersection_lane_id_list = [lanelet.lanelet_id for lanelet in commonroadObj.lanelets if LaneletType.INTERSECTION in lanelet.lanelet_type]
            self.straight_lane_id_list = [lanelet.lanelet_id for lanelet in commonroadObj.lanelets if LaneletType.INTERSECTION not in lanelet.lanelet_type]
        else:
            self.map_polylines_ids = []
            self._suc_edges = []
            self._pre_edges = []
            self._left_edges = []
            self._left_edge_directions = []
            self._right_edges = []
            self._right_edge_directions = []
            self.intersection_lane_id_list = []
            self.straight_lane_id_list = []

    def suc_edges(self, id=-1):
        if id == -1:
            return self._suc_edges
        else:
            if id not in self.map_polylines_ids:
                raise ValueError(f"Lanelet id {id} not found in map_polylines_ids")
            return self._suc_edges[self.map_polylines_ids.index(id)]

    def pre_edges(self, id=-1):
        if id == -1:
            return self._pre_edges
        else:
            if id not in self.map_polylines_ids:
                raise ValueError(f"Lanelet id {id} not found in map_polylines_ids")
            return self._pre_edges[self.map_polylines_ids.index(id)]

    def left_edges(self, id=-1):
        if id == -1:
            return self._left_edges
        else:
            if id not in self.map_polylines_ids:
                raise ValueError(f"Lanelet id {id} not found in map_polylines_ids")
            return self._left_edges[self.map_polylines_ids.index(id)]

    def right_edges(self, id=-1):
        if id == -1:
            return self._right_edges
        else:
            if id not in self.map_polylines_ids:
                raise ValueError(f"Lanelet id {id} not found in map_polylines_ids")
            return self._right_edges[self.map_polylines_ids.index(id)]

    def left_edge_directions(self, id=-1):
        if id == -1:
            return self._left_edge_directions
        else:
            if id not in self.map_polylines_ids:
                raise ValueError(f"Lanelet id {id} not found in map_polylines_ids")
            return self._left_edge_directions[self.map_polylines_ids.index(id)]

    def right_edge_directions(self, id=-1):
        if id == -1:
            return self._right_edge_directions
        else:
            if id not in self.map_polylines_ids:
                raise ValueError(f"Lanelet id {id} not found in map_polylines_ids")
            return self._right_edge_directions[self.map_polylines_ids.index(id)]

    def lane_shape(self, id=-1):
        if id == -1:
            return self._lane_shape
        else:
            if id not in self.map_polylines_ids:
                raise ValueError(f"Lanelet id {id} not found in map_polylines_ids")
            return self._lane_shape[self.map_polylines_ids.index(id)]

    def map_lanes(self, id=-1, idx=-1):
        if id == -1:
            return self._map_lanes
        else:
            if id not in self.map_polylines_ids:
                raise ValueError(f"Lanelet id {id} not found in map_polylines_ids")
            if idx == -1:
                return self._map_lanes[self.map_polylines_ids.index(id)]
            else:
                if idx >= len(self._map_lanes[self.map_polylines_ids.index(id)]):
                    raise ValueError(f"Index {idx} out of range for lane with id {id}")
                return self._map_lanes[self.map_polylines_ids.index(id)][idx]

    def lane_heading(self, id=-1, idx=-1):
        if id == -1:
            return self._lane_heading
        else:
            if id not in self.map_polylines_ids:
                raise ValueError(f"Lanelet id {id} not found in map_polylines_ids")
            if idx == -1:
                return self._lane_heading[self.map_polylines_ids.index(id)]
            else:
                if idx >= len(self._lane_heading[self.map_polylines_ids.index(id)]):
                    raise ValueError(f"Index {idx} out of range for lane with id {id}")
                return self._lane_heading[self.map_polylines_ids.index(id)][idx]
    
    def lane_seg_length(self, id=-1, idx=-1):
        if id == -1:
            return self._lane_seg_length
        else:
            if id not in self.map_polylines_ids:
                raise ValueError(f"Lanelet id {id} not found in map_polylines_ids")
            if idx == -1:
                return self._lane_seg_length[self.map_polylines_ids.index(id)]
            else:
                if idx >= len(self._lane_seg_length[self.map_polylines_ids.index(id)]):
                    raise ValueError(f"Index {idx} out of range for lane with id {id}")
                return self._lane_seg_length[self.map_polylines_ids.index(id)][idx]

    def to_dict(self):
        return {
            'center_point': self.center_point,
            'map_lanes': self._map_lanes,
            'lane_heading': self._lane_heading,
            'map_polylines_ids': self.map_polylines_ids,
            'suc_edges': self._suc_edges,
            'pre_edges': self._pre_edges,
            'left_edges': self._left_edges,
            'left_edge_directions': self._left_edge_directions,
            'right_edges': self._right_edges,
            'right_edge_directions': self._right_edge_directions,
            'lane_shape': self._lane_shape,
            'intersection_lane_id_list': self.intersection_lane_id_list,
            'straight_lane_id_list': self.straight_lane_id_list,
            'corner_coords': self.corner_coords,
        }
