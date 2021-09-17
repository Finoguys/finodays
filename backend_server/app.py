import sys

from flask import Flask, jsonify, request, json, make_response
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
import joblib
import traceback
import jsonpickle
import os
from catboost import CatBoostRegressor
import subprocess
from datetime import datetime
import subprocess
import colorsys
import math
from scipy.spatial import distance
from sklearn.cluster import MiniBatchKMeans
import matplotlib.pyplot as plt
import cv2

app = Flask(__name__)

saved_predictions = [[]]
immovable = [""]
car = [""]
car_img=[['']]



@app.route("/", methods=['GET'])
def hello():
    # print("lol", file=sys.stderr)
    # app.logger.info('testing info log')
    print('hello', flush=True)
    #
    # print('This is error output', file=sys.stderr)
    # print('This is standard output', file=sys.stdout)
    return "hey"


@app.route("/predict_immovable", methods=['POST'])
@cross_origin()
def predict_immovable():
    # print("lol", file=sys.stderr)
    # app.logger.info('testing info log')
    # print('Hi', flush=True)
    #
    # print('This is error output', file=sys.stderr)
    # print('This is standard output', file=sys.stdout)
    # lr = joblib.load("model.pkl")
    clf = CatBoostRegressor()
    clf.load_model("catboost_model")

    # for USA's homes
    # clf.predict(bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition, sqft_above, sqft_basement, yr_built, yr_renovated, latitude, longitude)

    # translating adress to the latitude and longitude
    # for example string request can be: street, city, statezip, country.
    # address - variable example

    if clf:
        print('This is clf output', file=sys.stdout)
        try:
            json = request.get_json()
            print(json, file=sys.stdout)
            # model_columns = joblib.load("model_cols.pkl")
            address = json[0]['address']
            command = "mapbox --access-token pk.eyJ1IjoiaXBpcG9zIiwiYSI6ImNrdGw5czZxbjFpbTUyd282YjlqY2ZvODMifQ.mnnD6BdczXSaIlFJFC_byQ geocoding --limit 1 "
            command += "\"" + address + "\""
            fileText = subprocess.check_output(command, shell=True).decode()

            index = fileText.find("center")
            index2 = fileText.find(']', index + 3)
            index3 = fileText.rfind(',', index + 3, index2)

            latitude = fileText[index + 9:index3]
            longitude = fileText[index3 + 1:index2]

            temp = list(json[0].values())
            # temp = [4, 5, 5566, 6666, 5, 6, 9, 8, 6, 7666, 0, 27.8, -122.502, 7899, 6666]

            temp.pop()
            temp.extend([latitude, longitude])
            print(temp, file=sys.stdout)

            # print(clf.predict([3.0, 1.50, 1340, 7912, 1.5, 0, 0, 3, 1340, 0, 1955, 2005, -122.338866, 47.765807]), file=sys.stdout)
            # vals = np.array(temp).reshape(1, len(temp))

            prediction = clf.predict(temp)
            print(prediction, file=sys.stdout)

            app.logger.info('testing info log')
            return jsonify({'prediction': str(prediction)})

        except:
            print('This is exceptional output ', traceback.format_exc(), file=sys.stdout)
            return jsonify({'trace': traceback.format_exc()})
    else:
        return ('No model here to use')


@app.route("/save_prediction", methods=['POST'])
@cross_origin()
def save_prediction():
    json = request.get_json()
    temp = list(json[0].values())
    saved_predictions[0].insert(0,{
        "name": json[0]['name'],
        "date": datetime.today().strftime('%d-%m-%Y'),
        "price": json[0]['price'],
        "immovable": immovable[0],
        "car": car[0],
    })
    immovable[0]=""
    car[0]=""
    print("============", file=sys.stdout)
    print(saved_predictions[0], file=sys.stdout)
    print("============diction", file=sys.stdout)
    return 'ok'

