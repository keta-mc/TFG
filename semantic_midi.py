from music21 import midi, stream, instrument, clef, key, meter, note, expressions, tie, spanner, environment

def partitura(tokens, instrumento, ruta_salida):
    partitura = stream.Stream()
    compas_actual = stream.Measure()

    instrumentos = instrument.fromString(instrumento)
    partitura.append(instrumentos)

    if tokens[-1] != 'barline-':
        tokens.append('barline- ')  # asegurar que la ultima token es un barline

    for i, token in enumerate(tokens):
        # obtener token anterior y siguiente si existen (para ligaduras)
        token_anterior = tokens[i-1] if i > 0 else None
        token_siguiente = tokens[i+1] if i < len(tokens)-1 else None

        notacion, info = token.split('-')
        match notacion:
            case 'clef':   # los tokens de clave tienen una estructura del tipo 'clef-G2'
                clave, linea = list(info)
                match clave:
                    case 'G':
                        c = clef.GClef()
                    case 'F':
                        c = clef.FClef()
                    case 'C':
                        c = clef.CClef()
                c.line = linea
                compas_actual.append(c)
        
            case 'keySignature':   # los tokens de armadura tienen una estructura del tipo 'keySignature-BbM'
                k = key.Key(info.replace('b','-'))  # 'BbM' -> 'B-M' music21 usa - para bemol
                compas_actual.append(k)

            case 'timeSignature': # los tokens de compas tienen una estructura del tipo 'timeSignature-3/4'
                if info == 'C/':
                    info = 'cut'  # music21 no acepta C/
                compas = meter.TimeSignature(info)  
                compas_actual.append(compas)   

            case 'note' | 'gracenote': # los tokens de nota tienen una estructura del tipo 'note-C4_quarter' y los tokens nota de adorno del tipo 'gracenote-D5_eighth.'
                tono = info.split('_') [0]
                n = note.Note(nameWithOctave = tono.replace('b','-'))  # 'Bb4' -> 'B-4' music21 usa - para bemol  
                duracion = info.split('_')[1:]
                if (len(duracion) == 2 and ((notacion == 'gracenote' or duracion[-1] != 'fermata'))) or  len(duracion) == 3:
                    duracion[0:2] = ['_'.join(duracion[0:2])]
                n.duration.dots = duracion[0].count('.')
                duracion[0] = duracion[0].replace('.','')
                match duracion[0]:
                    case 'whole' | 'half' | 'quarter' | 'eighth':
                        n.duration.type = duracion[0]
                    case 'sixteenth':
                        n.duration.type = '16th'
                    case 'thirty_second':
                        n.duration.type = '32nd'
                    case 'sixty_fourth':
                        n.duration.type = '64th'
                    case 'hundred_twenty_eighth':
                        n.duration.type = '128th'
                    case 'double_whole':
                        n.duration.type = 'breve'
                    case 'quadruple_whole':
                        n.duration.type = 'longa'
                if len(duracion) > 1 and duracion[1] == 'fermata':
                    calderon = expressions.Fermata()
                    calderon.type = 'upright'
                    n.expressions.append(calderon) # anadir calderón a la nota
                # ligaduras ---> 'tie'
                if token_siguiente == 'tie-':
                    n.tie = tie.Tie('start')
                elif token_anterior == 'tie-':
                    n.tie = tie.Tie('stop')
                if notacion == 'gracenote': # nota de adorno
                    na = n.getGrace()
                    compas_actual.append(na)
                else:
                    compas_actual.append(n) # nota normal

            case 'rest': # los tokens de silencio tienen una estructura del tipo 'rest-quarter'
                duracion = info.split('_')
                s = note.Rest()
                if len(duracion) == 2 and duracion.endswith('fermata') == 'False':
                    duracion[0:2] = ['_'.join(duracion[0:2])]
                s.duration.dots = duracion[0].count('.')
                duracion[0] = duracion[0].replace('.','')
                match duracion[0]:
                    case 'whole' | 'half' | 'quarter' | 'eighth':
                        s.duration.type = duracion[0]
                    case 'sixteenth':
                        s.duration.type = '16th'
                    case 'thirty_second':
                        s.duration.type = '32nd'
                    case 'sixty_fourth':
                        s.duration.type = '64th'
                    case 'double_whole':
                        s.duration.type = 'breve'
                    case 'quadruple_whole':
                        s.duration.type = 'longa'
                if len(duracion) > 1 and duracion[1] == 'fermata':
                    calderon = expressions.Fermata()
                    calderon.type = 'upright'
                    s.expressions.append(calderon) # anadir calderon al silencio
                compas_actual.append(s)
        
            case 'multirest':  # los tokens de silencio prolongado tienen una estructura del tipo 'multirest-3' (3 compases de silencio)
                for i in range(int(info)-1): # comprobar esto
                    sp = note.Rest()
                    sp.duration.type = 'whole'
                    compas_actual.append(sp)
                    partitura.append(compas_actual)
                    if i != (int(info)-1):
                        compas_actual = stream.Measure()

            case 'barline':  # los tokens de barra de compas tienen una estructura del tipo 'barline-'
                partitura.append(compas_actual)
                compas_actual = stream.Measure()

    compas_actual.makeAccidentals(inPlace=True, useKeySignature=True) # eliminar alteraciones accidentales redundantes

    mf = midi.translate.streamToMidiFile(partitura)
    mf.open(ruta_salida, 'wb')
    mf.write()
    mf.close()  