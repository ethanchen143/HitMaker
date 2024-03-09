import csv
import random
def choose(filename,energy,valence):
    # songs that fit user preference
    songs = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if abs(float(row['energy']) - energy) < 0.3 and abs(float(row['valence']) - valence) < 0.1:
                song = row
                songs.append(song)

    if len(songs) == 0:
        raise ValueError("no song found, try different values")

    # choose random songs
    rand = random.choice(songs)
    # some further cleanup
    to_delete = []
    for key in rand.keys():
        if len(key) < 8: continue
        if 'N' in rand[key] or '*' in rand[key]:
            # print("delete:"+rand[key])
            rand[key] = []
        if rand[key] in ['',[],None]:
            to_delete.append(key)
    for k in to_delete:
        rand.pop(k)

    # pick a random section, minimum 3-4 chords
    keys = []
    for key in rand.keys():
        if len(key) in [8,9]:
            keys.append(key)
    # find a section with more than 1 or two chords
    while(True):
        picked_key = random.choice(keys)
        if(len(rand[picked_key])> 12): break
    # print("picked key:"+picked_key)
    rand['section'] = picked_key.replace('_cp','')

    # convert chord progression to adhere to music21 chord naming convention
    correct_chords = []
    # Check if chord_progression is a list and convert it to a list if not
    if not isinstance(rand[picked_key], list):
        rand[picked_key] = [rand[picked_key]]
    for chord in rand[picked_key]:
        curr = chord.replace(':','')
        correct_chords.append(curr)

    rand['chord_progression'] = correct_chords

    # rid of extra information
    to_delete = []
    for key in rand.keys():
        if len(key) < 8 or key == 'chord_progression' or key == 'release year': continue
        to_delete.append(key)
    for k in to_delete:
        rand.pop(k)

    return rand

if __name__ == '__main__':
    print('song_chooser')