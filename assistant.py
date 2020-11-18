import datetime
import webbrowser 
import time

import pyttsx3 
import speech_recognition as sr

print("...")
textSpeech = pyttsx3.init() 

# Sets speed percent  
textSpeech.setProperty('rate', 140) 
# Set volume 0-1 
textSpeech.setProperty('volume', 0.5)

voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
textSpeech.setProperty('voice', voice_id) 
my_text = ''
def tts(text):
    textSpeech.say(text)
    textSpeech.runAndWait() 

speechRec = sr.Recognizer()

def stt():
    with sr.Microphone() as source:
        print("Talk...")
        audio_text = speechRec.listen(source)
        print("Time over, thanks")
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

def tellDay():
    dayOfWeek = datetime.datetime.today().weekday()
    dayDate = datetime.datetime.today().date()
    day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    return f'Today is {day_dict[dayOfWeek]} - {dayDate.day} {dayDate.month}'


def tellTime():
    time = datetime.datetime.now().strftime('%H:%M')  
    return f'It\'s {time}'


##################     

tts('How can I help you madam?')

while(True):
    
    query = stt()  

    if ('tell' or 'which' or 'what') and ('day' or 'today') in query.lower(): 
        print(tellDay())
        tts(tellDay())
        continue
    elif ('what' or 'tell') and 'time' in query.lower():
        print(tellTime())
        tts(tellTime())
        continue
    elif query == 'exit' or 'thanks exit':
        break
    else:
        break    
# TODO: listen only when talking 