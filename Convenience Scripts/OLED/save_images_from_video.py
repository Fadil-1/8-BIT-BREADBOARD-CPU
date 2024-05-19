# Code obtained from stack overflow: https://stackoverflow.com/questions/30136257/how-to-get-image-from-video-using-opencv-python

import cv2
import os

def video_to_frames(video, path_output_dir):
    # extract frames from a video and save to directory as 'x.png' where 
    # x is the frame index
    vidcap = cv2.VideoCapture(video)
    count = 0
    while vidcap.isOpened():
        success, image = vidcap.read()
        if success:
            cv2.imwrite(os.path.join(path_output_dir, '%d.png') % count, image)
            count += 1
        else:
            break
    cv2.destroyAllWindows()
    vidcap.release()

video_to_frames(r"/8-bit_cpu_work/EyeMoving.mp4", r"/8-bit_cpu_work/n")