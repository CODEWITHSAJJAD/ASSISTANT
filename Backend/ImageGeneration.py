import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep
def Open_Images(prompt):
    folder_path=r"Data"
    prompt=prompt.replace(" ","_")
    Files=[f"{prompt}{i}.jpg" for i in range(1,5)]
    for jpg_file in Files:
        image_path=os.path.join(folder_path,jpg_file)
        try:
            img=Image.open(image_path)
            print(f"opening image:{image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open{image_path}")
api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    responses=await asyncio.to_thread(requests.post,api_url,headers=headers,json=payload)
    return responses.content

async def generate_images(prompt: str):
    tasks=[]
    for _ in range(4):
        payload={
            "inputs":f"{prompt},quality=4k,sharpness=maximum,Ultra High details,high resolution,seed={randint(0,1000000)}",        
        }
        task=asyncio.create_task(query(payload))
        tasks.append(task)
    image_tytes_list=await asyncio.gather(*tasks)
    for i,image_tytes in enumerate(image_tytes_list):
        with open(fr"DATA\{prompt.replace(' ','_')}{i+1}.jpg","wb") as f:
            f.write(image_tytes)
def GenerateImages(prompt:str):
    asyncio.run(generate_images(prompt))
    Open_Images(prompt)
while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data","r") as f:
            Data:str=f.read()
        Prompt,Status=Data.split(",")
        if Status == "True":
            print("Generating Images...........")
            ImageStatus=GenerateImages(prompt=Prompt)
            with open(r"Frontend\Files\ImageGeneration.data","w") as f:
                f.write("False,False")
                break
        else:
            sleep(1)
    except Exception as e:
        print(e)



