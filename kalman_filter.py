import os
import numpy as np
import cv2
import csv

path = "/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/inference_results"
predictions = os.listdir(path)

def extract_frames(start, end):
    preds = []
    for p in predictions:
        if int(p[11:-4]) <= end and int(p[11:-4]) >= start:
            preds.append(p)
    preds = sorted(preds)
    return preds

def pos_vel_filter(initial_state):
    kf = cv2.KalmanFilter(7, 4)
    kf.statePre = np.zeros((7,1),dtype=np.float32)
    kf.statePre[:4] = initial_state
    # print(kf.statePre)
    kf.transitionMatrix = np.array([[1,0,0,0,1,0,0],[0,1,0,0,0,1,0],[0,0,1,0,0,0,1],[0,0,0,1,0,0,0],  [0,0,0,0,1,0,0],[0,0,0,0,0,1,0],[0,0,0,0,0,0,1]], dtype = np.float32)
    kf.measurementMatrix = np.array([[1,0,0,0,0,0,0],[0,1,0,0,0,0,0],[0,0,1,0,0,0,0],[0,0,0,1,0,0,0]], dtype = np.float32)
    kf.measurementNoiseCov = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]], dtype = np.float32)
    kf.measurementNoiseCov[2:,2:] *= 4. #tune this
    kf.errorCovPre=cv2.setIdentity(kf.errorCovPre, .1)
    kf.errorCovPre[4:,4:] *= 3. #smaller
    # kf.errorCovPre *= 3.
    kf.processNoiseCov = np.array([[1,0,0,0,1,0,0],[0,1,0,0,0,1,0],[0,0,1,0,0,0,1],[0,0,0,1,0,0,0],  [0,0,0,0,1,0,0],[0,0,0,0,0,1,0],[0,0,0,0,0,0,1]], dtype = np.float32)
    kf.processNoiseCov[-1,-1] *= 0.00001
    kf.processNoiseCov[4:,4:] *= 0.00001
    # print(kf.predict())
    return kf

def extract_ms(file):
    classes, labels, confidence = [], [], []
    with open('/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/inference_results/'+ file, 'r') as f:
        lines = f.readlines()
        if lines:
            for line in lines:
                comp = line.split()
                z = []
                classes.append(comp[0])
                z.append(np.float32(comp[1]))
                z.append(np.float32(comp[2]))
                z.append(np.float32(comp[3]))
                z.append(np.float32(comp[4]))
                confidence.append(int(comp[5]))
                z = np.array(z, dtype=np.float32).reshape((4,1))
                labels.append(z)
    return classes, labels, confidence

def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
	return iou

def get_box(prediction):
    center_x = prediction[0]
    center_y = prediction[1]
    width = prediction[2]
    height = prediction[3]
    x1 = center_x - width/2
    x2 = center_x + width/2
    y1 = center_y - height/2
    y2 = center_y + height/2
    return [x1, x2, y1, y2]

