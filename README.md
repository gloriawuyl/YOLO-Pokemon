# YOLO-Pokemon
Using YOLO to detect characters in Pokemon videos.

# Requirements

# How to use the YOLO model with Kalman filtering to detect Pokemon Characters in your video

# Data Pre-processing
Split the Pokemon video to scenes, and extract certain amount of random frames of each scene to consist the training dataset. Annotate the training frames with character labels and bounding boxes.

## Split Pokemon video to scenes
Use PySceneDetect to split the raw video into scenes. The following command will output scene numbers with corresponding frame number and time code in the destination csv file:

```
pyscenedetect -i videopath destination_csv list-scenes
```

## Integrate the raw video into scenes with corresponding frames
In create_segments.py, modify lines 7, 8, 9 to the root directory, video directory, and scene-segmentation directory. Run the code to create a path with every scene a folder consisting of its frames:

```
python create_segments.py
```
## Select the training frames
Randomly select specific amount of frames (by default 2) using select_file_annotation.py. Modify the input path and output path on line 18, 19.
```
python select_file_annotation.py
```

## Annotate characters with bounding boxes
Upload the training frames to SUPERVISELY to implement labeling with bounding boxes.
<img width="936" alt="Screen Shot 2022-06-21 at 9 15 39 PM" src="https://user-images.githubusercontent.com/80933162/174942143-f041bd91-1e3d-4741-b69d-d7eec771fd07.png">

Download the labels with images in YOLO format. The annotations will still be in JSON format, so extract the JSON files using parse_annotation.py. Modify line 54 to the parsed output path and line 55 to the annotation path.
```
python parse_annotation.py
```

# Train Models
Refer to darknet YOLO-4 repository for basic YOLO information.

## Configure the YOLO network

## Write train.txt

## Train YOLO network


# Inference
Inference all the frames using the trained YOLO network. Since the inference results will not appear in perfect YOLO format, we can save the terminal output of inferences and extract the labels to YOLO format.

## Inference all the frames
```
python inference.py
```

## Convert terminal output to YOLO format

# Result Data Filtering
