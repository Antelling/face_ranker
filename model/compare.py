"""
okay so this is meant to be in bamos/openface
it loops over a directory and saves the embeddings
"""

import argparse
import cv2
import json
import os

import numpy as np
np.set_printoptions(precision=2)

import openface

fileDir = "/root/openface/demos"
modelDir = os.path.join(fileDir, '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')


parser = argparse.ArgumentParser()

parser.add_argument('imgs', type=str, help="input directory.")
parser.add_argument('--dlibFacePredictor', type=str, help="Path to dlib's face predictor.",
                    default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
parser.add_argument('--networkModel', type=str, help="Path to Torch network model.",
                    default=os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'))
parser.add_argument('--imgDim', type=int,
                    help="Default image dimension.", default=96)
parser.add_argument('--verbose', action='store_true')

args = parser.parse_args()


align = openface.AlignDlib(args.dlibFacePredictor)
net = openface.TorchNeuralNet(args.networkModel, args.imgDim)


def getRep(imgPath):
    bgrImg = cv2.imread(imgPath)
    if bgrImg is None:
        raise Exception("Unable to load image: {}".format(imgPath))
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        raise Exception("Unable to find a face: {}".format(imgPath))

    alignedFace = align.align(args.imgDim, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
        raise Exception("Unable to align image: {}".format(imgPath))

    rep = net.forward(alignedFace)
    return rep

reps = {}
for file in os.listdir(args.imgs):
    try:
        filepath = os.path.join(args.imgs, file)
        rep = getRep(filepath)
        reps[file] = rep.tolist()
    except:
        pass

with open(os.path.join("/app/save", args.imgs + ".json"), "w") as f:
    f.write(
        json.dumps(reps)
    )