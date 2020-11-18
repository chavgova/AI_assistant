import datetime
import webbrowser 
import time
import wikipedia
import pyttsx3 
import speech_recognition as sr
from spotify_local import SpotifyLocal

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
    textSpeech.runAndWait() # TODO: stop talking if 'stop'/'shut up' is said -> stopTalking()


speechRec = sr.Recognizer()

def stt():
    with sr.Microphone() as source:
        print("I'm listening...")
        audio_text = speechRec.listen(source)
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

    elif 'Wikipedia' in query:
        query = query.replace('wikipedia', '')
        results = wikipedia.summary(query, sentences = 3) # too long?
        print(results)
        tts('According to wikipedia: ' + results)   
        continue
    elif ('take' or 'make') and 'note' in query:
        takeNote()
        continue
      
    elif query == 'exit' or 'thanks exit':
            tts('Okay then, goodbye')
            break

    else:
        break    


# TODO: listen only when talking 
# TODO: check wifi network ? 