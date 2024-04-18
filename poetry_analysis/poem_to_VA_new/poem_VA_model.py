from openai import OpenAI
import os
import json


class GPT_client:

    '''
    
    Get a client
    
    '''

    def __init__(self):
        cur_path = os.path.dirname(__file__)
        apiKeyPath = os.path.join(cur_path, "apiKey.txt")
        with open(apiKeyPath, "r") as f:
            apiKey = f.read().rstrip()
        self.classifier = OpenAI(api_key=apiKey)
        #self.emotion_list = "admiration, amusement, anger, annoyance, approval, caring, confusion, curiosity, desire, disappointment, disapproval, disgust, embarrassment, excitement, fear, gratitude, grief, joy, love, nervousness, optimism, pride, realization, relief, remorse, sadness, surprise, neutral"
        self.emotion_list = f"""happy, amazed, dazzled, allured, moved, 
        inspired, transcendence, spirituality, thrill, love, 
        affectionate, sensual, tender, softened, sentimental, 
        dreamy, nostalgic, melancholic, calm, relaxed, 
        serene, soothed, meditative, energetic, triumphant, 
        fiery, strong, heroic, stimulated, joyful, 
        animated, dancing, amused, agitated, nervous, 
        tense, impatient, irritated, sad, sorrowful"""


    '''
    
    Utility function
    
    '''

    def extract_sentences(self, poem):
        poem = poem.replace('\n', ' ')
        sentences = poem.split('.')
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        return sentences

    def sliding_window(self, poem):
        poem = poem.replace("\n", " ")
        words = poem.split()

        window_size = len(words)//5 if len(words) > 40 else len(words)//3
        step = window_size // 2

        segments = []
        current = 0

        while current + window_size < len(words):
            segments.append(' '.join(words[current:current + window_size]))
            current += step

        if current < len(words):
            segments.append(' '.join(words[current:]))
        
        return segments



    '''
    
    Detect and extract main emotions

    '''

    def get_completion(self, prompt, model="gpt-4-turbo-preview"):
        messages = [{"role": "user", "content": prompt}]
        response = self.classifier.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )
        return response.choices[0].message

    def detect_emotion(self, poem, progressive = 2, prompt = None):
        example_non_progressive = '[{"key":value}, {"key":value}]'
        example_progressive = '[{sentence_id:vale}, {sentence:sentence}, {sentence_emotion:{key:value}, {key:value}}]'
        if not prompt: 
            if progressive == 0:
                prompt = f"""For the poem delimited by triple backticks,\
                give me a list of six to eight emotions that the poem is\
                expressing, with each emotion labeled with its percentage.\
                The emotion should be based on the whole piece instead of \
                segments of the piece. Be careful for any twist or turning point \
                All emotion must be selected from the list delimited by\
                square bracket. \
                Provode them with JSON format with the following keys and with out anyother characters:
                "emotion_id", "emotion", "percentage"
                [{self.emotion_list}]
                ```{poem}```
                The output should be like a json file and should not contain any\
                charater to organize how the answer is displayed. Do not include\
                anything like "\n" or "```" or "json". The final list whould be a \
                whole json list like {example_non_progressive} instead of several seperated json list\
                """ 
            if progressive == 1:
                sentenceArray = self.extract_sentences(poem)
                prompt = f"""Based on the poem delimited by triple backticks,\
                for each sentence in the sentence array delimited in single backticks,\
                give me a list of three to five emotions that that sentence is\
                expressing, with each emotion labeled with its percentage.\
                When considering what emotions are expressed, please\
                consider it in the context of the whole poem.\
                the output should be a list containing several lists\
                All emotion must be selected from the list delimited by\
                square bracket. \
                Provode the result with JSON format with the following keys and with out anyother characters.\
                For the large list, the keys are:\
                "sentence_id", "sentence", "sentence_emotion"\
                For the sublists, the keys are:\
                "emotion_id", "emotion", "percentage"\
                ```{poem}```
                `{sentenceArray}`
                [{self.emotion_list}]
                The output should be like a json file and should not contain any\
                charater to organize how the answer is displayed. Do not include\
                anything like "\n" or "```" or "json". The final list whould be a \
                whole json list like {example_progressive}\
                """
            if progressive == 2:
                segmentArray = self.sliding_window(poem)
                prompt = f"""Based on the poem delimited by triple backticks,\
                for each segment in the sentence array delimited in single backticks,\
                give me a list of three to five emotions that that segment is\
                expressing, with each emotion labeled with its percentage.\
                When considering what emotions are expressed, please\
                consider it in the context of the whole poem.\
                the output should be a list containing several lists\
                All emotion must be selected from the list delimited by\
                square bracket. \
                Provode the result with JSON format with the following keys and with out anyother characters.\
                For the large list, the keys are:\
                "sentence_id", "sentence", "sentence_emotion"\
                For the sublists, the keys are:\
                "emotion_id", "emotion", "percentage"\
                ```{poem}```
                `{segmentArray}`
                [{self.emotion_list}]
                The output should be like a json file and should not contain any\
                charater to organize how the answer is displayed. Do not include\
                anything like "\n" or "```" or "json". The final list whould be a \
                whole json list like {example_progressive}\
                """

        response = self.get_completion(prompt)
        response.content = response.content.replace("```","").replace("```json", "")
        kept_emotions = json.loads(response.content)
        return kept_emotions

    # def wrapper(self, sentence):
    #     emotion_detected = self.detect_emotion(sentence)
    #     kept_emotions = self.get_emotion_list(emotion_detected)
    #     return kept_emotions
    

