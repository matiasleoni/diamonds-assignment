
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression

from joblib import dump

import os


data = pd.read_csv("diamonds.csv")
data = data[['carat', 'color', 'clarity', 'price']]
data = data[(data['carat']>0) & (data['price']>0)].reset_index(drop= True)


#cath_columns = list(data.select_dtypes(include=[object]).columns)
#num_columns = list(data.select_dtypes(exclude=[object]).columns)

cath_preprocessor = OneHotEncoder()
num_preprocessor = FunctionTransformer(func = np.log, inverse_func = np.exp)#, feature_names_out = lambda x,y:(x,y))
regressor = LinearRegression()

preprocessor = ColumnTransformer(
    transformers=[
        ('num_preprocessor', num_preprocessor, ['carat']),
        ('cath_preprocessor', cath_preprocessor, ['color', 'clarity'])
    ])
my_pipe = Pipeline([('transformaciones', preprocessor),('regresion', regressor)])



X = data.drop(['price'], axis = 1)
y = np.log(data['price'])

my_pipe.fit(X,y)




if(os.name == 'posix'):
   os.system('clear')
else:
   os.system('cls')

print('--------------------------------------------------------------------------------------------------')
print('The data Pipeline processed and fitted the model with the Diamond features found in "diamonds.csv"')

print("The coefficient of determination of the regression is  R^2 = {0:.3f}".format(my_pipe.score(X,y)))
print('--------------------------------------------------------------------------------------------------')

dump(my_pipe, 'my_pipeline.joblib') 

print('')
print('The data pipeline of the model was saved in the file "my_pipeline.joblib"')
print('It can be loaded anytime to make a prediction.')
print('If new priced Diamonds want to be used to improve the model fit they have to be appended')
print('in the "diamonds.csv" file because the type of algorithm we used cannot learn incrementally.')
print('--------------------------------------------------------------------------------------------------')



