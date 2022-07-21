import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
pparentdir = os.path.dirname(parentdir)
configdir = os.path.join(pparentdir, 'src')
sys.path.insert(0, configdir)
from config import inference_result_dir, inference_label_dir, class_map

def extract_label(input_path, output_path, class_map):
    txt_files = [f for f in os.listdir(input_path) if f.endswith('.txt')]

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
    extract_label(inference_result_dir, inference_label_dir, class_map)
            