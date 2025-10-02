import cv2
import os
import numpy as np
from preanalisis import detectarMargenes, detectarTAB

carpeta_salida = "trabajoFuturo/imagen_procesada2"

img = cv2.imread("cleaned_score.png", cv2.IMREAD_GRAYSCALE)

horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))

# MORPH_CLOSE with 3 iterations gives the best results of detecting the staff lines
# since the binary image is with white background, MORPH_BLACKHAT with 3 iterations gives only the musical objetcts
# detected_lines = cv2.morphologyEx(img, cv2.MORPH_CLOSE, horizontal_kernel, iterations=3) # for THRESH_BINARY
detected_lines = cv2.morphologyEx(img, cv2.MORPH_OPEN, horizontal_kernel, iterations=4) # for THRESH_BINARY_INV

inpainted = cv2.inpaint(img, detected_lines, inpaintRadius=0.1, flags=cv2.INPAINT_TELEA)

cv2.imshow("Inpaint", inpainted)
cv2.waitKey(0)
cv2.imwrite("cleaned_score.png", inpainted)
cv2.destroyAllWindows()

img = cv2.imread("cleaned_score.png", cv2.IMREAD_GRAYSCALE)


# Binarize the image (convert to black and white)
_, binary_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

# Convert the grayscale image to BGR for visualization
img_with_contour = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)

for contour in contours:
    cv2.drawContours(img_with_contour, [contour], -1, (0,255,0), 1)
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img_with_contour, (x,y), (x + w, y + h), (255,0,0), 1)


cv2.imshow('contour', img_with_contour)
cv2.waitKey(0)
cv2.destroyAllWindows()
