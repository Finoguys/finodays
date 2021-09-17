# Our site for Finodays
https://finodays-website.web.app/
![image_2021-09-17_23-54-49](https://user-images.githubusercontent.com/24477376/133852625-bb7bd80f-d9b5-4abd-87f3-e8ca387897c8.png)



# Machine learning for car price prediction

## Dataset
Dataset for teaching our ML model we got from [Kaggle - car price prediction](https://www.kaggle.com/hellbuoy/car-price-prediction). This dataset have 305 rows of information about different car with such data: symboling(Its assigned insurance risk rating, A value of +3 indicates that the auto is risky, -3 that it is probably pretty safe), car company, type of fuel, aspiration in a car, numbers of doors, body of car, type of drive wheel, location of car engine, wheel base of car, length of a car, width of a car, height of a car,
weight of a car without occupants or baggage, type of engine, cylinder placed in a car, size of a car, fuel system of a car, boreratio of a car, stroke or volume inside the engine, compression ratio of car, horsepower, car peak rpm, mileage in city, mileage on highway, price of a car. You can see dataset in file "CarPrice" and information about parameters in the file "DataDictionary".
In the dataset there was not car photos; and we decided to find photo of each car by our own. Also, we created script which can find color of a car from photo, sharpness and resolution. Photos you can see in folder photos. 3/4 of dataset we took for teaching ML and 1/4 for testing it. Final dataset you can see in file "carsWithAddInfo".

## Image process
We done python script image processing to transform image into car color, photo sharpness and resolution. Final code you can see in file "OneCarSetter".
![photo_2021-09-17_23-52-03](https://user-images.githubusercontent.com/24477376/133852231-dd8498af-8d09-4f0d-9d1a-a876d8d99497.jpg)
![photo_2021-09-17_23-51-57](https://user-images.githubusercontent.com/24477376/133852241-d046936a-32d3-4ddb-8623-cc24c26120fc.jpg)


### Color detection
First, the original image is filtered to clear artifacts and interference caused by high iso, poor lighting, or poor camera quality. To do this, a median filter is applied to the original image. Then the most interesting areas are highlighted in the image. To do this, each pixel of the image is center-weighted, as well as depending on its S and V components, when translated into the HSV color space, a weight is assigned. Then the prevailing colors are highlighted in the resulting image. To do this, pixels are considered as a weighted cloud of points in the color space, clusters are allocated in the cloud. The parameters are selected so that the Euclidean distance between the centers of these clusters in the HSV color space is greater than or equal to 30. The cluster that has the largest number of points in the resulting palette is considered the main color of the car

### Determining the sharpness of the image
To determine the sharpness of the image, the Laplace operator is used. It is enough to find the variance or calculate the difference between the lightest and darkest pixel in the resulting image

## CatBoost machine learning library
With cars CatBoost was not so good and got 54% of accuracy in test data. Code of teaching it you can see in file "CarPricePredictionLearn". 
Final model you can see in file "FinalCarCatBoostModel" and code for using it with image process you can see in file "ImportCarCatBoost".

# Machine learning for house price prediction

## Dataset
Dataset for teaching our ML model we got from [Kaggle - house price prediction](https://www.kaggle.com/shree1992/housedata). This dataset have 4600 rows of information about USA
houses with such data: price of house, number of bedrooms and bathrooms, footage of home and lot, number of floors, having or not water view, has been viewed or not, overall conditon, 
square footage of house apart from basement, square footage of the basement, built year, renovated year, street, city, statezip and country.
In the dataset there was only address in format of street, city, statezip and country; and we decided to transform address to the latitude and longitude because numbers
can give more information than words. We done it by [Mapbox](https://www.mapbox.com/). 3/4 of dataset we took for teaching ML and 1/4 for testing it.

## Machine learning library
### RandomForest
For the first time we tried to use RandomForestRegressor library. Results was not so bad and we reseived 60% of accuracy but it is not enough and we moved to another library. 
Code of teaching it you can see in file "RandomForestHousePriceLearning". Model you can see in file "RandomForestModel"
### CatBoost
CatBoost immediately after first teaching gave 89% of accuracy in test data. Code of teaching it you can see in file "HousePriceMLLearning". 
Final model you can see in file "modelForHousePrediction" and code for using it with mapbox address transformation in file "ImportCatBoostWithMLModel"

