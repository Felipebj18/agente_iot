import requests
import json
from dwInsertions import dw_insertions
from getJson import load_data

def getData(urls):
    import requests
    for nombre_url,url in urls.items():
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            extraerDatosFroniusDataManager(data)
        else:
            print("Error en la solicitud. Código de error:", response.status_code)

    return
        
def metodo_patch(datos):
    server_ip = "54.145.74.186"
    device_id = "FroniusDM_1"

    db_params = {
    "host": "54.145.74.186",
    "port": 5555,
    "database": "postgres",
    "user": "postgres",
    "password": "post123"
    }

    dw = dw_insertions(db_params)

    froniusDM_data = load_data("./urlOCBFroniusDataManager.json")

    try:
        cabeceras = {
            "Content-Type": "application/json"
        }
        url = f"http://{server_ip}:1026/v2/entities/{device_id}/attrs"
        
        respuesta = requests.patch(url, data=json.dumps(datos), headers=cabeceras)
        dw.insert_froniusdm(froniusDM_data)
        
        if respuesta.status_code == 204:
            return "Solicitud PATCH exitosa."
        else:
            return f"Error en la solicitud PATCH. Código de estado: {respuesta.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"



def extraerDatosFroniusDataManager(json_froniusDM):
    from datetime import datetime, timedelta

    data = json_froniusDM

    Temperatura_1 = data['Body']['Data']['1']['0']['Value']
    Temperatura_2 = data['Body']['Data']['1']['1']['Value']
    Radiacion = data['Body']['Data']['1']['2']['Value']

    data_final = {
        'Temperatura_1' : {
            "type": "Number",
            "value": Temperatura_1
        },
        'Temperatura_2' : {
            "type": "Number",
            "value": Temperatura_2
        },
        'Radiacion' :{
            "type": "Number",
            "value": Radiacion
        }
    }

    metodo_patch(data_final)
    return data_final