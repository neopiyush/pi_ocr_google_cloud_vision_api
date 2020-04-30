from flask import Response
from flask import Flask, escape, request
from datetime import datetime
from time import sleep
import io
import cv2
from PIL import Image

from google.cloud import vision
from google.cloud.vision import types

app = Flask(__name__)

client = vision.ImageAnnotatorClient()

def detect_text(path):
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.text_detection(image = image)
    texts = response.text_annotations
    string = ''

    for text in texts:
        string+=' ' + text.description
    return string
def detect_live_text():

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    file = 'live.png'
    cv2.imwrite(file,frame)

    result_text = detect_text(file)
    print(result_text)
    
    cap.release()
    cv2.destroyAllWindows()
    return result_text

@app.route("/ocr/")
def ocr():
    def streamer():
        while True:
            yield detect_live_text()+"\n"
            #yield "<p>{}</p>".format(detect_live_text())
            sleep(1)

    return Response(streamer())