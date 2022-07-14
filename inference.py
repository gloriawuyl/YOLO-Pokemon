import os
import subprocess
import time

def inference(image_paths_file, path_to_save_images, obj_dat, yolo_cnf, yolo_wghts):

    im_paths = open(image_paths_file, "r").readlines()

    for im in im_paths:
        result_file = path_to_save_images+str(im)[54:-5]+".txt"
        cmd = "./darknet detector test {} {} {} -dont_show \"{}\" -ext_output > {}".format(obj_dat, yolo_cnf, yolo_wghts, im, result_file)

        # The os.setsid() is passed in the argument preexec_fn so
        # it's run after the fork() and before  exec() to run the shell.

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)

        # it must be adjuste to your inference speed
        # on my rtx2080 takes 6 seconds max
        time.sleep(6)
        # Send the signal to all the process groups
        #os.killpg(os.getpgid(p.pid), signal.SIGTERM)

        image_name = (im.split('/')[-1]).split('.')[0]
        os.rename("predictions.jpg", os.path.join(path_to_save_images, image_name+'.jpg'))
        # print("img was saved")

    # for im in im_paths:
    #     result_file = "/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/annotation_frame/results/"+str(im)[27:-5]+".txt"
    #     print(result_file)

if __name__ == '__main__':
    image_paths_file = '/mnt/SSD5/gloria/YOLO/darknet/build/darknet/x64/data/test.txt'
    path_to_save_images = '/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/all_results/'
    obj_dat = "/mnt/SSD5/gloria/YOLO/darknet/build/darknet/x64/data/obj.data"
    yolo_cnf = "/mnt/SSD5/gloria/YOLO/darknet/cfg/yolo-obj.cfg"
    yolo_wghts = "/mnt/SSD5/gloria/YOLO/darknet/backup/yolo-obj_20000.weights"
    inference()