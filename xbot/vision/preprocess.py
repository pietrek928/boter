import numpy as np
import cv2 as cv


# white hsv = [0.0, 0.0, 255.0]
def match_color(im_bgr, col_hsv, score_pow=1.3):
    hsv_image = cv.cvtColor(im_bgr, cv.COLOR_BGR2HSV)
    white_hsv = np.array(col_hsv, dtype=np.float32)

    s_channel = hsv_image[:, :, 1]
    v_channel = hsv_image[:, :, 2]

    # Calculate the squared Euclidean distance in the SV plane
    # The subtraction is broadcast across the entire arrays.
    s_dist_sq = (s_channel - white_hsv[1])**score_pow
    v_dist_sq = (v_channel - white_hsv[2])**score_pow

    # Calculate the Euclidean distance
    distance = np.sqrt(1. / (s_dist_sq + v_dist_sq + 1))

    # 5. Normalize the distance to a 0-255 range and convert to an 8-bit integer
    # The maximum possible distance is sqrt(255^2 + 255^2) which is approx 360.6
    cv.normalize(distance, distance, 0, 255, cv.NORM_MINMAX)
    return distance.astype(np.uint8)