import cv2
import numpy as np
import os

from reconocimiento import inferencia
from semantic_midi import partitura

RUTA_MODELO = "modelos/semantic_model.meta"
RUTA_VOCABULARIO = "datos/vocabulary_semantic.txt"
RUTA_IMAGEN = "datos/images/000113818-1_1_1.png"
SALIDA_MIDI = "salida.mid"

if __name__ == "__main__":
    tokens = inferencia(RUTA_IMAGEN, RUTA_MODELO, RUTA_VOCABULARIO)
    print(tokens)
    partitura(tokens, SALIDA_MIDI)