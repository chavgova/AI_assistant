

#from chatbot import demo
#demo()



import tensorflow as tf
from keras.models import model_from_json

json_file = open("C:\Users\ok\Google Drive\My_AI\MY MODELS/model_08_FEMALE_sigmoid_EmoMix.json", 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("C:\Users\ok\Google Drive\My_AI\MY MODELS/Emotion_Voice_Detection_CNN_model_08_FEMALE_sigmoid_EmoMix.h5")
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

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)
   print(voice.id)
   engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()

# FIXME: spotify
from spotify_local import SpotifyLocal
    elif 'Spotify' in query:
        with SpotifyLocal() as s:
            s.playURI('spotify:playlist:3UoyI0Wog0JH30Up4GeLBC')
        continue






    if ('stop' or 'shut up') in stt():
        textSpeech.close()
        #stopTalking()