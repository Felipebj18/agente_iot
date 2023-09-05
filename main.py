import time
import threading
import fronius
import froniusDataManager

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
    thread_fronius = threading.Thread(
        target=setupThread,
        args=(fronius.getData, "http://10.60.63.10/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceId=1&DataCollection=CommonInverterData")
    )
    
    thread_froniusDataManager = threading.Thread(
        target=setupThread,
        args=(froniusDataManager.getData, "http://10.60.32.30/solar_api/v1/GetSensorRealtimeData.cgi?DataCollection=NowSensorData&Scope=System")
    )

    thread_fronius.start()
    thread_froniusDataManager.start()

    # Mantén el programa principal en ejecución
    thread_fronius.join()
    thread_froniusDataManager.join()


