from pathlib import Path
from msight_base.utils.data import read_msight_json_data
from msight_base.visualizer import Visualizer
import cv2

data_path = Path("./example_data/traj_geddes_huron")

tm = read_msight_json_data(data_path)
visualizer = Visualizer("./basemap_configs/huron_geddes.jpg")

for frame in tm.frames:
    # print(f"Frame {frame.step} at {frame.timestamp}")
    vis_img = visualizer.render(frame, with_traj=True)
    cv2.imshow("Frame", vis_img)
    cv2.waitKey(100)
cv2.destroyAllWindows()