def track_scene(start, end):
    preds = extract_frames(start, end)
    tracked_cls = set()
    kfs = {}
    for p in preds:
        bb0 = [] #classes tracked but not detected by YOLO
        bbs = []
        classes, labels, confidences = extract_ms(p)
        for idx, cls in enumerate(classes):
            if cls not in tracked_cls:
                if confidences[idx]>85: ## put it as a parameter
                    kf = pos_vel_filter(labels[idx])
                    kfs[cls] = kf
                    tracked_cls.add(cls)
                    kf.correct(labels[idx])
                    # x = kf.predict()
                    # print(cls, kf.predict())
                    pred = [labels[idx][0][0], labels[idx][1][0], labels[idx][2][0], labels[idx][3][0], cls, confidences[idx]]
                    bb0.append(pred)
            else:
                if(confidences[idx] > 80):
                    kf = kfs[cls]
                    kf.correct(labels[idx])
                    x = kf.predict()
                    pred = [labels[idx][0][0], labels[idx][1][0], labels[idx][2][0], labels[idx][3][0], cls, confidences[idx]]
                    # pred = [x[0][0], x[1][0], x[2][0], x[3][0]]
                    bbs.append(pred)
                else:
                    kf = kfs[cls]
                    x = kf.predict()
                    kalman_box = [x[0][0], x[1][0], x[2][0], x[3][0]]
                    kalman_boxx = get_box(kalman_box)
                    yolo_box = [labels[idx][0][0], labels[idx][1][0], labels[idx][2][0], labels[idx][3][0]]
                    yolo_boxx = get_box(yolo_box)
                    iou = bb_intersection_over_union(kalman_boxx, yolo_boxx)
                    if(iou > 0.6):
                        kf.correct(labels[idx])
                        yolo_box.append(cls)
                        yolo_box.append(confidences[idx])
                        bbs.append(yolo_box)
                    else:
                        # kalman_box.append(cls)
                        # kalman_box.append(-1)
                        # bbs.append(kalman_box)
                        yolo_box.append(cls)
                        yolo_box.append(confidences[idx])
                        bbs.append(yolo_box)
        cl_to_remove = []
        for cl in tracked_cls:
            if cl not in classes:
                kf = kfs[cl]
                x = kf.predict()
                pred = [x[0][0], x[1][0], x[2][0], x[3][0]]
                pred_box = get_box(pred)
                for bb in bb0:
                    if(bb_intersection_over_union(pred_box, get_box(bb[:4]))>0.7):
                        pred = bb[:4]
                        bb0.remove(bb)
                        # print("class ", bb[4], " is removed")
                        cl_to_remove.append(bb[4])
                        break
                pred.append(cl)
                pred.append(-1)
                bbs.append(pred)
            else:
                for pred_bb in bbs:
                    if pred_bb[4] == cl:
                        pred_box = get_box(pred_bb[:4])
                        for bb in bb0:
                            if(bb_intersection_over_union(pred_box, get_box( bb[:4]))>0.8) and (bb[4] != cl):
                                bb0.remove(bb)
                                cl_to_remove.append(bb[4])
                                break
        for c in cl_to_remove:
            tracked_cls.remove(c)
        for bb in bb0:
            bbs.append(bb)
        write_to_csv(bbs,p)
        draw_imgs(bbs,p)
    
def write_to_csv(bboxes, filename):
    if bboxes:
        # print(bboxes)
        name = "frame "+filename[11:-4]
        row = [name, '-1', '-1', '-1','-1', '-1', '-1', '-1', '-1','-1', '-1', '-1', '-1', '-1','-1', '-1', '-1', '-1', '-1','-1', '-1', '-1']
        for bbox in bboxes:
            x_c = bbox[0]
            y_c = bbox[1]
            ww = bbox[2]
            hh = bbox[3]
            cls = bbox[4]
            conf = bbox[5]
            row[int(cls)+1] = '[' + str(x_c) + ',' + str(y_c) + ',' + str(ww) + ',' + str(hh) + ']' + ', ' + str(conf)
        with open('frame_summary.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(row)


def draw_imgs(bboxes, filename):
    if bboxes:
        # print(filename)
        name = filename[5:-3] + 'jpg'
        img = cv2.imread('/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/all_results/'+ name)
        h, w, _ = img.shape
        for bbox in bboxes:
            # print('the bbox is', bbox)
            x_c = bbox[0]
            y_c = bbox[1]
            ww = bbox[2]
            hh = bbox[3]
            x1 = int(x_c * w - (ww/2 * w))
            y1 = int(y_c * h - (hh/2 * h))
            x2 = int(x_c * w + (ww/2 * w))
            y2 = int(y_c * h + (hh/2 * h))
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),3)
        cv2.imwrite('/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/new_result/'+ name,img)

# track_scene(2043,2107)
# track_scene(278, 312)
# track_scene(596, 672)

def filter_all():
    # segment_path = "/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/segment"
    headers = ['Frame', 'pokeball', 'Blastoise', 'pikachu', 'Ash', 'Professor', 'Pidgeotto', 'Nidorino', 'Gengar', 'Onix', 'Squirtle', 'mom', 'Rattata', 'Charmander', 'Charizard', 'Balbasaur', 'Zubat', 'Butterfree', 'Ho-oh', 'Raichu', 'Meowth', 'Marowak']
    with open('frame_summary.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)

    for i in range(1,464):
    # i = 6
        scene_path = "/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/segment/scene_" + str(i)
        imgs = os.listdir(scene_path)
        for img in imgs:
            if not img.startswith('image'):
                imgs.remove(img)
        imgs = sorted(imgs)
        start_idx = int(imgs[0][6:-4])
        end_idx = int(imgs[-1][6:-4])
        # print(start_idx)
        # print(end_idx)
        track_scene(start_idx, end_idx)

if __name__ == '__main__':
    filter_all()

# track_scene(1757,1828)
# track_scene(2043,2107)
# track_scene(278, 312)