#https://ddmal.music.mcgill.ca/research/The_McGill_Billboard_Project_(Chord_Analysis_Dataset)/

from parser import parse
from spotify_features import get_track_id, get_audio_features, get_track_release_year
import requests
import csv
import pygame.mixer
from song_chooser import choose
from midi_sound import cp_to_midi
from app import generate
import random

if __name__ == '__main__':
    pass
    # for _ in range(10):
    #     generate(random.random(),random.random())
    # # acquire useful data
    #     songs = parse('mcgill-billboard.txt')
    #     for song in songs:
    #         id = get_track_id(song.get('artist'), song.get('name'))
    #         if id == None:
    #             continue
    #         song['release year'] = get_track_release_year(id)
    #         features = get_audio_features(id)
    #         for key,value in features.items():
    #             song[key] = value
    #     with open('raw_data.csv', mode='w', newline='') as file:
    #         writer = csv.DictWriter(file, fieldnames= songs[0].keys())
    #         # Write the header
    #         writer.writeheader()
    #         # Write the rows
    #         writer.writerows(songs)

    # clean up
    #     input_filename = 'raw_data.csv'
    #     output_filename = 'cleaned_data.csv'
    #     with open(input_filename, mode='r') as infile:
    #         reader = csv.DictReader(infile)
    #         fieldnames = reader.fieldnames
    #         # Filter the rows
    #         filtered_rows = [row for row in reader if row['energy'] and (row['chorus_cp'] not in ['[]', '', None]
    #                                                                      or row['verse_cp'] not in ['[]', '', None]
    #                                                                      or row['bridge_cp'] not in ['[]', '', None]
    #                                                                      or row['intro_cp'] not in ['[]', '', None]
    #                                                                      or row['outro_cp'] not in ['[]', '', None] )]
    #     # write the filtered rows
    #     with open(output_filename, mode='w', newline='') as outfile:
    #         writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    #         writer.writeheader()
    #         writer.writerows(filtered_rows)



