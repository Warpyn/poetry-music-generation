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

    def get_sentence_VA(self, sentence):
        model = roberta_model()
        my_calc = VAcalculator(sentence, self.emotion_data_path)
        kept_emotions = model.wrapper(sentence)
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



    