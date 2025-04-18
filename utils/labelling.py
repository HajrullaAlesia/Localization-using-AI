import cv2
import math

class Labelling:
    def __init__(self):
        self.setLabelledbBoxes = []
        self.currentBoxes = []
        self.countClasses = {}

    def manage_label (self, box, classe, conf):
        labelledBox = LabelledBox(box, classe, conf)
        if self.setLabelledbBoxes :
            for labBox in self.setLabelledbBoxes:
                if labelledBox.compareLabBox(labBox):
                    labBox.refreshParam(labelledBox)
                    #labelledBox.numInstance = labBox.numInstance
                    #self.setLabelledbBoxes.remove(labBox)
                    #self.setLabelledbBoxes.append(labelledBox)
                    # create a function that just refreshes the parameters
                    return      # if the box has matched an existing one, we shut the function
            
            # if the box doesn't match any : it's a new one
            if classe in self.countClasses :   # if the class of the box is already in the list of the detected classes :
                labelledBox.numInstance = self.countClasses[classe] + 1
                self.countClasses[classe] += 1
                self.setLabelledbBoxes.append(labelledBox)
            else:  # if it's not in the list, we add the new key : 
                labelledBox.numInstance = 1
                self.countClasses[classe] = 1
                self.setLabelledbBoxes.append(labelledBox)
        else:
            labelledBox.numInstance = 1
            self.countClasses[classe] = 1
            self.setLabelledbBoxes.append(labelledBox)
        self.currentBoxes.append(labelledBox)

    def removeUnvisibleBoxes(self):  
        listUnvisBoxes = [item for item in self.setLabelledbBoxes if item not in self.currentBoxes]
        for box in self.currentBoxes:
            box.countMissing = 0
        for box in listUnvisBoxes:
            box.countMissing += 1
            if box.countMissing > 100 :
                self.setLabelledbBoxes.remove(box)

    def plotLabelledBoxes(self, img, thresh_conf):
        for labBox in self.setLabelledbBoxes:
            '''
            if labBox.outOfBorder(img.shape[1], img.shape[0]):
                self.setLabelledbBoxes.remove(labBox)
                break
            '''
            self.removeUnvisibleBoxes()
            if float(labBox.conf) > thresh_conf:
                color = (255, 0, 0)
                label = labBox.classe + str(labBox.numInstance)
                p1 = (int(round(labBox.center[0]-labBox.width/2)) , int(round(labBox.center[1]-labBox.height/2)))
                p2 = (int(round(labBox.center[0]+labBox.width/2)) , int(round(labBox.center[1]+labBox.height/2)))

                cv2.rectangle(img, p1, p2, color)
                h = 10
                w = 30
                txt_color=(255, 255, 255)
                outside = p1[1] - h - 3 >= 0  # label fits outside box
                p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
                cv2.rectangle(img, p1, p2, color, -1, cv2.LINE_AA)  # filled

                cv2.putText(img, label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2), 0, 1, txt_color,
                            thickness=1, lineType=cv2.LINE_AA)

        cv2.imshow("Labelling", img)
        self.currentBoxes.clear()

class LabelledBox:
    def __init__(self, box, classe, conf):
        self.center = (int(round(float(box[0]) + (float(box[2])-float(box[0]))/2)), int(round(float(box[1]) + (float(box[3])-float(box[1]))/2)))
        self.width = int(round(float(box[2]) - float(box[0])))
        self.height = int(round(float(box[3]) - float(box[1])))
        self.classe = classe
        self.conf = conf
        self.numInstance = 1
        self.countMissing = 0

    def refreshParam(self, box):
        self.center = box.center
        self.width = box.width
        self.height = box.height
        self.conf = box.conf
        self.countMissing = box.countMissing


    def compareLabBox(self, labBox):
        
        if self.classe == labBox.classe and math.dist(self.center, labBox.center) < 20 and min([self.width, labBox.width]) >= 0.75*max([self.width, labBox.width]) and min([self.height, labBox.height]) >= 0.75*max([self.height, labBox.height]):
            return True
        else :
            return False

    def outOfBorder(self, width_img, height_img):

        p1 = (int(round(self.center[0]-self.width/2)) , int(round(self.center[1]-self.height/2)))
        p2 = (int(round(self.center[0]+self.width/2)) , int(round(self.center[1]+self.height/2)))

        if p1[0] > width_img or p2[0] < 0 or p1[1] > height_img or p2[1] < 0:
            return True
        else:
            return False
                