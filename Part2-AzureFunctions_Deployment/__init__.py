import logging
import os

import azure.functions as func
from fastai.vision import *
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:

    path = Path.cwd()
    learn = load_learner(path)

#Uncomment this block of code if you wish to test image files from url
    # request_json = req.get_json()
    # r = requests.get(request_json['url'])

    # if r.status_code == 200:
    #     temp_image_name = "temp.jpg"        
    #     with open(temp_image_name, 'wb') as f:
    #         f.write(r.content)
    # else:
    #     return func.HttpResponse(f"Image download failed, url: {request_json['url']}")
    
    # img = open_image(temp_image_name)
    # pred_class, pred_idx, outputs = learn.predict(img)

    # return func.HttpResponse(f"request_json['url']: {request_json['url']}, pred_class: {pred_class}")

##########################################################################################

#For testing image files from local file, comment this block of code if you wish to test image files from url
    file_sent = None
    try:
        # Retrieve photo via HTTP Request
        file_sent = req.files['file']
        file_sent.seek(0)
    except Exception as e:
        return func.HttpResponse(
             str(e),
             status_code=400
        )

    # If file received
    if file_sent:

        img = open_image(file_sent)
        pred_class, pred_idx, outputs = learn.predict(img)

        prediction = "High probability"
        if outputs.max() < 0.9:
            prediction = "Prediction might not be accurate!"


        #return the prediction class type and the probability score.
        return func.HttpResponse(f"pred_class: {pred_class}, score:{outputs.max()}, prediction: {prediction}")

    # No photo received
    else:
        return func.HttpResponse(
             "Please pass a file",
             status_code=400
        )
#########################################################################################################


