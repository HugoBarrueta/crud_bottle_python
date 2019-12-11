from sys import argv
#De bottle importamos las librerias a utilizar
from bottle import route, run, template, request, static_file, error,view
import sqlite3 #unicamente importamos sqlite3 para su utilización
import smtplib #importamos smtplib para el envio de correos electronicos

#db_name = 'data/products.db' #acceso a la base de datos
db_name = 'data/Persona.db'

#Concexion con base de datos
def run_query(query, parameters = ()):
    with sqlite3.connect(db_name) as conn: #conectamos a la bd y le damos el nombre de conn
        cursor = conn.cursor()
        result = cursor.execute(query, parameters) #obtiene los parametros para ser ejecutado
        conn.commit #ejecuta la funcion
    return result

#Ruta de inicio al cargar la página
@route('/') 
def index(): #funcion que realizara al cargar la página principal
    try:
        #obtenemos los productos con comando de SQLite y los guardamos en una variable
        query = "SELECT codigo, nombre,aPaterno, aMaterno, fecNac FROM persona" 
        #llamamos a la funcion de la conexion y la guaramos en una variable
        #Aqui de igual forma ejecutamos la funcion
        db_rows = run_query(query)
        #Guardamos en una variable el template a ocupar junto con los datos seleccionados de la bd
        output = template('temp/index', rows = db_rows)
        #Retornamos la variable output para mostrar la tabla en la web
        return output

    except IndexError as e:
        return "error", e
     
#Ruta para agregar productos, utilizando un metodo GET
@route('/add_persona', method = 'GET') 
def add_persona(): #función que realizara al cargar la página con la ruta especifica
    try:
        #Al ejecutar el boton llamado 'add' obtenemos una respuestra true
        if request.GET.get('add','').strip(): 
            #obtendra los datos especificos de cada uno de los campos y los guardara 
            #dentro de una variable especifica a cada uno de ellos
            codigo = request.GET.get('codigo','').strip()
            nombre = request.GET.get('nombre','').strip()
            apaterno = request.GET.get('apaterno','').strip()
            amaterno = request.GET.get('amaterno','').strip()
            fecnac = request.GET.get('fecnac','').strip()
            #Realizamos el comando de insercion de sqlite
            #Dentro de cada parentecis especificamos que se ingresaran datos
            query = 'INSERT INTO persona VALUES(NULL, ?, ?, ?, ?, ?)'
            #En parameters guardamos en orden especifico a los datos de la tabla
            #como tienen que ser ingresados a base de datos
            parameters = (codigo, nombre, apaterno, amaterno, fecnac)
            #Enviamos los datos dentro de las variables
            #y a su vez ejecutamos el query
            run_query(query, parameters)
            #al ser ejecutada la funcion correctamente 
            #regresamos un mensaje de Exito!.
            return template('temp/success')
        else:
            #si el boton presionado no es llamado 'add'
            #Redireccionara a la pantall para agregar los datos
            #que queremos agregar
            return template('temp/add')
            
    except IndexError as e:
        return "Error", e


