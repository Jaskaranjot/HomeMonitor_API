import os
import random
import time
import requests


image_path = './images'
url = 'http://127.0.0.1:5000/api/image'

def post_server_image(use_image):

    file = {'image': open(use_image, 'rb')}
    response = requests.post(url, files=file)
    
    print(f"{use_image} .")

while True:
    picture = [f for f in os.listdir(image_path) if f.endswith(('.jpg', '.jpeg'))]
    image = os.path.join(image_path, random.choice(picture))
    post_server_image(image)        
    time.sleep(10)