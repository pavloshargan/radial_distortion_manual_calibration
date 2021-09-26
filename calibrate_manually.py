import cv2
import numpy as np
import sys


img_orig = cv2.imread("/home/pavlo/Pictures/fisheye.jpg")

width  = img_orig.shape[1]
height = img_orig.shape[0]
shape = (height, width)

k1 = 500.
k2 = 500.
k3 = 500.
Cx = width/2.0
Cy = height/2.0
zoom = 200

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

def trackbarsHandler(x):
    global shape
    # get current positions of four trackbars
    k1 = cv2.getTrackbarPos('k1', 'image')
    k2 = cv2.getTrackbarPos('k2', 'image')
    k3 = cv2.getTrackbarPos('k3', 'image')
    zoom = cv2.getTrackbarPos('zoom', 'image')


    
    k1, k2, k3 = (k1-500)/100000000, (k2-500)/10000000000000, (k3-500)/100000000000000000

    distCoeff = np.zeros((5,1),np.float64)

    # assume unit matrix for camera
    cam = np.eye(3,dtype=np.float32)

    cam[0,2] = width/2.0  # define center x
    cam[1,2] = height/2.0 # define center y
    cam[0,0] = 10.        # define focal length x
    cam[1,1] = 10.        # define focal length y

    distCoeff[0,0] = k1
    distCoeff[1,0] = k2
    distCoeff[2,0] = 0
    distCoeff[3,0] = 0
    distCoeff[4,0] = k3
    

    nk = cam.copy()
    nk[0,0]=cam[0,0]/(zoom/100)
    nk[1,1]=cam[1,1]/(zoom/100)
    dst = cv2.undistort(img_orig.copy(),cam,distCoeff, None, nk)
    # img = cv2.fisheye.undistortImage(img_copy, K, D, None, nk)
    
    
    cv2.imshow('image',dst)
    
    print(cam, distCoeff)


   
    # Create a black image, a window

# create trackbars for color change
# cv2.createTrackbar('Fx', 'image', 0, 1000, trackbarsHandler)
# cv2.createTrackbar('Fy', 'image', 0, 1000, trackbarsHandler)
cv2.createTrackbar('k1', 'image', 0, 1000, trackbarsHandler)
cv2.createTrackbar('k2', 'image', 0, 1000, trackbarsHandler)
cv2.createTrackbar('k3', 'image', 0, 1000, trackbarsHandler)
cv2.createTrackbar('zoom', 'image', 0, 1000, trackbarsHandler)

# cv2.setTrackbarPos('Fx', 'image', int(Fx))
# cv2.setTrackbarPos('Fy', 'image', int(Fy))

cv2.setTrackbarPos('k1', 'image', int(k1))
cv2.setTrackbarPos('k2', 'image', int(k2))
cv2.setTrackbarPos('k3', 'image', int(k3))
cv2.setTrackbarPos('zoom', 'image', int(zoom))



cv2.imshow('image', img_orig)

while True:
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
