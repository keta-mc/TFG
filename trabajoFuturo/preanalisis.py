import cv2
import os
import numpy as np


def binarizar(ruta_imagen):
    carpeta_salida = "trabajoFuturo/imagen_procesada2"
    os.makedirs(carpeta_salida, exist_ok=True)

    imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

    _, binary = cv2.threshold(f"{imagen}", 127, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    imagen_clara = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    cv2.imwrite(os.path.join(carpeta_salida, "imagen.png"), imagen_clara)

def detectarMargenes():
    carpeta_salida = "trabajoFuturo/imagen_procesada2"

    imagen = cv2.imread(os.path.join(carpeta_salida, "imagen.png"), cv2.IMREAD_GRAYSCALE)

    kernel_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))

    barras_y_lineas = cv2.morphologyEx(imagen, cv2.MORPH_ERODE, kernel_vertical, iterations=6)

    contornosv, _ = cv2.findContours(barras_y_lineas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Inicilizar variables
    x_min = np.inf
    x_max = -np.inf

    for cnt in contornosv:
        # Extraer coordenadas x de los contornos
        xs = cnt[:, :, 0] # cnt tiene forma (num_puntos, 1, 2), [:, :, 0] son las coordenadas x
        x_min = min(x_min, xs.min())
        x_max = max(x_max, xs.max())

    return x_max, x_min

def detectarTAB(x_max, x_min):
    carpeta_salida = "trabajoFuturo/imagen_procesada2"

    imagen_clara = cv2.imread(os.path.join(carpeta_salida, "imagen.png"), cv2.IMREAD_GRAYSCALE)

    x_max, x_min = detectarMargenes()
    
    kernel_horizontal = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))

    lineas_detectadas = cv2.morphologyEx(imagen_clara, cv2.MORPH_OPEN, kernel_horizontal, iterations=6) # para THRESH_BINARY_INV

    contornos, _ = cv2.findContours(lineas_detectadas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contornos = sorted(contornos, key=lambda c: cv2.boundingRect(c)[1]) # Ordenado por coordenada y

    lineas_tab = np.zeros_like(lineas_detectadas) # Imagen en blanco para dibujar las líneas de interés (TAB)
    lineas_dur = np.zeros_like(lineas_detectadas) # Imagen en blanco para dibujar las líneas de duración de las notas

    for cnt in contornos:
        x, y, w, h = cv2.boundingRect(cnt)

        if h <= 3:  # Filtrar por altura
            y_centro = y + h // 2
            cv2.line(lineas_tab, (x_min, y_centro), (x_max, y_centro), 255, 2) # Dibuja una línea blanca en la imagen de TAB
        else:
            cv2.drawContours(lineas_dur, [cnt], -1, 255, thickness=cv2.FILLED) # Dibuja en blanco las líneas de duración

    cv2.imwrite(os.path.join(carpeta_salida, "lineas_duracion.png"), lineas_dur)
    cv2.imwrite(os.path.join(carpeta_salida, "lineas_filtradas.png"), lineas_tab)