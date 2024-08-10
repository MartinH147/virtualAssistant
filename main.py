# credit to https://www.youtube.com/watch?v=OqFI_g8vAoc&t=137s

from datetime import datetime
from logging.config import listen
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import ssl
import os
import subprocess
from googletrans import Translator
import string
import random

# Speech engine initialisation
try:
    engine = pyttsx3.init('dummy')
    print('Engine initialised.')
except ImportError:
    print('Requested driver is not found')
except RuntimeError:
    print('Driver failed to initialize')
except NameError:
    print('Name not defined')
except:
    print('Error')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female
rate = engine.getProperty('rate')
engine.setProperty('rate', rate)
activationWord = 'craig'

# Wolfram Alpha Client
appId = "KXYP3X-E6WW5P97WR"
wolframClient = wolframalpha.Client(appId)
# Disable certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

def speak(text):
    engine.say(text)
    engine.runAndWait()


def search_wikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No wikipedia result')
        return 'No result received'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print('Recognising speech...')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'

    return query

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def search_wolframAlpha(query = ''):
    response = wolframClient.query(query)
    # @success: Wolfram Alpha was able to resolve the query
    # #@numpods: Number of results returned
    # pod: List of results. This can also contain subpods
    if response['@success'] == 'false':
        return 'Could not compute'

    # Query resolved
    else:
        result = ''
        # Question
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]
        # May contain the answer, has the highest confidence value
        # if it's primary, or has the title of result or definition, then it's the official result
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            # Get the result
            result = listOrDict(pod1['subpod'])
            # Remove the bracketed section
            return result.split('(')[0]
        else:
            question = listOrDict(pod0['subpod'])
            # Remove the bracketed section
            return question.split('(')[0]
            # Search wikipedia instead
            print('Computation failed. Querying the universal databank instead...')
            speak('Computation failed. Querying the universal databank instead...')
            search_wikipedia(question)



# Main loop
if __name__ == '__main__':
    print('All systems nominal.')
    speak('All systems nominal.')

    # Get current hour
    now = datetime.now()
    hour = now.strftime("%H")
    hour = int(hour)

    if hour < 12:
        print('Good morning.')
        speak('Good morning.')
    elif hour < 18:
        print('Good afternoon.')
        speak('Good afternoon.')
    else:
        print('Good evening.')
        speak('Good evening.')

    while True:
        # Parse as a list
        query = parseCommand().lower().split()

        if query[0] == activationWord:
            query.pop(0)

            # Navigation
            if query[0] == 'go' and query[1] == 'to':
                print('Opening...')
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.open(f'http://{query}', new=2)

            # Search Google
            if query[0] == 'google':
                query.pop(0)
                search = '+'.join(query)
                print(f'Opening...{search}')
                speak(f'Opening...{search}')
                webbrowser.open(f'https://www.google.com/search?q={search}', new=2)

            # Wikipedia
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                print('Querying the universal databank...')
                speak('Querying the universal databank...')
                print(search_wikipedia(query))
                speak(search_wikipedia(query))

            # Wolfram Alpha
            if query[0] == 'compute':
                query = ' '.join(query[1:])
                print('Computing...')
                speak('Computing...')
                try:
                    result = search_wolframAlpha(query)
                    print(result)
                    speak(result)
                except:
                    print('Unable to compute.')
                    speak('Unable to compute.')

            # Note taking
            if query[0] == 'note':
                print('Ready to record your note...')
                speak('Ready to record your note...')
                newNote = parseCommand().lower()
                now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                with open('note_%s.txt' % now, 'w') as newFile:
                    newFile.write(newNote)
                print('Note written.')
                speak('Note written.')

            # Open Application
            if query[0] == 'open':
                query.pop(0)
                if ' ' in query:
                    app = "\ ".join(query)
                else:
                    app = ' '.join(query)
                print(f'Opening...{app}')
                speak(f'Opening...{app}')
                os.system(f"open /System/Applications/{app}.app")


            # Music Control

            # Pause
            if query[0] == 'pause':
                print('Pausing...')
                speak('Pausing...')
                subprocess.call(['osascript', '-e', 'tell application "Music" to pause'])

            # Play
            if query[0] == 'play':
                print('Playing...')
                speak('Playing...')
                subprocess.call(['osascript', '-e', 'tell application "Music" to play'])


            # Set translate language preference
            if query[0] == 'set' and query[1] == 'language' and query[2] == 'to':
                query = ' '.join(query[3:])
                translator = Translator(dest=f"{query}")

            # Translate
            if query[0] == 'translate':
                query.pop(0)
                text = f'''{query}'''
                translator = Translator()
                # lang = translator.detect(text)
                res = translator.translate(text).text
                translation = "".join(char for char in res if char not in string.punctuation)
                print(translation)
                speak(translation)

            # Thanks
            if query[0] == 'thanks' and query[1] == activationWord:
                print('No problem. Happy to help!')
                speak('No problem. Happy to help!')

            # Motivation
            if query[0] == 'motivation':
                rand = random.randint(1, 4)
                if rand == 1:
                    print("Doubt kills more dreams than failure ever will.")
                    speak("Doubt kills more dreams than failure ever will.")
                elif rand == 2:
                    print("You were born to win, but to be a winner, you must plan to win, prepare to win, and expect to win.")
                    speak("You were born to win, but to be a winner, you must plan to win, prepare to win, and expect to win.")
                elif rand == 3:
                    print("The best way to get started is to quit talking and begin doing.")
                    speak("The best way to get started is to quit talking and begin doing.")
                elif rand == 4:
                    print("Recipe for success: Study while others are sleeping; work while others are loafing; prepare while others are playing; and dream while others are wishing.")
                    speak("Recipe for success: Study while others are sleeping; work while others are loafing; prepare while others are playing; and dream while others are wishing.")
                elif rand == 5:
                    print("")
                    speak("")
                else:
                    print("Nup, you're screwed")
                    speak("Nup, you're screwed")
