import time

def getData(urls):
    print(urls)
    import requests
    for nombre_url,url in urls.items():
        response = requests.get(url)

        if response.status_code == 200:#si la petición es exitosa
            data = response.json()
            extraerDatosFroniusDataManager(data)
            print("Los datos de la URL ", nombre_url, "son:")
            print()
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
    print("FRONIUS DATA MANAGER")
    print(data_final)
    return data_final