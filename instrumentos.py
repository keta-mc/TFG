from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

# Crear MIDI y pista
mid = MidiFile(ticks_per_beat=480)  # 480 ticks = 1 negra
track = MidiTrack()
mid.tracks.append(track)

# Instrumento: Saxofón Alto (program 65)
track.append(Message('program_change', program=65, time=0))

# Tempo: 120 BPM
tempo = bpm2tempo(120)
track.append(MetaMessage('set_tempo', tempo=tempo))

# Notas con tiempos (nota MIDI, duración en ticks)
# corchea = 240 ticks (480 / 2)
# negra = 480 ticks
# silencio = simplemente aumenta el "time" antes de la siguiente nota
notes = [
    (60, 240),   # C4 - corchea
    (62, 240),   # D4 - corchea
    (None, 240), # silencio - corchea
    (64, 480),   # E4 - negra
    (65, 240),   # F4 - corchea
    (67, 240),   # G4 - corchea
]

# Agregar las notas
for note, duration in notes:
    if note is not None:
        track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=note, velocity=64, time=duration))
    else:
        # Silencio: solo esperar 'duration' sin tocar nada
        track.append(Message('note_off', note=0, velocity=0, time=duration))

# Guardar archivo
mid.save("melodia_saxo.mid")