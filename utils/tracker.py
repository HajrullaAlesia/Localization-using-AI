
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import sys
import numpy as np


class TrackEnv: 
    def __init__(self):

        self.trackers = []
        self.lock = False
        self.track_alg = None
        self.OPENCV_OBJECT_TRACKERS = None

        self.track_type()

    def track_type(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", type=str, help="path to input video file")
        ap.add_argument("-t", "--tracker", type=str, default="kcf",
            help="OpenCV object tracker type")

        #opt = ap.parse_args(['--tracker', 'tld', '--video', 'C:/Users/demar/Documents/Travail/UTC/ISCF/Code/Test_YOLO/images/video_car.avi'])
        opt = ap.parse_args(['--tracker', 'csrt'])

        args = vars(opt)
        self.track_alg = args["tracker"]
        # initialize a dictionary that maps strings to their corresponding
        # OpenCV object tracker implementations
        self.OPENCV_OBJECT_TRACKERS = {
            "csrt": cv2.legacy.TrackerCSRT_create,
            "kcf": cv2.legacy.TrackerKCF_create,
            "boosting": cv2.legacy.TrackerBoosting_create,
            "mil": cv2.legacy.TrackerMIL_create,
            "tld": cv2.legacy.TrackerTLD_create,
            "medianflow": cv2.legacy.TrackerMedianFlow_create,
            "mosse": cv2.legacy.TrackerMOSSE_create
        }


    def add_tracker(self, img, box):
        if self.lock or len(self.trackers) > 2:
            return
        init_bb = (int(box[0]), int(box[1]), int(box[2]-box[0]), int(box[3]-box[1]))
        add = True
        for box_tracker in self.trackers:
            if np.all(np.asarray(init_bb) == np.asarray(box_tracker.initBB)):
                add = False
                break
        if add :
            new_tracker = Tracker(self.OPENCV_OBJECT_TRACKERS[self.track_alg](), init_bb)

            new_tracker.tracker.init(img, init_bb)
            self.trackers.append(new_tracker)

    def lock_add(self):
        self.lock = True

    def unlock_add(self):
        self.lock = False

    def manage_BB (self):
        for tracker in self.trackers:
            if tracker.count_miss == 50:
                self.trackers.remove(tracker)
        if len(self.trackers) < 3:
            self.trackers.clear()
            self.unlock_add()


    def track(self, img):
        # check to see if we are currently tracking an object
        if self.trackers:
            
            # grab the new bounding box coordinates of the object
            for box_tracker in self.trackers:
                (success, box) = box_tracker.tracker.update(img)
                box_tracker.new_bb = box
            # check to see if the tracking was a success
                if success:
                    (x, y, w, h) = [int(v) for v in box]
                    cv2.rectangle(img, (x, y), (x + w, y + h),
                        (0, 255, 0), 2)
                else : 
                    box_tracker.count_miss +=1
            
            self.lock_add()
            self.manage_BB()
            

            
        # show the output frame
        cv2.imshow("Frame", img)
        #key = cv2.waitKey(1) & 0xFF

                
        
class Tracker():
    def __init__(self, tracker, initBB):
        self.tracker = tracker
        self.initBB = initBB
        self.new_bb = self.initBB
        self.count_miss = 0

    
    