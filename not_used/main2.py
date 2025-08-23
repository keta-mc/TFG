import cv2
import numpy as np
import os

from not_used.preprocessing import cleanAndBinarize, staffLineDetectionAndRemoval

if __name__ == "__main__":
    carpetaImages = './data/images'

    imagenes = os.listdir(carpetaImages)

    imagen = [f for f in imagenes]

    for img in imagen:
        ruta_img = os.path.join(carpetaImages, img)
        cleanAndBinarize(ruta_img)
        staffLineDetectionAndRemoval()
    
    cv2.destroyAllWindows()