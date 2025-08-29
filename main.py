import os
import shutil
from reconocimiento import inferencia
from semantic_midi import partitura
from reproducir import reproducir_musica
from preprocesamiento import detectarLineasPentagrama

RUTA_MODELO = "modelos/semantic_model.meta"
RUTA_VOCABULARIO = "datos/vocabulary_semantic.txt"
RUTA_IMAGEN_INICIAL= "datos/imagenes/foto1.jpeg" 
SALIDA_MIDI = "salida.mid"

if __name__ == "__main__":
    pentagramas = int(input("Introduce el número de pentagramas de la imagen: "))

    if pentagramas == 1:
        tokens = inferencia(RUTA_IMAGEN_INICIAL, RUTA_MODELO, RUTA_VOCABULARIO)
        print("Tokens reconocidos:")
        print(tokens)
    
    elif pentagramas > 1: 
        ruta_carpeta_imagenes = detectarLineasPentagrama(RUTA_IMAGEN_INICIAL)
    
        imagenes = os.listdir(ruta_carpeta_imagenes)
        imagenes = [f for f in imagenes]

        tokens = []

        c = 0 # contador para evitar que se le asigne un clef y timeSignature preestablecido
        for img in imagenes:
            ruta_img = os.path.join(ruta_carpeta_imagenes, img)

            token = inferencia(ruta_img, RUTA_MODELO, RUTA_VOCABULARIO)
            c += 1
            # si token no es el primero eliminar el clef y el timeSignature del resto de elementos
            if c > 1:
                token = token[2:]
            tokens.extend(token)
    
        print("Tokens reconocidos:")
        print(tokens)

    instrumento = input("Introduce el instrumento(por defecto 'Piano'): ")
    if instrumento == "":
        instrumento = "Piano"

    partitura(tokens, instrumento, SALIDA_MIDI)
    print(f"Archivo MIDI guardado en {SALIDA_MIDI}")
    reproducir_musica(SALIDA_MIDI)

    if pentagramas > 1:  
        if os.path.exists(ruta_carpeta_imagenes) and os.path.isdir(ruta_carpeta_imagenes):
            shutil.rmtree(ruta_carpeta_imagenes)