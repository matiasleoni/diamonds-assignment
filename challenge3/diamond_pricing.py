from joblib import load

import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression



import os

my_pipe = load('my_pipeline.joblib')

if(os.name == 'posix'):
   os.system('clear')
else:
   os.system('cls')


print('--------------------------------------------------------------------------------------------------')
while True:
  a_carat = input('Introduce Carat of the Diamond (should be a number > 0) and press enter:')
  try:
    a_carat = float(a_carat)
    break
  except ValueError:
    print('You must introduce a number. Please try again.')
    pass
print('--------------------------------------------------------------------------------------------------')
while True:
  a_color = input('Enter the Diamond Color (a letter from D to J) and press enter:')
  if a_color.upper() in list('DEFGHIJ'):
    break
  else:
    print(f'{a_color} is not a correct value. Please try again.')
print('--------------------------------------------------------------------------------------------------')
while True:
  print('Possible values of a Diamond Clarity are: I1, IF, SI1, SI2, VS1, VS2, VVS1, VVS2')
  a_clarity = input('Enter the Diamond Clarity and press enter:')
  if a_clarity.upper() in ["I1", "IF", "SI1", "SI2", "VS1", "VS2", "VVS1", "VVS2"]:
    break
  else:
    print(f'{a_clarity} is not a correct value. Please try again.')


data = pd.DataFrame([[a_carat, a_color.upper(), a_clarity.upper()]], columns = ['carat', 'color', 'clarity'])

a_price = np.exp(my_pipe.predict(data)[0])

to_format = (a_carat, a_color.upper(), a_clarity.upper(), a_price)

print('--------------------------------------------------------------------------------------------------')
print("The estimation for the value of a diamond with") 
print("{0} carats, {1} color and {2} clarity is ${3:,.2f}".format(*to_format))
