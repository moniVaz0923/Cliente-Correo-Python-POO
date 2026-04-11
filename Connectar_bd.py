import mysql.connector

try:
    conexion = mysql.connector.connect(
        host="bfjm6tvgjghm0h0dprcw-mysql.services.clever-cloud.com",
        user="u7f21txv45ys4qul",
        password="u03SnyKrk1LWMVymzhcK",
        database="bfjm6tvgjghm0h0dprcw",
        port=3306
    )
    
    if conexion.is_connected():
        print("¡Conexión exitosa a la base de datos en la nube!")
        # Importante: recordá crear el cursor dentro de tus funciones
        # cursor = conexion.cursor()

except mysql.connector.Error as err:
    print(f"Error al conectar: {err}")