@app.route("/get_predictions", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_predictions():
    print({"response saved": str(json.dumps(saved_predictions[0]))})

    return {"response": str(json.dumps(saved_predictions[0]))}


@app.route("/save_immovable", methods=['POST'])
@cross_origin()
def save_immovable():
    json = request.get_json()
    temp = list(json[0].values())
    immovable[0] = str(jsonpickle.encode(request.get_json(), unpicklable=False))
    print(immovable, file=sys.stdout)

    return 'ok'


@app.route("/save_car", methods=['POST'])
@cross_origin()
def save_car():
    json = request.get_json()
    temp = list(json[0].values())
    car[0] = str(jsonpickle.encode(request.get_json(), unpicklable=False))
    print(car, file=sys.stdout)
    return 'ok'


@app.route("/get_immovable", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_immovable():
    # if len(immovable)>0:
    #     return str(jsonpickle.encode(immovable, unpicklable=False))
    print({"response" : immovable[0]})
    return {"response" : immovable[0]}
@app.route("/get_car", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_car():
    print({"response": car[0]})
    return {"response": car[0]}



def hasher(inp):
  newInp = 0
  for i in range(0,len(inp)):
    newInp += ord(inp[i])*(i+1)
  return newInp


def bgr2hsv(bgr):
    return rgb2hsv([bgr[2],bgr[1], bgr[0]])

def rgb2hsv(rgb):
    red=rgb[0]
    green=rgb[1]
    blue=rgb[2]
    red_percentage = red / float(255)
    green_percentage = green / float(255)
    blue_percentage = blue / float(255)

    color_hsv_percentage = colorsys.rgb_to_hsv(red_percentage, green_percentage, blue_percentage)

    color_h = round(360 * color_hsv_percentage[0])
    color_s = round(100 * color_hsv_percentage[1])
    color_v = round(100 * color_hsv_percentage[2])
    color_hsv = (color_h, color_s, color_v)
    return color_hsv


def getPalette(imageIn):
    imageRes=cv2.resize(imageIn,(640,480))
    (h, w) = imageRes.shape[:2]
    image = cv2.medianBlur(imageRes, (max(h,w)//70)//2*2+1)
    imagehsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    sumPixels=h*w
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    pix_weight=np.ndarray([h,w])
    for am in range(h):
        for bm in range(w):
            pix_weight[am][bm]=((min(am,bm,h-am,w-bm)/(min(w,h)/2)*
                                 ((imagehsv[am][bm][1]/255*imagehsv[am][bm][2]/255))**(1/10)))**4
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    pix_weight_1d = pix_weight.reshape((pix_weight.shape[0] * pix_weight.shape[1]))
    clusters=32
    while(clusters>2):
        clt = MiniBatchKMeans(n_clusters=clusters)
        labels = clt.fit_predict(image,sample_weight=pix_weight_1d)
        allcols=[]
        for i in range(len(clt.cluster_centers_)):
            allcols.append(rgb2hsv(clt.cluster_centers_[i]))
        dists=distance.cdist(allcols, allcols)
        distsr=[]
        for av in dists:
            for aa in av:
                distsr.append(aa)
        if((sorted(distsr)[len(dists):])[1]<15):
            clusters//=2
        if((sorted(distsr)[len(dists):])[1]<30):
            clusters-=1
        else:
            break


    quant = clt.cluster_centers_.astype("uint8")[labels]
    quant = quant.reshape((h, w, 3))
    image = image.reshape((h, w, 3))
    quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
    palette=dict()
    for it in range(len(quant)):
        i=quant[it]
        for jt in range(len(i)):
            j=i[jt]
            cor=tuple(j)
            score=pix_weight[it][jt]
            if cor in palette:
                palette[cor]=palette[cor]+score
            else:
                palette[cor]=score
    for key in palette:
        palette[key]=palette[key]/sumPixels
    palette=dict(sorted(palette.items(), key=lambda item: item[1])[::-1])
    pw=(pix_weight/255)**(4/5)
    pw=cv2.merge([pw,pw,pw])
    quantpreview=quant*pw
    return palette

def getObjectColorHSV(image):
    palette = getPalette(image)
    vals = []
    cols = []
    cols_r = []
    for i in palette.keys():
        vals.append(palette[i])
        cols_r.append(i)
        cols.append('#%02x%02x%02x' % i[::-1])

    plot_vals = np.array(vals)
    plot_cols = np.array(cols)

    carcolor = cols_r[0]

    return bgr2hsv(carcolor)

def getImageResolution(image):
    (h, w) = image.shape[:2]
    return (h,w)
def getImageSharpnessScore(imageIn):
    return cv2.Laplacian(imageIn, cv2.CV_64F).var()//1


@app.route("/predict_car", methods=['POST'])
@cross_origin()
def predict_car():
    clf = CatBoostRegressor()
    clf.load_model("FinalCarCatBoostModel")

    if clf:
        print('This is clf output', file=sys.stdout)
        try:
            json = request.get_json()
            print(json, file=sys.stdout)
            # model_columns = joblib.load("model_cols.pkl")

            # all these categories should be hashed by hasher before putting to the predict
            cat_text = ['CarName', 'fueltype', 'aspiration', 'doornumber',
                        'carbody', 'enginelocation', 'drivewheel', 'enginetype', 'cylindernumber', 'fuelsystem']


            temp = list(json[0].values())
            # temp = [4, 5, 5566, 6666, 5, 6, 9, 8, 6, 7666, 0, 27.8, -122.502, 7899, 6666]
            params = [
                "symboling",
                "CarName",
            "fueltype",
            "aspiration",
            "doornumber",
            "carbody",
            "drivewheel",
            "enginelocation",
            "wheelbase",
            "carlength",
            "carwidth",
            "carheight",
            "curbweight",
            "enginetype",
            "cylindernumber",
            "enginesize",
            "fuelsystem",
            "boreratio",
            "stroke",
            "compressionratio",
            "horsepower",
            "peakrpm",
            "citympg",
            "highwaympg",
            ]
            for i in range(len(temp)):
                if params[i] in cat_text:
                    temp[i] = hasher(temp[i])
            # print(clf.predict([3.0, 1.50, 1340, 7912, 1.5, 0, 0, 3, 1340, 0, 1955, 2005, -122.338866, 47.765807]), file=sys.stdout)
            # vals = np.array(temp).reshape(1, len(temp))

            temp.extend(car_img[0])

            prediction = clf.predict(temp)
            print(prediction, file=sys.stdout)

            app.logger.info('testing info log')
            return jsonify({'prediction': str(prediction)})

        except:
            print('This is exceptional output ', traceback.format_exc(), file=sys.stdout)
            return jsonify({'trace': traceback.format_exc()})
    else:
        return ('No model here to use')

    # for Cars
    # clf.predict(symboling,CarName,fueltype,aspiration,doornumber,carbody,drivewheel,
    # enginelocation,wheelbase,carlength,carwidth,carheight,curbweight,enginetype,
    # cylindernumber,enginesize,fuelsystem,boreratio,stroke,compressionratio,horsepower,peakrpm,
    # citympg,highwaympg,colorH,colorS,colorV,imgSharpness,imgResX,imgResY)



    # # There should be a path to the jpg file(car photo)
    # image = cv2.imread('photos/1.jpg', cv2.IMREAD_COLOR)
    #
    # colorFinal = getObjectColorHSV(image)
    # imgRes = getImageResolution(image)
    #
    # # Info for prediction(last 6 parameters)
    # imgSharpness = getImageSharpnessScore(image)
    # colorH = colorFinal[0]
    # colorS = colorFinal[1]
    # colorV = colorFinal[2]
    # imgResX = imgRes[0]
    # imgResY = imgRes[1]
    #
    # # example
    # clf.predict()
@app.route("/car_image", methods=['POST'])
@cross_origin()
def car_image():
    path = ""

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "No file found"
        user_file = request.files['file']
        temp = request.files['file']
        if user_file.filename == "":
            return "file name not found …"
        else:
            path = os.path.join(os.getcwd() + '\\modules\\static\\' + user_file.filename)
            user_file.save(path)
        # There should be a path to the jpg file(car photo)
        image = cv2.imread('path', cv2.IMREAD_COLOR)

        colorFinal = getObjectColorHSV(image)
        imgRes = getImageResolution(image)

        # Info for prediction(last 6 parameters)
        imgSharpness = getImageSharpnessScore(image)
        colorH = colorFinal[0]
        colorS = colorFinal[1]
        colorV = colorFinal[2]
        imgResX = imgRes[0]
        imgResY = imgRes[1]

        car_img[0]=[imgSharpness,colorH, colorS, colorV, imgResX, imgResY]
        print(car_img[0], file=sys.stdout)


if __name__ == '__main__':
    app.run(debug=False)

# app.run(host='0.0.0.0', port=5000)
