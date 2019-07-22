import cv2
import os


import openface



class TripletEmbedding(object):
    def __init__(self,
                 dlibFacePredictor="shape_predictor_68_face_landmarks.dat",
                 networkModel="nn4.small2.v1.t7",
                 imgDim=96):
        self.modelDir = "/home/anthony/software/openface/models"
        self.dlibFacePredictor = os.path.join(self.modelDir, "dlib", dlibFacePredictor)
        self.networkModel = os.path.join(self.modelDir, "openface", networkModel)
        self.imgDim = imgDim
        self.align = openface.AlignDlib(self.dlibFacePredictor)
        self.net = openface.TorchNeuralNet(self.networkModel, imgDim)

    def getEmbedding(self, imgPath):
        bgrImg = cv2.imread(imgPath)
        if bgrImg is None:
            raise Exception("Unable to load image: {}".format(imgPath))
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

        bb = self.align.getLargestFaceBoundingBox(rgbImg)
        if bb is None:
            raise Exception("Unable to find a face: {}".format(imgPath))

        alignedFace = self.align.align(self.imgDim, rgbImg, bb,
                                  landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            raise Exception("Unable to align image: {}".format(imgPath))

        rep = self.net.forward(alignedFace)
        return rep