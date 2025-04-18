import cv2
import numpy as np

class Disparity:
    def __init__(self):
        self.stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
        self.img = np.ones((720,1280)).astype('uint8')
        self.last_img = self.img

    def actualize (self, img_shape):
        self.shape = (img_shape[0], img_shape[1])
        self.img = np.zeros(self.shape).astype('uint8')

    def center_boxes(self, box):
        center_ell = (int(round(int(box[0]) + (int(box[2])-int(box[0]))/2)), int(round(int(box[1]) + (int(box[3])-int(box[1]))/2)))
        cv2.ellipse(self.img, center_ell, (5,5), angle = 0, startAngle = 0, endAngle = 360, color = 255, thickness = 10)        

    def display_disparity(self):
        disparity = self.stereo.compute(self.last_img, self.img)
        disparity = cv2.normalize(disparity, None, alpha = 0, beta = 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        cv2.imshow('frame', disparity)
        self.last_img = self.img