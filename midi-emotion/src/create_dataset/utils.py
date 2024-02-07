import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import hashlib
import json
import pypianoroll
import numpy as np
import pretty_midi
import csv
import time

"""
You'll need a client ID and a client secret:
https://developer.spotify.com/dashboard/applications
Then, fill in the variables client_id and client_secret
"""

## KEY 1
# client_id = '9f2cb0e8699f42f1a735e24202abe09d'
# client_secret = '16e9fd67f81643c4aec77eb02a20f8d0'

## KEY 2
# client_id = 'dc962a7f3b9d4086b2dd71284892c4ed'
# client_secret = '355cb4f618324115863134bd1dbca743'

## KEY 3
# client_id = 'be668bffb26244ed90d953fe65dfbcd0'
# client_secret = '67f8400feab344c18a9d856d62051eda'

## KEY 4
# client_id = '72e2bf192d6d46539051d04067b47617'
# client_secret = 'df3c551e33864f7eb7f16985a036123a'

## KEY 5
# client_id = 'e2d8d79a94614210846240556792e39a'
# client_secret = '28ba2d3b25064e7c8d94e51fd795b794'

## KEY 6
# client_id = 'eb11114403bb4ca696f81a33586e3ea2'
# client_secret = 'da7b86d4cb864c19992a0da1ae4a6d4b'

## KEY 7
# client_id = '5cf7660681cc459b8aea4ad70ec1c3d7'
# client_secret = 'f98d7bf3424e430ea9481efa2a614f67'

## KEY 8
# client_id = '79f90a5257154c6d8b1a70a694d9ccdb'
# client_secret = '421c13239dd54ea28b03c320068f1429'

## KEY 9
# client_id = '92bbaa66324c44a49a88d3e99ee637e5'
# client_secret = '34a1586b8c6b42e7b0b74c406ba22658'

## KEY 10
# client_id = '9201603659554c829e28d527170af68a'
# client_secret = '6604728f365f47dfb14504e5a94325be'

## KEY 11
# client_id = 'b3b08b6f842d4b46b9fcab2445a2a260'
# client_secret = '2036b2cda22a4d2f863eebbf5124745a'

## KEY 12
client_id = '16d396e8838b4190bded8ca2058d944a'
client_secret = '442d80f697874e3f9f0a7413299ebc0d'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_drums_note_density(mid):
    drum_mid = pretty_midi.PrettyMIDI()
    for instrument in mid.instruments:
        if instrument.is_drum:
            drum_mid.instruments.append(instrument)
    if len(drum_mid.instruments) != 1 or len(drum_mid.instruments[0].notes) == 0:
        return float("nan")
    else:
        start_time = drum_mid.instruments[0].notes[0].start
        end_time = drum_mid.instruments[0].notes[-1].end
        duration = end_time - start_time
        n_notes = len(drum_mid.instruments[0].notes)
        density = n_notes / duration
        return density

