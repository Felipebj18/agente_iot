from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import requests
from dwInsertions import dw_insertions
from getJson import load_data

microInvertersData = {}

# Función para desplazarse hasta que el elemento sea visible
def scroll_to_element(driver, element):
    try:
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.perform()
    except Exception as e:
        print()

# Opciones para ejecutar Firefox en modo headless
firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True

# Credenciales de inicio de sesión
usuario = "microredupb@gmail.com"
contraseña = "MicroRedUPB0."

# URL de inicio de sesión
url_login = "https://enlighten.enphaseenergy.com/login/"

def getData():
    # Crear una instancia del navegador en modo headless
    driver = webdriver.Firefox(options=firefox_options)
    driver.maximize_window()

    # Navegar a la página de inicio de sesión
    driver.get(url_login)

    # Ingresar el nombre de usuario y la contraseña
    driver.find_element_by_xpath('//*[@id="user_email"]')\
        .send_keys(usuario)
    driver.find_element_by_xpath('//*[@id="user_password"]')\
        .send_keys(contraseña)

    # Hacer clic en el botón de inicio de sesión
    driver.find_element_by_xpath('//*[@id="submit"]')\
        .click()

    url_pagina_objetivo = "https://enlighten.enphaseenergy.com/systems/256274/devices?status=active"
    driver.get(url_pagina_objetivo)

    #buscar energía total
    time.sleep(2)
    totalEnergyElement = driver.find_element_by_xpath('//*[@id="energy_lifetime"]/div[2]/div/div/span[1]')
    units = totalEnergyElement.get_attribute('data-units')
    EnergyTotal = totalEnergyElement.get_attribute('data-value')

    # Buscar el elemento de energía de hoy
    energyTodayElement = driver.find_element_by_xpath('//*[@id="energy_today"]/div[2]/div[1]/div/span[1]')
    EnergyDay = energyTodayElement.get_attribute('data-value')
    energyTodayUnit = energyTodayElement.get_attribute('data-units')

    # Encontrar la tabla de microinversores
    microInvertersTable = driver.find_element_by_xpath('//*[@id="user_pcu_devices_datatables"]/tbody')

    # Localizar el elemento select
    select_element = driver.find_element_by_xpath('//*[@id="user_pcu_devices_datatables_length"]/label/select')

    # Seleccionar la opción que muestra 25 elementos
    scroll_to_element(driver, select_element)
    option_to_select = select_element.find_element_by_xpath('//option[text()="25"]')
    option_to_select.click()

    # Esperar un breve momento para que la página se actualice con la nueva opción
    time.sleep(2)

    # Inicializar una variable para el total de potencia
    PAC = 0

    # Iterar a través de las filas de la tabla (20 filas en total)
    for i in range(1, 21):
            # Encontrar el elemento NumSerie
            serialIDXPath = '//*[@id="user_pcu_devices_datatables"]/tbody/tr[{0}]/td[2]/div/a'.format(i)
            tempWebElementSerialID = driver.find_element_by_xpath(serialIDXPath)
            scroll_to_element(driver, tempWebElementSerialID)  # Desplazar hasta que el elemento sea visible
            numSerie = tempWebElementSerialID.text

            # Encontrar el elemento PotenciaGenerada
            valueXPath = '//*[@id="user_pcu_devices_datatables"]/tbody/tr[{0}]/td[5]/span'.format(i)
            tempWebElementValue = driver.find_element_by_xpath(valueXPath)
            scroll_to_element(driver, tempWebElementValue)  # Desplazar hasta que el elemento sea visible
            potenciaGenerada = float(tempWebElementValue.text)

            # Agregar los datos al diccionario
            microInvertersData[numSerie] = potenciaGenerada

            # Agregar la potencia generada a la variable totalPower
            PAC += potenciaGenerada

    createPostJSON(EnergyDay, EnergyTotal, PAC, microInvertersData)

    driver.quit()
    return

def createPostJSON(EnergyDay, EnergyTotal, PAC, microInvertersData):
    json_data = {
        "EnergyDay": {
            "type": "Number",
            "value": EnergyDay,
            "metadata": {}
        },
        "EnergyTotal": {
            "type": "Number",
            "value": EnergyTotal,
            "metadata": {}
        },
        "PAC": {
            "type": "Number",
            "value": PAC,
            "metadata": {}
        }
    }

    num_series = list(microInvertersData.keys())[:20] 
    for i, numSerie in enumerate(num_series, 1):
        key = "P_I{}".format(i)
        value = microInvertersData.get(numSerie, 0.0) 
        json_data[key] = {
            "type": "Number",
            "value": value,
            "metadata": {
            }
        }

    # Convertir el diccionario en formato JSON
    json_str = json.dumps(json_data, indent=4)

    actualizarEntidad(json_str)
    return

def actualizarEntidad(json_data):
    db_params = {
    "host": "54.145.74.186",
    "port": 5555,
    "database": "postgres",
    "user": "postgres",
    "password": "post123"
    }

    dw = dw_insertions(db_params)

    enphaseData = load_data("./urlOCBEnphase.json")

    try:
        url = 'http://54.145.74.186:1026/v2/entities/Enphase_1/attrs'
        
        response = requests.patch(url, data=json_data, headers={'Content-Type': 'application/json'})
        
        dw.insert_enphase(enphaseData)
        return
        
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")

