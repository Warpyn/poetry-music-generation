from poem_VA_model import*
from VAcalculator import*
import sys
import csv


EMOTION_FILE_PATH = './content/emotionVAScaled.csv'         

class poem_to_VA:

    def __init__(self, paragraph, output_file_name = 'VA_output.csv', emotion_data_path = EMOTION_FILE_PATH):
        self.paragraph = paragraph.split("|")
        self.emotion_data_path = emotion_data_path
        self.output_file_name = output_file_name
        self.kept_emotions = []

    def get_sentence_VA(self, sentence):
        model = GPT_client()
        my_calc = VAcalculator(sentence, self.emotion_data_path)
        kept_emotions = model.detect_emotion(sentence)
        self.kept_emotions = kept_emotions
        final_vet = my_calc.wrapper(kept_emotions)
        return final_vet
    
    def get_VA_per_sentence(self):
        sentences = self.paragraph
        VA_results = []
        for sentence in sentences:
            if sentence:
                valence, arousal = self.get_sentence_VA(sentence)
                VA_results.append([valence, arousal])
        return VA_results
    
    def to_csv(self, VA_results):
        with open(self.output_file_name, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Sentence", "Valence", "Arousal"])
            for sentence, (valence, arousal) in zip(self.paragraph, VA_results):
                csvwriter.writerow([sentence, valence, arousal])

    def wrapper(self):
        VA_results = self.get_VA_per_sentence()
        self.to_csv(VA_results)

# if __name__ == "__main__":
#     poems = """Your laughter, 
#       a blossoming bud, 
#       eyes like peacock, 
#       vivacious, sweet your laughter, 
#       what are the feelings, 
#       on your faces, 
#       your laughter, 
#       like a melodious rain, 
#       creates sensations in the heart, 
#       your laughter
#       benumbs the eyes
#       i pray, 

#       you carry on laughing | We left that old ungainly house
# When my dog died there, after
# The burial, after the rose
# Flowered twice, pulling it by its
# Roots and carting it with our books,
# Clothes and chairs in a hurry.
# We live in a new house now,
# And, the roofs do not leak, but, when
# It rains here, I see the rain drench
# That empty house, I hear it fall
# Where my puppy now lies,
# Alone..
# """
#     my_converter = poem_to_VA(poems)
#     my_converter.wrapper()

    