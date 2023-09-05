import time

def getData(url):
    import requests
    response = requests.get(url)

    if response.status_code == 200:#si la petición es exitosa
        # data = response.json()
        # return data
        print("código 200")
        return
    else:
        print("Error en la solicitud. Código de error:", response.status_code)
        
#print(metodoGet("http://10.60.32.30/solar_api/v1/GetSensorRealtimeData.cgi?DataCollection=NowSensorData&Scope=System"))


def extraerDatosFroniusDataManager(json_froniusDM):#json_froniusDM es el json obtenido de aplicar la función metodoGet con la url del fronius data manager como parámetro
    import requests
    import json
    from datetime import datetime, timedelta

    
    params = {
        "DataCollection": "NowSensorData",
        "Scope": "System"
    }

    
    data = json_froniusDM
    timestamp = data['Head']['Timestamp']
    dt = datetime.fromisoformat(timestamp)
    fecha = dt.strftime("Timestamp: %Y-%m-%d %H:%M:%S")
    data_final = {
        'Temperatura_1' : data['Body']['Data']['1']['0'],
        'Temperatura_2' : data['Body']['Data']['1']['1'],
        'Radiacion' :data['Body']['Data']['1']['2'],
        'Timestamp' : fecha
    }
    return data_final



def imprimirFroniusDataManager(data):
    for key, value in data.items():
        if key == 'Timestamp':
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value['Value']} {value['Unit']}")

    

    
    
# imprimirFroniusDataManager(extraerDatosFroniusDataManager(metodoGet("http://10.60.32.30/solar_api/v1/GetSensorRealtimeData.cgi?DataCollection=NowSensorData&Scope=System")))