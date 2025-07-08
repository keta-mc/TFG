import os
import cv2
from preprocessing import cleanAndBinarize, staffLineDetectionAndRemoval

cleanAndBinarize("data/images/000100134-4_1_1.png")
staffLineDetectionAndRemoval()
