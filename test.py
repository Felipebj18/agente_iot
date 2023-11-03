import psycopg2
from datetime import datetime, timezone
import pytz

def insert_fronius(db_params, data):
    # print("Ingresa al método insert_fronius DW")
    # print(type(device_id))
    try:
        conn = psycopg2.connect(**db_params)
    except Exception as e:
        print("Error al conectar a la DB", e)
    if conn:
        try:
            cursor = conn.cursor()
            for device_id, device_data in data.items():
            # Insertar los datos en DIM_FroniusDevice                    
                insert_query = """
                    INSERT INTO DIM_FroniusDevice (FD_EnergyDay, FD_ENERGYYEAR, FD_UAC, FD_UDC, FD_IAC, FD_IDC, FD_PAC, FD_NominalPower, FD_TimeStamp, FD_DeviceName)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                cursor.execute(
                    insert_query,
                        (
                            device_data.get('DAY_ENERGY', 0),
                            device_data.get('YEAR_ENERGY', 0),
                            device_data.get('UAC', 0),
                            device_data.get('UDC', 0),
                            device_data.get('IAC', 0),
                            device_data.get('IDC', 0),
                            device_data.get('PAC', 0),
                            250.0,  
                            datetime.now(pytz.timezone("America/Bogota")),
                            device_id
                        )
                    )

            conn.commit()
            # print("Datos enviados a DIM fronius")

            conn.close()
        except Exception as e:
                print(f"Error al insertar los datos en DIM_FroniusDevice: {e}")
