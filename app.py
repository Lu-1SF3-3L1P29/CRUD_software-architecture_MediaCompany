from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from controller.controllerSub import *
from controller.controllercon import *
from controller.controllerad import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mysql.connector

#Para subir archivo tipo foto al servidor
import os
from werkzeug.utils import secure_filename 


#aDeclarando nombre de la aplicación e inicializando, crear la aplicación Flask


app = Flask(__name__)
application = app

msg  =''
tipo =''

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sql10658339:tI6ZDDAk7d@sql10.freesqldatabase.com/sql10658339'

app.secret_key = 'AS_MediaCompany'


@app.route('/', methods=['GET','POST'])
def inicio():
    return render_template('public/login.html')

@app.route('/lsub', methods=['GET','POST'])
def inicioSub():
    return render_template('public/layout.html', miData = listaSub())

@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('public/about.html')

#RUTAS
@app.route('/registrar-sub', methods=['GET','POST'])
def addSub():
    return render_template('public/acciones/add.html')

@app.route('/sub', methods=['POST'])
def formAddSub():
    if request.method == 'POST':
        nombre               = request.form['nombre']
        edad              = request.form['edad']

        
        
        if(request.files['foto'] !=''):
            file     = request.files['foto'] #recibiendo el archivo
            nuevoNombreFile = recibeFoto(file) #Llamado la funcion que procesa la imagen
            resultData = registrarSub(nombre, edad, nuevoNombreFile)
            if(resultData ==1):
                return render_template('public/layout.html', miData = listaSub(), msg='El Registro fue un éxito', tipo=1)
            else:
                return render_template('public/layout.html', msg = 'Metodo HTTP incorrecto', tipo=1)   
        else:
            return render_template('public/layout.html', msg = 'Debe cargar una foto', tipo=1)
            


@app.route('/form-update-sub/<string:id>', methods=['GET','POST'])
def formViewUpdate(id):
    if request.method == 'GET':
        resultData = updateSub(id)
        if resultData:
            return render_template('public/acciones/update.html',  dataInfo = resultData)
        else:
            return render_template('public/layout.html', miData = listaSub(), msg='No existe el subcriptor', tipo= 1)
    else:
        return render_template('public/layout.html', miData = listaSub(), msg = 'Metodo HTTP incorrecto', tipo=1)          
 
   
  
@app.route('/ver-detalles-sub/<int:idSub>', methods=['GET', 'POST'])
def viewDetalleSub(idSub):
    msg =''
    if request.method == 'GET':
        resultData = detallesSub(idSub) #Funcion que almacena los detalles del carro
        
        if resultData:
            return render_template('public/acciones/view.html', infoSub = resultData, msg='Detalles del Subcriptor', tipo=1)
        else:
            return render_template('public/acciones/layout.html', msg='No existe el subcriptor', tipo=1)
    return redirect(url_for('inicioSub'))
    

@app.route('/actualizar-sub/<string:idSub>', methods=['POST'])
def  formActualizarSub(idSub):
    if request.method == 'POST':
        nombre           = request.form['nombre']
        edad          = request.form['edad']
        
        #Script para recibir el archivo (foto)
        if(request.files['foto']):
            file     = request.files['foto']
            fotoForm = recibeFoto(file)
            resultData = recibeActualizarSub(nombre,edad, fotoForm, idSub)
        else:
            fotoSub  ='sin_foto.jpg'
            resultData = recibeActualizarSub(nombre, edad , fotoSub, idSub)

        if(resultData ==1):
            return render_template('public/layout.html', miData = listaSub(), msg='Datos del subcriptor actualizados', tipo=1)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/layout.html', miData = listaSub(), msg='No se pudo actualizar', tipo=1)


#Eliminar carro
@app.route('/borrar-sub', methods=['GET', 'POST'])
def formViewBorrarSub():
    if request.method == 'POST':
        idSub         = request.form['id']
        nombreFoto      = request.form['nombreFoto']
        resultData      = eliminarSub(idSub, nombreFoto)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])




def eliminarSub(idSub='', nombreFoto=''):
        
    conexion_MySQLdb = connectionBD() #Hago instancia a mi conexion desde la funcion
    cur              = conexion_MySQLdb.cursor(dictionary=True)
    
    cur.execute('DELETE FROM subs WHERE id=%s', (idSub,))
    conexion_MySQLdb.commit()
    resultado_eliminar = cur.rowcount #retorna 1 o 0
    #print(resultado_eliminar)
    
    basepath = os.path.dirname (__file__) #C:\xampp\htdocs\localhost\Crud-con-FLASK-PYTHON-y-MySQL\app
    url_File = os.path.join (basepath, 'static/assets/fotos_subs', nombreFoto)
    os.remove(url_File) #Borrar foto desde la carpeta
    #os.unlink(url_File) #Otra forma de borrar archivos en una carpeta
    

    return resultado_eliminar



