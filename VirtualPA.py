import speech_recognition as sr
import playsound  # to play saved mp3 file
from gtts import gTTS  # google text to speech
import os  # to save/open files
import wolframalpha  # to calculate strings into formula
from selenium import webdriver  # to control browser operations
import time
import pyjokes  # imports jokes
import requests  # requests api for weather

num = 1


def assistant_speaks(output):
    global num

    # num to rename every audio file
    # with different name to remove ambiguity
    num += 1
    print("PerSon : ", output)

    toSpeak = gTTS(text=output, lang='en', slow=False)
    # saving the audio file given by google text to speech
    file = str(num) + ".mp3"
    toSpeak.save(file)

    # playsound package is used to play the same file.
    playsound.playsound(file, True)
    os.remove(file)


def get_audio():
    rObject = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        print("Speak...")

        # recording the audio using speech recognition
        audio = rObject.listen(source, phrase_time_limit=5)
    print("Stop.")  # limit 5 secs

    try:

        text = rObject.recognize_google(audio, language='en-US')
        print("You : ", text)
        return text

    except:

        assistant_speaks("Could not understand your audio !")
        return 0


# Driver Code
if __name__ == "__main__":
    assistant_speaks("Hello I am your Personal Assistant. Please tell the password before proceding ")
    password = get_audio()
    if(''.join(str(password))=='1234'):
        assistant_speaks("Welcome")
    else:
        assistant_speaks("You are not authorised to use the services")
        exit()
    assistant_speaks("Please tell your name?")
    name = get_audio()
    if(name==0):
        name="Priyanshu"
    assistant_speaks("Hello, " + name + '.')

    while (1):

        assistant_speaks("What can i do for you?")
        text = get_audio()

        if text == 0:
            continue
        text = text.lower()

        if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text):
            assistant_speaks("Ok bye, " + name + '.')
            break


        def search_web(input):

            driver = webdriver.Chrome('./chromedriver')
            driver.implicitly_wait(1)
            driver.maximize_window()
            if 'youtube' in input.lower():
                assistant_speaks("Opening Youtube")
                indx = input.lower().split().index('youtube')
                query = input.split()[indx + 1:]
                driver.get("http://www.youtube.com/results?search_query=" + '+'.join(query))
                time.sleep(10)
                return

            elif 'wikipedia' in input.lower():
                assistant_speaks("Opening Wikipedia")
                indx = input.lower().split().index('wikipedia')
                query = input.split()[indx + 1:]
                driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
                time.sleep(10)
                return
            elif 'search' in input:
                indx = input.lower().split()
                indx.remove("search")
                driver.get("https://www.google.com/search?q=" + '+'.join(indx))
                time.sleep(10)

            elif "play" in input.lower():
                indx = input.lower.split()
                indx.remove("play")
                driver.get("https://gaana.com/search/"+str(indx))
            else:
                driver.get("https://www.google.com/search?q="+'+'.join(input.split()))
                time.sleep(10)
            return





        def open_application(input):

            if "chrome" in input:
                assistant_speaks("opening Google Chrome")
                os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
                return


            elif "music" in input:
                assistant_speaks("opening music app")
                os.startfile(
                    'C:\Program Files\Windows Media Player\wmplayer.exe')
                time.sleep(15)
                return

            elif "excel" in input:
                assistant_speaks("Opening Microsoft Excel")
                os.startfile(
                    'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Excel 2013.lnk')
                return

            else:

                assistant_speaks("Application not available")
                return

        def jokes():
            assistant_speaks(pyjokes.get_joke())



        def weather(data):

            api_key = "cd6bf05f0b5a1fe8eed43dfccded3a5b"

            base_url = "http://api.openweathermap.org/data/2.5/weather?"

            city_name = data

            complete_url = base_url + "appid=" + api_key + "&q=" + city_name

            response = requests.get(complete_url)

            x = response.json()

            if x["cod"] != "404":

                y = x["main"]

                current_temperature = y["temp"]

                current_pressure = y["pressure"]

                current_humidiy = y["humidity"]

                z = x["weather"]

                weather_description = z[0]["description"]

                assistant_speaks(" Temperature (in kelvin unit) = " +
                      str(current_temperature) +
                      "\n atmospheric pressure (in hPa unit) = " +
                      str(current_pressure) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                print(" City Not Found ")

        def process_text(input):
            try:
                if 'search' in input :
                    search_web(input)
                    return

                elif "who are you" in input or "define yourself" in input:
                    speak = '''Hello, I am Your personal Assistant. 
                    I am here to make your life easier. You can command me to perform 
                    various tasks such as calculating sums or opening applications etcetra'''
                    assistant_speaks(speak)
                    return

                elif "who made you" in input or "created you" in input:
                    speak = "I have been created by Priyanshu Pareta."
                    assistant_speaks(speak)
                    return

                elif "udemy" in input:
                    speak = """Opening udemy"""
                    assistant_speaks(speak)
                    return

                elif "calculate" in input.lower():

                    # write your wolframalpha app_id here
                    app_id = "PQHGK4-V2L5RJ37KY"
                    client = wolframalpha.Client(app_id)

                    indx = input.lower().split().index('calculate')
                    query = input.split()[indx + 1:]
                    res = client.query(' '.join(query))
                    answer = next(res.results).text
                    assistant_speaks("The answer is " + answer)
                    return

                elif 'open' in input:


                    open_application(input.lower())
                    return

                elif 'joke' in input:
                    assistant_speaks("Here is a joke for you")
                    jokes()
                elif "weather" in input:
                    assistant_speaks("Which city's weather do you want to know")
                    city = get_audio()
                    assistant_speaks("Weather in "+city+"is")
                    weather(city)

                else:

                    assistant_speaks("I can search the web for you. Do you want to continue?")
                    ans = get_audio()
                    if 'yes' in str(ans) or 'yeah' in str(ans):
                        search_web(input)
                    else:
                        return
            except:

                assistant_speaks("I don't understand, I can search the web for you. Do you want to continue?")
                ans = get_audio()
                if 'yes' in str(ans) or 'yeah' in str(ans):
                    search_web(input)
                else:
                    assistant_speaks("Okay I'll leave then")

        process_text(text)


