
#Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector

def connectionBD():
    mydb = mysql.connector.connect(
        host ="LuisFelipe.mysql.pythonanywhere-services.com",
        user ="LuisFelipe",
        passwd ="3n=,8MtnwML$)z,",
        database = "LuisFelipe$MC"
        )
    if mydb:
        print ("Conexion exitosa a BD")
        return mydb
    else:
        print("Error en la conexion a BD")
    
