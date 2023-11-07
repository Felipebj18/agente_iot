import psycopg2
from datetime import datetime, timezone, timedelta
import pytz

class dw_insertions:
    def __init__(self, db_params):
        try:
            self.db_params = db_params
            self.conn = self.connect_to_database()
        except Exception as e:
            print("Error al crear objeto conn:", e)

    def connect_to_database(self):
        try:
            conn = psycopg2.connect(**self.db_params)
            return conn
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def insert_fronius(self, data):
        print("Ingresa al método insert_fronius DW")

        if self.conn:
            try:
                cursor = self.conn.cursor()

                for device_id, device_data in data.items():                  
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

                self.conn.commit()
                self.close_connection(self)

            except Exception as e:
                print(f"Error al insertar los datos en DIM_FroniusDevice: {e}")

    def insert_enphase(self, data):

        bogota_timezone = timezone(timedelta(hours=-5))
        current_time_bogota = datetime.now(bogota_timezone)

        e_nominal_power = 250.0
        if self.conn:
            try:
                cursor = self.conn.cursor()

                for device_id, device_data in data.items():
                    insert_query = """
                        INSERT INTO DIM_Enphase (E_EnergyDay, E_PAC, P_I1, P_I2, P_I3, P_I4, P_I5, P_I6, P_I7, P_I8, P_I9, P_I10, P_I11, P_I12, P_I13, P_I14, P_I15, P_I16, P_I17, P_I18, P_I19, P_I20, E_NominalPower, E_TimeStamp,E_DeviceName)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
                    """
                    
                    cursor.execute(
                        insert_query,
                                (
                                    float(device_data.get('EnergyDay', 0)),
                                    int(device_data.get('PAC', 0)),
                                    int(device_data.get('P_I1', 0)),
                                    int(device_data.get('P_I2', 0)),
                                    int(device_data.get('P_I3', 0)),
                                    int(device_data.get('P_I4', 0)),
                                    int(device_data.get('P_I5', 0)),
                                    int(device_data.get('P_I6', 0)),
                                    int(device_data.get('P_I7', 0)),
                                    int(device_data.get('P_I8', 0)),
                                    int(device_data.get('P_I9', 0)),
                                    int(device_data.get('P_I10', 0)),
                                    int(device_data.get('P_I11', 0)),
                                    int(device_data.get('P_I12', 0)),
                                    int(device_data.get('P_I13', 0)),
                                    int(device_data.get('P_I14', 0)),
                                    int(device_data.get('P_I15', 0)),
                                    int(device_data.get('P_I16', 0)),
                                    int(device_data.get('P_I17', 0)),
                                    int(device_data.get('P_I18', 0)),
                                    int(device_data.get('P_I19', 0)),
                                    int(device_data.get('P_I20', 0)),
                                    e_nominal_power,
                                    current_time_bogota,
                                    device_id
                                )
                    )

                self.conn.commit()
            except Exception as e:
                print(f"Error al insertar los datos en DIM_Enphase: {e}")

    def insert_froniusdm(self, data):
        if self.conn:
            try:
                cursor = self.conn.cursor()

                for device_id, device_data in data.items():
                    insert_query = """
                        INSERT INTO DIM_FroniusDataManager (FDM_Radiacion, FDM_Temperatura1, FDM_Temperatura2, FDM_NominalPower, FDM_TimeStamp, FDM_DeviceName)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(
                        insert_query,
                        (
                            device_data.get('Radiacion', 0),
                            device_data.get('Temperatura_1', 0),
                            device_data.get('Temperatura_2', 0),
                            250.0,  
                            datetime.now(pytz.timezone("America/Bogota")),
                            device_id
                        )
                    )

                self.conn.commit()
            except Exception as e:
                print(f"Error al insertar los datos en DIM_FroniusDataManager: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()