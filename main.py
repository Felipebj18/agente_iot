import time
import threading
import fronius
import froniusDataManager
import enphaseManager
import InsertFacts
import json

def openJson(fileName):
    with open(fileName, 'r') as archivo_json:
        datos = json.load(archivo_json)

    return datos

intervalo_consulta = 30

def setupThread(getDataFunction, url):
    while True:
        getDataFunction(url)
        time.sleep(intervalo_consulta)

def setupThreadEnphase(getDataFunction):
    while True:
        getDataFunction()
        time.sleep(intervalo_consulta)

def setupThreadInsertFacts():
    while True:
        InsertFacts.insertIntoDwh()
        time.sleep(intervalo_consulta)

        
if __name__ == "__main__":
    urls_fronius = openJson('./urlsFronius.json')
    urls_fronius_data_manager = openJson('./urlsFroniusDataManager.json')

    thread_fronius = threading.Thread(
        target=setupThread,
        args=(fronius.getData, urls_fronius)
    )
    
    thread_froniusDataManager = threading.Thread(
        target=setupThread,
        args=(froniusDataManager.getData, urls_fronius_data_manager)
    )

    thread_enphaseManager = threading.Thread(
        target=setupThreadEnphase,
        args=(enphaseManager.getData,)
    )

    thread_insert_dwh = threading.Thread(
        target=setupThreadInsertFacts
    )

    thread_fronius.start()
    thread_froniusDataManager.start()
    thread_enphaseManager.start()
    thread_insert_dwh.start()

    thread_fronius.join()
    thread_froniusDataManager.join()
    thread_enphaseManager.join()
    thread_insert_dwh.join()


