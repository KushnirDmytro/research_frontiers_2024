from constants import *
from imagepreprocessor import ImagePreprocessor
from utils import *
import cv2
import matplotlib.pyplot as plt
import json
from numpyarrayencoder import NumpyArrayEncoder
import copy
import time


def estimate_camera_motion():
    image_preprocessor = ImagePreprocessor()
    K = image_preprocessor.intrinsic_camrera_matrix

    features = load_features()
    pre_calc_poses = load_poses()
    
    
    frame_count = 0
    init_point = np.array([0, 0, 0, 1])
    H = np.eye(4)
    t = np.array([0, 0, 0]).reshape(3,1)
    R = np.eye(3)

    camera_pose = np.eye(4)

    ESTIMATION_METHOD = 'INBUILT_POSE_SELF'
    start = time.clock()
    while True:
        frame1 = read_image(INIT_IMAGE + frame_count)
        frame2 = read_image(INIT_IMAGE + frame_count + 1)

        if (frame1 is None) or (frame2 is None) or (cv2.waitKey(1) == 27):
            break
        
        frame_name = str(INIT_IMAGE + frame_count)

        pose = pre_calc_poses.get(frame_name)

        if pose is None:

            features1, features2 = extract_features(frame1, frame2, features, frame_name)

            fundamental_matrix, point_list1, point_list2 = fundmntl_mat_from_8_point_ransac(features1, features2)
            essential_mat = calc_essential_matrix(K, fundamental_matrix)
            
            poses = get_possible_camera_poses(essential_mat)
            pose = get_correct_pose(poses, point_list1, point_list2, non_linear_flag=False)
            new_R = pose[:, :COL4]
            new_t = pose[:, COL4].reshape(3,1)
            
            pre_calc_poses[frame_name] = list(pose)
            

            with open(POSE_FILE, 'w') as pose_file:
                json.dump(pre_calc_poses, pose_file, cls=NumpyArrayEncoder)
        else:
            pose = np.asarray(pose)
            new_R = pose[:, :COL4]
            new_t = pose[:, COL4].reshape(3,1)

        

        new_pose = np.column_stack((new_R, new_t))
        new_pose = np.vstack((new_pose, np.array([0,0,0,1])))

        camera_pose = camera_pose @ new_pose
        x_coord = camera_pose[ROW1, -1]
        z_coord = camera_pose[ROW3, -1]

        print('\n\nframe_count', frame_count, frame_name)
        print('\n\nTime taken: ', (time.clock() - start))

        plt.scatter(x_coord, -z_coord, color='r') 
        plt.pause(0.00001)

        plt.savefig(PLOT_FILE_PATH.format(ESTIMATION_METHOD, frame_name.zfill(ZERO_PAD)), bbox_inches='tight')
        
        frm = cv2.resize(frame1, (0,0), fx=0.5, fy=0.5)
        cv2.imshow('Frame', frm)
        
        frame_count += 1

        #if INIT_IMAGE + frame_count == STOP_IMAGE:
        #    break
    
    cv2.destroyAllWindows()
    plt.show()


if __name__ == "__main__":
    estimate_camera_motion()
    