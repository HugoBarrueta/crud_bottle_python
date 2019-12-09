from sys import argv
from bottle import route, run, template, request, static_file, error,view
import sqlite3
import smtplib

db_name = 'data/products.db' #acceso a la base de datos


#Concexion con base de datos
def run_query(query, parameters = ()):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit #ejecuta la funcion
    return result

@route('/')
def index():
    try:
        
        query = "SELECT codigo, name, price, stock FROM products"
        db_rows = run_query(query)

        #output = template('temp/make_table', rows = db_rows)
        output = template('temp/index', rows = db_rows)

        return output


    except IndexError as e:
        return "error", e
        

@route('/add_products', method = 'GET')
def add_products():
    try:
        if request.GET.get('add','').strip():

            code = request.GET.get('code','').strip()
            name = request.GET.get('name','').strip()
            price = request.GET.get('price','').strip()
            stock = request.GET.get('stock','').strip()

            query = 'INSERT INTO products VALUES(NULL, ?, ?, ?, ?)'
            parameters = (code, name, price, stock)
            run_query(query, parameters)

            return template('temp/success')
        else:
            return template('temp/add')
            

    except IndexError as e:
        return "Error", e

@route('/product/:no', method = 'GET')
def edit_product(no):
    try:

        if request.GET.get('save','').strip():
            
            new_name = request.GET.get('name','').strip()
            new_price = request.GET.get('price','').strip()
            new_stock = request.GET.get('stock','').strip()

            query = "UPDATE products SET name = ?, price = ?, stock = ? WHERE codigo LIKE ?"
            parameters = (new_name, new_price, new_stock, no)
            run_query(query, parameters)

            #return "Actualizado correctamente"
            return template('temp/success')
        elif request.GET.get('update','').strip():
            
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
            cod = request.GET.get('guitar','').strip()
            c.execute("SELECT name, price, stock FROM products WHERE codigo LIKE ?", (cod, ))        
            data = c.fetchone()

            return template('temp/edit', old=data, no=cod)
           

        elif request.GET.get('delete','').strip():
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
            cod = request.GET.get('guitar','').strip()
            c.execute("SELECT name, price, stock FROM products WHERE codigo LIKE ?", (cod, ))        
            data = c.fetchone()
            return template('temp/delete', old=data, no=cod)

    except ValueError as e:
        return "Error", e
        

def mail(msg):
    message = msg
    subject = "Excepcion encontrada"

    message = 'Subject: {}\n\n{}'.format(subject, message)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('hramonbf@gmail.com', 'clzqmbayjodeslci')

    server.sendmail('hramonbf@gmail.com', 'hbarruetaf97@gmail.com', message)

    server.quit()

    

@route('/delete/:no')
def delete(no):
    try:
        if request.GET.get('del','').strip():
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
            cod = request.GET.get('guitar','').strip()
            new_name = request.GET.get('name','').strip()
            new_price = request.GET.get('price','').strip()
            new_stock = request.GET.get('stock','').strip()
            c.execute("DELETE FROM products WHERE codigo = ? AND name= ? AND price = ? AND stock =?", (cod, new_name, new_price, new_stock, ))
            c.fetchone()
            #query = "DELETE FROM products WHERE codigo = ? AND name= ? AND price = ? AND stock =?"
            #parameters = (cod, new_name, new_price, new_stock)
            #run_query(query, parameters)

            return template('temp/success')
    except ValueError as e:
        
        return "error", e




@error(404)
def erro404(error):
    mail(error)
    return template('temp/error404')

@error(500)
def error500(error):
    mail(error)
    return template('temp/error500')

@error(503)
def error503(error):
    mail(error)
    return template('temp/error500')

run(host='crud-bottle.herokuapp.com', port=3000, debug= True, reloader=True)
