from music21 import stream, chord, metadata, midi, pitch, interval, tempo, duration, meter
def cp_to_midi(chord_progression,bpm,name,metre,midi_path):
    # Extract the string from the list
    cp_string = chord_progression[0]
    cp_string = cp_string.replace("[", "").replace("]", "").replace("'", "")

    # Chord Lists
    chords = cp_string.split(", ")
    s = stream.Stream()

    # Set Tempo, Meter and Name
    if bpm == 0: bpm = 120
    metronome_mark = tempo.MetronomeMark(bpm)
    s.insert(0, metronome_mark)
    s.timeSignature = meter.TimeSignature(metre)
    s.id = name
    # Add chords to the stream and set duration
    for c in chords:
        # print(c)
        ch = chord.Chord(chord_to_pitches(c))
        ch.duration = duration.Duration('whole')
        s.append(ch)

    # Add metadata
    s.metadata = metadata.Metadata()
    s.metadata.title = name
    # Write to MIDI
    s.write('midi', fp=f'{midi_path}/{name}.mid')

# returns a list of pitches
def chord_to_pitches(chord):
    # Define basic chord structures
    general_chord = {
        'min13': ['P1', 'm3', 'P5', 'm7', 'M9', 'M13'],
        'maj13': ['P1', 'M3', 'P5', 'M7', 'M9', 'M13'],
        'min11': ['P1', 'm3', 'P5', 'm7', 'M9', 'P11'],
        'maj11': ['P1', 'M3', 'P5', 'M7', 'M9', 'A11'],
        'min9': ['P1', 'm3', 'P5', 'm7', 'M9'],
        'maj9': ['P1', 'M3', 'P5', 'M7', 'M9'],
        'min6': ['P1', 'm3', 'P5', 'M6'],
        'maj6': ['P1', 'M3', 'P5', 'M6'],
        'minmaj7': ['P1', 'm3', 'P5', 'M7'],
        'sus2': ['P1', 'M2', 'P5'],
        'sus4': ['P1', 'P4', 'P5'],
        'min7': ['P1', 'm3', 'P5', 'm7'],
        'maj7': ['P1', 'M3', 'P5', 'M7'],
        'hdim7': ['P1', 'm3', 'd5', 'm7'],
        'dim7': ['P1', 'm3', 'd5', 'd7'],
        'maj': ['P1', 'M3', 'P5'],
        'min': ['P1', 'm3', 'P5'],
        'aug': ['P1', 'M3', 'A5'],
        'dim': ['P1', 'm3', 'd5'],
        '13': ['P1', 'M3', 'm7', 'M9','M13'],
        '11': ['P1', 'M3', 'm7','M9','P11'],
        '5' : ['P1','P5'],
        '1': ['P1'],
        '9': ['P1', 'M3', 'm7', 'M9'],
        '7': ['P1', 'M3', 'P5', 'm7'],
    }
    pitches = []
    # case when first char is &pause
    if chord[0] in ['&','(']:
        return []
    root = pitch.Pitch(chord[0])
    if chord[1] in ['#','b']:
        if root.name in ['G','A','B']: root = pitch.Pitch(chord[0:2]+str(3))
        else: root = pitch.Pitch(chord[0:2]+str(4))
    else:
        if root.name in ['G','A','B']: root = pitch.Pitch(chord[0]+str(3))
        else: root = pitch.Pitch(chord[0]+str(4))
    for type in list(general_chord.keys()):
        if type in chord:
            for inter in list(general_chord[type]):
                curr_inter = interval.Interval(inter)
                curr_pitch = curr_inter.transposePitch(root)
                pitches.append(curr_pitch)
            break

    # inversion cases
    low_root = pitch.Pitch(root.nameWithOctave[:-1] + str(int(root.nameWithOctave[-1])-1))
    if '/b3' in chord:
        og_pitch = interval.Interval('m3').transposePitch(low_root)
        pitches.append(og_pitch)
    elif '/3' in chord:
        og_pitch = interval.Interval('M3').transposePitch(low_root)
        pitches.append(og_pitch)
    elif '/5' in chord: # power chord
        og_pitch = low_root
        pitches.append(og_pitch)
    elif '/7' in chord:
        og_pitch = interval.Interval('M7').transposePitch(low_root)
        pitches.append(og_pitch)
    elif '/b7' in chord:
        og_pitch = interval.Interval('m7').transposePitch(low_root)
        pitches.append(og_pitch)
    elif '/9' in chord:
        og_pitch = interval.Interval('M9').transposePitch(low_root)
        pitches.append(og_pitch)

    # extra extension notes
    if '(b7' in chord or 'b7)' in chord:
        pitches.append(interval.Interval('m7').transposePitch(root))
    elif '(7' in chord or '7)' in chord:
        pitches.append(interval.Interval('M7').transposePitch(root))
    if '(b9' in chord or 'b9)' in chord:
        pitches.append(interval.Interval('m9').transposePitch(root))
    elif '(#9'in chord or '#9)' in chord:
        pitches.append(interval.Interval('a9').transposePitch(root))
    elif '(9' in chord or '9)' in chord:
        pitches.append(interval.Interval('M9').transposePitch(root))
    if '(#11' in chord or '#11)' in chord:
        pitches.append(interval.Interval('A11').transposePitch(root))
    elif '(11' in chord or '11)' in chord:
        pitches.append(interval.Interval('P11').transposePitch(root))
    if '(b13' in chord or 'b13)' in chord:
        pitches.append(interval.Interval('m13').transposePitch(root))
    elif '(13' in chord or '13)' in chord:
        pitches.append(interval.Interval('M13').transposePitch(root))

    return pitches
