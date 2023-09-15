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

def extrerDatosFronisDevices(json_froniusDevice):
    try:
        data = json_froniusDevice["Body"]["Data"]
        device_info = json_froniusDevice["Head"]["RequestArguments"]
        time_stamp = json_froniusDevice["Head"]["Timestamp"]
        data_final = {
            "DAY_ENERGY": data["DAY_ENERGY"],
            "DEVICE_STATUS": data["DeviceStatus"],
            "FAC": data["FAC"],
            "IAC": data["IAC"],
            "IDC": data["IDC"],
            "PAC": data["PAC"],
            "TOTAL_ENERGY": data["TOTAL_ENERGY"],
            "UAC": data["UAC"],
            "UDC": data["UDC"],
            "YEAR_ENERGY": data["YEAR_ENERGY"],
            "DeviceClass": device_info["DeviceClass"],
            "DeviceId": device_info["DeviceId"],
            "Timestamp": time_stamp
        }
        print("FRONIUS DEVICE:")
        print(data_final)
        crearPostJSON(data_final)
        # return data_final
        return
    except Exception as e:
        print(f"Se produjo una excepción en la variable '{e.args[0]}' y el DeviceId es '{device_info['DeviceId']}'")


# def crearPostJSON(data_final):
#     post_json = {}

#     for key, value in data_final.items():
#         post_value = {"type": "Number"}

#         if isinstance(value, dict):
#             post_value["value"] = value.get("Value", None)
#         else:
#             post_value["value"] = value

#         post_json[key] = post_value

#     print(post_json)
#     return post_json

def crearPostJSON(data_final):
    post_json = {}

    for key, value in data_final.items():
        if key == "Timestamp" or key == "DeviceClass" or key == "DeviceId":
            continue  # Ignorar la llave "Timestamp"
        
        post_value = {"type": "Number"}

        if key == "DEVICE_STATUS":
            status_code = value.get("StatusCode", None)
            if status_code is not None:
                post_value["value"] = status_code
                post_json[key] = post_value
        elif isinstance(value, dict):
            post_value["value"] = value.get("Value", None)
            post_json[key] = post_value
        else:
            post_value["value"] = value
            post_json[key] = post_value

    print(post_json)
    return post_json

# Con esta actualización, si "DEVICE_STATUS" no está presente en "data_final" o si "StatusCode" es None en "DEVICE_STATUS", entonces "DEVICE_STATUS" en "post_json" será None. De lo contrario, se almacenará el valor del "StatusCode" en "DEVICE_STATUS".










