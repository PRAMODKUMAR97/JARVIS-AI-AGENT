import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pywhatkit as wk
import webbrowser
import psutil
import os
import cv2
import pyautogui
import time
import operator
import requests
import sys
import google.generativeai as genai
import re
from dotenv import load_dotenv

HF_TOKEN = "api key"

genai.configure(api_key="api key")

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 16:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Hey Boss, How are you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=10)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None


def create_image_with_huggingface(prompt):
    try:
        url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        response = requests.post(url, headers=headers, json={"inputs": prompt})

        if response.status_code != 200:
            print("API Error:", response.text)
            speak("Image generation failed.")
            return None

        content_type = response.headers.get("Content-Type", "")
        if "image" in content_type:
            image_path = "generated_image.png"
            with open(image_path, "wb") as f:
                f.write(response.content)
            return image_path
        else:
            print("Not an image response:", response.text)
            return None

    except Exception as e:
        print(f"Image creation failed: {e}")
        return None

def get_weather(city="mangaluru"):
    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url)
        if response.status_code == 200:
            weather_report = response.text.strip()
            print(f"Weather: {weather_report}")
            speak(f"The currnt weather in the {city} is {weather_report}")
        else:
            print(f"Failed to get weather. Status code: {response.status_code}")
            speak("Sorry, I couldn't fetch the weather.")
    except Exception as e:
        print(f"Weather Error: {e}")
        speak("Sorry, something went wrong while fetching the weather.")

def search_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=1)
        speak(results)
        return results
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("No results found.")

