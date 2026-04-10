import mysql.connector 

def obtener_conexion():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root", 
            password="MoniVaz1002@",
            database="corre_electronico"
        )
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None