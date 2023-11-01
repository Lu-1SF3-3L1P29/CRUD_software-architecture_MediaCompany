
#Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector

def connectionBD():
    mydb = mysql.connector.connect(
        host ="dpg-cl0pl6gp2gis738ukop0-a",
        port = "5432",
        user ="mediacompanyusers",
        passwd ="ZUJ5PNy4pRuqOSj2NC7pc6LVf9cEe5iX",
        database = "mediacompany"
        )
    if mydb:
        print ("Conexion exitosa a BD")
        return mydb
    else:
        print("Error en la conexion a BD")
    

    
    
    