import cv2
from preprocessing import cleanAndBinarize, staffLineDetectionAndRemoval

imagenes = ['data/images/000102308-1_2_1.png','data/images/000118417-1_2_1.png','data/images/000132119-1_1_2.png','data/images/100500172-1_2_1.png']


cleanAndBinarize(imagenes[3])

img = cv2.imread("cleaned_score.png", cv2.IMREAD_GRAYSCALE)

horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))

# MORPH_CLOSE with 3 iterations gives the best results of detecting the staff lines
# since the binary image is with white background, MORPH_BLACKHAT with 3 iterations gives only the musical objetcts
# detected_lines = cv2.morphologyEx(img, cv2.MORPH_CLOSE, horizontal_kernel, iterations=3) # for THRESH_BINARY
detected_lines = cv2.morphologyEx(img, cv2.MORPH_OPEN, horizontal_kernel, iterations=4) # for THRESH_BINARY_INV

cv2.imshow('lines',detected_lines)
cv2.waitKey(0)

inpainted = cv2.inpaint(img, detected_lines, inpaintRadius=0.1, flags=cv2.INPAINT_TELEA)

cv2.imshow("Inpaint", inpainted)
cv2.waitKey(0)
cv2.destroyAllWindows()