def get_md5(path):
    with open(path, "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    return md5

def get_hash(path):
    if path[-4:] == ".mid":
        try:
            mid = pretty_midi.PrettyMIDI(path)
        except:
            return "empty_pianoroll"
        try:
            rolls = mid.get_piano_roll()
        except:
            return "empty_pianoroll"
        if rolls.size == 0:
            return "empty_pianoroll"
    else:
        pr = pypianoroll.load(path)
        tracks = sorted(pr.tracks, key=lambda x: x.name)
        rolls = [track.pianoroll for track in tracks if track.pianoroll.shape[0] > 0]
        if rolls == []:
            return "empty_pianoroll"
        rolls = np.concatenate(rolls, axis=-1)
    hash_ = hashlib.sha1(np.ascontiguousarray(rolls)).hexdigest()
    return hash_

def get_note_density(mid):
    duration = mid.get_end_time()
    n_notes = sum([1 for instrument in mid.instruments for note in instrument.notes])
    density = n_notes / duration
    return density

def get_tempo(mid):
    tick_scale = mid._tick_scales[-1][-1]
    resolution = mid.resolution
    beat_duration = tick_scale * resolution
    mid_tempo = 60 / beat_duration
    return mid_tempo

def get_n_instruments(mid):
    n_instruments = sum([1 for instrument in mid.instruments if instrument.notes != []])
    return n_instruments

def try_multiple(func, *args, **kwargs):
    n_max = 29
    n = 0
    failed = True
    while failed:
        if n > n_max:
            return None
        try:
            if args:
                out = func(*args)
            elif kwargs:
                out = func(**kwargs)
            failed = False
        except Exception as e:
            # print(e.error_description)
            if e.args[0] == 404:
                return None
            else:
                n += 1
    return out

def search_spotify(title, artist, album=None):
    query = '"{}"+artist:"{}"'.format(title, artist)
    if album is not None:
        query += '+album:"{}"'.format(album)
    if len(query) <= 250:
        result = try_multiple(sp.search, q=query, type='track')
        items = result['tracks']['items']
    else:   # spotify doesnt search with a query longer than 250 characters
        items = []
    return items


def search_spotify_flexible(title, artist, album):
    # Find Spotify URI based on metadata
    items = search_spotify(title, artist, album)
    if items == []:
        items = search_spotify(title, artist)
    if items == []:
        title = fix_string(title)
        items = search_spotify(title, artist)
    if items == []:
        artist = fix_string(artist)
        items = search_spotify(title, artist)
    if items == []:
        artist = strip_artist(artist)
        items = search_spotify(title, artist)
    if items == []:
        return None

    elif len(items) == 1:
        item = items[0]
    else:
        # Return most popular
        max_popularity = 0
        best_ind = 0
        for i, item in enumerate(items):
            if item is not None:
                if item["popularity"] > max_popularity:
                    max_popularity = item["popularity"]
                    best_ind = i
        item = items[best_ind]
    return item

def matching_strings_flexible(a, b):
    if a == "" or b == "":
        matches = 0.0
    else:
        a = fix_string(a)
        b = fix_string(b)
        a = a.replace("'", "")
        b = b.replace("'", "")
        min_len = min(len(a), len(b))
        matches = 0
        for i in range(min_len):
            if a[i] == b[i]:
                matches += 1
        matches /= min_len
    return matches

def get_spotify_features(uri_list):
    features = try_multiple(sp.audio_features, uri_list)
    return features

def get_spotify_tracks(uri_list):
    if len(uri_list) > 50:
        uri_list = uri_list[:50]
    tracks = try_multiple(sp.tracks, uri_list)
    if tracks == None:
        return None
    else:
        return tracks["tracks"]


def strip_artist(s):
    s = s.lower()   # lowercase
    s = s.replace("the ", "")
    keys = [' - ', '/', ' ft', 'feat', 'featuring', ' and ', ' with ', '_', ' vs', '&', ';', '+']
    for key in keys:
        loc = s.find(key)
        if loc != -1:
            s = s[:loc]
    return s

def fix_string(s):
    if s != "":
        s = s.lower()   # lowercase
        s = s.replace('\'s', '')    # remove 's
        s = s.replace('_', ' ')    # remove _
        s = re.sub("[\(\[].*?[\)\]]", "", s)    # remove everything in parantheses
        if s[-1] == " ":    # remove space at the end
            s = s[:-1]
    return s

def logprint(s, f):
    f.write(s + '\n')

def get_spotify_ids(json_path):
    with open(json_path) as f_json:
        json_data = json.load(f_json)
        json_data = json_data["response"]["songs"]
        if len(json_data) == 0:
            spotify_ids = []
        else:
            json_data = json_data[0]
            spotify_ids = []
            for track in json_data["tracks"]:
                if track["catalog"] == "spotify" and "foreign_id" in list(track.keys()):
                    spotify_ids.append(track["foreign_id"].split(":")[-1])
    return spotify_ids

def read_csv(input_file_path, delimiter=","):
    with open(input_file_path, "r") as f_in:
        reader = csv.DictReader(f_in, delimiter=delimiter)
        data = [{key: value for key, value in row.items()} for row in reader]
    return data