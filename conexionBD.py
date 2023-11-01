
#Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector

def connectionBD():
    mydb = mysql.connector.connect(
        host ="sql10.freesqldatabase.com",
        user ="sql10658339",
        passwd ="tI6ZDDAk7d",
        database = "sql10658339"
        )
    if mydb:
        print ("Conexion exitosa a BD")
        return mydb
    else:
        print("Error en la conexion a BD")
    
