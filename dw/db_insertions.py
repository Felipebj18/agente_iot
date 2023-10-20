import psycopg2
from random import random
from datetime import datetime

# Datos de conexión a la base de datos
db_params = {
    "host": "nombre_de_tu_servidor_de_db",  # Cambia esto al host correcto
    "database": "DW_SSFV",
    "user": "tu_usuario_de_db",
    "password": "tu_contraseña_de_db"
}

# Conexión a la base de datos
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

#CREACIÓN DE LAS VARIABLES 
# DIM_Enphase
e_energy_day = random() * 100
e_pac = random() * 100
p_i1 = random() * 10
e_nominal_power = random() * 1000  
e_timestamp = datetime.now()
# Añadir los otros campos

# DIM_FroniusDevice
fd_energy_day = random() * 100
fd_energy_year = random() * 1000
fd_uac = random() * 100
# Añadir los otros campos

# DIM_FroniusDataManager
fdm_radiacion = random() * 1000
fdm_temperatura1 = random() * 100
# Añadir los otros campos

# Insertar datos en DIM_Enphase
insert_query = """
    INSERT INTO DIM_Enphase (E_EnergyDay, E_PAC, P_I1, E_NominalPower, E_TimeStamp)
    VALUES (%s, %s, %s, %s, %s)
"""

cur.execute(insert_query, (e_energy_day, e_pac, p_i1, e_nominal_power, e_timestamp))

# Insertar datos en DIM_FroniusDevice
insert_query = """
    INSERT INTO DIM_FroniusDevice (FD_EnergyDay, FD_EnergyYear, FD_UAC, FD_TimeStamp)
    VALUES (%s, %s, %s, %s)
"""

cur.execute(insert_query, (fd_energy_day, fd_energy_year, fd_uac, datetime.now()))

# Insertar datos en DIM_FroniusDataManager
insert_query = """
    INSERT INTO DIM_FroniusDataManager (FDM_Radiacion, FDM_Temperatura1, FDM_TimeStamp)
    VALUES (%s, %s, %s)
"""

cur.execute(insert_query, (fdm_radiacion, fdm_temperatura1, datetime.now()))

conn.commit()
conn.close()