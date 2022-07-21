import os
import cv2
import pandas as pd
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
pparentdir = os.path.dirname(parentdir)
configdir = os.path.join(pparentdir, 'src')
sys.path.insert(0, configdir)
from config import video_dir, scenes_dir, segmentation_dir

from tqdm import tqdm


def init_video_writer(destination, index):
    destination_dir = os.path.join(destination, "segment", f"scene_{index}.avi")
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    out = cv2.VideoWriter(destination_dir, fourcc, FPS, SHAPE)

    return out

def main():
    VIDEO_DIR = video_dir
    os.makedirs(segmentation_dir, exist_ok=True)
    FPS = 23
    SHAPE = (480, 640)
    csv_file = pd.read_csv(scenes_dir, skiprows=1)

    video = cv2.VideoCapture(video_dir)

    max_scene = csv_file["Scene Number"].max()
    last_frame = csv_file.iloc[max_scene - 1]["Start Frame"] + csv_file.iloc[max_scene - 1]["Length (frames)"]
    index = 1

    # Init video writer
    # out = init_video_writer(VIDEO_SEGMENTATION_DIR, index)

    for current_frame in tqdm(range(last_frame)):
        if index < len(csv_file) and current_frame == csv_file.iloc[index]["Start Frame"]:
            # out.release()
            index += 1
            # out = init_video_writer(VIDEO_SEGMENTATION_DIR, index)

        ret, frame = video.read()
        #frame = cv2.resize(frame, SHAPE)

        destination_dir = os.path.join(segmentation_dir, "segment", f"scene_{index}")
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir, exist_ok=True)

        cv2.imwrite(os.path.join(destination_dir, f"image_{current_frame}.jpg"), frame)
        # out.write(frame)

    # out.release()

if __name__ == '__main__':
    main()