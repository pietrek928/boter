import numpy as np
import cv2 as cv


def match_color(im_rgb, col_rgb, score_pow=1.3):
    hsv_image = cv.cvtColor(im_rgb, cv.COLOR_RGB2HSV)
    col_hsv = cv.cvtColor(np.array([[col_rgb]], dtype=np.uint8), cv.COLOR_RGB2HSV)[0, 0].astype(np.float32)

    s_channel = hsv_image[:, :, 1]
    v_channel = hsv_image[:, :, 2]

    # Calculate the squared Euclidean distance in the SV plane
    # The subtraction is broadcast across the entire arrays.
    s_dist_sq = np.abs(s_channel - col_hsv[1])**score_pow
    v_dist_sq = np.abs(v_channel - col_hsv[2])**score_pow

    # Calculate the Euclidean distance
    distance = np.sqrt(1. / (s_dist_sq + v_dist_sq + 1))

    # 5. Normalize the distance to a 0-255 range and convert to an 8-bit integer
    # The maximum possible distance is sqrt(255^2 + 255^2) which is approx 360.6
    cv.normalize(distance, distance, 0, 255, cv.NORM_MINMAX)
    return distance.astype(np.uint8)
