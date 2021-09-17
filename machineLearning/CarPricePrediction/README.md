# Machine learning for car price prediction

## Dataset
Dataset for teaching our ML model we got from [Kaggle - car price prediction](https://www.kaggle.com/hellbuoy/car-price-prediction). This dataset have 305 rows of information about different car with such data: symboling(Its assigned insurance risk rating, A value of +3 indicates that the auto is risky, -3 that it is probably pretty safe), car company, type of fuel, aspiration in a car, numbers of doors, body of car, type of drive wheel, location of car engine, wheel base of car, length of a car, width of a car, height of a car,
weight of a car without occupants or baggage, type of engine, cylinder placed in a car, size of a car, fuel system of a car, boreratio of a car, stroke or volume inside the engine, compression ratio of car, horsepower, car peak rpm, mileage in city, mileage on highway, price of a car. You can see dataset in file "CarPrice" and information about parameters in the file "DataDictionary".
In the dataset there was not car photos; and we decided to find photo of each car by our own. Also, we created script which can find color of a car from photo, sharpness and resolution. 3/4 of dataset we took for teaching ML and 1/4 for testing it. Final dataset you can see in file "carsWithAddInfo".

## Image process
We done python script image processing to transform image into car color, photo sharpness and resolution. Final code you can see in file "OneCarSetter".

### Color detection
First, the original image is filtered to clear artifacts and interference caused by high iso, poor lighting, or poor camera quality. To do this, a median filter is applied to the original image. Then the most interesting areas are highlighted in the image. To do this, each pixel of the image is center-weighted, as well as depending on its S and V components, when translated into the HSV color space, a weight is assigned. Then the prevailing colors are highlighted in the resulting image. To do this, pixels are considered as a weighted cloud of points in the color space, clusters are allocated in the cloud. The parameters are selected so that the Euclidean distance between the centers of these clusters in the HSV color space is greater than or equal to 30. The cluster that has the largest number of points in the resulting palette is considered the main color of the car

### Determining the sharpness of the image
To determine the sharpness of the image, the Laplace operator is used. It is enough to find the variance or calculate the difference between the lightest and darkest pixel in the resulting image

## CatBoost machine learning library
With cars CatBoost was not so good and got 54% of accuracy in test data. Code of teaching it you can see in file "CarPricePredictionLearn". 
Final model you can see in file "FinalCarCatBoostModel" and code for using it with image process you can see in file "ImportCarCatBoost".
