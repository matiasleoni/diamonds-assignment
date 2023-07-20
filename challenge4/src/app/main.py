from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import pandas as pd
import numpy as np
from joblib import load

app = FastAPI()

my_pipe = load('app/my_pipeline.joblib')

root_html_file = open('app/root.html', "r")
root_html_code = root_html_file.read()
root_html_file.close()



@app.get("/")
async def root():
    """
    API GET request to the root endpoint, responding with HTML containing basic instructions.
    Parameters:
        None
    Returns:
        fastapi.responses.HTMLResponse: An HTML response containing basic instructions.
    """
    return HTMLResponse(content = root_html_code)


@app.get("/pricing/{carat}/{color}/{clarity}")
def pricing(carat, color, clarity):
    """
    API GET request to price a Diamond based on carat, color, and clarity.
    Parameters:
        carat: The carat weight of the diamond. It should be a positive number.
        color: The color of the diamond. Should be a single uppercase letter from 'D' to 'J'.
        clarity: The clarity of the diamond. Should be one of 'I1', 'IF', 'SI1', 'SI2', 'VS1', 'VS2', 'VVS1', or 'VVS2'.
    Returns:
        dict: A dictionary containing the following information:
            - 'Carat': The carat weight of the diamond (float).
            - 'Color': The color of the diamond (str).
            - 'Clarity': The clarity of the diamond (str).
            - 'Price': The price of the diamond (float) if the input values are valid, or an error message (str) if any input is incorrect.
    """
    control = True
    # Check if carat is float
    try:
        carat = float(carat)
    except ValueError:
        control = False
        error_msg = 'You must introduce a number for carat. Please try again.'    
    # Check color is in list
    if color.upper() not in list('DEFGHIJ'):
        control = False
        error_msg = f'{color} is not a correct value for color. Please use a letter from D to J.'
    # Check clarity is in list
    if clarity.upper() not in ["I1", "IF", "SI1", "SI2", "VS1", "VS2", "VVS1", "VVS2"]:
        control = False
        error_msg = f'{clarity} is not a correct value for clarity. Please use I1, IF, SI1, SI2, VS1, VS2, VVS1, VVS2.'

    # If all checks passed, predict and present price (with input info), else show error.
    if control:
        data = pd.DataFrame([[carat, color, clarity]], columns = ['carat', 'color', 'clarity'])
        price = np.exp(my_pipe.predict(data)[0])
        dic_answer = {"Carat": carat, "Color": color, "Clarity": clarity, "Price": price}
    else:
        dic_answer = {"Carat": carat, "Color": color, "Clarity": clarity, "Price": error_msg}
    
    return dic_answer