def handle_query(query, ai):      
    if "hey jarvis" in query:
            print("Yes sir")
            speak("Yes sir")
          
    elif "who are you" in query:
            print("My name is Jarvis")
            speak("My name is Jarvis")
            print("I can do everything that my creator programmed me to do")
            speak("I can do everything that my creator programmed me to do")
            
    elif "who created you" in query:
            print("I do not know his name. I was created using Python language in Visual Studio Code.")
            speak("I do not know his name. I was created using Python language in Visual Studio Code.")


    elif "what is the time" in query or "what is the current time" in query or "what is the current time, jarvis" in query or "jarvis time" in query or "time please" in query or "current time" in query:
         strTime = datetime.datetime.now().strftime("%H:%M:%S")
         speak(f"Sir, the time is {strTime}")

    elif 'open google' in query or "just open google" in query or "open the chrome" in query or "open chrome" in query or "open browser" in query or "open the browser" in query:
         webbrowser.open('https://www.google.com') 
        
    elif 'close chrome' in query or 'close this chrome' in query or 'close the chrome' in query or "close the browser" in query or "close browser" in query or "close this browser" in query:
         os.system("taskkill /f /im chrome.exe")  

    elif 'search on google' in query or "google search" in query or "open google search" in query:
        speak("What should I search?")
        search_query = takeCommand()
        if search_query:
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            search_wikipedia(search_query)


    elif 'just open youtube' in query or "open youtube" in query:
        speak("opening youtube")
        webbrowser.open('https://www.youtube.com')
        
    elif 'close youtube' in query or 'close this youtube' in query or 'close the youtube' in query:
         os.system("taskkill /f /im chrome.exe")

    elif 'search on youtube' in query or "youtube search" in query or "open youtube search" in query:
        speak("What would you like to watch?")
        video_query = takeCommand()
        if video_query:
            wk.playonyt(video_query)
         
    elif 'give me a youtube list' in query:
         query = query.replace("search on youtube", "")
         webbrowser.open(f"www.youtube.com/results?search_query={query}")

    elif 'songs' in query or 'song' in query or 'music' in query:
        speak("Which song would you like to watch?")
        video_query = takeCommand()
        if video_query:
            wk.playonyt(video_query)

    elif "pause" in query or "pause the vedio" in query or "pause vedio" in query or "pause a vedio" in query:
      pyautogui.press("k")
      speak("video paused")
      
    elif "play" in query or "play the vedio" in query or "paly vedio" in query or "play a vedio" in query:
      pyautogui.press("k")
      speak("video played")

    elif "mute" in query or "mute the volume" in query or "mute the system volume" in query:
      pyautogui.press("m")
      speak("system volume  is muted")

    elif 'maximize this window' in query or 'maximize window' in query or 'maximize' in query:
            pyautogui.hotkey('alt', 'space')
            time.sleep(1)
            pyautogui.press('x')
            
    elif 'minimise this window' in query or 'minimise window' in query or 'minimise' in query:
            pyautogui.hotkey('alt', 'space')
            time.sleep(1)
            pyautogui.press('n')
           
    elif 'open new window' in query or 'open a window' in query or 'open window' in query:
            pyautogui.hotkey('ctrl', 'n')
            
    elif 'open incognito window' in query or "open incognito" in query:
            pyautogui.hotkey('ctrl', 'shift', 'n')
            
    elif 'open history' in query or "open the history" in query:
            pyautogui.hotkey('ctrl', 'h')
            
    elif 'open downloads' in query or 'open download' in query or "open the downloads" in query:
            pyautogui.hotkey('ctrl', 'j')
            
    elif 'previous tab' in query:
            pyautogui.hotkey('ctrl', 'shift', 'tab')
            
    elif 'next tab' in query:
            pyautogui.hotkey('ctrl', 'tab')           
            
    elif 'copy' in query or 'copy the word' in query or 'copy this sentence' in query or 'copy this word' in query:
         pyautogui.hotkey('ctrl', 'c')
                
    elif 'delete' in query or 'delete the word' in query or 'delete this sentence' in query or 'delete this word' in query:
         pyautogui.hotkey('delete')
        
    elif 'enter' in query: 
     pyautogui.press('enter')

    elif 'tab' in query: 
     pyautogui.press('tab')    
        
    elif 'space' in query:
     pyautogui.press('backspace')  

    elif 'escape' in query: 
     pyautogui.press('esc')  

    elif 'capslock' in query: 
     pyautogui.press('capslock')

    elif 'cut' in query or 'cut the word' in query or 'cut this sentence' in query or 'cut this word' in query:
         pyautogui.hotkey('ctrl', 'x')
    
    elif 'paste' in query or 'paste the word' in query or 'paste this sentence' in query or 'paste this word' in query:
         pyautogui.hotkey('ctrl', 'v')
         
    elif 'close tab' in query or "close the tab" in query:
            pyautogui.hotkey('ctrl', 'w')
            
    elif 'close window' in query or 'close this windows' in query or 'close the window' in query:
            pyautogui.hotkey('ctrl', 'shift', 'w')

    elif 'clear browsing history' in query or 'clear all the browsing history' in query:
            pyautogui.hotkey('ctrl', 'shift', 'delete')

    elif 'open file explorer' in query or 'open explorer' in query or 'show my files' in query:
           speak("opening file explorer")
           print('opening file explorer')
           os.startfile("C:\\") 

    elif 'close file explorer' in query or 'close explorer' in query:
           os.system("taskkill /f /im explorer.exe")

    elif "open paint" in query or "i need to draw something " in query or "drawing" in query or "paint" in query:
         speak("opening paint")
         print('OPEING PAINT')
         npath = "C:\\Windows\\system32\\mspaint.exe"
        
    elif "close paint" in query: #16
         os.system("taskkill /f /im mspaint.exe")

    elif "open notepad" in query or "notepad" in query or "open the notepad" in query or "open a page to write" in query or "give me page" in query or "give me a page" in query or "open a sheet" in query or "open a sheet of papper" in query:
         speak("opening notepad")
         print("opening notepad")
         npath = "C:\\WINDOWS\\system32\\notepad.exe"
         os.startfile(npath)

    elif "close notepad" in query or "close the page" in query or "close the sheet" in query:
         os.system("taskkill /f /im notepad.exe")

    elif 'open microsoft store' in query or "ms store" in query or "open the microsoft store" in query or "microsoft store" in query or "download a game" in query or "open the store" in query or "open store" in query or "download game" in query:
        speak("Opening microsoft store")
        print("Opening microsoft store")
        os.system("start ms-windows-store:")   
    
    elif "close microsoft store" in query or "close the microsoft store" in query or "close play store" in query or "close store" in query:
         os.system("taskkill /f /im WinStore.App.exe")   

    elif 'open vs code' in query or "open the vs code" in query or "open the visual studio" in query or "visual studio" in query or "vs code" in query or "open visual studio" in query or "open the window to write a code" in query or "open window to write a code" in query or "write a code" in query:
        speak("Opening Visual Studio Code.")
        print("Opening Visual Studio Code.")
        os.system("code")  # This command opens VS Code
    
    elif "close vs code" in query or "close visualstudio" in query:  
        os.system("taskkill /F /IM Code.exe") 

    elif "open gmail" in query:
        speak("opening gmail")
        print("opening gmail")
        webbrowser.open('https://mail.google.com/mail/u/0/#inbox') 
        
    elif 'close gamil' in query:
         os.system("taskkill /f /im chrome.exe")

    elif 'open whatsapp' in query:
       speak("Opening WhatsApp.")
       print("Opening WhatsApp.")
       os.system("start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App")

    elif "close whatsapp" in query: #16
        os.system("taskkill /F /IM WhatsApp.exe")      
    
    elif 'open word' in query or "microsoft word" in query or "ms word" in query or "open ms word" in query or "open microsoft word" in query:
      speak("Opening Microsoft Word.")
      print("Opening Microsoft Word.")
      os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")

    elif "close word" in query or "close ms word" in query or "close microsoft word" in query:
      os.system("taskkill /F /IM WINWORD.EXE") 

    elif 'open excel' in query or "microsoft excel" in query or "ms excel" in query or "open ms excel" in query or "open microsoft excel" in query:
      speak("Opening Microsoft Excel.")
      print("Opening Microsoft Excel.")
      os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")
    
    elif "close excel" in query or "close ms excel" in query or "close microsoft excel" in query:  
      os.system("taskkill /F /IM EXCEL.EXE")

    elif 'open powerpoint' in query or "open ppt" in query:
      speak("Opening Microsoft PowerPoint.")
      print("Opening Microsoft PowerPoint.")
      os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE")

    elif "close powerpoint" in query or "close ppt" in query:  
      os.system("taskkill /F /IM POWERPNT.EXE")

    elif "open command prompt" in query or "command promplt" in query or "cmd" in query or "open cmd" in query or "open prompt" in query:
         speak("opening command prompt")
         print("opening command prompt")
         os.system("start cmd")

    elif "close command prompt" in query or "close cmd" in query or "close prompt" in query:
         os.system("taskkill /f /im cmd.exe")


    elif 'open photos' in query or 'open gallery' in query:
         speak("opening photos")
         os.system("start ms-photos:")

    elif 'close photos' in query or 'close gallery' in query:
         os.system("taskkill /f /im Photos.exe")

    elif 'open settings' in query or 'open windows settings' in query:
        speak("opening settings")
        os.system("start ms-settings:")

    elif ('close settings') in query or 'close windows settings' in query:
         os.system("taskkill /f /im SystemSettings.exe")

    elif "close movie" in query: #21
         os.system("taskkill /f /im vlc.exe")

    elif "close music" in query: #22
         os.system("taskkill /f /im vlc.exe")

    elif "shutdown the system" in query or "shutdown" in query or "shutdown system" in query:
         speak("shutdowning the system")
         os.system("shutdown /s /t 5")

    elif "restart the system" in query or "restart" in query or "restart system" in query:
         speak("restrating the system")
         os.system("shutdown -r -t 5") 
        
    elif "lock the system" in query or "lock" in query or "lock system" in query:
         speak("locking the system")
         os.system("rundll32.exe user32.dll,LockWorkStation")
             
    elif "hibernate the system" in query or "hibernate" in query or "hibernate system" in query:
         speak("hibernateing the system")
         os.system("rundll32.exe powrprof.dll,SetSuspendState Hibernate")

    elif "open camera" in query.lower():
         speak("Opening the camera.")
         cap = cv2.VideoCapture(0)

         while True:
            ret, img = cap.read()
            if not ret:
              speak("Failed to capture video.")
              break

            img = cv2.flip(img, 1)
            cv2.putText(img, "Say 'take photo' or 'close camera'", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow('Webcam', img)
            cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)
            cv2.moveWindow("Webcam", 100, 100)
            cv2.waitKey(1)

            query = takeCommand().lower()

            if "take photo" in query:
               speak("What should I name the photo?")
               photo_name = takeCommand().lower().strip()
               photo_name = photo_name.replace(" ", "_")  
               filename = f"{photo_name}.jpg"
               cv2.imwrite(filename, img)
               speak(f"Photo saved as {filename}.")

            elif "close camera" in query:
              speak("Closing the camera.")
              break

         cap.release()
         cv2.destroyAllWindows()

    elif "go to sleep" in query or "bye jarvis" in query or "good bye" in query:
           speak('alright then, I am switching off')
           print('alright then, I am switching off')
           sys.exit()

    elif "take screenshot" in query or "screeshot" in query or "take the screenshot" in query: 
           speak("tell me a name for the file")
           name = takeCommand().lower()
           time.sleep(3)
           img = pyautogui.screenshot()
           img.save(f"{name}.png")
           speak("screenshot saved")

    elif "calculate" in query: #31
            r = sr.Recognizer()
            with sr.Microphone() as source:
              speak("ready...")
              print("listening...")
              r.adjust_for_ambient_noise(source)
              audio = r.listen(source)
            my_string= r.recognize_google(audio)
            print(my_string)
            def get_operator_fn(op):
              return {
                 '+': operator.add,
                 '-': operator.sub,
                 'x': operator.mul,
                 'divided': operator.truediv,
                }[op]
            def eval_binary_expr(op1, oper, op2):
                op1, op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)
            speak("your result is" + str(eval_binary_expr(*my_string.split())))


    elif "what is my ip address" in query or   "give me the ip address of the system" in query or "ip address of the system" in query or  "ip address" in query:
      speak("Checking...")
      print("Checking...")

      try:
        ip_add = requests.get('https://api.ipify.org', timeout=5).text
        print(ip_add)
        speak("Your IP address is")
        speak(ip_add)
      except Exception as e:
        speak("The network is weak, please try again later.")

               
    elif "volume up" in query or "raise the volume" in query or "raise volume" in query or "increase the volume" in query or "increase volume" in query:
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           pyautogui.press("volumeup")
           
    elif "volume down" in query or "reduce the volume" in query or "reduce volume" in query or "decrease the volume" in query or "decrease volume" in query:
           pyautogui.press("volumedown")
           pyautogui.press("volumedown")
           pyautogui.press("volumedown")
           pyautogui.press("volumedown")
           pyautogui.press("volumedown")
           pyautogui.press("volumedown")
           pyautogui.press("volumedown")
           pyautogui.press("volumedown")
           pyautogui.press("volumedown")
           pyautogui.press("volumedown")
           pyautogui.press("volumedown")
           pyautogui.press("volumedown")
           pyautogui.press("volumedown")

    elif "battery" in query or "battery percentage" in query:
        battery = psutil.sensors_battery()
        speak(f"Current battery level is {battery.percent} percent.")


    elif "scroll down" in query:
        speak("Scrolling down")
        def scroll_screen(direction='down', amount=10, delay=0.1):
            scroll_value = -1 if direction == 'down' else 1
            for _ in range(amount):
                pyautogui.scroll(scroll_value * 100)
                time.sleep(delay)

        scroll_screen('down', amount=5, delay=0.2)

    elif "scroll up" in query:
        speak("Scrolling up")
        def scroll_screen(direction='up', amount=10, delay=0.1):
            scroll_value = -1 if direction == 'down' else 1
            for _ in range(amount):
                pyautogui.scroll(scroll_value * 100)
                time.sleep(delay)

        scroll_screen('up', amount=5, delay=0.2)

    elif "scroll to top" in query:
        speak("Scrolling to the top")
        for _ in range(30):  
          pyautogui.scroll(100)
          time.sleep(0.05)

    elif "scroll to bottom" in query:
        speak("Scrolling to the bottom")
        for _ in range(30):  
         pyautogui.scroll(-100)
         time.sleep(0.05)

    elif "weather" in query:
        match = re.search(r"weather in ([a-zA-Z\s]+)", query)
        city = match.group(1).strip() if match else "mangaluru"
        get_weather(city)

    elif "create image of" in query or "draw image of" in query:
        prompt = query.replace("create image of", "").replace("draw image of", "").strip()
        speak(f"Creating an image of {prompt}")
        image_path = create_image_with_huggingface(prompt)
        if image_path:
            speak("Image created successfully.")
            os.startfile(image_path)
        else:
            speak("Sorry, I couldn't generate the image.")

    else:
        ai_response = ai.send_request(query)
        print(f"AI Response: {ai_response}")
        speak(ai_response)


