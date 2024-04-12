from poem_VA_model import*
from VAcalculator import*
import sys
import csv


EMOTION_FILE_PATH = './content/emotionaVA_scaled_dic.csv'         

class poem_to_VA:

    def __init__(self, paragraph, output_file_name = 'VA_output.csv', emotion_data_path = EMOTION_FILE_PATH):
        self.paragraph = paragraph.split("|")
        self.emotion_data_path = emotion_data_path
        self.output_file_name = output_file_name
        self.kept_emotions = []

    def get_sentence_VA(self, poem, progressive = True):
        model = GPT_client()
        my_calc = VAcalculator(poem, self.emotion_data_path)
        kept_emotions= model.detect_emotion(poem, progressive)
        self.kept_emotions = kept_emotions
        if not progressive:
            final_val = my_calc.wrapper(kept_emotions)
            print(kept_emotions)
        if progressive:
            final_val = []
            for sen in kept_emotions:
                sentence_VA = my_calc.wrapper(sen["sentence_emotion"])
                final_val.append(sentence_VA)
        return final_val
    
    def get_VA_per_poem(self, progressive = True):
        poems = self.paragraph
        VA_results = []
        for poem in poems:
            if poem:
                if not progressive:
                    valence, arousal = self.get_sentence_VA(poem, progressive)
                    VA_results.append([valence, arousal])
                if progressive:
                    # valence_array = [VA[0] for VA in self.get_sentence_VA(poem, progressive)]
                    # arousal_array = [VA[1] for VA in self.get_sentence_VA(poem, progressive)]
                    # VA_results = [valence_array, arousal_array]
                    VA_results.append(self.get_sentence_VA(poem, progressive))
        return VA_results
    
    def to_csv(self, VA_results, progressive = True):
        if not progressive:
            self.output_file_name = "Non_progressive_output.csv"
        with open(self.output_file_name, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Poem", "Valence", "Arousal"])
            if not progressive:
                for poem, (valence, arousal) in zip(self.paragraph, VA_results):
                    csvwriter.writerow([poem, valence, arousal])
            if progressive:
                for poem, va_per_poem in zip(self.paragraph, VA_results):
                    valence_array = [va[0] for va in va_per_poem]
                    arousal_array = [va[1] for va in va_per_poem]
                    csvwriter.writerow([poem, valence_array, arousal_array])

    def wrapper(self, progressive = True):
        VA_results = self.get_VA_per_poem(progressive)
        self.to_csv(VA_results, progressive)

if __name__ == "__main__":
#     poems = """What is this life if, full of care,
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
# We have no time to stand and stare.
# | When despair for the world grows in me
# and I wake in the night at the least sound
# in fear of what my life and my children’s lives may be,
# I go and lie down where the wood drake
# rests in his beauty on the water, and the great heron feeds.
# I come into the peace of wild things
# who do not tax their lives with forethought
# of grief. I come into the presence of still water.
# And I feel above me the day-blind stars
# waiting with their light. For a time
# I rest in the grace of the world, and am free.
# | Half a league,
# half a league,
# Half a league onward,
# All in the valley of Death
# Rode the six hundred.
# "Forward, the Light Brigade!
# Charge for the guns!" he said:
# Into the valley of Death
# Rode the six hundred.
# "Forward, the Light Brigade!"
# Was there a man dismay'd?
# Not tho' the soldier knew
# Some one had blunder'd:
# Their's not to make reply,
# Their's not to reason why,
# Their's but to do and die:
# Into the valley of Death
# Rode the six hundred.
# | We are the hollow men
# We are the stuffed men
# Leaning together
# Headpiece filled with straw. Alas!
# Our dried voices, when
# We whisper together
# Are quiet and meaningless
# As wind in dry grass
# Or rats' feet over broken glass
# In our dry cellar
# """
#     poems = """
# O Captain! my Captain! our fearful trip is done,
# The ship has weather'd every rack, the prize we sought is won.
# The port is near, the bells I hear, the people all exulting,
# While follow eyes the steady keel, the vessel grim and daring;
# | I wandered lonely as a cloud
# That floats on high o'er vales and hills,
# When all at once I saw a crowd,
# A host, of golden daffodils;
# Beside the lake, beneath the trees,
# | Once upon a midnight dreary, while I pondered, weak and weary,
# Over many a quaint and curious volume of forgotten lore.
# While I nodded, nearly napping, suddenly there came a tapping,
# As of some one gently rapping, rapping at my chamber door.
# | Nature's first green is gold,
# Her hardest hue to hold.
# Her early leaf's a flower;
# But only so an hour.
# Then leaf subsides to leaf.
# So Eden sank to grief,
# """
#     poems = """
#     Blood red,
# Shing evily,
# Silently laughing at my pain.
# He enjoys it,
# No...He loves it, The pain he makes others feel.
# He does not speak,
# But I know when I feel his eyes piercing mine, 
# He is laughing inside.
# I shiver in fear,
# When his eyes, 
# Come near.
# It is true im scared,
# Of his eyes and him, 
# His eyes tell the things he does not.
# His eyes, 
# Blood red, 
# Tourment me.

# """
#     my_converter = poem_to_VA(poems)
#     my_converter.wrapper(progressive=True)

    