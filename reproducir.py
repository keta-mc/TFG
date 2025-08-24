import pygame

def reproducir_musica(archivo_midi):
    pygame.init()
    pygame.mixer.music.load(archivo_midi)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)