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

lineas_detectadas = cv2.morphologyEx(imagen_clara, cv2.MORPH_OPEN, kernel_horizontal, iterations=5) # para THRESH_BINARY_INV

cv2.imshow('lineas', lineas_detectadas)
cv2.waitKey(0)
cv2.destroyAllWindows()

contornos, _ = cv2.findContours(lineas_detectadas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contornos = sorted(contornos, key=lambda c: cv2.boundingRect(c)[1]) # Ordenado por coordenada y

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
        
    x_min = min(xs) - 10
    x_max = max(xe) 
    y_min = min(ys) - 40
    y_max = max(ye) + 40

    cv2.rectangle(imagen, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

    _, imagen = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)

    recorte = imagen[y_min:y_max, x_min:x_max]

    _, recorte = cv2.threshold(recorte, 127, 255, cv2.THRESH_BINARY)
    
    if recorte.size == 0:
        continue
    else:
        num = i // 6 + 1
        ruta_salida = os.path.join(carpeta_salida, f"pentagrama_{num:02d}.png") # por si hay más de 10 pentagramas, que en el main se ordenen bien
        cv2.imwrite(ruta_salida, recorte)
    
cv2.imshow('imagen con rectangulos', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite(os.path.join(carpeta_salida, "imagen_con_rectangulos.png"), imagen)
# Guardar la imagen con los rectángulos dibujados
