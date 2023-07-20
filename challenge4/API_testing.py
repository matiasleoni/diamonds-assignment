import pandas as pd
import numpy as np

import time

import requests
from ast import literal_eval

from joblib import load

# Dictionary of cathegories to be randomly chosen
cathegories = {'colors': list('DEFGHIJ'), 'clarities': ["I1","IF","SI1","SI2","VS1","VS2","VVS1","VVS2"]}

# Load trained Pipeline object
my_pipe = load('src_local/app/my_pipeline.joblib')


def random_URL():
    '''
    Generate a random URL for a pricing page using random values for carat, color, and clarity parameters.
    Parameters: None
    Return: url (str): A string representing the randomly generated URL following the format 
    "http://18.234.46.13/pricing/<carat>/<color>/<clarity>".
    '''
    # Generate a random carat value between 0 and 10
    carat = str(np.random.uniform(0,10))
    # Randomly choose a color from the 'colors' category
    color = np.random.choice(cathegories['colors'])
    # Randomly choose a clarity from the 'clarities' category
    clarity = np.random.choice(cathegories['clarities'])
    # Return the generated URL
    return "http://18.234.46.13/pricing/"+carat+"/"+color+"/"+clarity



number_of_tests= 10

# Construct a list of response dictionaries using number_of_tests random URLs
responses = []
for test in range(number_of_tests):
    URL = random_URL()
    print("Requesting: ", random_URL())
    initial_time = time.time()
    json_response = requests.get(URL).content
    final_time = time.time()
    print("Response time: {0:,.1f} seconds".format(final_time-initial_time))
    print("-----------------------------------------------------")
    dict_response = literal_eval(json_response.decode('utf-8'))
    responses.append(dict_response)

# drop the responses in a pandas dataframe to be able to compare the given price 
# with that predicted by the model
responses_df = pd.DataFrame(responses)
responses_df.columns= responses_df.columns.str.lower()

# count the number of correct API responses
correct_answers = (abs(np.exp(my_pipe.predict(responses_df))-responses_df['price']) < 10**(-8)).sum()

print("Number of tests performed: ", number_of_tests)

print("Number of tests passed: ", correct_answers)

if correct_answers == number_of_tests:
    print("FLAWLESS")
else:
    print("Some tests didn't pass. CHECK CODE")

    
