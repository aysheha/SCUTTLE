# This program takes an image, applies filters with openCV, and returns
# a color target if located in the image.  The target parameters are (x,y,radius).

# Import external libraries
import cv2
import numpy as np

# Import internal programs
import L1_camera as cam

width = 120                                                 # width of image being processed (pixels)
color_range = np.array([[45, 60, 180], [115, 180, 255]])        # enter values here if running standalone program.
#blue H min 145; S min 25; V min 100
#blue H max 255; S max 255; V max 255
#pink min 95, 70, 25
#pink max 200, 200, 255


# This function searches an image for an object of the specified color.  Returns array containing [x, y, radius] in pixels.
def colorTarget(color_range=((45, 60, 180), (115, 180, 255))):

    image = cam.newImage()
    frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(frame_to_thresh, color_range[0], color_range[1])
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,kernel)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]    # generates number of contiguous "1" pixels
    if len(cnts) > 0:   
        c = max(cnts, key=cv2.contourArea)                                                  # return the largest target area
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])
        if radius > 0:
            return np.array([round(x, 1), round(y, 2), round(radius, 2), center_x, center_y])
                                                                   # begin processing if there are "1" pixels discovered
    else:
        return np.array([-1, -1, 0, -1, -1])

def horizLoc(target_x):                             # generate an estimate of the angle of the target from center
    if target_x is not None:
        viewAngle = 90                              # camera view, degrees
        ratio = target_x / width                    # divide by pixels in width
        wrtCenter = ratio - 0.5                     # offset.  Now, positive value = right, negative = left
        targetTheta = -1 * wrtCenter * viewAngle    # scale the value roughly to degrees
        return int(targetTheta)
    else:
        return None


if __name__ == "__main__":
    while True:
        target = colorTarget(color_range)           # grab target x, y, radius
        x = target[0]
        radius = target[2]
        if x is None:
            print("no target located.")
        else:
            targetTheta = horizLoc(x)
            print(targetTheta)
            print("x:", x, "\t", "radius:", radius)