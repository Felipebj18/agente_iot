import time

def getData(urls):
    print(urls)
    import requests
    for nombre_url,url in urls.items():
        response = requests.get(url)

        if response.status_code == 200:#si la petición es exitosa
            data = response.json()
            extrerDatosFronisDevices(data)
            print("Los datos de la URL ", nombre_url, "son:")
            print()
        else:
            print("Error en la solicitud. Código de error:", response.status_code)
        
#print(metodoGet("http://10.60.32.30/solar_api/v1/GetSensorRealtimeData.cgi?DataCollection=NowSensorData&Scope=System"))

def extrerDatosFronisDevices(json_froniusDevice):#json_froniusDevice es el json obtenido de aplicar la función metodoGet con la url del fronius device como parámetro
    data = json_froniusDevice["Body"]["Data"]
    device_info = json_froniusDevice["Head"]["RequestArguments"]
    time_stamp = json_froniusDevice["Head"]["Timestamp"]
    data_final = {
        
    "DAY_ENERGY":data["DAY_ENERGY"],
    "DEVICE_STATUS" : data["DeviceStatus"],
    "FAC" : data["FAC"],
    "IAC" : data["IAC"],
    "IDC" : data["IDC"],
    "PAC" : data["PAC"],
    "TOTAL_ENERGY":data["TOTAL_ENERGY"],
    "UAC" : data["UAC"],
    "UDC" : data["UDC"],
    "YEAR_ENERGY":data["YEAR_ENERGY"],
    "DeviceClass" : device_info["DeviceClass"],
    "DeviceId" : device_info["DeviceId"],
    "Timestamp": time_stamp   
    }
    print("FRONIUS DEVICE:")
    print(data_final)
    return data_final

