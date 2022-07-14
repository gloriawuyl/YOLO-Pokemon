import csv
import cv2

def crop_character(character, inputfile, inputpath, outputpath):
    class_map = {'pokeball': '0', 'Blastoise': '1', 'pikachu': '2', 'Ash': '3', 'Professor': '4', 'Pidgeotto': '5', 'Nidorino': '6', 
            'Gengar': '7', 'Onix': '8', 'Squirtle': '9', 'mom': '10', 'Rattata': '11', 'Charmander': '12', 'Charizard': '13', 
            'Balbasaur': '14', 'Zubat': '15', 'Butterfree': '16', 'Ho-oh': '17', 'Raichu': '18', 'Meowth': '19', 'Marowak': '20'}
    with open(inputfile) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in rows:
            count = count + 1
            if count == 1:
                continue
            if row[int(class_map[character])+1] != '-1':
                frame_num = row[0][6:]
                image_file = inputpath + frame_num + '.jpg'
                image = cv2.imread(image_file)
                h, w, _ = image.shape
                labels = row[4].split(',')
                x_c = float(labels[0][1:])
                y_c = float(labels[1])
                ww = float(labels[2])
                hh = float(labels[3][:-1])
                x1 = max(int(x_c * w - (ww/2 * w)),0)
                y1 = max(int(y_c * h - (hh/2 * h)),0)
                x2 = max(int(x_c * w + (ww/2 * w)),0)
                y2 = max(int(y_c * h + (hh/2 * h)),0)
                if x1 > x2 or y1 > y2:
                    cropped_img = image
                    continue
                else:
                    cropped_img = image[y1:y2, x1:x2]
                cv2.imwrite(outputpath + frame_num+'.jpg',cropped_img)


if __name__ == '__main__':
    file = "/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/annotation_frame/frame_summary.csv"
    input_path = "/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/all_images/image_"
    output_path = '/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/ash_crop/'
    crop_character('Ash', file, input_path, output_path)
