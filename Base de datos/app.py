import sqlite3
from flask import Flask, request, render_template, url_for, redirect
lista = []
app = Flask(__name__)
lista = []
def get_db_gf_connection():
    conn = sqlite3.connect('organizador.db') 
    return conn

lista_gastos = []

gasto_fijo = [
        {'name': 'Producto', 'precio': 0}
    ]

gasto_diario = [
        {'name': 'Producto', 'precio': 0}
    ]

ingreso_mensual = [
        {'name': 'Monto', 'precio': 0}
    ]

ahorro = [
        {'name': 'Porcentaje', 'precio': 0}
    ]


# imprimir la tabla de gastos fijos
def organizacion():
    conn = get_db_gf_connection()
    data = conn.execute('SELECT * FROM gf').fetchall()
    conn.close()
    return data


# imprimir la tabla de gastos diarios
def imprimirgd():
    conn = get_db_gf_connection()
    data = conn.execute('SELECT * FROM gp').fetchall()
    conn.close()
    return data

# imprimir ingresos mensuales
def imprimirim():
    conn = get_db_gf_connection()
    data = conn.execute('SELECT * FROM im').fetchall()
    conn.close()
    return data


@app.route('/', methods=['GET', 'POST'])
def index(gasto_fijo=gasto_fijo, gasto_diario=gasto_diario, ingreso_mensual=ingreso_mensual, ahorro=ahorro):
    # inicio de calculo de gastos fijos
    global a
    a = 0
    variable_gf = organizacion()
    for lista in variable_gf:
        numero = lista[1]
        a = a + numero
        print(numero)
        print(a)
    # inicio de calculo de gastos diarios
    global contador
    contador = 0
    variable_gd = imprimirgd()
    for listita in variable_gd:
        numerito = listita[1]
        contador = contador + numerito
    
    # inicio de calculo de ingreso mensual
    global contar
    contar = 0
    variable_im = imprimirim()
    for ingreso in variable_im:
        numero_im = ingreso[1]
        contar = contar + numero_im
        
    # calculo del porcentaje de ahorro
    porcentaje = 0.20
    total_ahorro = contar * porcentaje
    print(total_ahorro)
    
    # calculo del restante
    suma_total = a + contador + total_ahorro
    total_restante = contar - suma_total
    print(total_restante)
    
    return render_template('index.html', ahorro=ahorro, gasto_diario=gasto_diario, gastos_fijos=gasto_fijo, ingreso_mensual=ingreso_mensual,a=a, contador = contador, contar = contar, total_ahorro = total_ahorro, total_restante = total_restante)


@app.route('/registro')
def registro():
    return render_template('login.html')

@app.route('/addgf', methods=['GET', 'POST'])
def addgf():
    if request.method == 'POST':
        gf = {
            'name': request.form['name'],
            'precio': request.form['gastof']
        }
        gasto_fijo.append(gf)
        conn = get_db_gf_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO GF(id_datos, Gastos) VALUES (?, ?)', (1, gf['precio']))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/addgd', methods=['GET', 'POST'])
def addgd():
    if request.method == 'POST':
        gd = {
            'name': request.form['name'],
            'precio': request.form['gastod']
        }
        gasto_diario.append(gd)
        conn = get_db_gf_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO GP(id_datos, Gastos_p) VALUES (?, ?)', (1, gd['precio']))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/addim', methods=['GET', 'POST'])
def addim():
    if request.method == 'POST':
        im = {
            'name': request.form['name'],
            'precio': request.form['ingresom']
        }
        ingreso_mensual.append(im)
        conn = get_db_gf_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO IM(id_datos, IM) VALUES (?, ?)', (1, im['precio']))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/addah', methods=['GET', 'POST'])
def addah():
    if request.method == 'POST':
        ah = {
            'name': request.form['name'],
            'precio': request.form['ahorro']
        }
        ahorro.append(ah) 
    return redirect(url_for('index'))

# imprimir la tabla de gastos fijos
def organizacion():
    conn = get_db_gf_connection()
    data = conn.execute('SELECT * FROM gf').fetchall()
    conn.close()
    return data

# recorrer y sumar la tabla gastos fijos
# @app.route('/recorrergf')
# def recorrer():
#     global a
#     a = 0
#     variable = organizacion()
#     for listita in variable:
#         numero = listita[1]
#         a = a + numero
#         print(a)
#     return render_template('index.html', a = a)

# agregar a gastos fijos 
@app.route('/agregargf', methods=['POST', 'GET'])
def gf():
    conn = get_db_gf_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO GF(id_datos, Gastos) VALUES (?, ?)', (1, gf))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# agregar a gastos diarios
@app.route('/agregargd', methods=['POST', 'GET'])
def gd():
    if request.method == 'POST':
        gd = request.form['gastosd']
        print(gd)
        conn = get_db_gf_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO GP(id_datos, Gastos_p) VALUES (?, ?)', (1, gd))
        conn.commit()
        conn.close()
        return 'Correcto'
    return render_template('gasto.html')


# recorrer y sumar la tabla gastos fijos
@app.route('/recorrergd')
def recorrergf():
    global contador
    contador = 0
    variable = imprimirgd()
    for listita in variable:
        numero = listita[1]
        contador = contador + numero
    return render_template('gasto.html', contador = contador)

# agregar a ingresos mensuales
@app.route('/agregarim', methods=['POST', 'GET'])
def im():
    if request.method == 'POST':
        im = request.form['gastosim']
        print(im)
        conn = get_db_gf_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO IM(id_datos, IM) VALUES (?, ?)', (1, im))
        conn.commit()
        conn.close()
        return 'Correcto'
    return render_template('gasto.html')



# def resultado():
#     # gasto diario
#     global contador
#     contador = 0
#     gd = imprimirgd()
#     for numero in gd:
#         numero_final = numero[1]
#         contador = contador + numero_final

#     # gasto fijo
#     global a
#     a = 0
#     gf = organizacion()
#     for numerito in gf:
#         numerito_final = numerito[1]
#         print(numerito_final)
#         a += numerito_final

#     global x
#     x = 0
#     monto_final = 0
#     im = imprimirim()
#     for monto in im:
#         monto_final = monto[1]
#         x = x + monto_final
#         print(x)
#     porcentaje = monto_final * 0.10
#     print(contador)
#     print(a)
#     suma = a + contador
#     print(suma)
#     resta = x - suma
#     print(resta)


# resultado()
if __name__ == '__main__':
    app.run(debug=True, port=5000)
