import numpy as np
import cv2
import json


class VideoWriter(object):

    def __init__(self, name, out_size_w=960, out_size_h=720):

        self.video_writer = cv2.VideoWriter(
            name + '.mp4', cv2.VideoWriter_fourcc(*'MP4V'),
            10.0, (out_size_w, out_size_h))
        self.video_writer_cat = cv2.VideoWriter(
            name + '_cat.mp4', cv2.VideoWriter_fourcc(*'MP4V'),
            10.0, (out_size_h + out_size_w, out_size_h))

        self.out_size_w = out_size_w
        self.out_size_h = out_size_h

    def save_frame(self, vis_det, vis_loc):

        vis_det = cv2.resize(vis_det, (self.out_size_w, self.out_size_h))
        vis_loc = cv2.resize(vis_loc, (self.out_size_h, self.out_size_h))

        self.video_writer.write(vis_det[:, :, ::-1])

        frame_cat = np.concatenate([vis_det, vis_loc], axis=1)
        self.video_writer_cat.write(frame_cat[:, :, ::-1])

        cv2.namedWindow('frame_cat', cv2.WINDOW_NORMAL)
        cv2.imshow('frame_cat', frame_cat[:, :, ::-1])
        cv2.waitKey(1)


############ some helper functions ##############

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def parse_config(path_to_json=r'./config.json'):
    with open(path_to_json) as f:
      data = json.load(f)
    return Struct(**data)



################ BB draw on 2D image... ####################

def draw_bb_on_image(vehicle_list, img):

    for i in range(len(vehicle_list)):
        v = vehicle_list[i]
        x_bottom_c, y_bottom_c = v.pixel_bottom_center.x, v.pixel_bottom_center.y
        diagonal_length = v.diagonal_length_pixel

        # draw box
        pt1 = (int(x_bottom_c - diagonal_length / 2), int(y_bottom_c - diagonal_length / 2))
        pt2 = (int(x_bottom_c + diagonal_length / 2), int(y_bottom_c + diagonal_length / 2))
        cv2.rectangle(img, pt1=pt1, pt2=pt2, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)
        box_tmp = img[pt1[1]:pt2[1], pt1[0]:pt2[0], :]
        img[pt1[1]:pt2[1], pt1[0]:pt2[0], 1:] = (0.75 * box_tmp[:, :, 1:]).astype(np.uint8)

        # draw bottom center
        cv2.circle(img, (x_bottom_c, y_bottom_c), 2, (255, 0, 0), -1)
        # text = 'id=%s' % v.id
        # pt = (x_bottom_c, y_bottom_c - 5)
        # cv2.putText(img, text=text, org=pt, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #             fontScale=0.5, color=(255, 255, 0), thickness=1, lineType=cv2.LINE_AA)

    return img


################ BB (YOLOX) draw on 2D image... ####################
# Instead of draw the square, we directly draw the rect predicted by YOLOX

def draw_bb_on_image_yolox(vehicle_list, img):

    for i in range(len(vehicle_list)):
        v = vehicle_list[i]
        x_bottom_c, y_bottom_c = v.pixel_bottom_center.x, v.pixel_bottom_center.y
        x1, y1, x2, y2 = v.pixel_bbox

        # draw box
        pt1 = (int(x1), int(y1))
        pt2 = (int(x2), int(y2))
        cv2.rectangle(img, pt1=pt1, pt2=pt2, color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)
        box_tmp = img[pt1[1]:pt2[1], pt1[0]:pt2[0], :]
        img[pt1[1]:pt2[1], pt1[0]:pt2[0], 1:] = (0.75 * box_tmp[:, :, 1:]).astype(np.uint8)

        # draw bottom center
        cv2.circle(img, (x_bottom_c, y_bottom_c), 2, (255, 0, 0), -1)
        # text = 'id=%s' % v.id
        # pt = (x_bottom_c, y_bottom_c - 5)
        # cv2.putText(img, text=text, org=pt, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #             fontScale=0.5, color=(255, 255, 0), thickness=1, lineType=cv2.LINE_AA)

    return img

# map center lat/lon
# use the following for Ann Arbor Ellsworth Roundabout
LAT0, LON0 = 42.229392, -83.739012


def coord_normalization(lat, lon, center_lat=LAT0, center_lon=LON0):
    "from lat/lon to local coordinate with unit meter"
    lat_norm = (lat - center_lat) * 111000.
    lon_norm = (lon - center_lon) * 111000. * np.cos(center_lat/180.*np.pi)
    return lat_norm, lon_norm


def coord_unnormalization(lat_norm, lon_norm, center_lat=LAT0, center_lon=LON0):
    "from local coordinate with unit meter to lat/lon"
    lat = lat_norm / 111000. + center_lat
    lon = lon_norm / 111000. / np.cos(center_lat/180.*np.pi) + center_lon
    return lat, lon

