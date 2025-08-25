import pygame

def reproducir_musica(archivo_midi):
    pygame.init() # inicializar pygame
    pygame.mixer.music.load(archivo_midi) # cargar archivo MIDI
    pygame.mixer.music.play() # reproducir archivo MIDI

    print("Reproduciendo música...")
    
    while pygame.mixer.music.get_busy(): # esperar a que termine la reproduccion
        pygame.time.Clock().tick(10) # comprueba cada 10 veces por segundo si sigue sonando, para reducir uso CPU
    
    print("Reproducción terminada.")