import numpy as np
import cv2
import os
import json
import math
from msight_base import TrajectoryManager
from .utils import coord_normalization, coord_unnormalization


def _draw_vehicle_as_point(vis, ptc, color):
    # draw circle boundary
    cv2.circle(vis, tuple(ptc), 10, color, -1)
    # draw center location
    cv2.circle(vis, tuple(ptc), 4, (255, 255, 0), -1)


def _draw_vehicle_as_box(vis, pts, color):
    # fill rectangle
    cv2.fillPoly(vis, [np.array(pts)], color, lineType=cv2.LINE_AA)


def _draw_vehicle_heading_as_arrow(vis, ptc, heading, color):
    # draw heading
    # convert degree to radian
    heading = math.radians(-heading + 90)

    line_length = 50
    pt1 = (int(ptc[0]), int(ptc[1]))
    pt2 = (int(ptc[0] + line_length*np.cos(heading)),
           int(ptc[1] + line_length*np.sin(heading)))
    cv2.arrowedLine(vis, pt1=pt1, pt2=pt2, color=color,
                    thickness=3, line_type=cv2.LINE_AA)


def _draw_predicted_future(vis, pts, color):
    # draw mean trajectory
    for i in range(len(pts)-1):
        pt1 = (int(pts[i][0]), int(pts[i][1]))
        pt2 = (int(pts[i+1][0]), int(pts[i+1][1]))
        cv2.line(vis, pt1=pt1, pt2=pt2, color=color,
                 thickness=1, lineType=cv2.LINE_AA)


def _draw_trust_region(vis, pts, r, color):
    # draw trust regions
    # vis: image
    # pts: points
    # r: radius
    # color: color
    for i in range(len(pts)):
        ptc = (int(pts[i][0]), int(pts[i][1]))
        rx, ry = int(r[i][0]), int(r[i][1])  # trust region
        cv2.ellipse(vis, center=ptc, axes=(rx, ry), angle=0, startAngle=0, endAngle=360,
                    color=color, thickness=1, lineType=cv2.LINE_AA)


def _print_vehicle_info(vis, ptc, v, color):
    # print latitude
    pt = (ptc[0] + 15, ptc[1])
    text = "%.6f" % v.x
    cv2.putText(vis, text=text, org=pt, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5, color=color, thickness=1, lineType=cv2.LINE_AA)
    # print longitude
    pt = (ptc[0] + 15, ptc[1] + 20)
    text = "%.6f" % v.y
    cv2.putText(vis, text=text, org=pt, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5, color=color, thickness=1, lineType=cv2.LINE_AA)
    # print id
    pt = (ptc[0] + 15, ptc[1] + 40)
    text = f"id: {v.traj_id}"

    cv2.putText(vis, text=text, org=pt, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5, color=color, thickness=1, lineType=cv2.LINE_AA)
    # pt = (ptc[0] + 15, ptc[1] + 60)
    # if hasattr(v, 'lane') and v.lane is not None:
    #     text = f"lane: {v.lane}"
    #     cv2.putText(vis, text=text, org=pt, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    #                 fontScale=0.5, color=color, thickness=1, lineType=cv2.LINE_AA)
    # # print category
    # if v.category is not None:
    #     pt = (ptc[0] + 15, ptc[1] + 40)
    #     if label_list is not None:
    #         text = "%s" % label_list.id2label[str(v.category)]
    #     else:
    #         text = "Category: %d" % v.category
    #     cv2.putText(vis, text=text, org=pt, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    #                 fontScale=0.5, color=color, thickness=1, lineType=cv2.LINE_AA)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def parse_config(path_to_json=r'./config.json'):
    with open(path_to_json) as f:
        data = json.load(f)
    return Struct(**data)


