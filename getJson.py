import requests
import json

def get_json_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error retrieving data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# def openJson(fileName):
#     with open(fileName, 'r') as archivo_json:
#         datos = json.load(archivo_json)

#     return datos


def load_data(urls):
    
    with open(urls, 'r') as archivo_json:
        datos = json.load(archivo_json)
    final_dict={}
    for url_id in datos:
        url=datos[url_id]["url"]
        aux_data = get_json_from_url(url)
        result_dict = {}
        for key, value in aux_data.items():
            if isinstance(value, dict) and 'value' in value:
                # Si el valor es un diccionario con una clave "value", asigna ese valor
                result_dict[key] = value['value']
            else:
                result_dict[key] = value
        id=result_dict["id"]
        if 'id' in result_dict:
            result_dict.pop('id')
        final_dict[id]=result_dict
    return final_dict