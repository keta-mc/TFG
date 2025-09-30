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
import numpy as np

carpeta_salida = "imagen_procesada2"
os.makedirs(carpeta_salida, exist_ok=True)

imagen = cv2.imread("datos/TAB/unaMattina/pagina_01.png" , cv2.IMREAD_GRAYSCALE)

_, binary = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY_INV)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
imagen_clara = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

#cv2.imshow('img', imagen_clara)
kernel_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))

barras_y_lineas = cv2.morphologyEx(imagen_clara, cv2.MORPH_OPEN, kernel_vertical, iterations=5)

cv2.imwrite(os.path.join(carpeta_salida, "barras_y_lineas.png"), barras_y_lineas)

kernel_horizontal = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))

lineas_detectadas = cv2.morphologyEx(imagen_clara, cv2.MORPH_OPEN, kernel_horizontal, iterations=6) # para THRESH_BINARY_INV

imagen_color = cv2.cvtColor(imagen, cv2.COLOR_GRAY2BGR)

contornos, _ = cv2.findContours(lineas_detectadas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#contornos = sorted(contornos, key=lambda c: cv2.boundingRect(c)[1]) # Ordenado por coordenada y

lineas_tab = np.zeros_like(lineas_detectadas) # Imagen en blanco para dibujar las líneas de interés (TAB)
lineas_dur = np.zeros_like(lineas_detectadas) # Imagen en blanco para dibujar las líneas de duración de las notas

for cnt in contornos:
    x, y, w, h = cv2.boundingRect(cnt)

    if h <= 3:  # Filtrar por altura
        cv2.drawContours(lineas_tab, [cnt], -1, 255, thickness=cv2.FILLED) # Dibuja la línea en blanco

        y_centro = y + h // 2
        cv2.line(lineas_tab, (x, y_centro), (x + w, y_centro), 255, 2) # Dibuja una línea blanca en la imagen de TAB
    else:
        cv2.drawContours(lineas_dur, [cnt], -1, 255, thickness=cv2.FILLED) # Dibuja en blanco las líneas de duración

cv2.imwrite(os.path.join(carpeta_salida, "lineas_duracion.png"), lineas_dur)

kernel_union = cv2.getStructuringElement(cv2.MORPH_RECT, (250, 1))
lineas_tab = cv2.morphologyEx(lineas_tab, cv2.MORPH_CLOSE, kernel_union, iterations=2)

cv2.imwrite(os.path.join(carpeta_salida, "lineas_filtradas.png"), lineas_tab)
'''for c in contornos:
    x, y, w, h = cv2.boundingRect(c)

    if h > 5:
        continue

    y_centro = y + h // 2

    cv2.line(imagen_color, (x, y_centro), (x + w, y_centro), (0, 0, 255), 2) # Dibuja una línea roja en la imagen original

cv2.imwrite(os.path.join(carpeta_salida, "lineas_detectadas.png"), imagen_color)

for i in range(0, len(contornos), 6):
    grupo = contornos[i:i+6]
    if len(grupo) < 6:
        continue

    xs, ys, xe, ye = [], [], [], []
    for g in grupo:
        x, y, w, h = cv2.boundingRect(g)
        xs.append(x)
        ys.append(y)
        xe.append(x + w)
        ye.append(y + h)

    x_min = max(0, min(xs) - 10)
    x_max = max(xe)
    y_min = max(0, min(ys) - 40)
    y_max = min(imagen.shape[0], max(ye) + 40)

    cv2.rectangle(imagen_color, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

    _, imagen_bin = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)

    recorte = imagen_bin[y_min:y_max, x_min:x_max]

    # _, recorte = cv2.threshold(recorte, 127, 255, cv2.THRESH_BINARY)
    
    if recorte.size == 0:
        continue
    
    num = i // 6 + 1
    ruta_salida = os.path.join(carpeta_salida, f"pentagrama_{num:02d}.png") # por si hay más de 10 pentagramas, que en el main se ordenen bien
    cv2.imwrite(ruta_salida, recorte)

cv2.imwrite(os.path.join(carpeta_salida, "imagen_con_recortes.png"), imagen_color)
# Guardar la imagen con los rectángulos dibujados'''