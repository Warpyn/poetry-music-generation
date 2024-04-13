from poem_VA_model import*
import pandas as pd
import os
import math

class VAcalculator:

    def read_emotion_file_to_VA_dic(self, file_path):
        emotion_dataframe = pd.read_csv(file_path)
        emotion_dic = emotion_dataframe.to_dict(orient='records')
        VA_format = {emotion['word']: [emotion['valance'], emotion['arousal']] for emotion in emotion_dic}
        return VA_format


    def __init__(self, emotions, emotion_data_path = './content/emotionaVA_scaled_dic.csv'):
        self.emotion_dic = self.read_emotion_file_to_VA_dic(emotion_data_path)
        self.emotions = emotions
        

    def get_VA_vectors(self, kept_emotions): 
        VA_vectors = []
        for emotion in kept_emotions:
            emo = emotion['emotion']
            if emo in self.emotion_dic:
                VA_vectors.append([self.emotion_dic[emo], emotion['percentage']])
            else:
                VA_vectors.append([self.emotion_dic["neutral"], emotion["percentage"]])
        return VA_vectors #format: [[[v1,a1], percentage1], [[v2,a2], percentage2]...]
    
    def get_VA_sum(self, VA_vectors):
        vector_sum = [0, 0]
        weight_sum = 0
        for vector in VA_vectors:
            vector_sum[0] += vector[0][0] * vector[1]
            vector_sum[1] += vector[0][1] * vector[1]
            weight_sum += vector[1]
        return vector_sum, weight_sum
    
    # def VA_normalize(self, VA_vector_sum):
    #     sum_of_squares = VA_vector_sum[0] ** 2 + VA_vector_sum[1] ** 2
    #     magnitude = math.sqrt(sum_of_squares)
    #     sum_normalized = [VA_vector_sum[0] / magnitude, VA_vector_sum[1] / magnitude]
    #     return sum_normalized

    def VA_weighting(self, VA_vector_sum, weight_sum):
        valence_normalized = VA_vector_sum[0] / weight_sum
        arousal_normalized = VA_vector_sum[1] / weight_sum
        sum_normalized = [round(valence_normalized, 3), round(arousal_normalized, 3)]
        return sum_normalized
            
    
    def wrapper(self, emotions):
        VA_vectors = self.get_VA_vectors(emotions)
        vector_sum, weight_sum = self.get_VA_sum(VA_vectors)
        # sum_normalized = self.VA_normalize(vector_sum)
        sum_normalized = self.VA_weighting(vector_sum, weight_sum)
        return sum_normalized
    

# if __name__ == "__main__":
    
    # #kept_emotions = [{'label': 'joy', 'score': 0.8082323670387268}, {'label': 'anger', 'score': 0.051088836044073105}, {'label': 'annoyance', 'score': 0.03365428373217583}, {'label': 'neutral', 'score': 0.0223822221159935}]
    
    # kept_emotions = [{ "emotion_id": 1, "emotion": "admiration", "percentage": 20 }, { "emotion_id": 2, "emotion": "joy", "percentage": 20 }, { "emotion_id": 3, "emotion": "love", "percentage": 20 }, { "emotion_id": 4, "emotion": "gratitude", "percentage": 15 }, { "emotion_id": 5, "emotion": "excitement", "percentage": 10 }, { "emotion_id": 6, "emotion": "curiosity", "percentage": 10 }, { "emotion_id": 7, "emotion": "optimism", "percentage": 5 }]
    # my_calculator = VAcalculator(kept_emotions)
    # df = my_calculator.read_emotion_file_to_VA_dic('./content/emotionaVA_scaled_dic.csv')
    
    
    
    
    # print(df)
    # # vector = my_calculator.get_VA_vectors(kept_emotions)
    # # print(vector)
    # result = my_calculator.wrapper(kept_emotions)
    # print(result)
