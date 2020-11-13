import datetime
import webbrowser 
import time
#from chatbot import demo
#demo()

print("heyy")

import speech_recognition as sr
speechRec = sr.Recognizer()

with sr.Microphone() as source:
    print("Talk")
    audio_text = speechRec.listen(source)
    print("Time over, thanks")
# recognize_() method will throw a request error if the API is unreachable, hence using exception handling
    
    try:
        print("Text: " + speechRec.recognize_google(audio_text))
    except:
         print("Sorry, I did not get that")
         
"""

import tensorflow as tf
from keras.models import model_from_json

json_file = open('/content/drive/My Drive/My_AI/MY MODELS/model_08_FEMALE_sigmoid_EmoMix.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("/content/drive/My Drive/My_AI/MY MODELS/Emotion_Voice_Detection_CNN_model_08_FEMALE_sigmoid_EmoMix.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
opt = tf.keras.optimizers.Adam(learning_rate=0.0001) ###
loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
#score = loaded_model.evaluate(x_testcnn, y_test, verbose=0)
#print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))



def command():
    # voice command 
    return 0;
    

def say():
    # speech
    return 0;

def tellDay():
    dayOfWeek = datetime.datetime.today().weekday()
    dayDate = datetime.datetime.today().date()
    day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    return f'Today is {day_dict[dayOfWeek]} - {dayDate.day} {dayDate.month}'


def tellTime():
    time = str(datetime.datetime.now())  # there must be something better 
    return f'It\'s {time.hour} {time.minutes}'


while(True):
    query = input() # command()

    if 'tell' or 'which' or 'what' and 'day' or 'today' in query.lower(): 
        print(tellDay())
        break # continue
    elif 'what' or 'tell' and 'time' in query.lower():
        print(tellTime())
        break # continue
    elif query == 'exit':
        break
    else:
        break    
"""
import pyttsx3 

converter = pyttsx3.init() 

# Sets speed percent  
converter.setProperty('rate', 140) 
# Set volume 0-1 
converter.setProperty('volume', 0.5)

voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
converter.setProperty('voice', voice_id) 

converter.say('Gabi, go to work already!')
converter.runAndWait() 
"""
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)
   print(voice.id)
   engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()

"""
