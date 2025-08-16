# Borrar los 10 primeros pixeles de la imagen
import cv2

img = cv2.imread("cleaned_score.png", cv2.IMREAD_GRAYSCALE)

horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))


detected_lines = cv2.morphologyEx(img, cv2.MORPH_OPEN, horizontal_kernel, iterations=4) # for THRESH_BINARY_INV

inpainted = cv2.inpaint(img, detected_lines, inpaintRadius=0.1, flags=cv2.INPAINT_TELEA)

cv2.imshow("Inpaint", inpainted)
cv2.waitKey(0)
cv2.imwrite("cleaned_score.png", inpainted)
cv2.destroyAllWindows()