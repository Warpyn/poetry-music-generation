"""
Full workflow of poetry text to generated MIDI.

TODO: Implement music generation command (once midi-emotion dynamic generation is tested).
TODO: Identify midi output filepath.
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

# call emotion-music generation
cwd = os.getcwd().split('/')
newdir = cwd.copy()
newdir.remove('control')
newdir.append('midi-emotion')
newdir.append('dev_src')
newdir = '/'.join(cwd)
os.chdir(newdir)

# will be modified
gen_len = 3072
max_input_len = 512
batch_size = 1
max_condition = 0.8
temps = [1.0, 1.0]

for rowIndex in range(num_rows):
    valence, arousal = float(vaDF["Valence"][rowIndex]), float(vaDF["Arousal"][rowIndex])
    # generate command -- will need to modify dynamic generate file to accept and test custom inputs of any size

# identify midi output filepaths

