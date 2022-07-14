import json
import os

def parse_annotation(annpath, outpath):
    class_map = {'pokeball': '0', 'Blastoise': '1', 'pikachu': '2', 'Ash': '3', 'Professor': '4', 'Pidgeotto': '5', 'Nidorino': '6', 
                'Gengar': '7', 'Onix': '8', 'Squirtle': '9', 'mom': '10', 'Rattata': '11', 'Charmander': '12', 'Charizard': '13', 
                'Balbasaur': '14', 'Zubat': '15', 'Butterfree': '16', 'Ho-oh': '17', 'Raichu': '18', 'Meowth': '19', 'Marowak': '20'}

    imgs = os.listdir(annpath)

    for img in imgs:
        with open('ann/'+img, 'r') as f:
            data = json.load(f)

        class_label = []
        center_x = []
        center_y = []
        width = []
        height = []

        for obj in data['objects']:
            class_label.append(obj['classTitle'])
            x1 = obj['points']['exterior'][0][0]
            x2 = obj['points']['exterior'][1][0]
            y1 = obj['points']['exterior'][0][1]
            y2 = obj['points']['exterior'][1][1]
            center_x.append((x1+x2)/2/1920)
            center_y.append((y1+y2)/2/1080)
            width.append((x2-x1)/1920)
            height.append((y2-y1)/1080)

        lines = []
        for i in range(len(class_label)):
            line = ""
            line += class_map[class_label[i]]
            line += " "
            line += str(center_x[i])
            line += " "
            line += str(center_y[i])
            line += " "
            line += str(width[i])
            line += " "
            line += str(height[i])
            lines.append(line)

        filename = outpath+img[0:-9]

        with open(filename+'.txt', 'w') as f:
            for line in lines:
                f.write(line)
                f.write('\n')

if __name__ == '__main__':
    output_path = '/mnt/SSD5/gloria/YOLO/darknet/build/darknet/x64/data/obj/'
    annotation_path = 'ann'
    parse_annotation(annotation_path, output_path)