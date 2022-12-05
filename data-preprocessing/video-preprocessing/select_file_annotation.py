import os, shutil
import numpy as np
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
pparentdir = os.path.dirname(parentdir)
configdir = os.path.join(pparentdir, 'src')
sys.path.insert(0, configdir)
from config import annotation_frames_dir, segmentation_dir

def random_select(infolder, outfolder, num = 2):
    print(infolder)
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
    random_select(segmentation_dir, annotation_frames_dir, num = 2)