class AI:
    def __init__(self):
     pass

    def clean_response(self, text):
        # Remove bold/italic markdown-like syntax
        text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)  # Removes *, **, or *** around words
        text = re.sub(r'`{1,3}(.*?)`{1,3}', r'\1', text)    # Removes inline code formatting
        return text.strip()
    
    def send_request(self, query):
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(query)

            # Use .text or fallback to parts
            response_text = getattr(response, 'text', None)
            if not response_text and hasattr(response, 'parts'):
                response_text = "".join(part.text for part in response.parts)

            if not response_text:
                return "No response available."

            sentences = response_text.split('.')
            return sentences[0].strip() + '.' if sentences else response_text.strip()

        except Exception as e:
            print(f"AI Error: {e}")
            return "Sorry, I couldn't process your request."
        
if __name__ == "__main__":
    # Password Authentication
    print("Please say the password to acess Jarvis.")
    speak("Please say the password to access Jarvis.")
    for i in range(3):
        user_password = takeCommand()
        if user_password:
            with open("password.txt", "r") as pw_file:
                stored_password = pw_file.read().strip()
            if user_password == stored_password:
                print("WELCOME SIR! Jarvis is now activated.")
                speak("WELCOME SIR! Jarvis is now activated. ")
                break
            elif i == 2:
                speak("Access denied. Shutting down.")
                sys.exit()
            else:
                print("Incorrect password. Try again.")
                speak("Incorrrect password. Try again")
    
    ai = AI()
    wishMe()
    while True:
        user_input = takeCommand()
        if user_input:
            if "exit" in user_input:
                speak("Goodbye!")
                print("Goodbye!")
                sys.exit()
            elif "exit" in user_input:
                print("Goodbye!")
                speak("Goodbye!")
                sys.exit()
            handle_query(user_input, ai)
