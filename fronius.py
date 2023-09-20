import requests
import json

def getData(urls):
    print(urls)
    import requests
    for nombre_url,url in urls.items():
        response = requests.get(url)

        if response.status_code == 200:#si la petición es exitosa
            data = response.json()
            extrerDatosFronisDevices(data, url)
        else:
            print("Error en la solicitud. Código de error:", response.status_code)
        


def extrerDatosFronisDevices(json_froniusDevice, url):
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
        crearPostJSON(data_final, url)
        # return data_final
        return
    except Exception as e:
        print(f"Se produjo una excepción en la variable '{e.args[0]}' y el DeviceId es '{device_info['DeviceId']}'")


def crearPostJSON(data_final, url):
    # print("La URL es: ", url)
    deviceID = 0
    post_json = {}

    for key, value in data_final.items():
        if key == "Timestamp" or key == "DeviceClass" or key == "DeviceId" or key == "DEVICE_STATUS":
            if (key == "DeviceId"):
                deviceID = value
            continue  # Ignorar la llave "Timestamp"
        
        post_value = {"type": "Number"}

        if isinstance(value, dict):
            post_value["value"] = value.get("Value", None)
            post_json[key] = post_value
        else:
            post_value["value"] = value
            post_json[key] = post_value

    postUrl = transform_url(url, deviceID)
    actualizarEntidad(postUrl, post_json)
    return


def transform_url(url, deviceId):
    # Definir la IP fija Esta dirección IP está quemada en el código y debe llamarse desde archivo externo
    ip = "54.145.74.186"
    
    # Obtener la última parte de la URL original (DeviceId)
    parts = url.split("/")
    original_device_id = parts[-1].split("=")[-1]
    
    # Crear el nuevo DeviceId según las reglas dadas
    if url.startswith("http://10.60.63.10"):
        new_device_id = f"FronuisB18_{deviceId}"
    elif url.startswith("http://10.60.32.30"):
        new_device_id = f"FronuisB11_{deviceId}"
    else:
        raise ValueError("URL no válida")
    
    # Construir la nueva URL
    new_url = f"http://{ip}:1026/v2/entities/{new_device_id}/attrs"
    
    return new_url



def actualizarEntidad(url, json_data):
    try:
        print(url)
        # Convertir el diccionario en una cadena JSON con comillas dobles
        json_str = json.dumps(json_data).replace("'", "\"")
        print(json_str)
        
        # Realizar la petición HTTP PATCH con el JSON en el cuerpo del mensaje
        response = requests.patch(url, data=json_str, headers={'Content-Type': 'application/json'})
        
        # Imprimir el código de respuesta
        # print(f"Código de respuesta: {response.status_code}")
        
        # Imprimir la respuesta completa
        # print(f"Respuesta: {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")











