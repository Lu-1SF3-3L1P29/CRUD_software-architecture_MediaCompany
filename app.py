from flask import Flask, render_template, request, redirect, url_for, jsonify
from controller.controllerSub import *
from controller.controllerCon import *

#Para subir archivo tipo foto al servidor
import os
from werkzeug.utils import secure_filename 


#aDeclarando nombre de la aplicación e inicializando, crear la aplicación Flask


app = Flask(__name__)
application = app

FLASK_DEBUG = True
FLASK_RUN_HOST="0.0.0.0"
FLASK_RUN_PORT=10000

msg  =''
tipo =''

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sql10658339:tI6ZDDAk7d@sql10.freesqldatabase.com/sql10658339'



@app.route('/', methods=['GET','POST'])
def inicio():
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
    return redirect(url_for('inicio'))
    

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

       
@app.route('/', methods=['GET','POST'])
def iniciocon():
    return render_template('public/layout.html', miDatacon = listaCon())


#RUTAS
@app.route('/registrar-con', methods=['GET','POST'])
def addCon():
    return render_template('public/accionescontent/addcon.html')


 
#Registrando nuevo carro
@app.route('/con', methods=['POST'])
def formAddCon():
    if request.method == 'POST':

        
        if(request.files['foto'] !=''):
            file     = request.files['foto'] #recibiendo el archivo
            nuevoNombreFile = recibeFoto(file) #Llamado la funcion que procesa la imagen
            resultData = registrarCon(file)
            if(resultData ==1):
                return render_template('public/layout.html', miData = listaCon(), msg='El Registro fue un éxito', tipo=1)
            else:
                return render_template('public/layout.html', msg = 'Metodo HTTP incorrecto', tipo=1)   
        else:
            return render_template('public/layout.html', msg = 'Debe cargar una foto', tipo=1)
            


@app.route('/form-update-con/<string:id>', methods=['GET','POST'])
def formViewUpdatecon(id):
    if request.method == 'GET':
        resultData = updateCon(id)
        if resultData:
            return render_template('public/accionescontent/updatecon.html',  dataInfo = resultData)
        else:
            return render_template('public/layout.html', miData = listaCon(), msg='No existe contenido', tipo= 1)
    else:
        return render_template('public/layout.html', miData = listaCon(), msg = 'Metodo HTTP incorrecto', tipo=1)          
 
   
  
@app.route('/ver-detalles-con/<int:idCon>', methods=['GET', 'POST'])
def viewDetalleCon(idCon):
    msg =''
    if request.method == 'GET':
        resultData = detallesCon(idCon) #Funcion que almacena los detalles del carro
        
        if resultData:
            return render_template('public/accionescontent/viewcon.html', infoCon = resultData, msg='Detalles del contenido', tipo=1)
        else:
            return render_template('public/acciones/layout.html', msg='No existe tal contenido', tipo=1)
    return redirect(url_for('inicio'))
    

@app.route('/actualizar-con/<string:idCon>', methods=['POST'])
def  formActualizarCon(idCon):
    if request.method == 'POST':

        
        #Script para recibir el archivo (foto)
        if(request.files['foto']):
            file     = request.files['foto']
            fotoForm = recibeFoto(file)
            resultData = recibeActualizarCon(fotoForm, idCon)
        else:
            fotoCon  ='sin_foto.jpg'
            resultData = recibeActualizarCon(fotoCon, idCon)

        if(resultData ==1):
            return render_template('public/layout.html', miData = listaCon(), msg='Datos del contenido actualizados', tipo=1)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/layout.html', miData = listaCon(), msg='No se pudo actualizar', tipo=1)


#Eliminar carro
@app.route('/borrar-con', methods=['GET', 'POST'])
def formViewBorrarCon():
    if request.method == 'POST':
        idCon         = request.form['id']
        nombreFoto      = request.form['nombreFoto']
        resultData      = eliminarCon(idCon, nombreFoto)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])




def eliminarCon(idCon='', nombreFoto=''):
        
    conexion_MySQLdb = connectionBD() #Hago instancia a mi conexion desde la funcion
    cur              = conexion_MySQLdb.cursor(dictionary=True)
    
    cur.execute('DELETE FROM content WHERE id=%s', (idCon,))
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
    nuevoNombreFile     = stringAleatorio() + extension
    #print(nuevoNombreFile)
        
    upload_path = os.path.join (basepath, 'static/assets/fotos_cont', nuevoNombreFile) 
    file.save(upload_path)

    return nuevoNombreFile

  
#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('inicio'))
    
    
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)

    