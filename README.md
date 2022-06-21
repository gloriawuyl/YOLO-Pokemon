# YOLO-Pokemon
Using YOLO to detect characters in Pokemon videos.

# Requirements

# How to use the YOLO model with Kalman filtering to detect Pokemon Characters in your video

# Data Pre-processing
Split the Pokemon video to scenes, and extract the first and last two frames of each scene to consist the training dataset. Annotate the training frames with character labels and bounding boxes.

## Split Pokemon video to scenes
Use PySceneDetect to split frames to scenes.

## Convert the raw videos to frames corresponding to each scene
In create_segments.py, modify the video path and the csv file path.

## Annotate characters with bounding boxes
Upload the training frames to Supervisely.

# Train Models

# Inference Results

# Result Data Filtering
