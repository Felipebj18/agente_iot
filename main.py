import time
import threading
import fronius
import froniusDataManager

import json

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

    thread_fronius.start()
    thread_froniusDataManager.start()

    # Mantén el programa principal en ejecución
    thread_fronius.join()
    thread_froniusDataManager.join()


