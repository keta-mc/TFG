from reconocimiento import inferencia
from semantic_midi import partitura
from reproducir import reproducir_musica

RUTA_MODELO = "modelos/semantic_model.meta"
RUTA_VOCABULARIO = "datos/vocabulary_semantic.txt"
RUTA_IMAGEN = "datos/imagenes/pantera_rosa.png"
SALIDA_MIDI = "salida.mid"

if __name__ == "__main__":
    tokens = inferencia(RUTA_IMAGEN, RUTA_MODELO, RUTA_VOCABULARIO)
    print("Tokens reconocidos:")
    print(tokens)
    instrumento = input("Introduce el instrumento(por defecto 'Piano'): ")
    if instrumento == "":
        instrumento = "Piano"
    partitura(tokens, instrumento, SALIDA_MIDI)
    print(f"Archivo MIDI guardado en {SALIDA_MIDI}")
    reproducir_musica(SALIDA_MIDI)