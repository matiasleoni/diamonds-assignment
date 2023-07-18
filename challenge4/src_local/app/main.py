from fastapi import FastAPI

import pandas as pd
import numpy as np
from joblib import load

app = FastAPI()

my_pipe = load('app/my_pipeline.joblib')





from fastapi.responses import HTMLResponse

### get en el ROOT de la API. Debería dar instrucciones
@app.get("/")
async def root():
    ret='''
<html>
<body>
<h2>Hey User!</h2>
<p>For the API technical documentation visit /docs. <p/>
<p>You can use the API /pricing feature by selecting carat, 
color and clarity of the diamond in the html address itself. <p/>
<p>The API works with a GET request with URL parameters following the structure /pricing/{carat}/{color}/{clarity} </p>
<p>For example if you want to price a 2.5 carat diamond with color "F"
and clarity "VS1" you should request the address</p>
<ul>
    <li> /pricing/2.5/F/VS1</li>
</ul>
<p> and you will get the estimated price of the diamond. The API will respond with a JSON of the form:</p>
<ul>
    <li> {"Carat":2.5,"Color":"F","Clarity":"VS1","price":33980.43123071548}</li>
</ul>
<p> The value for the {carat} parameter should be a number. <p/>
<p> For {color}, it should be a letter from D to J.<p/>
<p> For clarity, one of the cathegories:  "I1", "IF", "SI1", "SI2", "VS1", "VS2", "VVS1", "VVS2".
<p/>
<a href = "mailto: matiasleoni@gmail.com">Admin Mail</a>
</body>
</html>
'''
    #my_dic = {"price": a_price}
    #return my_dic
    return HTMLResponse(content=ret)
#    return {"message": "Hello World, trial {}.".format(1)}


### get de la API para obtener recomendaciones dado un advertiser y un modelo
@app.get("/pricing/{carat}/{color}/{clarity}")
def reco(carat, color, clarity):
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
        dic_answer = {"Carat": carat, "Color": color, "Clarity": clarity, "price": price}
    else:
        dic_answer = {"Carat": carat, "Color": color, "Clarity": clarity, "price": error_msg}
    
    return dic_answer


### get de la API para obtener recomendaciones dado un advertiser y un modelo
'''@app.get("/history/{ADV}")
def historic(ADV):
    global contador_consultas_advertiser
    filter_dates_list = [(datetime.date.today()-num*datetime.timedelta(days=1)).strftime("%Y-%m-%d") for num in range(7)]
    filter_dates = str(filter_dates_list).replace("[","(").replace("]",")")
    

    query = f"""SELECT DISTINCT fecha, 'modeltop' as modelo, product_id from modeltop
    WHERE fecha IN{filter_dates} AND advertiser_id= '{ADV}'
    UNION
    SELECT DISTINCT fecha, 'modelctr' as modelo, product_id from modelctr
    WHERE fecha IN{filter_dates} AND advertiser_id= '{ADV}'"""

    engine = None
    try:
        engine = psycopg2.connect(**db_conf)
        consulta=engine.cursor()
        consulta.execute(query)
        rows = consulta.fetchall()
        lista_productos = []
        for row in rows:
            lista_productos.append(row)
        #result = {ADV: lista_productos}
        result = lista_productos
        consulta.close()
    except psycopg2.DatabaseError as error:
        result = {"Problema en la base de datos": "Consulte administrador."}
    finally:
        if engine is not None:
            engine.close()
    
    if type(result) == dict:
        dic_out = result
    elif type(result) == list:
        dic_out = {}
        for date in filter_dates_list:
            lista1 = []
            lista2 = []
            for line in result:
                if line[0] == date and line[1] == 'modeltop':
                    lista1.append(line[2])
                elif line[0] == date and line[1] == 'modelctr':
                    lista2.append(line[2])

            dic_out[date] = {"TopProduct": lista1, "TopCTR": lista2}

    contador_consultas_advertiser += 1
    return dic_out



@app.get("/stats")
def stats():
    #contador_consultas_modelo
      
    filter_date = (datetime.date.today()-0*datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    query1 = """WITH prov AS(
        SELECT DISTINCT advertiser_id FROM modeltop
        UNION
        SELECT DISTINCT advertiser_id FROM modelctr)
        SELECT COUNT(*) FROM prov"""
    query2 = f"""SELECT DISTINCT modelctr.advertiser_id, 
        modelctr.product_id as reco_ctr,
        modeltop.product_id as reco_top
    FROM modelctr
    JOIN modeltop ON modelctr.advertiser_id = modeltop.advertiser_id
    WHERE modelctr.product_id = modeltop.product_id
        and modelctr.fecha = '{filter_date}'
        and modeltop.fecha = '{filter_date}'
    ORDER BY advertiser_id"""
    
    engine = None
    try:
        engine = psycopg2.connect(**db_conf)
        consulta=engine.cursor()
        consulta.execute(query1)
        rows1 = consulta.fetchall()
        cantidad_advs = rows1[0][0]
        consulta.execute(query2)
        repetidos = consulta.fetchall()
        consulta.close()
    except psycopg2.DatabaseError as error:
        cantidad_advs = {"Problema en la base de datos": "Consulte administrador."}
        #print(error.pgerror.split("\n")[0])
    finally:
        if engine is not None:
            engine.close()
    
    lista_unicos = []
    for row in repetidos:
        lista_unicos.append(row[0])
    lista_unicos = set(lista_unicos)
    dic_out2 = {}
    for elem in lista_unicos:
        lista3 = []
        for row in repetidos:
            if row[0] == elem:
                lista3.append(row[1])
        dic_out2[elem]=lista3

    return {'Cantidad de advertisers':cantidad_advs, 
            "Número consultas /recommendations/": contador_consultas_modelo,
            "Número consultas /history/": contador_consultas_advertiser,
            "Advertiser con recos coincidentes": dic_out2 }'''

