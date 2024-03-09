# returns a list of dictionaries
def parse(filename):
    def process_chord_progression(chord_lines):
        chords = []
        previous_chord = ''
        for line in chord_lines:
            bars = line.split('|')[1:-1]
            for bar in bars:
                bar_chords = bar.split()
                for chord in bar_chords:
                    if chord == '.':
                        chords.append(previous_chord)
                    else:
                        chords.append(chord)
                        previous_chord = chord
        return chords

    songs = []
    song = {}
    verse_lines,chorus_lines,intro_lines,outro_lines,bridge_lines = [],[],[],[],[]
    # (pre verse ,pre chorus,solo,interlude,fadeout)
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('# title:') and not song:
                song['name'] = line.split(': ', 1)[1]
            elif line.startswith('# artist:'):
                song['artist'] = line.split(': ', 1)[1]
            elif line.startswith('# metre:'):
                song['meter'] = line.split(': ', 1)[1]
            elif 'chorus' in line or 'solo' in line:
                chorus_lines.append(line)
            elif 'verse' in line or 'pre-chorus' in line:
                verse_lines.append(line)
            elif 'intro' in line or 'pre-verse' in line:
                intro_lines.append(line)
            elif 'outro' in line or 'fadeout' in line:
                outro_lines.append(line)
            elif 'bridge' in line or 'interlude' in line:
                bridge_lines.append(line)
            # Check if a new song is starting
            elif line.startswith('# title:') and song:
                song['chorus_cp'] = process_chord_progression(chorus_lines)
                song['verse_cp'] = process_chord_progression(verse_lines)
                song['intro_cp'] = process_chord_progression(intro_lines)
                song['outro_cp'] = process_chord_progression(outro_lines)
                song['bridge_cp'] = process_chord_progression(bridge_lines)
                songs.append(song)
                song = {}
                song['name'] = line.split(': ', 1)[1]
                verse_lines,chorus_lines,intro_lines,outro_lines,bridge_lines = [],[],[],[],[]

        # Add the last song if exists
        if song:
            song['chorus_cp'] = process_chord_progression(chorus_lines)
            song['verse_cp'] = process_chord_progression(verse_lines)
            song['intro_cp'] = process_chord_progression(intro_lines)
            song['outro_cp'] = process_chord_progression(outro_lines)
            song['bridge_cp'] = process_chord_progression(bridge_lines)
            songs.append(song)
    return songs

if __name__ == '__main__':
    print('parser')