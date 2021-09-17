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
