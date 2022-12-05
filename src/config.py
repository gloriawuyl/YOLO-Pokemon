# The path to the original video
video_dir = "/Users/gloriawu/Desktop/YOLO-Pokemon/data/S1E1.mp4"

# The path to the scene csv from pyscenedetect
scenes_dir = "/Users/gloriawu/Desktop/YOLO-Pokemon/data/S1E1-Scenes.csv"

# The path to save the frame segmentations
segmentation_dir = "/Users/gloriawu/Desktop/YOLO-Pokemon/video_segmentation/segment/segment"

# The path to save the selected frames for annotation
annotation_frames_dir = "/Users/gloriawu/Desktop/YOLO-Pokemon/annotation_frame"

# The path of YOLO format annotation
ann_dir = ""

# The path for parsed annotation
parsed_ann_dir = ""

# The path for inferenced terminal results
inference_result_dir = ""

# The path for extracted inference label
inference_label_dir = ""

# The path for inferenced images
inference_image_dir = ""

# The path to kalman filtered images
kf_filtered_dir = ""

# The supervisely class map
class_map = {'pokeball': '0', 'Blastoise': '1', 'pikachu': '2', 'Ash': '3', 'Professor': '4', 'Pidgeotto': '5', 'Nidorino': '6', 
                'Gengar': '7', 'Onix': '8', 'Squirtle': '9', 'mom': '10', 'Rattata': '11', 'Charmander': '12', 'Charizard': '13', 
                'Balbasaur': '14', 'Zubat': '15', 'Butterfree': '16', 'Ho-oh': '17', 'Raichu': '18', 'Meowth': '19', 'Marowak': '20'}


