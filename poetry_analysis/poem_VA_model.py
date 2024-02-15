import transformers
transformers.logging.set_verbosity(transformers.logging.ERROR)
from transformers import pipeline


class roberta_model:

    '''
    
    Get the model
    
    '''

    def __init__(self):
        self.classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
    

    '''
    
    Detect and extract main emotions

    '''


    def detect_emotion(self, sentence):
        emotion_detected = self.classifier(sentence)[0]
        return emotion_detected
    
    def get_emotion_list(self, emotion_detected):
        main_emotion = emotion_detected[0]
        kept_emotions = []
        kept_emotions.append(main_emotion)
        for i in range(1, len(emotion_detected)):
            if main_emotion['score'] / emotion_detected[i]['score'] <= 8:
                kept_emotions.append(emotion_detected[i])
        if len(kept_emotions) < 4:
            kept_emotions = emotion_detected[:4]
            
        return kept_emotions #format: [{'lable': 'emotion', 'score': xx}]

    def wrapper(self, sentence):
        emotion_detected = self.detect_emotion(sentence)
        kept_emotions = self.get_emotion_list(emotion_detected)
        return kept_emotions
    

# if __name__ == "__main__":
#     my_model = roberta_model()
#     detected_emotions = my_model.detect_emotion("I am very happy but also angry today.")
#     print("detected: ")
#     print(detected_emotions)
#     kept_emotions = my_model.get_emotion_list(detected_emotions)
#     print("kept: ")
#     print(kept_emotions)