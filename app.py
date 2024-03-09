#energy,valence -> float
import csv
import pygame.mixer
from song_chooser import choose
from midi_sound import cp_to_midi

# use os path for data
import sys
import os
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(application_path, 'cleaned_data.csv')


def generate(energy,valence,midi_path):
    song = choose(data_file_path,energy,valence)
    cp_to_midi(song['chord_progression'],round(float(song['tempo'])),song['name']+'__'+song['artist']+'__' + song['section'],song['meter'],midi_path)
    return song

def play(midiname):
    pygame.mixer.init(frequency=44100, size=-8, channels=2, buffer=1024)
    pygame.mixer.music.load(midiname)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def stop():
    pygame.mixer.music.stop()