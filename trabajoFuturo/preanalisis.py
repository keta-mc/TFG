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


def detectarMargenes(carpeta_salida):
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


def detectarTAB(carpeta_salida, x_max, x_min):
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


def recortarTAB():
    carpeta_entrada = "trabajoFuturo/imagen_procesada2"
    imagen_clara = cv2.imread(os.path.join(carpeta_entrada, "imagen.png"), cv2.IMREAD_GRAYSCALE)

    imagen_lineas_tab = cv2.imread(os.path.join(carpeta_entrada, "lineas_filtradas.png"), cv2.IMREAD_GRAYSCALE)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    lineas_tab = cv2.morphologyEx(imagen_lineas_tab, cv2.MORPH_OPEN, kernel, iterations=6) # para THRESH_BINARY_INV

    contornosTAB, _ = cv2.findContours(lineas_tab, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contornosTAB = sorted(contornosTAB, key=lambda c: cv2.boundingRect(c)[1])

    carpeta_salida = "trabajoFuturo/imagen_procesada2/pentagramas"
    os.makedirs(carpeta_salida, exist_ok=True)

    for i in range(0, len(contornosTAB), 6):
        grupo = contornosTAB[i:i+6]
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
        x_max = max(0, max(xe) + 10)
        y_min = max(0, min(ys) - 40)
        y_max = min(imagen_clara.shape[0], max(ye) + 240)

        _, imagen_bin = cv2.threshold(imagen_clara, 127, 255, cv2.THRESH_BINARY)

        recorte = imagen_bin[y_min:y_max, x_min:x_max]
    
        if recorte.size == 0:
            continue
    
        num = i // 6 + 1
        ruta_salida = os.path.join(carpeta_salida, f"pentagrama_{num:02d}.png") # por si hay más de 10 pentagramas, que en el main se ordenen bien
        cv2.imwrite(ruta_salida, recorte)