import os

# path = '/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/all_results'
# path1 = '/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/annotation_frame/img'
# # txt_files = os.listdir(path)
# txt_files = [f for f in os.listdir(path) if f.endswith('.txt')]
# print(len(txt_files))
# txt_files = ['/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/results/image_1341.txt', '/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/results/image_10691.txt']

def extract_label(input_path, output_path, class_map):
    # path = '/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/all_results'
    # path1 = '/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/annotation_frame/img'
# txt_files = os.listdir(path)
    txt_files = [f for f in os.listdir(input_path) if f.endswith('.txt')]

    # class_map = {'pokeball': '0', 'Blastoise': '1', 'pikachu': '2', 'Ash': '3', 'Professor': '4', 'Pidgeotto': '5', 'Nidorino': '6', 
    #             'Gengar': '7', 'Onix': '8', 'Squirtle': '9', 'mom': '10', 'Rattata': '11', 'Charmander': '12', 'Charizard': '13', 
    #             'Balbasaur': '14', 'Zubat': '15', 'Butterfree': '16', 'Ho-oh': '17', 'Raichu': '18', 'Meowth': '19', 'Marowak': '20'}

    for file in txt_files:
        lines = []
        class_label = []
        confidences = []
        center_x = []
        center_y = []
        width = []
        height = []
        with open(input_path+'/'+file, 'r') as f:
            line_count = 0
            for line in f:
                line_count += 1
                if(line_count >= 13):
                    components = line.split()
                    class_label.append(components[0][0:-1])
                    confidences.append(components[1][0:-1])
                    x1 = float(components[3])
                    y1 = float(components[5])
                    w = float(components[7])
                    h = float(components[9][0:-1])
                    center_x.append((x1 + w/2)/1920)
                    center_y.append((y1 + h/2)/1080)
                    width.append(w/1920)
                    height.append(h/1080)
        for i in range(len(class_label)):
            l = ""
            l += class_map[class_label[i]]
            l += " "
            l += str(center_x[i])
            l += " "
            l += str(center_y[i])
            l += " "
            l += str(width[i])
            l += " "
            l += str(height[i])
            l += " "
            l += str(confidences[i])
            lines.append(l)

        final_filename = output_path+'/pred_'+file
        with open(final_filename, 'w') as f:
            for line in lines:
                f.write(line)
                f.write('\n')

if __name__ == '__main__':
    input_path = '/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/all_results'
    output_path = '/mnt/SSD5/gloria/YOLO/darknet/data/Pokemon/reference_results'
    class_map = {'pokeball': '0', 'Blastoise': '1', 'pikachu': '2', 'Ash': '3', 'Professor': '4', 'Pidgeotto': '5', 'Nidorino': '6', 
                'Gengar': '7', 'Onix': '8', 'Squirtle': '9', 'mom': '10', 'Rattata': '11', 'Charmander': '12', 'Charizard': '13', 
                'Balbasaur': '14', 'Zubat': '15', 'Butterfree': '16', 'Ho-oh': '17', 'Raichu': '18', 'Meowth': '19', 'Marowak': '20'}
    extract_label(input_path, output_path, class_map)
            