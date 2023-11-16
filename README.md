# Agente IoT para Smart Energy Center - UPB

Este proyecto fue desarrollado para el Smart Energy Center (SEC) en el marco de la migración de la arquitectura de datos existente a una nueva arquitectura. Se centra específicamente en el Sistema Solar Fotovoltaico (SSFV) de la Universidad Pontificia Bolivariana (UPB).

## Descripción del Proyecto

El Sistema Solar Fotovoltaico (SSFV) de la UPB consta de 6 dispositivos Fronius, 1 dispositivo Fronius Data Manager y 1 dispositivo Enphase Manager, que administra 20 microinversores. Estos dispositivos proporcionan datos en tiempo real esenciales para la administración y la toma de decisiones informada sobre el SSFV.

## Solución y Arquitectura

La solución propuesta se integra a una arquitectura inteligente basada en Fiware, que incluye Orion Context Broker, Grafana, Quantumleap, CrateDB y MongoDB. Además, se incorporó una bodega de datos (DW) PostgreSQL a la arquitectura final.

## Funcionalidades del Agente IoT

### 1. Primer Proceso de ETL

Este proceso extrae datos desde las fuentes de datos, los limpia y transforma en un formato compatible con Orion Context Broker, y luego los envía al broker.

### 2. Segundo Proceso de ETL

Extrae datos desde Orion Context Broker, los transforma y limpia, y los carga en las dimensiones de la bodega de datos.

### 3. Tercer Proceso de ETL

Extrae datos de cada dimensión de la bodega de datos, calcula indicadores de interés para el SSFV, limpia y transforma, y finalmente carga los datos listos para ser visualizados en la tabla de hechos de la bodega de datos.

## Implementación Técnica

La aplicación realiza las siguientes operaciones:

- Extracción de dispositivos Fronius y Fronius Data Manager a través del protocolo TCP/IP con peticiones HTTP.
- Extracción de Enphase Manager mediante web scraping automatizado.

La aplicación hace uso de múltiples hilos para cada una de las funciones mencionadas.

## Restricciones

1. **Intranet de la UPB:** La aplicación funciona únicamente dentro de la intranet de la UPB debido a políticas de seguridad frente a las fuentes de datos.
   
2. **Nuevas Fuentes de Datos:** Agregar nuevas fuentes de datos es posible, pero deben ser del mismo tipo que las fuentes utilizadas previamente. La limpieza de datos requiere la conversión de un modelo particular de datos, y la lectura de datos del Enphase Manager se realiza mediante web scraping, lo que implica programar el proceso desde cero para cada nueva fuente.

## Despliegue de la Aplicación

Siga estos pasos para desplegar el Agente IoT:

1. Clone el repositorio: `git clone https://github.com/Felipebj18/agente_iot.git`
2. Navegue al directorio del proyecto: `cd Agente-IoT`
3. Instale las dependencias: `pip install -r requirements.txt`
4. Asegúrese de tener instalados **docker** y **docker-compose**, luego, ejecute el comando `docker-compose up`
5. Levante el agente ejecutando el comando: `python agente_iot.py`
6. Ingrese a la url `http://localhost:3000` para acceder al servicio de Grafana, en el cuál podrá crear los tableros y páneles que requiera

La aplicación **agente iot** se ejecutará directamente en la terminal y estará lista para su uso.

_Nota: La aplicación Agente IoT no se conteneriza, ya que no es un servicio web y se trata de una aplicación que se ejecuta en la terminal o consola._




