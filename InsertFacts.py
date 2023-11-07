import psycopg2
from datetime import datetime, timezone
import pytz

def connect_to_database(db_params):
    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def get_last_dim_enphase_record(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dim_enphase ORDER BY e_timestamp DESC LIMIT 1")
        record = cursor.fetchone()
        cursor.close()
        if record:
            return record
        else:
            return None
    except Exception as e:
        print(f"Error al obtener el último registro de dim_enphase: {e}")
        return None

def get_last_dim_froniusdatamanager_record(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dim_froniusdatamanager ORDER BY fdm_timestamp DESC LIMIT 1")
        record = cursor.fetchone()
        cursor.close()
        if record:
            return record
        else:
            return None
    except Exception as e:
        print(f"Error al obtener el último registro de dim_froniusdatamanager: {e}")
        return None

def get_last_dim_froniusdevice_records(conn, limit=6):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dim_froniusdevice ORDER BY fd_timestamp DESC LIMIT %s", (limit,))
        records = cursor.fetchall()
        cursor.close()
        if records:
            return records
        else:
            return None
    except Exception as e:
        print(f"Error al obtener los últimos registros de dim_froniusdevice: {e}")
        return None
    

def calculateFdInd(records):
    indicators = []

    ind_fd_fc = records[1] / (records[8] * 24)
    indicators.append(ind_fd_fc)

    ind_fd_hsp = (records[1] / 2) / 1000
    indicators.append(ind_fd_hsp)

    ind_fd_uacvsudc = records[3] / records[4]
    indicators.append(ind_fd_uacvsudc)

    ind_fd_iacvsidc = records[5] / records[6]
    indicators.append(ind_fd_iacvsidc)
    
    return indicators

def calculateEInd(record):

    indicators = []

    ind_e_hsp = (record[1] / 2) / 1000
    indicators.append(ind_e_hsp)

    ind_e_fc = record[1] / (record[23] * 24)
    indicators.append(ind_e_fc)

    return indicators

def insertIntoDwh():
    print("INGRESA AL MÉTODO INSERT INTO DW")
    indicators = []
    fd_indicators = []
    e_indicators = []

    db_params = {
        "host": "54.145.74.186",
        "port": 5555,
        "database": "postgres",
        "user": "postgres",
        "password": "post123"
    }

    conn = connect_to_database(db_params)

    if conn:
        last_dim_enphase_record = get_last_dim_enphase_record(conn)
        last_dim_froniusdevice_records = get_last_dim_froniusdevice_records(conn, limit=6)

        if last_dim_enphase_record:
           e_indicators = calculateEInd(last_dim_enphase_record)

        if last_dim_froniusdevice_records:
            for record in last_dim_froniusdevice_records:
                fd_indicators.append(calculateFdInd(record))

        conn.close()


    #IDs FDs
    id_fd1 = last_dim_froniusdevice_records[0][0]
    id_fd2 = last_dim_froniusdevice_records[1][0]
    id_fd3 = last_dim_froniusdevice_records[2][0]
    id_fd4 = last_dim_froniusdevice_records[3][0]
    id_fd5 = last_dim_froniusdevice_records[4][0]
    id_fd6 = last_dim_froniusdevice_records[5][0]

    #ID E
    id_e = last_dim_enphase_record[0]

    #Indicadores FD
    ind_fd1_fc = fd_indicators[0][0]
    ind_fd2_fc = fd_indicators[1][0]
    ind_fd3_fc = fd_indicators[2][0]
    ind_fd4_fc = fd_indicators[3][0]
    ind_fd5_fc = fd_indicators[4][0]
    ind_fd6_fc = fd_indicators[5][0]

    ind_fd1_hsp = fd_indicators[0][1]
    ind_fd2_hsp = fd_indicators[1][1]
    ind_fd3_hsp = fd_indicators[2][1]
    ind_fd4_hsp = fd_indicators[3][1]
    ind_fd5_hsp = fd_indicators[4][1]
    ind_fd6_hsp = fd_indicators[5][1]

    ind_fd1_uacvsudc = fd_indicators[0][2]
    ind_fd2_uacvsudc = fd_indicators[1][2]
    ind_fd3_uacvsudc = fd_indicators[2][2]
    ind_fd4_uacvsudc = fd_indicators[3][2]
    ind_fd5_uacvsudc = fd_indicators[4][2]
    ind_fd6_uacvsudc = fd_indicators[5][2]

    ind_fd1_iacvsidc = fd_indicators[0][3]
    ind_fd2_iacvsidc = fd_indicators[1][3]
    ind_fd3_iacvsidc = fd_indicators[2][3]
    ind_fd4_iacvsidc = fd_indicators[3][3]
    ind_fd5_iacvsidc = fd_indicators[4][3]
    ind_fd6_iacvsidc = fd_indicators[5][3]

    #Indicadores E
    ind_e_hsp = e_indicators[0]
    ind_e_fc = e_indicators[1]
    potencia_promedio = sum(last_dim_enphase_record[i] for i in range(3, 23)) / 20
    ind_e_meanp = potencia_promedio

    #Facts timestamptz
    # Obtiene la fecha y hora actual en la zona horaria de Bogotá
    bogota_timezone = pytz.timezone("America/Bogota")
    facts_timestamp = datetime.now(bogota_timezone)

    #E devicename
    e_devicename = last_dim_enphase_record[25]

    #FD devicenames
    fd1_devicename = last_dim_froniusdevice_records[0][10]
    fd2_devicename = last_dim_froniusdevice_records[1][10]
    fd3_devicename = last_dim_froniusdevice_records[2][10]
    fd4_devicename = last_dim_froniusdevice_records[3][10]
    fd5_devicename = last_dim_froniusdevice_records[4][10]
    fd6_devicename = last_dim_froniusdevice_records[5][10]


    try: 
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        insert_query = """
                INSERT INTO facts_ssfv (id_fd1, id_fd2, id_fd3, id_fd4, id_fd5, id_fd6, id_e,
                ind_fd1_fc, ind_fd2_fc, ind_fd3_fc, ind_fd4_fc, ind_fd5_fc, ind_fd6_fc,
                ind_fd1_hsp, ind_fd2_hsp, ind_fd3_hsp, ind_fd4_hsp, ind_fd5_hsp, ind_fd6_hsp,
                ind_fd1_uacvsudc, ind_fd2_uacvsudc, ind_fd3_uacvsudc, ind_fd4_uacvsudc, ind_fd5_uacvsudc, ind_fd6_uacvsudc,
                ind_fd1_iacvsidc, ind_fd2_iacvsidc, ind_fd3_iacvsidc, ind_fd4_iacvsidc, ind_fd5_iacvsidc, ind_fd6_iacvsidc,
                ind_e_hsp, ind_e_fc, ind_e_meanp,
                facts_timestamp, e_devicename, fd1_devicename, fd2_devicename, fd3_devicename, fd4_devicename, 
                fd5_devicename, fd6_devicename)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(insert_query, (id_fd1, id_fd2, id_fd3, id_fd4, id_fd5, id_fd6, id_e,
                  ind_fd1_fc, ind_fd2_fc, ind_fd3_fc, ind_fd4_fc, ind_fd5_fc, ind_fd6_fc,
                  ind_fd1_hsp, ind_fd2_hsp, ind_fd3_hsp, ind_fd4_hsp, ind_fd5_hsp, ind_fd6_hsp,
                  ind_fd1_uacvsudc, ind_fd2_uacvsudc, ind_fd3_uacvsudc, ind_fd4_uacvsudc, ind_fd5_uacvsudc, ind_fd6_uacvsudc,
                  ind_fd1_iacvsidc, ind_fd2_iacvsidc, ind_fd3_iacvsidc, ind_fd4_iacvsidc, ind_fd5_iacvsidc, ind_fd6_iacvsidc,
                  ind_e_hsp, ind_e_fc, ind_e_meanp,
                  facts_timestamp, e_devicename, fd1_devicename, fd2_devicename, fd3_devicename, fd4_devicename, 
                  fd5_devicename, fd6_devicename))
        
        conn.commit()

        conn.close()
        
        print("Insersión a la DB realizada")

    except Exception as e:
        print(f"Error al insertar los datos en la DB: {e}")