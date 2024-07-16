from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, Clientes, Vehiculos, Maestro, Detalles
import logging

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

@app.route('/clientes', methods=['GET'])
def clientes():
    clientes = Clientes.query.all()
    return render_template('clientes.html', clientes=clientes)


@app.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Clientes.query.get_or_404(id)
    
    # Log para verificar los diagnósticos asociados al cliente
    logging.debug(f'Diagnósticos asociados al cliente {cliente.id}: {cliente.maestro}')
    
    if request.method == 'GET':
        return render_template('editar_cliente.html', cliente=cliente)
    elif request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.telefono = request.form['telefono']
        cliente.direccion = request.form['direccion']
        cliente.codigo = request.form['codigo']
        db.session.commit()
        return redirect(url_for('clientes'))
    
@app.route('/clientes/<int:cliente_id>/nuevo_diagnostico', methods=['POST'])
def nuevo_diagnostico(cliente_id):
    cliente = Clientes.query.get_or_404(cliente_id)

    # Procesar el formulario de nuevo diagnóstico
    fecha = request.form['fecha']
    encargado = request.form['encargado']
    area = request.form['area']
    servicios = request.form['servicios']
    codigo_diag = request.form['codigo_diag']
    comentarios = request.form['comentarios']
    horas = float(request.form['horas'])
    cotizar = 'cotizar' in request.form  # Verifica si el checkbox está marcado

    # Crear un nuevo detalle asociado al maestro del cliente
    maestro = cliente.maestro[0]  # Ajusta según tu modelo si un cliente puede tener múltiples maestros
    nuevo_detalle = Detalles(fecha=fecha, encargado=encargado, area=area, servicios=servicios,
                            codigo_diag=codigo_diag, comentario=comentarios, horas=horas, cotizar=cotizar)
    maestro.detalles.append(nuevo_detalle)
    db.session.add(nuevo_detalle)
    db.session.commit()

    return redirect(url_for('editar_cliente', id=cliente.id))


@app.route('/clientes/<int:id>/eliminar', methods=['POST'])
def eliminar_cliente(id):
    cliente = Clientes.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('clientes'))

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'GET':
        # Lógica para mostrar el formulario para añadir un nuevo cliente
        return render_template('nuevo_cliente.html')
    elif request.method == 'POST':
        # Lógica para procesar el formulario y agregar un nuevo cliente a la base de datos
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        codigo = request.form['codigo']
        cliente_nuevo = Clientes(nombre=nombre, telefono=telefono, direccion=direccion, codigo=codigo)
        db.session.add(cliente_nuevo)
        db.session.commit()
        return redirect(url_for('clientes'))  # Redirige al listado de clientes después de agregar uno nuevo
    

if __name__ == '__main__':
    app.run(debug=True, port=8000)