class Visualizer:
    """
    Basemap for detection visualization. Show and map detection to base map layer.
    Pixel image: vehicle bounding box, vehicle id
    Map layer: location, heading, rect box, trajectory, predicted future...
    """

    def __init__(self, map_image_path, map_width=1024, map_height=1024, RGB=False):
        self.h, self.w = map_height, map_width

        self.f = parse_config(os.path.splitext(map_image_path)[0] + '.json')
        self.transform_wd2px, self.transform_px2wd = self._create_coord_mapper()

        basemap = cv2.imread(map_image_path, cv2.IMREAD_COLOR)
        if not RGB:
            basemap = cv2.cvtColor(basemap, cv2.COLOR_BGR2RGB)
        self.basemap = cv2.resize(basemap, (map_width, map_height))
        self.basemap = (self.basemap.astype(np.float64) * 0.3).astype(np.uint8)

        np.random.seed(0)
        self.color_table = np.random.randint(80, 255, (10, 3))
        np.random.seed()

        self.traj_manager = TrajectoryManager()
        self.traj_layer = np.zeros([self.h, self.w, 3], dtype=np.uint8)
        self.traj_alpha = np.zeros([self.h, self.w, 3], dtype=np.float32)

        if os.path.exists(r'./vehicle_category.json'):
            self.label_list = parse_config(r'./vehicle_category.json')
        else:
            self.label_list = None

    def _create_coord_mapper(self):

        # wd_tl, wd_tr, wd_bl, wd_br = self.f.tl.copy(), self.f.tr.copy(), self.f.bl.copy(), self.f.br.copy()
        px_tl, px_tr, px_bl, px_br = [0, 0], [
            self.w-1, 0], [0, self.h-1], [self.w-1, self.h-1]

        # normalize to local coordination
        wd_tl = coord_normalization(
            self.f.tl[0], self.f.tl[1], self.f.tl[0], self.f.tl[1])
        wd_tr = coord_normalization(
            self.f.tr[0], self.f.tr[1], self.f.tl[0], self.f.tl[1])
        wd_bl = coord_normalization(
            self.f.bl[0], self.f.bl[1], self.f.tl[0], self.f.tl[1])
        wd_br = coord_normalization(
            self.f.br[0], self.f.br[1], self.f.tl[0], self.f.tl[1])

        wd_points = np.array([wd_tl, wd_tr, wd_bl, wd_br], np.float32)
        px_points = np.array([px_tl, px_tr, px_bl, px_br], np.float32)

        transform_wd2px = cv2.getPerspectiveTransform(
            src=wd_points, dst=px_points)
        transform_px2wd = cv2.getPerspectiveTransform(
            src=px_points, dst=wd_points)

        return transform_wd2px, transform_px2wd

    def _world2pxl(self, pt_world, output_int=True):

        # normalize to local coordination
        pt_world = np.array(pt_world).reshape([-1, 2])
        lat, lon = pt_world[:, 0], pt_world[:, 1]
        lat_norm, lon_norm = coord_normalization(
            lat, lon, self.f.tl[0], self.f.tl[1])
        pt_world = np.array([lat_norm, lon_norm]).T

        pt_world = np.array(pt_world).reshape([-1, 1, 2]).astype(np.float32)
        pt_pixel = cv2.perspectiveTransform(pt_world, self.transform_wd2px)
        pt_pixel = np.squeeze(pt_pixel)

        if output_int:
            pt_pixel = pt_pixel.astype(np.int32)

        return pt_pixel

    def _pxl2world(self, pt_pixel):

        pt_pixel = np.array(pt_pixel).reshape([-1, 1, 2]).astype(np.float32)
        pt_world = cv2.perspectiveTransform(
            pt_pixel, self.transform_px2wd).astype(np.float64)
        pt_world = np.squeeze(pt_world)
        pt_world = pt_world.reshape([-1, 2])

        # unnormalize to world coordination
        lat_norm, lon_norm = pt_world[:, 0], pt_world[:, 1]
        lat, lon = coord_unnormalization(
            lat_norm, lon_norm, self.f.tl[0], self.f.tl[1])
        pt_world = np.array([lat, lon]).T

        return pt_world

    def draw_points(self, frame, show_heading=False):
        # TODO: draw vehicle as box when show_heading is True
        if len(frame) == 0:
            return self.basemap

        vis = np.copy(self.basemap)

        for i in range(0, len(frame)):
            v = frame[i]

            if v.x is None or v.y is None:
                continue

            color = self.color_table[hash(v.traj_id) % 10].tolist()

            ptc = self._world2pxl([v.x, v.y])

            # box unavailiable, draw a circle instead
            _draw_vehicle_as_point(vis, ptc, color)

            # print vehicle info beside box
            _print_vehicle_info(vis, ptc, v, (255, 255, 0),)

        return vis

    def draw_trajectory(self, frame, linewidth=2):

        # update trajectory manager
        for v in frame:
            self.traj_manager.add_object(v, v.traj_id, frame.step, timestamp=frame.timestamp)

        # update alpha (fade out)
        self.traj_alpha *= 0.95

        # draw trajectory
        for v in self.traj_manager.last_frame:
            pt_map = self._world2pxl([v.x, v.y])
            v_ = v.prev
            if v_ is None:
                # print('prev is None')
                continue
            pt_map_prev = self._world2pxl([v_.x, v_.y])

            pt1 = (int(pt_map[0]), int(pt_map[1]))
            pt2 = (int(pt_map_prev[0]), int(pt_map_prev[1]))

            color = self.color_table[hash(v.traj_id) % 10].tolist()

            cv2.line(self.traj_layer, pt1=pt1, pt2=pt2,
                        color=color, thickness=linewidth)
            cv2.line(self.traj_alpha, pt1=pt1, pt2=pt2,
                        color=(0.8, 0.8, 0.8), thickness=linewidth)

        return self.traj_layer, self.traj_alpha

    @staticmethod
    def layer_blending(base_layer, traj_layer, traj_alpha):
        base_layer = base_layer.astype(np.float32)/255.
        traj_layer = traj_layer.astype(np.float32)/255.
        vis = base_layer*(1-traj_alpha) + traj_layer*traj_alpha
        return vis

    def draw_polygon(self, base_layer, polygon, color, thickness=2):
        pts = self._world2pxl(polygon)
        layer = cv2.polylines(
            base_layer, [pts], isClosed=True, color=color, thickness=thickness)
        return layer

    def render(self, frame,  with_traj=True, linewidth=2, show_heading=False):
        base_layer = self.draw_points(
            frame, show_heading=show_heading)
        if with_traj:
            traj_layer, traj_alpha = self.draw_trajectory(
                frame, linewidth)
            map_vis = self.layer_blending(base_layer, traj_layer, traj_alpha)
            map_vis = (map_vis*255.).astype(np.uint8)
        else:
            map_vis = base_layer

        return map_vis
