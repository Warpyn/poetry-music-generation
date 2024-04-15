import os
import pandas as pd
import numpy as np

PATH_TO_MUSIC_GENERATIONS_OUTPUT_PATHS = "../midi-emotion/dev_src/generationPaths.txt"
PATH_TO_SOUNDFONT = "../FluidR3_GM_GS.sf2"
PATH_TO_WAV_OUTPUT_DIR = "../wav_output" 

# clear generation paths
with open(PATH_TO_MUSIC_GENERATIONS_OUTPUT_PATHS, "w") as f:
    f.close()

# change directory to necessary source directory

cwd = os.getcwd()
newdir = cwd.split('/')
newdir.remove('scripts-dev')
newdir.append('midi-emotion')
newdir.append('dev_src')
newdir = '/'.join(newdir)
os.chdir(newdir)

# generate command
VAconditions = [(-0.8, -0.8), (0.8, 0.8), (-0.8, -0.8)]
valences = [ i for i, j in VAconditions ]
arousals = [ j for i, j in VAconditions ]
numSentences = len(valences)

gen_len = 3072
max_input_len = 512
batch_size = 1
temps = [1.5, 0.7]
# for each unit = 1 / 2*sentences-1
keep_unchanged = 1.0 / ((2.0*numSentences)-1.0)

# currently using max condition to generate all change conditions
# need to modify generate file to create custom conditions

os.system(f"python dynamic-generate.py --model_dir continuous_concat --conditioning continuous_concat --batch_size {batch_size} --gen_len {gen_len} --max_input_len {max_input_len} --smooth_change --keep_unchanged {keep_unchanged} --temp {temps[0]} {temps[1]} --valence_dynamic {" ".join(valences)} --arousal_dynamic {" ".join(arousals)}")

os.chdir(cwd)
with open(PATH_TO_MUSIC_GENERATIONS_OUTPUT_PATHS, "r") as f:
    midiOutputPaths = f.read().splitlines()
    assert len(midiOutputPaths) > 0, "no midi output paths found"
midiOutputPaths = [path.replace("..", "midi-emotion") for path in midiOutputPaths]

# convert each midi to wav using fluidsynth
for i, midiOutputPath in enumerate(midiOutputPaths):
    assert midiOutputPath[-3:] == "mid", f"{midiOutputPath} is not a path to a midi file"
    if not(os.path.isdir(PATH_TO_WAV_OUTPUT_DIR)):
        os.makedirs(PATH_TO_WAV_OUTPUT_DIR)
    outputFilename = midiOutputPath.split('/')[-1][:-4]
    os.system(f"fluidsynth -F {PATH_TO_WAV_OUTPUT_DIR}/{outputFilename}.wav {PATH_TO_SOUNDFONT} ../{midiOutputPath}")