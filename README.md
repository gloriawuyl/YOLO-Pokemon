# YOLO-Pokemon
Using YOLO to detect characters in Pokemon videos.

```diff
! Need to write paths to config, and exclude YOLO repository. (action needed)
```

# Requirements

# How to use the YOLO model with Kalman filtering to detect Pokemon Characters in your video

# Data Pre-processing
Split the Pokemon video to scenes, and extract certain amount of random frames of each scene to consist the training dataset. Annotate the training frames with character labels and bounding boxes.

## Input Data Format
The raw data is a video.

## Step 1: Split Pokemon video to scenes
Use PySceneDetect to split the raw video into scenes. The following command will output scene numbers with corresponding frame number and time code in destination_csv in your current datafolder:

```
scenedetect -i videopath detect-content list-scenes
```

## Integrate the raw video into scenes with corresponding frames
In create_segments.py, modify lines 7, 8, 9 to the root directory, video directory, and scene-segmentation directory. Run the code to save the frames within every scene in a subfolder within the scene-segmentation directory:

```
python create_segments.py
```

## Select the training frames
Randomly select specific amount of frames (by default 2) using select_file_annotation.py. Modify the input path and output path on line 18, 19.
```
python select_file_annotation.py
```
Run the above code and the selected frames for annotation will be saved in outfolder specified in the code.

## Annotate characters with bounding boxes
Upload the training frames to SUPERVISELY to implement labeling with bounding boxes.
<img width="936" alt="Screen Shot 2022-06-21 at 9 15 39 PM" src="https://user-images.githubusercontent.com/80933162/174942143-f041bd91-1e3d-4741-b69d-d7eec771fd07.png">

Download the labels with images in YOLO format. The annotations will still be in JSON format, so extract the JSON files using parse_annotation.py. Modify line 54 to the parsed output path and line 55 to the annotation path. The annotation result will be saved in YOLO format to the output path for training preparation.
```
python parse_annotation.py
```

# Train Models
Refer to darknet YOLO-4 repository for basic YOLO information.

## Configure the YOLO network and download the pre-trained weights
Follow the steps in https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects

## Write train.txt
To scalably write the images into train.txt, run the following code with line 11 the input image directory and line 12 the traintxt file path.
```
python write_txt.py
```

## Train YOLO network
Run the command to train the YOLO network:
```
./darknet detector train data/obj.data yolo-obj.cfg yolov4.conv.137
```
The trained weights, including checkpoints and final weights, will be stored in path build\darknet\x64\backup\.

# Inference
Inference all the frames using the trained YOLO network. Since the inference results will not appear in perfect YOLO format, we can save the terminal output of inferences and extract the labels to YOLO format.

## Inference all the frames
Modify line 33-37 with inference image path and yolo configurations, run the code:
```
python inference.py
```

## Convert terminal output to YOLO format
Extract the YOLO format labels from terminal output txt results with the code:
```
python extract_label.py
```
Modify input_path on line 66 to path_to_save_image folder for inferencing.

# Result Data Filtering
Since the YOLO dectection could not be flawless, we could filter some mistakes using Kalman Filter. We could eliminate the identification of a irrelevant class or make up the mistake of failing to identify a continuously appeared class.
```
python opencv_kf.py
```
The code will draw the filtered bounding boxes on the corresponding frame, and write the information of bounding boxes with corresponding character to a csv file.
