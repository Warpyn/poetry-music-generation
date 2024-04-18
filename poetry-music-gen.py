"""
Full workflow of poetry text to generated MIDI.

Different poems are separated by "|".
Dynamic generation is split by either by sentence using a "." as a delimiter, or using a sliding window.
"""

import argparse
import os
import json
import pandas as pd

parser = argparse.ArgumentParser(description="Convert poetry as text to music as MIDI.")
parser.add_argument('-f', '--filepath', action='store_true', help='whether or given input is a filepath to a text file')
parser.add_argument('input', type=str, help='The input (a filepath to a text file or line of text)')
parser.add_argument('--gen_type', choices=['static', 'sentences', 'windowed'], required=True)
args = parser.parse_args()

PATH_TO_POETRY_EMOTION_SCRIPT = "./poetry_analysis/poem_to_VA_new/main.py"
PATH_TO_POETRY_STATIC_EMOTION_OUTPUT = "./poetry_analysis/poem_to_VA_new/Non_progressive_output.csv"
PATH_TO_POETRY_DYNAMIC_EMOTION_OUTPUT = "./poetry_analysis/poem_to_VA_new/VA_output.csv"
PATH_TO_MUSIC_GENERATIONS_OUTPUT_PATHS = "./midi-emotion/dev_src/generationPaths.txt"
PATH_TO_SOUNDFONT = "./FluidR3_GM_GS.sf2"
PATH_TO_WAV_OUTPUT_DIR = "./wav_output" 

# clears output paths text file
with open(PATH_TO_MUSIC_GENERATIONS_OUTPUT_PATHS, "w") as f:
    f.close()

# read input poetry
if args.filepath:
    assert args.input[-3:] == "txt", f"Input file {args.input} is not a txt file"
    with open(args.input, 'r') as f:
        poetryInput = f.read()
else:
    poetryInput = args.input

# call poetry-emotion conversion
generationTypeCodeDict = {"static": 0, "sentences": 1, "windowed": 2}
generationTypeCode = generationTypeCodeDict[args.gen_type]
poems = poetryInput.split('|')
numPoems = len(poems)
os.system(f'python {PATH_TO_POETRY_EMOTION_SCRIPT} "{poetryInput}" {generationTypeCode}')

# read poetry-emotion csv output
vaDF = pd.read_csv(PATH_TO_POETRY_DYNAMIC_EMOTION_OUTPUT if generationTypeCode != 0 else PATH_TO_POETRY_STATIC_EMOTION_OUTPUT) 
num_rows, _ = vaDF.shape
assert num_rows == numPoems, "unexpected output length for poetry analysis"

# call emotion-music generation
cwd = os.getcwd()
newdir = cwd.split('/')
newdir.append('midi-emotion')
newdir.append('dev_src')
newdir = '/'.join(newdir)
os.chdir(newdir)

gen_len = 3072
max_input_len = 512
batch_size = 1
temps = [1.5, 0.7]

if generationTypeCode != 0:
    
    # dynamic emotion generation
    for rowIndex in range(num_rows):
        
        valences = json.loads(vaDF["Valence"][rowIndex])
        arousals = json.loads(vaDF["Arousal"][rowIndex])

        numEmotionStates = len(valences)
        keep_unchanged = 1.0 / ((2.0*numEmotionStates)-1.0)

        valencesStr = " ".join([str(v) for v in valences])
        arousalsStr = " ".join([str(a) for a in arousals])

        os.system(f"python dynamic-generate.py --model_dir continuous_concat --conditioning continuous_concat --batch_size {batch_size} --gen_len {gen_len} --max_input_len {max_input_len} --smooth_change --keep_unchanged {keep_unchanged} --temp {temps[0]} {temps[1]} --valence_dynamic {valencesStr} --arousal_dynamic {arousalsStr}")

else:
    
    # static emotion generation
    for rowIndex in range(num_rows):
        valence, arousal = float(vaDF["Valence"][rowIndex]), float(vaDF["Arousal"][rowIndex])
        arousal = -0.2 if arousal == 0 else arousal
        arousal = 0.2 * arousal/abs(arousal) if abs(arousal) < 0.2 else arousal
        os.system(f"python generate.py --model_dir continuous_concat --conditioning continuous_concat --valence {valence} --arousal {arousal} --batch_size {batch_size} --gen_len {gen_len} --max_input_len {max_input_len}")

# identify midi output filepaths
os.chdir(cwd)
with open(PATH_TO_MUSIC_GENERATIONS_OUTPUT_PATHS, "r") as f:
    midiOutputPaths = f.read().splitlines()
    assert len(midiOutputPaths) > 0, "no midi output paths found"
    assert len(midiOutputPaths) == numPoems, f"{len(midiOutputPaths)} midi files generated for {numPoems} poems" 
midiOutputPaths = [path.replace("..", "midi-emotion") for path in midiOutputPaths]

# convert each midi to wav using fluidsynth
for i, midiOutputPath in enumerate(midiOutputPaths):
    assert midiOutputPath[-3:] == "mid", f"{midiOutputPath} is not a path to a midi file"
    if not(os.path.isdir(PATH_TO_WAV_OUTPUT_DIR)):
        os.makedirs(PATH_TO_WAV_OUTPUT_DIR)
    respectivePoemStr = poems[i].rstrip().lstrip().replace('\n','').replace(' ','').replace('!','').replace("'","").replace('"','')
    outputFilename = respectivePoemStr[:20] if len(respectivePoemStr) > 20 else respectivePoemStr
    os.system(f"fluidsynth -F {PATH_TO_WAV_OUTPUT_DIR}/{outputFilename}.wav {PATH_TO_SOUNDFONT} {midiOutputPath}")