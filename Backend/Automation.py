from AppOpener import close,open as appopen
from webbrowser import open as webopen
from pywhatkit import search,playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

env_vars=dotenv_values(".env")
GroqAPIKey=env_vars.get("GROQ_API_KEY")
classes=["zCubwf","hgKElc","LTKOO sY7ric","Z0LcW","gsrt vk_bk FzWSb YwPhnf","pclqee","tw-Data-text tw-text-small tw-ta",
         "IZ6rdc","O5uR6d LTKOO","vlzY6d","webanswers-webanswers_table_webanswers-table","dDoNo ikb4Bb gsrt","ssXLaOe",
         "LWkfKe","VQF4g","qv3Wpe","kno-rdesc","SPZz6b"]
useragent="Mozila/5.0 (Windows NT 10.0; Win64; x86) AppleWebkit/537.86 (KHTML,like Gecko) Chrome/89.0.142.86 Safari/537.36"
client=Groq(api_key=GroqAPIKey)
professional_responses=[
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate you ask.",
]
messages=[]
SystemChatBot=[{"role":"system","content":f"Hello,I am {os.environ['Username']},You're a content wirter.You have to write content like letters,codes,essays,applicatons,notes,songs,poems etc."}]
def GoogleSearch(Topic):
    search(Topic)
    return True
def content(Topic):
    def OpenNotepad(File):
        default_text_editor='notepad.exe'
        subprocess.Popen([default_text_editor,File])
    def ContentWriter(Prompt):
        messages.append({"role":"user","content":f"{Prompt}"})
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        Answer=""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer+=chunk.choices[0].delta.content
        Answer=Answer.replace("</s>","")                
        messages.append({"role":"assistant","content":Answer})
        return Answer
    Topic: str =Topic.replace("content ","")
    ContentByAI=ContentWriter(Topic)
    with open(rf"Data\{Topic.lower().replace(' ','')}.txt","w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()
    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")
    return True

def YoutubeSearch(Topic):
    UrlSearch= f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(UrlSearch)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app,sess=requests.session()):
    try:
        appopen(app,match_closest=True,output=True,throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return[]
            soup=BeautifulSoup(html,"html.parser")
            links=soup.find_all("a",{'jsname':"UWckNb"})
            return [link.get('href') for link in links]
        def search_google(query):
            url=f"https://www.google.com/search?q={query}"
            headers={"User-Agent":useragent}
            response=sess.get(url,headers=headers)
            if response.status_code==200:
                return response.text
            else:
                print("Failed to retrieve search results.")
            return None
        html=search_google(app)
        if html:
            link=extract_links(html)[0]
            webopen(link)
        return True

def CloseApp(app):
    if "chrome" == app:
        pass
    else:
        try:
            close(app,match_closest=True,output=True,throw_error=True)
            return True
        except:
            return False
def System(command):
    def mute():
        keyboard.press_and_release("voluume mute")
    def unmute():
        keyboard.press_and_release("voluume mute")
    def voluem_up():
        keyboard.press_and_release("voluume up")
    def volume_down():
        keyboard.press_and_release("voluume down")

    if command=="mute":
        mute()
    elif command=="umnute":
        unmute()
    elif command=="volume up":
        voluem_up()
    elif command=="volume down":
        volume_down()
    return True
async def TranslateAndExecute(commands:list[str]):
    funcs=[]
    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file" in command:
                pass
            else:
                fun=asyncio.to_thread(OpenApp,command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun=asyncio.to_thread(CloseApp,command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun=asyncio.to_thread(PlayYoutube,command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun=asyncio.to_thread(content,command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun=asyncio.to_thread(GoogleSearch,command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun=asyncio.to_thread(System,command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Funtion Found, For{command}")
    results=await asyncio.gather(*funcs)
    for result in results:
        if isinstance(result,str):
            yield result
        else:
            yield result


async def Automation(commands:list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True

# if __name__=="__main__":
#     asyncio.run(Automation(["open whatsapp","content song for me","play pall pall"]))