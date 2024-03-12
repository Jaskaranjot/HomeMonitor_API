import sqlite3
from flask import Flask, request, jsonify
import uuid
import os
import requests

app = Flask(__name__)

#connection =  sqlite3.connect("pictures.db")
#cursor = connection.cursor()
#cursor.execute("create table images (id integer primary key, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,filename)")
#cursor.execute("create table tags (imageId integer, tag, foreign key (imageId) references images (id))")
#connection.commit()

dir_name = "upload_images"

@app.route("/api/image", methods=["POST"])
def post_image():

    if 'image' not in request.files:
        return{
            "error":"image is not included"
        },400
    file = request.files['image']
    filename = str(uuid.uuid4())
    file.save(f'{dir_name}/{filename}.jpg')

   
    connection =  sqlite3.connect("pictures.db")
    cursor = connection.cursor()

    cursor.execute(f"insert into images (filename) values ('{filename}.jpg')")
    connection.commit()

    api_key = 'acc_4980b510607ad5f'
    api_secret = 'd708e54218f997bf7f3c442c6d01486b'
    url = 'https://api.imagga.com/v2/tags'
    file= {'image': open(f"{dir_name}/{filename}.jpg", 'rb')}
    response = requests.post(url,auth=(api_key, api_secret),files=file)
    image=response.json()
    imagga = image['result']['tags']
    for image in imagga:
        cursor.execute(f"insert into tags (tag ) values ('{image['tag']['en']}')")
    connection.commit()
