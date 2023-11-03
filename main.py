import time
import threading
import fronius
import froniusDataManager
import enphaseManager
import InsertFacts

import json

import requests
import json

# def enviar_datos_post(url, datos):
#     try:
       
#         cabeceras = {
#             "Content-Type": "application/json"
#         }

        
#         respuesta = requests.post(url, data=json.dumps(datos), headers=cabeceras)

        
#         if respuesta.status_code == 200:
#             return "Solicitud POST exitosa."
#         else:
#             return f"Error en la solicitud POST. Código de estado: {respuesta.status_code}"
#     except Exception as e:
#         return f"Error: {str(e)}"




# Abre el archivo JSON
def openJson(fileName):
    with open(fileName, 'r') as archivo_json:
        datos = json.load(archivo_json)

    return datos

# Tiempo entre consultas (30 segundos en este caso)
intervalo_consulta = 30

def setupThread(getDataFunction, url):
    while True:
        getDataFunction(url)
        time.sleep(intervalo_consulta)

def setupThreadEnphase(getDataFunction):
    while True:
        getDataFunction()
        time.sleep(intervalo_consulta) #Se debe actualizar a 5 min

def setupThreadInsertFacts():
    while True:
        InsertFacts.insertIntoDwh()
        time.sleep(intervalo_consulta)

        
if __name__ == "__main__":
    '''
    En los args hay que pasar la URLS
    '''
    # SE ADQUIEREN LAS URL EN JSON
    urls_fronius = openJson('./urlsFronius.json')
    # print(urls_fronius)
    urls_fronius_data_manager = openJson('./urlsFroniusDataManager.json')
    # print(urls_fronius_data_manager)
    thread_fronius = threading.Thread(
        target=setupThread,
        args=(fronius.getData, urls_fronius)
    )
    # executeThread()
    
    thread_froniusDataManager = threading.Thread(
        target=setupThread,
        args=(froniusDataManager.getData, urls_fronius_data_manager)
    )

    thread_enphaseManager = threading.Thread(
        target=setupThreadEnphase,
        args=(enphaseManager.getData,)
    )

    # ####################################
    thread_insert_dwh = threading.Thread(
        target=setupThreadInsertFacts
    )

    # ####################################


    thread_fronius.start()
    thread_froniusDataManager.start()
    thread_enphaseManager.start()
    thread_insert_dwh.start()

    # Mantén el programa principal en ejecución
    thread_fronius.join()
    thread_froniusDataManager.join()
    thread_enphaseManager.join()
    thread_insert_dwh.join()