#Ruta especifica para Editar, Eliminar y Generar PDF de acuerdo al codigo
@route('/persona/:no', method = 'GET')
#funcion que ejecutara la ruta especifica
#Recibe un valor 'no' el cual se ocupara para identificar los datos en la base de datos
def edit_product(no):
    try:
        #Si el botón presionado es llamado 'save' ejecutara la funcion
        if request.GET.get('save','').strip():
            #Guardamos los datos obtenidos en los campos de edicion de acuerdo a su nuevo valor
            new_nombre = request.GET.get('nombre','').strip()
            new_apaterno = request.GET.get('apaterno','').strip()
            new_amaterno = request.GET.get('amaterno','').strip()
            new_fecnac = request.GET.get('fecnac','').strip()
            #Realizamos la función UPDATE especificando con los signos '?'
            #que ingresaremos datos especificos
            query = "UPDATE persona SET nombre = ?, aPaterno = ?, aMaterno = ?, fecNac = ? WHERE codigo LIKE ?"
            #dentro de parameters guardamos en orden especifico a la funcion 
            #los datos que seran agregados
            parameters = (new_nombre, new_apaterno, new_amaterno, new_fecnac, no)
            #ejecutamos el Query envianod los valores correspondientes
            run_query(query, parameters)
            #Al completar la accion regresamos un mensaje de Exito!.
            return template('temp/success')

        #Si el bontón presionado es llamado 'update' realizara la siguiente función
        elif request.GET.get('update','').strip():
            #Realizamos la conexion con la base de datos
            conn = sqlite3.connect(db_name)
            #Guardamos dentro de una variable las funciones de SQLite
            c = conn.cursor()
            #Guardamos el valor del campo 'guitar' en una variable
            cod = request.GET.get('person','').strip()
            #Ejecutamos el comando para obtener el dato que queremos editar
            c.execute("SELECT nombre, aPaterno, aMaterno, fecNac FROM persona WHERE codigo LIKE ?", (cod, ))  
            #Guardamos el query en una variable      
            data = c.fetchone()
            #Retornamos la vista para editar los datos
            #En old=data enviamos los datos obtenido para asignarlo en cada campo de texto de la vista
            #en no=cod enviamo el identificador del dato a editar
            return template('temp/edit', old=data, no=cod)
           
        #Si el boton presionado es llamado 'delete' realizara la soguiente función
        elif request.GET.get('delete','').strip():
            #Conectamos con base de datos
            conn = sqlite3.connect(db_name)
            #Guardamos dentro de una variable las funciones de SQLite
            c = conn.cursor()
            #obtenemos y gardamos en una variable el dato identificador del producto a eliminar
            cod = request.GET.get('person','').strip()
            #Ejecutamos la funcion a eliminar y agregamos el identificador del dato que queremos
            #Eliminar
            c.execute("DELETE FROM persona WHERE codigo = ?", (cod, ))
            #Ejecutamos el query
            conn.commit()
            #Retornamos una vista de Exito!.
            return template('temp/success')
    except ValueError as e:
        return "Error", e

#Función para enviar el mail
#Recibe un parametro 'msg' que es el mensaje que se enviara
def mail(msg):
    #Guardamos el mensaje dentro de una variable
    message = msg
    #Guardamos dentro de una variable el mensaje que queremos mostrar como asunto
    subject = "Excepcion encontrada"
    #Dentro de la variable mandamos el formato del mensaje donde
    #Especificamos que 'subject' ira como Asunto
    #y 'message' ira como mensaje 
    message = 'Subject: {}\n\n{}'.format(subject, message)
    #Realizamos la activacion del servicio de Gmail
    #especificando su protocolo y puerto 
    #lo guardamos dentro de una variable
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #Activamos el servicio de Gmail
    server.starttls()
    #Iniciamos sesión con un correo valido y una contraseña
    #NOTA: La contraseña puede o no funcionar
    #en este caso es una contraseña generada especificamente para esto
    server.login('hramonbf@gmail.com', 'clzqmbayjodeslci')
    #Enviamos el correo electronico
    #Especificando el correo que lo envia, a quien va dirigido, y el mensaje
    server.sendmail('hramonbf@gmail.com', 'hbarruetaf97@gmail.com', message)
    #IMPORTANTE. Apagar el servidor 
    server.quit()

#ERRORES CONTROLADOS
#Especificamos un que es un error 404
@error(404)
def erro404(error): #la funcion recibe un error como parametro, la Funcion se ejecuta automaticamente
    mail(error) #Utilizamos la funcion mail, enviamos el error para que se envie como mensaje
    return template('temp/error404') #retornamos una vista especificando el error
#Especificamos que es un error 500
@error(500)
def error500(error): #Esta funcion recibe un error como parametro
    mail(error) #Utilizamos la funcion mail, enviamos el error
    return template('temp/error500') #retornamos una vista especificando el error
#Especificamos que es un error 503
@error(503)
def error503(error): #Esta funcion recibe un error como parametro
    mail(error) ##Utilizamos la funcion mail, enviamos el error
    return template('temp/error500') #retornamos una vista especificando el error

if __name__ == '__main__': #Especificamos que si es la app principal
    run(host='0.0.0.0', port=argv[1]) #Corremos la app Especificando el host y puerto
    #El host se especifica '0.0.0.0' para que cuando se publique se otorgue automaticamente un host
    #El port se especifica argv[1] para que el mismo host 
    #run(host='localhost', port=3000, reloader="true")
