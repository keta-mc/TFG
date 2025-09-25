'''import cv2

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
cv2.destroyAllWindows()'''


import cv2
import os

carpeta_salida = "imagen_procesada2"
os.makedirs(carpeta_salida, exist_ok=True)

imagen = cv2.imread("datos/TAB/unaMattina/pagina_01.png" , cv2.IMREAD_GRAYSCALE)

_, binary = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY_INV)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
imagen_clara = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

#cv2.imshow('img', imagen_clara)

kernel_horizontal = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))

lineas_detectadas = cv2.morphologyEx(imagen_clara, cv2.MORPH_OPEN, kernel_horizontal, iterations=6) # para THRESH_BINARY_INV

imagen_color = cv2.cvtColor(imagen, cv2.COLOR_GRAY2BGR)

contornos, _ = cv2.findContours(lineas_detectadas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contornos = sorted(contornos, key=lambda c: cv2.boundingRect(c)[1]) # Ordenado por coordenada y

for c in contornos:
    x, y, w, h = cv2.boundingRect(c)

    if h > 5:
        continue

    y_centro = y + h // 2

    cv2.line(imagen_color, (x, y_centro), (x + w, y_centro), (0, 0, 255), 2) # Dibuja una línea roja en la imagen original

cv2.imwrite(os.path.join(carpeta_salida, "lineas_detectadas.png"), imagen_color)