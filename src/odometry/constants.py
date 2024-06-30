N_POINT = 8
RANSAC_THRESH = 1 #0.06 #0.001
MODEL_DIR = '../data/Oxford_dataset/model/'
DATA_DIR = '../data/Oxford_dataset/stereo/centre/'
PROCESSED_DATA_DIR = '../data/processed_data/frames/'
FEATURE_FILE = '../data/processed_data/feature/features.json'
FEATURE_FILES_DIR = '../data/processed_data/feature/'
PLOT_FILE_PATH = '../data/processed_data/plots/{}/{}.png'
POSE_FILE = 'poses.json'
ZERO_PAD = 7
INIT_IMAGE = 20
STOP_IMAGE = 200# 300

CROP_MIN = 150 # 150

X, Y, Z = 0, 1, 2
ROW1, ROW2, ROW3, ROw4 = 0, 1, 2, 3
COL1, COL2, COL3, COL4 = 0, 1, 2, 3
LAST_COL = -1