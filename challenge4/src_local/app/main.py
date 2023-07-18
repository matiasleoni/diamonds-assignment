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





### API GET on root. It responds with HTML with basic instructions.
@app.get("/")
async def root():
    return HTMLResponse(content = root_html_code)


### API GET to price a Diamond
@app.get("/pricing/{carat}/{color}/{clarity}")
def pricing(carat, color, clarity):
    control = True
    try:
        carat = float(carat)
    except ValueError:
        control = False
        error_msg = 'You must introduce a number for carat. Please try again.'    
    if color.upper() not in list('DEFGHIJ'):
        control = False
        error_msg = f'{color} is not a correct value for color. Please use a letter from D to J.'
    if clarity.upper() not in ["I1", "IF", "SI1", "SI2", "VS1", "VS2", "VVS1", "VVS2"]:
        control = False
        error_msg = f'{clarity} is not a correct value for clarity. Please use I1, IF, SI1, SI2, VS1, VS2, VVS1, VVS2.'

    if control:
        data = pd.DataFrame([[carat, color, clarity]], columns = ['carat', 'color', 'clarity'])
        price = np.exp(my_pipe.predict(data)[0])
        dic_answer = {"Carat": carat, "Color": color, "Clarity": clarity, "Price": price}
    else:
        dic_answer = {"Carat": carat, "Color": color, "Clarity": clarity, "Price": error_msg}
    
    return dic_answer