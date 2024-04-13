"""
Full workflow of poetry text to generated MIDI.

TODO: Implement music generation command (once midi-emotion dynamic generation is tested).
TODO: fluidsynth for midi => wav implementation.
"""

import argparse
import os
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description="Convert poetry as text to music as MIDI.")
parser.add_argument('-f', '--filepath', action='store_true', help='whether or given input is a filepath to a text file')
parser.add_argument('input', type=str, help='The input (a filepath to a text file or line of text)')
args = parser.parse_args()

PATH_TO_POETRY_EMOTION_SCRIPT = "./poetry_analysis/poem_to_VA_new/main.py"
PATH_TO_POETRY_EMOTION_OUTPUT = "./poetry_analysis/poem_to_VA_new/VA_output.csv"
PATH_TO_MUSIC_GENERATIONS_OUTPUT_PATHS = "./midi-emotion/dev_src/generationPaths.txt"
PATH_TO_SOUNDFONT = "./FluidR3_GM_GS.sf2"
PATH_TO_WAV_OUTPUT_DIR = "./wav_output" 

# clears output paths text file
with open(PATH_TO_MUSIC_GENERATIONS_OUTPUT_PATHS, "w") as f:
    f.close()

# read input poetry
if args.filepath:
    assert args.input[-3] == "txt", f"Input file {args.input} is not a txt file"
    with open(args.filepath, 'r') as f:
        poetryInput = f.read()
else:
    poetryInput = args.input

# call poetry-emotion conversion
os.system(f"python {PATH_TO_POETRY_EMOTION_SCRIPT} {poetryInput}")

# read poetry-emotion csv output
vaDF = pd.read_csv(PATH_TO_POETRY_EMOTION_OUTPUT)
num_rows, _ = vaDF.shape
isDynamicConditioning = num_rows > 1

# call emotion-music generation
cwd = os.getcwd().split('/')
newdir = cwd.copy()
newdir.append('midi-emotion')
newdir.append('dev_src')
newdir = '/'.join(cwd)
os.chdir(newdir)

gen_len = 3072
max_input_len = 512
batch_size = 1

if isDynamicConditioning:
    raise Exception("dynamic conditioning is not yet implemented.")
    # for rowIndex in range(num_rows):
    #     valence, arousal = float(vaDF["Valence"][rowIndex]), float(vaDF["Arousal"][rowIndex])
    #     # generate command -- will need to modify dynamic generate file to accept and test custom inputs of any size
else:
    # static conditioning
    valence, arousal = float(vaDF["Valence"][0]), float(vaDF["Arousal"][0])
    os.system(f"python generate.py --model_dir continuous_concat --conditioning continuous_concat --valence {valence} --arousal {arousal} --batch_size {batch_size} --gen_len {gen_len} --max_input_len {max_input_len}")

# identify midi output filepaths
os.chdir(cwd)
with open(PATH_TO_MUSIC_GENERATIONS_OUTPUT_PATHS, "r") as f:
    midiOutputPaths = f.read().splitlines()
    assert len(midiOutputPaths) > 0, "no midi output paths found" 
midiOutputPaths = [path.replace("..", "midi-emotion") for path in midiOutputPaths]

# convert each midi to wav using fluidsynth
for midiOutputPath in midiOutputPaths:
    assert midiOutputPath[-3] == ".mid", f"{midiOutputPath} is not a path to a midi file"
    filename = midiOutputPath.split('/')[-1][:-4]
    if not(os.path.isdir(PATH_TO_WAV_OUTPUT_DIR)):
        os.makedirs(PATH_TO_WAV_OUTPUT_DIR)
    os.system(f"fluidsynth -F {PATH_TO_WAV_OUTPUT_DIR}/{filename}.wav {PATH_TO_SOUNDFONT} {midiOutputPath}")