def recibeFoto(file):
    print(file)
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFile     = stringAleatorio() + extension
    #print(nuevoNombreFile)
        
    upload_path = os.path.join (basepath, 'static/assets/fotos_subs', nuevoNombreFile) 
    file.save(upload_path)

    return nuevoNombreFile

       
@app.route('/lcon', methods=['GET','POST'])
def iniciocon():
    return render_template('public/layoutcon.html', miDatacon = listacon())


#RUTAS
@app.route('/registrar-con', methods=['GET','POST'])
def addcon():
    return render_template('public/accionescontent/addcon.html')


 
#Registrando nuevo contenido
@app.route('/con', methods=['POST'])
def formAddcon():
    if request.method == 'POST':
        nombre = request.form['nombre']

        if(request.files['foto'] !=''):
            file     = request.files['foto'] #recibiendo el archivo
            nuevoNombreFilecon = recibeFotocon(file) #Llamado la funcion que procesa la imagen
            resultData = registrarcon(nombre, nuevoNombreFilecon)
            if(resultData ==1):
                return render_template('public/layoutcon.html', miDatacon = listacon(), msg='El Registro fue un éxito', tipo=1)
            else:
                return render_template('public/layoutcon.html', msg = 'Metodo HTTP incorrecto', tipo=1)   
        else:
            return render_template('public/layoutcon.html', msg = 'Debe cargar una foto', tipo=1)
            


@app.route('/form-update-con/<string:id>', methods=['GET','POST'])
def formViewUpdatecon(id):
    if request.method == 'GET':
        resultData = updatecon(id)
        if resultData:
            return render_template('public/accionescontent/updatecon.html',  dataInfo = resultData)
        else:
            return render_template('public/layoutcon.html', miDatacon = listacon(), msg='No existe contenido', tipo= 1)
    else:
        return render_template('public/layoutcon.html', miDatacon = listacon(), msg = 'Metodo HTTP incorrecto', tipo=1)          
 
   
  
@app.route('/ver-detalles-con/<int:idcon>', methods=['GET', 'POST'])
def viewDetallecon(idcon):
    msg =''
    if request.method == 'GET':
        resultData = detallescon(idcon) #Funcion que almacena los detalles del carro
        
        if resultData:
            return render_template('public/accionescontent/viewcon.html', infocon = resultData, msg='Detalles del contenido', tipo=1)
        else:
            return render_template('public/layoutcon.html', msg='No existe tal contenido', tipo=1)
    return redirect(url_for('iniciocon'))
    

@app.route('/actualizar-con/<string:idcon>', methods=['POST'])
def  formActualizarcon(idcon):
    if request.method == 'POST':
        nombre           = request.form['nombre']
        
        #Script para recibir el archivo (foto)
        if(request.files['foto']):
            file     = request.files['foto']
            fotoForm = recibeFotocon(file)
            resultData = recibeActualizarcon(nombre, fotoForm, idcon)
        else:
            fotocon  ='sin_foto.jpg'
            resultData = recibeActualizarcon(nombre,fotocon, idcon)

        if(resultData ==1):
            return render_template('public/layoutcon.html', miDatacon = listacon(), msg='Datos del contenido actualizados', tipo=1)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/layoutcon.html', miDatacon = listacon(), msg='No se pudo actualizar', tipo=1)


#Eliminar carro
@app.route('/borrar-con', methods=['GET', 'POST'])
def formViewBorrarcon():
    if request.method == 'POST':
        idcon         = request.form['id']
        nombreFoto      = request.form['nombreFoto']
        resultData      = eliminarcon(idcon, nombreFoto)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])




def eliminarcon(idcon='', nombreFoto=''):
        
    conexion_MySQLdb = connectionBD() #Hago instancia a mi conexion desde la funcion
    cur              = conexion_MySQLdb.cursor(dictionary=True)
    
    cur.execute('DELETE FROM content WHERE id=%s', (idcon,))
    conexion_MySQLdb.commit()
    resultado_eliminar = cur.rowcount #retorna 1 o 0
    #print(resultado_eliminar)
    
    basepath = os.path.dirname (__file__) #C:\xampp\htdocs\localhost\Crud-con-FLASK-PYTHON-y-MySQL\app
    url_File = os.path.join (basepath, 'static/assets/fotos_cont', nombreFoto)
    os.remove(url_File) #Borrar foto desde la carpeta
    #os.unlink(url_File) #Otra forma de borrar archivos en una carpeta
    

    return resultado_eliminar



def recibeFotocon(file):
    print(file)
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFilecon     = stringAleatorio() + extension
    #print(nuevoNombreFile)
        
    upload_path = os.path.join (basepath, 'static/assets/fotos_cont', nuevoNombreFilecon) 
    file.save(upload_path)

    return nuevoNombreFilecon


@app.route('/lad', methods=['GET','POST'])
def inicioad():
    return render_template('public/layoutad.html', miDataad = listaad())

