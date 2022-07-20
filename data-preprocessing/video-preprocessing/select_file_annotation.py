import os, shutil
import numpy as np
import sys
sys.path.insert(0, '/Users/gloriawu/Desktop/YOLO-Pokemon/src')
from config import annotation_dir, segmentation_dir

def random_select(infolder, outfolder, num = 2):
    for subfolder in os.listdir(infolder):
        print(subfolder)
        folder = os.path.join(infolder, subfolder)
        scene_files = os.listdir(folder)
        selected_files = np.random.choice(scene_files, num)
        for s in selected_files:
            source_fn = os.path.join(folder, s)
            out_fn = os.path.join(outfolder, s)
            shutil.copyfile(source_fn, out_fn)
    


if __name__ == '__main__':
    random_select(segmentation_dir, annotation_dir, num = 2)

