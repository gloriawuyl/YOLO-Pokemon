# YOLO-Pokemon
Using YOLO to detect characters in Pokemon videos.

# Requirements

# How to use the YOLO model with Kalman filtering to detect Pokemon Characters in your video

# Data Pre-processing
Split the Pokemon video to scenes, and extract certain amount of random frames of each scene to consist the training dataset. Annotate the training frames with character labels and bounding boxes.

## Input Data Format
The raw data is a video.

## Specify Configurations
Fill the paths with your own directory paths in config.py:

**video_dir** = path of original video \
**scenes_dir** = path of scene split csv \
**segmentation_dir** = segmented frames directory \
**annotation_frames_dir** = path of selected frames per scene \
**ann_dir** = path of annotated results on the selected frames \
**parsed_ann_dir** = path of parsed annotation (after running parse_annotation.py) \
**inference_result_dir** = path of saved terminal and image results for inferencing all the frames (after running inference.py) \
**inference_label_dir** = path of cleaned YOLO format results of inference (after running extract_label.py) \
**kf_filtered_dir** = path of images containing results filtered by kalman filter \
**class_map** = the dictionary mapping the character name to index 

## Step 1: Split Pokemon video to scenes
Use PySceneDetect to split the raw video into scenes. The following command will output scene numbers with corresponding frame number and time code in video-Scenes.csv in your current datafolder:

```
scenedetect -i videopath detect-content list-scenes
```
Remember to store the path of the csv as scenes_dir in config.

## Integrate the raw video into scenes with corresponding frames
Run the code to save the frames within every scene in a subfolder within the scene-segmentation directory:

```
python data-preprocessing/video-preprocessing/create_segments.py
```

## Select the training frames
Randomly select specific amount of frames (by default 2) using select_file_annotation.py. 
```
python data-preprocessing/video-preprocessing/select_file_annotation.py
```
Run the above code and the selected frames for annotation will be saved in outfolder specified in the code. Be sure to create the annotation folder in advance.

## Annotate characters with bounding boxes
Upload the training frames to SUPERVISELY to implement labeling with bounding boxes.
<img width="936" alt="Screen Shot 2022-06-21 at 9 15 39 PM" src="https://user-images.githubusercontent.com/80933162/174942143-f041bd91-1e3d-4741-b69d-d7eec771fd07.png">

Download the labels with images in YOLO format. The annotations will still be in JSON format, so extract the JSON files using parse_annotation.py. The annotation result will be saved in YOLO format to the output path for training preparation.
```
python data-preprocessing/parse_annotation.py
```

# Train Models
Refer to darknet YOLO-4 repository for basic YOLO information.

## Configure the YOLO network and download the pre-trained weights
Follow the steps in https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects

## Write train.txt
To scalably write the images into train.txt, run the following code with line 11 the input image directory and line 12 the traintxt file path.
```
python utils/write_txt.py
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
Run the code:
```
python inference.py
```
Change image_paths_file to the path to your configured test.txt for YOLO; path_to_save_images to the path of your desired destination to save the inferenced image and terminal output; obj_dat, yolo_cnf, yolo_wghts to your data, config, and model weights path.

## Convert terminal output to YOLO format
Extract the YOLO format labels from terminal output txt from the inference results with the code:
```
python utils/extract_label.py
```

# Result Data Filtering
Since the YOLO dectection could not be flawless, we could filter some mistakes using Kalman Filter. We could eliminate the identification of a irrelevant class or make up the mistake of failing to identify a continuously appeared class.
```
python kalman_filter.py
```
The code will draw the filtered bounding boxes on the corresponding frame, and write the information of bounding boxes with corresponding character to a csv file.

# Other aiding tools
We could also visualize our character detection results by cropping out certain character/class predicted.
```
python utils/crop_character.py
```