#RUTAS
@app.route('/registrar-ad', methods=['GET','POST'])
def addad():
    return render_template('public/accionesad/addad.html')

@app.route('/ad', methods=['POST'])
def formAddad():
    if request.method == 'POST':
        nombre               = request.form['nombre']
        precio              = request.form['precio']

        
        
        if(request.files['foto'] !=''):
            file     = request.files['foto'] #recibiendo el archivo
            nuevoNombreFilead = recibeFotoad(file) #Llamado la funcion que procesa la imagen
            resultData = registrarad(nombre, precio, nuevoNombreFilead)
            if(resultData ==1):
                return render_template('public/layoutad.html', miDataad = listaad(), msg='El Registro fue un éxito', tipo=1)
            else:
                return render_template('public/layoutad.html', msg = 'Metodo HTTP incorrecto', tipo=1)   
        else:
            return render_template('public/layoutad.html', msg = 'Debe cargar una foto', tipo=1)
            


@app.route('/form-update-ad/<string:id>', methods=['GET','POST'])
def formViewUpdatead(id):
    if request.method == 'GET':
        resultData = updatead(id)
        if resultData:
            return render_template('public/accionesad/updatead.html',  dataInfo = resultData)
        else:
            return render_template('public/layoutad.html', miDataad = listaad(), msg='No existe tal publicidad', tipo= 1)
    else:
        return render_template('public/layoutad.html', miDataad = listaad(), msg = 'Metodo HTTP incorrecto', tipo=1)          
 
   
  
@app.route('/ver-detalles-ad/<int:idad>', methods=['GET', 'POST'])
def viewDetallead(idad):
    msg =''
    if request.method == 'GET':
        resultData = detallesad(idad) #Funcion que almacena los detalles del carro
        
        if resultData:
            return render_template('public/accionesad/viewad.html', infoad = resultData, msg='Detalles de la publicidad', tipo=1)
        else:
            return render_template('public/layoutad.html', msg='No existe tal publicidad', tipo=1)
    return redirect(url_for('inicioad'))
    

@app.route('/actualizar-ad/<string:idad>', methods=['POST'])
def  formActualizarad(idad):
    if request.method == 'POST':
        nombre           = request.form['nombre']
        precio          = request.form['precio']
        
        #Script para recibir el archivo (foto)
        if(request.files['foto']):
            file     = request.files['foto']
            fotoForm = recibeFotoad(file)
            resultData = recibeActualizarad(nombre,precio, fotoForm, idad)
        else:
            fotoad  ='sin_foto.jpg'
            resultData = recibeActualizarad(nombre, precio , fotoad, idad)

        if(resultData ==1):
            return render_template('public/layoutad.html', miDataad = listaad(), msg='Datos de la publicidad actualizados', tipo=1)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/layoutad.html', miDataad = listaad(), msg='No se pudo actualizar', tipo=1)


#Eliminar carro
@app.route('/borrar-ad', methods=['GET', 'POST'])
def formViewBorrarad():
    if request.method == 'POST':
        idad         = request.form['id']
        nombreFoto      = request.form['nombreFoto']
        resultData      = eliminarad(idad, nombreFoto)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])




def eliminarad(idad='', nombreFoto=''):
        
    conexion_MySQLdb = connectionBD() #Hago instancia a mi conexion desde la funcion
    cur              = conexion_MySQLdb.cursor(dictionary=True)
    
    cur.execute('DELETE FROM ad WHERE id=%s', (idad,))
    conexion_MySQLdb.commit()
    resultado_eliminar = cur.rowcount #retorna 1 o 0
    #print(resultado_eliminar)
    
    basepath = os.path.dirname (__file__) #C:\xampp\htdocs\localhost\Crud-con-FLASK-PYTHON-y-MySQL\app
    url_File = os.path.join (basepath, 'static/assets/fotos_ad', nombreFoto)
    os.remove(url_File) #Borrar foto desde la carpeta
    #os.unlink(url_File) #Otra forma de borrar archivos en una carpeta
    

    return resultado_eliminar



def recibeFotoad(file):
    print(file)
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFilead     = stringAleatorio() + extension
    #print(nuevoNombreFile)
        
    upload_path = os.path.join (basepath, 'static/assets/fotos_ad', nuevoNombreFilead) 
    file.save(upload_path)

    return nuevoNombreFilead

  
#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('inicio'))
    
    
    
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        conexion_MySQLdb = connectionBD()
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('public/layout.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('public/login.html', mesage = mesage)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        conexion_MySQLdb = connectionBD()
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NOT NULL, %s, %s, %s)', (userName, email, password, ))
            conexion_MySQLdb.commit()
            cursor.close() #Cerrando conexion SQL
            conexion_MySQLdb.close() #cerrando conexion de la BD
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('public/register.html', mesage = mesage)



##if __name__ == '__main__':
    ##app.run(host='0.0.0.0', port=10000, debug=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="10000", debug=True) #the IP address of the ix15 which is given by our lan router 