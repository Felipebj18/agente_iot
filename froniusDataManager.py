import time
import requests
import json
from dwInsertions import dw_insertions
from getJson import load_data

def getData(urls):
    # print(urls)
    import requests
    for nombre_url,url in urls.items():
        response = requests.get(url)

        if response.status_code == 200:#si la petición es exitosa
            data = response.json()
            # print(data)
            extraerDatosFroniusDataManager(data)
            # print("Los datos de la URL ", nombre_url, "son:")
            print()
            # return
        else:
            print("Error en la solicitud. Código de error:", response.status_code)
            # return
    return
        
#print(metodoGet("http://10.60.32.30/solar_api/v1/GetSensorRealtimeData.cgi?DataCollection=NowSensorData&Scope=System"))

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
        
        # print("Fronius Data Manager:")
        # print(f"Respuesta: {respuesta.text}")
        print("Fronius Data Manager")
        print(respuesta.status_code)
        if respuesta.status_code == 204:
            # print("Fronius Data Manager")
            # print(respuesta.status_code)
            return "Solicitud PATCH exitosa."
        else:
            return f"Error en la solicitud PATCH. Código de estado: {respuesta.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"



def extraerDatosFroniusDataManager(json_froniusDM):#json_froniusDM es el json obtenido de aplicar la función metodoGet con la url del fronius data manager como parámetro
    from datetime import datetime, timedelta
    
    # params = {
    #     "DataCollection": "NowSensorData",
    #     "Scope": "System"
    # }

    
    data = json_froniusDM
    # timestamp = data['Head']['Timestamp']
    # dt = datetime.fromisoformat(timestamp)
    # fecha = dt.strftime("Timestamp: %Y-%m-%d %H:%M:%S")
#     {
#     "Radiacion": {
#         "type": "Number",
#         "value": 344,
#         "metadata": {}
#     },
#     "Temperatura_1": {
#         "type": "Number",
#         "value": 59.96724,
#         "metadata": {}
#     },
#     "Temperatura_2": {
#         "type": "Number",
#         "value": 1.8852,
#         "metadata": {}
#     }
# }
    # print(data['Body']['Data']['1']['0']['Value'])
    # print(data['Body']['Data']['1']['1'])
    # print(data['Body']['Data']['1']['2'])
    Temperatura_1 = data['Body']['Data']['1']['0']['Value']
    Temperatura_2 = data['Body']['Data']['1']['1']['Value']
    Radiacion = data['Body']['Data']['1']['2']['Value']

    # print(Temperatura_1)
    # print(Temperatura_2)
    # print(Radiacion)
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
        # 'Timestamp' : fecha
    }
    # print("FRONIUS DATA MANAGER")
    # print(data_final)
    metodo_patch(data_final)
    return data_final