from poem_VA_model import*
from VAcalculator import*
import os
import sys
import csv

EMOTION_FILE_PATH = os.path.dirname(__file__)+'/content/emotionaVA_scaled_dic.csv'         

class poem_to_VA:

    def __init__(self, paragraph, output_file_name = 'VA_output.csv', emotion_data_path = EMOTION_FILE_PATH):
        self.paragraph = paragraph.split("|")
        self.emotion_data_path = emotion_data_path
        self.output_file_name = output_file_name
        self.kept_emotions = []

    def get_sentence_VA(self, poem, progressive = 2):
        model = GPT_client()
        my_calc = VAcalculator(poem, self.emotion_data_path)
        kept_emotions= model.detect_emotion(poem, progressive)
        self.kept_emotions = kept_emotions
        if progressive == 0:
            final_val = my_calc.wrapper(kept_emotions)
            # print(kept_emotions)
        if progressive > 0:
            final_val = []
            for sen in kept_emotions:
                sentence_VA = my_calc.wrapper(sen["sentence_emotion"])
                final_val.append(sentence_VA)
        return final_val
    
    def get_VA_per_poem(self, progressive = 2):
        poems = self.paragraph
        VA_results = []
        for poem in poems:
            if poem:
                if progressive == 0:
                    valence, arousal = self.get_sentence_VA(poem, progressive)
                    VA_results.append([valence, arousal])
                if progressive > 0:
                    VA_results.append(self.get_sentence_VA(poem, progressive))
        return VA_results
    
    def to_csv(self, VA_results, progressive = 2):
        if progressive == 0:
            self.output_file_name = "Non_progressive_output.csv"
        elif progressive == 1:
            self.output_file_name = "Non_sliding_window_progressive_output.csv"
        with open(os.path.dirname(__file__)+'/'+self.output_file_name, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Poem", "Valence", "Arousal"])
            if progressive == 0:
                for poem, (valence, arousal) in zip(self.paragraph, VA_results):
                    csvwriter.writerow([poem, valence, arousal])
            if progressive > 0:
                for poem, va_per_poem in zip(self.paragraph, VA_results):
                    valence_array = [va[0] for va in va_per_poem]
                    arousal_array = [va[1] for va in va_per_poem]
                    csvwriter.writerow([poem, valence_array, arousal_array])

    def wrapper(self, progressive = 2):
        VA_results = self.get_VA_per_poem(progressive)
        self.to_csv(VA_results, progressive)

if __name__ == "__main__":
#     poems = """When despair for the world grows in me
# and I wake in the night at the least sound
# in fear of what my life and my children’s lives may be,
# I go and lie down where the wood drake
# rests in his beauty on the water, and the great heron feeds.
# I come into the peace of wild things
# who do not tax their lives with forethought of grief.
# I come into the presence of still water.
# And I feel above me the day-blind stars
# waiting with their light. For a time
# I rest in the grace of the world, and am free. |
# What is this life if, full of care,
# We have no time to stand and stare.

# No time to stand beneath the boughs
# And stare as long as sheep or cows.

# No time to see, when woods we pass,
# Where squirrels hide their nuts in grass.

# No time to see, in broad daylight,
# Streams full of stars, like skies at night.

# No time to turn at Beauty's glance,
# And watch her feet, how they can dance.

# No time to wait till her mouth can
# Enrich that smile her eyes began.

# A poor life this if, full of care,
# We have no time to stand and stare. | 

# Nature's first green is gold,

# Her hardest hue to hold.

# Her early leaf's a flower;

# But only so an hour.

# Then leaf subsides to leaf.

# So Eden sank to grief,

# So dawn goes down to day.

# Nothing gold can stay. | 

# We are the hollow men
# We are the stuffed men

# Leaning together

# Headpiece filled with straw. Alas!

# Our dried voices, when

# We whisper together

# Are quiet and meaningless

# As wind in dry grass

# Or rats' feet over broken glass

# In our dry cellar | 

# I wandered lonely as a cloud
# That floats on high o'er vales and hills,
# When all at once I saw a crowd,
# A host, of golden daffodils;
# Beside the lake, beneath the trees,


# """
    poems = """
What is this life if, full of care,
We have no time to stand and stare.

No time to stand beneath the boughs
And stare as long as sheep or cows.

No time to see, when woods we pass,
Where squirrels hide their nuts in grass.

No time to see, in broad daylight,
Streams full of stars, like skies at night.

No time to turn at Beauty's glance,
And watch her feet, how they can dance.

No time to wait till her mouth can
Enrich that smile her eyes began.

A poor life this if, full of care,
We have no time to stand and stare. |

When despair for the world grows in me
and I wake in the night at the least sound
in fear of what my life and my children's lives may be,
I go and lie down where the wood drake
rests in his beauty on the water, and the great heron feeds.
I come into the peace of wild things
who do not tax their lives with forethought
of grief. I come into the presence of still water.
And I feel above me the day-blind stars
waiting with their light. For a time
I rest in the grace of the world, and am free. 



"""
    my_converter = poem_to_VA(poems)
    my_converter.wrapper(progressive = 2)

    