# if __name__ == "__main__":
#     my_model = GPT_client()
#     poem1 = """We left that old ungainly house
# #         When my dog died there, after
# #         The burial, after the rose
# #         Flowered twice, pulling it by its
# #         Roots and carting it with our books,
# #         Clothes and chairs in a hurry.
# #         We live in a new house now,
# #         And, the roofs do not leak, but, when
# #         It rains here, I see the rain drench
# #         That empty house, I hear it fall
# #         Where my puppy now lies,
# #         Alone."""
#     detected_emotions, if_progressive = my_model.detect_emotion(poem1)
#     print(detected_emotions)
#     poem2 = """
#         We left that old ungainly house
#         When my dog died there, after
#         The burial, after the rose
#         Flowered twice, pulling it by its
#         Roots and carting it with our books,
#         Clothes and chairs in a hurry.
#         We live in a new house now,
#         And, the roofs do not leak, but, when
#         It rains here, I see the rain drench
#         That empty house, I hear it fall
#         Where my puppy now lies,
#         Alone..
#     """
#     poem3 = """
#     Thanks for believing in me.
#     Thanks for showing me you care.
#     Thanks for holding my hand
#     Thanks for being there.
#     Thanks for being the best
#     Thanks for making me glad
#     Thanks for loving me with all your heart.
#     Thanks for being my dad.
#     Now after every 'thanks for' add never.
# """
#     poem4 = """
#     Two people are walking through a bare, cold wood;
# the moon keeps pace with them and draws their gaze.
# The moon moves along above tall oak trees,
# there is no wisp of cloud to obscure the radiance
# to which the black, jagged tips reach up.
# A woman's voice speaks:
# I am carrying a child, and not by you.
# I am walking here with you in a state of sin.
# I have offended grievously against myself.
# I despaired of happiness,
# and yet I still felt a grievous longing
# for life's fullness, for a mother's joys
# and duties; and so I sinned,
# and so I yielded, shuddering, my sex
# to the embrace of a stranger,
# and even thought myself blessed.
# Now life has taken its revenge,
# and I have met you, met you.
# She walks on, stumbling.
# She looks up; the moon keeps pace.
# Her dark gaze drowns in light.
# A man's voice speaks:
# Do not let the child you have conceived
# be a burden on your soul.
# Look, how brightly the universe shines!
# Splendour falls on everything around,
# you are voyaging with me on a cold sea,
# but there is the glow of an inner warmth
# from you in me, from me in you.
# That warmth will transfigure the stranger's child,
# and you bear it me, begot by me.
# You have transfused me with splendour,
# you have made a child of me.
# He puts an arm about her strong hips.
# Their breath embraces in the air.
# Two people walk on through the high, bright night.
# """
#     poem = """Who rides, so late, through night and wind?
# It is the father with his child.
# He has the boy well in his arm,
# He holds him safely, he keeps him warm.

# My son, why do you hide your face in fear?
# Father, do you not see the Erl-King?
# The Erl-King with crown and cape?
# My son, it is a streak of fog.

# "You dear child, come, go with me!
# (Very) beautiful games, I play with you;
# Many colourful flowers are on the beach,
# My mother has many a golden robe."

# My father, my father, and do you not hear
# What the Erl-King quietly promises me?
# Be calm, stay calm, my child;
# Through dry leaves, the wind is sighing.

# "Do you, fine boy, want to go with me?
# My daughters shall wait on you finely;
# My daughters lead the nightly dance,
# And rock and dance and sing to bring you in."

# My father, my father, and don't you see there
# The Erl-King's daughters in the gloomy place?
# My son, my son, I see it clearly:
# There shimmer the old willows so grey.

# "I love you, your beautiful form excites me;
# And if you're not willing, then I will use force."
# My father, my father, he's touching me now!
# The Erl-King has done me harm!

# It horrifies the father; he swiftly rides on,
# He holds the moaning child in his arms,
# Reaches the farm with great difficulty;
# In his arms, the child was dead."""
#     poem5 = """
#     Aggression

# Ours is a silence
# that waits. Endlessly waits.

# And then, unable to bear it
# any further, it breaks into wails.

# But not all suppressed reactions
# end in our bemoaning the tragedy.

# Sometimes,
# the outward signals
# of inward struggles takes colossal forms
# And the revolution happens because our dreams explode.
# """
#     poem6 = """
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

#     """
#     poem7 = """
# At last I find a meaning of soul's birth
# Into this universe terrible and sweet,
# I who have felt the hungry heart of earth
# Aspiring beyond heaven to Krishna's feet.
# I have seen the beauty of immortal eyes,
# And heard the passion of the Lover's flute,
# And known a deathless ecstasy's surprise
# And sorrow in my heart for ever mute.
# Nearer apd nearer now the music draws,
# Life shudders with a strange felicity;
# All Nature is a wide enamoured pause
# Hoping her lord to touch, to clasp, to be.
# For this one moment lived the ages past;
# The world now throbs fulfilled in me at last""" 
#     detected_emotions = my_model.detect_emotion(poem7)
#     print("detected: ")
#     print(detected_emotions)
    # kept_emotions = my_model.get_emotion_list(detected_emotions)
    # print("kept: ")
    # print(kept_emotions)