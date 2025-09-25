from pdf2image import convert_from_path
import os

def pdf_a_imagenes(ruta_pdf, carpeta_base="datos/TAB"):
    # Nombre de la subcarpeta donde se guardarán las imágenes
    subcarpeta = os.path.splitext(os.path.basename(ruta_pdf))[0]
    
    # Carpeta final donde se guardarán las imágenes
    carpeta_salida = os.path.join(carpeta_base, subcarpeta)

    # Crear la carpeta de salida si no existe
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # Convertir PDF a imágenes
    imagenes = convert_from_path(ruta_pdf)

    # Guardar imágenes en la carpeta de salida
    for i, img in enumerate(imagenes):
        num = i + 1
        img.save(os.path.join(carpeta_salida, f"pagina_{num:02d}.png"), "PNG")

def procesar_carpeta(carpeta_pdf="datos/tabPDF", carpeta_base="datos/TAB"):
    # Crear la carpeta base si no existe
    os.makedirs(carpeta_base, exist_ok=True)

    # Procesar cada archivo PDF en la carpeta
    for archivo in os.listdir(carpeta_pdf):
        if archivo.lower().endswith(".pdf"):
            ruta_pdf = os.path.join(carpeta_pdf, archivo)
            pdf_a_imagenes(ruta_pdf, carpeta_base)


# Ejemplo de uso
procesar_carpeta()
