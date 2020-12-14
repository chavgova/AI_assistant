import datetime
import webbrowser 
import time
import wikipedia
import pyttsx3 
import speech_recognition as sr
from spotify_local import SpotifyLocal
import numpy as np
import random
from PyDictionary import PyDictionary

dictionary=PyDictionary()
######### EMOTION RECOGNITION
import tensorflow as tf
from tensorflow.keras.models import model_from_json
import librosa
import os
import pandas as pd
import glob 
from librosa import display
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import LabelEncoder

json_file = open(r"C:\Users\ok\Documents\GABRIELA\ASSISTANT\MODELS\model_08_FEMALE_sigmoid_EmoMix.json", 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights(r"C:\Users\ok\Documents\GABRIELA\ASSISTANT\MODELS\Emotion_Voice_Detection_CNN_model_08_FEMALE_sigmoid_EmoMix.h5")
print('=> THE FEMALE MODEL IS LOADED')
######### EMOTION RECOGNITION - end

audio_counter = 0
wav_file = None
speech_emos_list_values = None

print("...")
textSpeech = pyttsx3.init() 

# Sets speed percent  
textSpeech.setProperty('rate', 145) 
# Set volume 0-1 
textSpeech.setProperty('volume', 0.5)

voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
textSpeech.setProperty('voice', voice_id) 
my_text = ''

def tts(text):
    textSpeech.say(text)
    textSpeech.runAndWait() # TODO: stop talking if 'stop'/'shut up' is said -> stopTalking()


speechRec = sr.Recognizer()

def stt():
    with sr.Microphone() as source:
        print("I'm listening...")
        audio_text = speechRec.listen(source)       
        with open(f'your_file_{audio_counter}.wav', 'wb') as file:
            wav_file = audio_text.get_wav_data()
            file.write(wav_file)
        print("...")
    # recognize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            my_text = speechRec.recognize_google(audio_text)
            print("Text: " + my_text)            
            #tts('You just said: ' + my_text) 
            return my_text
        except:
            print("I did not get that, sir")
            tts("I did not get that sir")
            exit()   # TODO: think of something better -> retry?


def extractFeatures(my_file, **kwargs):
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
    X, sample_rate = librosa.core.load(my_file)
    if chroma or contrast:
        stft = np.abs(librosa.stft(X))
    result = np.array([])
    if mfcc:
        mfccs = np.mean(librosa.feature.mfcc(y = X, sr = sample_rate, n_mfcc = 40).T, axis = 0)
        result = np.hstack((result, mfccs))  # 40 values 
    if chroma:
        chroma = np.mean(librosa.feature.chroma_stft(S = stft, sr = sample_rate).T,axis = 0)
        result = np.hstack((result, chroma))  # 12 values 
    if mel:
        mel = np.mean(librosa.feature.melspectrogram(X, sr = sample_rate).T,axis = 0)
        result = np.hstack((result, mel))  # 128 values 
    if contrast:
        contrast = np.mean(librosa.feature.spectral_contrast(S = stft, sr = sample_rate).T,axis = 0)
        result = np.hstack((result, contrast)) # 7 values 
    if tonnetz:
        tonnetz = np.mean(librosa.feature.tonnetz(y = librosa.effects.harmonic(X), sr = sample_rate).T,axis = 0)
        result = np.hstack((result, tonnetz)) # 6 values 

    return result

def emoRec():
    X, sample_rate = librosa.load(f'your_file_{audio_counter}.wav', res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
    sample_rate = np.array(sample_rate)

    demo_file = os.fspath(f'your_file_{audio_counter}.wav')
    features_live  = extractFeatures(demo_file, mel = True, mfcc = True, contrast = True, chroma = True, tonnetz = True)
    features_live = pd.DataFrame(data = features_live)
    features_live = features_live.stack().to_frame().T

    lb = LabelBinarizer()
    features_live_2d = np.expand_dims(features_live, axis = 2)
    live_preds = loaded_model.predict(features_live_2d, batch_size = 32, verbose = 1)
    speech_emos_list_values = live_preds
    print(live_preds)
    #lb.fit(live_preds)
    all = np.argsort(-live_preds, axis = 1)[:, :8]
    for i in all:
        print((lb.inverse_transform((i))))
    best_n = np.argsort(-live_preds)[:, :3] # best_n = [* * *]

    first_second = 0
    second_third = 0

    for n in best_n:
        k = n
        num = 1
        for k in n:   
            if num == 1: first_second = live_preds[0][k] / live_preds[0][n][1]  
            elif num == 2: second_third = live_preds[0][k] / live_preds[0][n][2]
            num += 1

    for i in best_n:
        print((lb.inverse_transform((i))))

    print()
    print('First/Second:')
    print(first_second)
    print('Second/Third:')
    print(second_third)    

def stopTalking():  #### 
    return ''

def tellDay():
    dayOfWeek = datetime.datetime.today().weekday()
    dayDate = datetime.datetime.today().date()
    day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    return f'Today is {day_dict[dayOfWeek]} - {dayDate.day} {dayDate.month}'


def tellTime():
    time = datetime.datetime.now().strftime('%H:%M')  
    return f'It\'s {time}'

def takeNote():
        file = open('aiNotes.txt', 'a+')
        tts('What should I write?')
        note = stt()
        tts("What about a title?")
        ans = stt()
        if ans == 'no':
            d = datetime.datetime.now()
            file.write(d.strftime('\r\n' + '%d-%b-%Y | %I:%M %p') + '\n--> ' + note)
            tts('Done!')
        else:
            file.write(datetime.datetime.now().strftime('\r\n' + '%d-%b-%Y | %I:%M %p') + f' < {ans.upper()} > \n--> ' + note)   
            tts('Done!') 
        file.close()    

def guessTheNumberGame():
    theNum = int(random.randint(0,100))
    print('----> GUESS THE NUMBER GAME <----')
    print(theNum)
    tts('Guess the number between 0 and 100! You have 5 chances! Go!')
    chance = 0
    query = stt()
    while query != 'exit game' and chance < 5:        
        try: 
            guess = int(query)
            chance += 1
            print(chance)
            if chance == 5:
                tts('Well, That was your last chance and you lost!')
                tts(f'The number is {theNum}.')
                break
            if guess == theNum:
                tts(f"That's it! You guessed it after {chance} chances!")
                break
            elif guess > theNum:
                tts('go lower')
            elif guess < theNum:
                tts('go higher') 
        except: 
            tts('This is not a number.')  
        query = stt()   
        

# TODO: clearNote()?
# TODO: newNote()?
# TODO: to-do list - 'add to my Todo list ....', 'whats on my todo list', Deadlines and reminders 
# TODO: translate words - print (dictionary.translate("life",'es'))








###############################################################################################################     

tts('How can I help you madam?')

while(True):
    
    query = stt() 
    #emoRec() 
    audio_counter += 1


    if ('tell' or 'which' or 'what') and ('day' or 'today') in query.lower(): 
        print(tellDay())
        tts(tellDay())
        continue

    elif ('what' or 'tell') and 'time' in query.lower():
        print(tellTime())
        tts(tellTime())
        continue

    elif 'Wikipedia' in query:
        query = query.replace('wikipedia', '')
        query = query.replace('according', '')
        results = wikipedia.summary(query, sentences = 3) # too long?
        print(results)
        tts('According to wikipedia: ' + results)   
        continue

    elif ('take' or 'make') and 'note' in query.lower():
        takeNote()
        continue

    elif 'play' and 'guess the number game' in query.lower():
        guessTheNumberGame()
        print('--- end ---')
        continue

    elif (('tell me' or 'give me') and "number") in query.lower():
        start_index = query.find('between')
        end_index = start_index + len('between')
        if start_index == -1:
            tts(str(random.randint(1,101)))
        else:
            rangeRandom = query[end_index+1:].split(' ')
            a,b = int(rangeRandom[0]), int(rangeRandom[2])
            tts(str(random.randint(a, b)))
        continue

    elif (('tell' or 'give' or 'what') and 'synonym') in query.lower():
        word = query.replace('tell', '')
        word = word.replace('give', '')
        word = word.replace('me', '')
        word = word.replace('a', '')
        word = word.replace('the', '')
        word = word.replace('word', '')
        word = word.replace('of', '')
        word = word.replace('synonym', '')
        word = word.replace('what', '')
        word = word.replace("what's", '')
        word = word.replace('is', '')
        word = word.strip()
        one, two = dictionary.synonym(word)[:2]
        print(f'Synonyms of {word} are {one} and {two}.')
        tts(f'Synonyms of {word} are {one} and {two}.')

    elif (('tell' or 'give' or 'what') and 'antonym') in query.lower():
        word = query.replace('tell', '')
        word = word.replace('give', '')
        word = word.replace('me', '')
        word = word.replace('a', '')
        word = word.replace('the', '')
        word = word.replace('word', '')
        word = word.replace('of', '')
        word = word.replace('antonym', '')
        word = word.replace('what', '')
        word = word.replace("what's", '')
        word = word.replace('is', '')
        word = word.strip()
        one, two = dictionary.antonym(word)[:2]
        print(f'Antonyms of {word} are {one} and {two}.')
        tts(f'Antonyms of {word} are {one} and {two}.')    

    elif (('tell' or 'give' or 'what') and 'meaning') in query.lower():
        word = query.replace('tell', '')
        word = word.replace('give', '')
        word = word.replace('me', '')
        word = word.replace('a', '')
        word = word.replace('the', '')
        word = word.replace('word', '')
        word = word.replace('of', '')
        word = word.replace('meaning', '')
        word = word.replace('what', '')
        word = word.replace("what's", '')
        word = word.replace('is', '')
        word = word.strip()
        print(dictionary.meaning(word).values())
        meaning, *_ = dictionary.meaning(word).values()
        print(f'The meaning of {word} is {meaning[0]} or {meaning[1]}.')
        tts(f'The meaning of {word} is {meaning[0]} or {meaning[1]}.')   

    elif query == 'exit' or 'thanks exit':
            tts('Okay then, goodbye')
            break    

    else:
        break    




# TODO: listen only when talking / wake up word
# TODO: check wifi network ? 
# TODO: guide - ask it what it can do/how it works -> a speech explaining what functionalities there are
# TODO: tell weather 
       