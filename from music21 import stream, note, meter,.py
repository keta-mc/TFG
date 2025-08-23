from music21 import stream, note, meter, spanner

N = 4
part = stream.Stream()
part.append(meter.TimeSignature('4/4'))
for i in range(N):
    m = stream.Measure()
    r = note.Rest()
    r.duration.type = 'whole'
    m.append(r)
    part.append(m)
part.show()
