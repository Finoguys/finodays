# import the necessary packages
import colorsys
import math

from scipy.spatial import distance
from sklearn.cluster import MiniBatchKMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2

def bgr2hsv(bgr):
    return rgb2hsv([bgr[2],bgr[1], bgr[0]])

def rgb2hsv(rgb):
    red=rgb[0]
    green=rgb[1]
    blue=rgb[2]
    red_percentage = red / float(255)
    green_percentage = green / float(255)
    blue_percentage = blue / float(255)

    # get hsv percentage: range (0-1, 0-1, 0-1)
    color_hsv_percentage = colorsys.rgb_to_hsv(red_percentage, green_percentage, blue_percentage)

    # get normal hsv: range (0-360, 0-255, 0-255)
    color_h = round(360 * color_hsv_percentage[0])
    color_s = round(100 * color_hsv_percentage[1])
    color_v = round(100 * color_hsv_percentage[2])
    color_hsv = (color_h, color_s, color_v)
    return color_hsv


def getPalette(imageIn):
    imageRes=cv2.resize(imageIn,(640,480))
    (h, w) = imageRes.shape[:2]
    #image = cv2.bilateralFilter(image, 15, 75, 75)
    image = cv2.medianBlur(imageRes, (max(h,w)//70)//2*2+1)
    imagehsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    sumPixels=h*w
    # convert the image from the RGB color space to the L*a*b*
    # color space -- since we will be clustering using k-means
    # which is based on the euclidean distance, we'll use the
    # L*a*b* color space where the euclidean distance implies
    # perceptual meaning
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    # reshape the image into a feature vector so that k-means
    # can be applied
    pix_weight=np.ndarray([h,w])
    for am in range(h):
        for bm in range(w):
            pix_weight[am][bm]=((min(am,bm,h-am,w-bm)/(min(w,h)/2)*
                                 ((imagehsv[am][bm][1]/255*imagehsv[am][bm][2]/255))**(1/10)))**4
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    pix_weight_1d = pix_weight.reshape((pix_weight.shape[0] * pix_weight.shape[1]))
    # apply k-means using the specified number of clusters and
    # then create the quantized image based on the predictions
    clusters=32
    while(clusters>2):
        clt = MiniBatchKMeans(n_clusters=clusters)
        labels = clt.fit_predict(image,sample_weight=pix_weight_1d)
        #labels = clt.fit_predict(image)
        allcols=[]
        for i in range(len(clt.cluster_centers_)):
            allcols.append(rgb2hsv(clt.cluster_centers_[i]))
        dists=distance.cdist(allcols, allcols)
        distsr=[]
        for av in dists:
            for aa in av:
                distsr.append(aa)
        #print(sorted(distsr)[len(dists):])
        #print(clusters)
        #print()
        if((sorted(distsr)[len(dists):])[1]<15):
            clusters//=2
        if((sorted(distsr)[len(dists):])[1]<30):
            clusters-=1
        else:
            break


    quant = clt.cluster_centers_.astype("uint8")[labels]
    # reshape the feature vectors to images
    quant = quant.reshape((h, w, 3))
    image = image.reshape((h, w, 3))
    # convert from L*a*b* to RGB
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
    #cv2.imshow("image", np.hstack([imageRes/255, quantpreview]))
    return palette

def getObjectColorHSV(image):
    palette = getPalette(image)
    # carcolorslice=list(palette.keys())[0:2]
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


from pandas import read_csv as read
path = "CarPrice.csv"
data = read(path, delimiter=",")

j = 204
image = cv2.imread('photos/'+str(j)+'.jpg', cv2.IMREAD_COLOR)
print(getImageSharpnessScore(image))
print(getObjectColorHSV(image))
print(getImageResolution(image))

