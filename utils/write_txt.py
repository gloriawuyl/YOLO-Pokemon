import os
import json

def write_txt(img_dir):
    img_names = os.listdir(img_dir, dest_dir)
    with open(dest_dir, 'w') as f:
        for img_name in img_names:
            f.write(img_dir+'/'+img_name+'\n')

if __name__ == '__main__':
    img_dir = '/Users/gloriawu/Desktop/YOLO-Pokemon/darknet/data/Pokemon/all_images'
    dest_dir = '/Users/gloriawu/Desktop/YOLO-Pokemon/darknet/build/darknet/x64/data/test.txt'
    write_txt()