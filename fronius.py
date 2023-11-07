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
            extrerDatosFronisDevices(data, url)
        else:
            print("Error en la solicitud. Código de error:", response.status_code)
    return


def extrerDatosFronisDevices(json_froniusDevice, url):
    try:
        data = json_froniusDevice["Body"]["Data"]
        device_info = json_froniusDevice["Head"]["RequestArguments"]
        time_stamp = json_froniusDevice["Head"]["Timestamp"]
        deviceID = int(device_info["DeviceId"])
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
            "DeviceId": deviceID,
            "Timestamp": time_stamp
        }
        crearPostJSON(data_final, url)
        return
    except Exception as e:
        print("Error en ", url)
        print(f"Se produjo una excepción en la variable '{e.args[0]}' y el DeviceId es '{device_info['DeviceId']}'")
        return


def crearPostJSON(data_final, url):
    try:
        deviceID = 0
        post_json = {}

        for key, value in data_final.items():
            if key == "Timestamp" or key == "DeviceClass" or key == "DeviceId" or key == "DEVICE_STATUS":
                if (key == "DeviceId"):
                    deviceID = value
                continue
            
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
    except Exception as e:
        print("Error creando el JSON del post a OCB: ", e)


def transform_url(url, deviceId):
    try:
        ip = "54.145.74.186"
        parts = url.split("/")
        original_device_id = parts[-1].split("=")[-1]
        
        if url.startswith("http://10.60.63.10"):
            new_device_id = f"FroniusB18_{deviceId}"
        elif url.startswith("http://10.60.32.30"):
            new_device_id = f"FroniusB11_{deviceId}"
        else:
            raise ValueError("URL no válida")

        new_url = f"http://{ip}:1026/v2/entities/{new_device_id}/attrs"
        
        return new_url
    except Exception as e:
        print("Error en transform al transformar la URL: ", e)



def actualizarEntidad(url, json_data):
    db_params = {
    "host": "54.145.74.186",
    "port": 5555,
    "database": "postgres",
    "user": "postgres",
    "password": "post123"
    }


    dw = dw_insertions(db_params)

    fronius_data = load_data("./urlOCBFronius.json")

    try:
        json_str = json.dumps(json_data).replace("'", "\"")

        response = requests.patch(url, data=json_str, headers={'Content-Type': 'application/json'})
        
        dw.insert_fronius(fronius_data)

        return
        
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")
        return











