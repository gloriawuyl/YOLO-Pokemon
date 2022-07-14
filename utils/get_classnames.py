import os
import json

class_map = {}
imgs = os.listdir('ann')
index = 0

for img in imgs:
    with open('ann/'+img, 'r') as f:
        data = json.load(f)
    for obj in data['objects']:
        if not obj['classTitle'] in class_map:
            class_map[obj['classTitle']] = str(index)
            index += 1

print(class_map)
