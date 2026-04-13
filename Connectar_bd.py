import mysql.connector

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="bfjm6tvgjghm0h0dprcw-mysql.services.clever-cloud.com",
            user="u7f21txv45ys4qul",
            password="u03SnyKrk1LWMVymzhcK",
            database="bfjm6tvgjghm0h0dprcw",
            port=3306,
            autocommit=True
        )
        if conexion.is_connected():
            return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar: {err}")
        return None
    