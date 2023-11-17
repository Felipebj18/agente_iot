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



Información adicional sobre como cambiar las configuraciones del sistema y documentación del código puede encontrarla en nuestra [wiki](https://github.com/Felipebj18/agente_iot/wiki).
