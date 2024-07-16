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

# Crear Cliente
@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'GET':
        return render_template('nuevo_cliente.html')
    elif request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        
        cliente_nuevo = Clientes(nombre=nombre, telefono=telefono, direccion=direccion)
        db.session.add(cliente_nuevo)
        db.session.commit()
        
        # Verificar si el cliente tiene un maestro asociado, si no existe, crearlo
        if not cliente_nuevo.maestro:
            nuevo_maestro = Maestro(id_cliente=cliente_nuevo.id)
            db.session.add(nuevo_maestro)
            db.session.commit()

        return redirect(url_for('clientes'))

# Editar Cliente
@app.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Clientes.query.get_or_404(id)

    if cliente.maestro:
        for maestro in cliente.maestro:
            for detalle in maestro.detalles:
                print(f"Fecha: {detalle.fecha}, Encargado: {detalle.encargado}, Área: {detalle.area}, Servicios: {detalle.servicios}")
    
    if request.method == 'GET':
        return render_template('editar_cliente.html', cliente=cliente)
    elif request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.telefono = request.form['telefono']
        cliente.direccion = request.form['direccion']
        db.session.commit()
        return redirect(url_for('clientes'))

# Crear Nuevo Diagnóstico
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
    cotizar = 'cotizar' in request.form

    # Verificar si el cliente tiene un maestro asociado, si no existe, crearlo
    if not cliente.maestro:
        nuevo_maestro = Maestro(id_cliente=cliente.id)
        db.session.add(nuevo_maestro)
        db.session.commit()

    # Crear un nuevo detalle asociado al maestro del cliente
    maestro = cliente.maestro[0]  # Ajustar según el modelo si un cliente puede tener múltiples maestros
    nuevo_detalle = Detalles(
        fecha=fecha, encargado=encargado, area=area, servicios=servicios,
        codigo_diag=codigo_diag, comentario=comentarios, horas=horas, cotizar=cotizar
    )
    maestro.detalles.append(nuevo_detalle)
    db.session.add(nuevo_detalle)
    db.session.commit()

    return redirect(url_for('editar_cliente', id=cliente.id))

# Editar diagnostico
@app.route('/clientes/<int:cliente_id>/editar-diagnostico/<int:detalle_id>', methods=['GET', 'POST'])
def editar_diagnostico(cliente_id, detalle_id):
    cliente = Clientes.query.get_or_404(cliente_id)
    detalle = Detalles.query.get_or_404(detalle_id)

    if request.method == 'GET':
        return render_template('editar_diagnostico.html', cliente=cliente, detalle=detalle)
    elif request.method == 'POST':
        detalle.fecha = request.form['fecha']
        detalle.encargado = request.form['encargado']
        detalle.area = request.form['area']
        detalle.servicios = request.form['servicios']
        detalle.codigo_diag = request.form['codigo_diag']
        detalle.comentarios = request.form['comentarios']
        detalle.horas = float(request.form['horas'])  # Asegúrate de manejar la conversión adecuada
        detalle.cotizar = 'cotizar' in request.form  # Verifica si el checkbox está marcado

        db.session.commit()
        return redirect(url_for('editar_cliente', id=cliente.id))

# Eliminar Diagnostico
@app.route('/clientes/<int:cliente_id>/eliminar_diagnostico/<int:detalle_id>', methods=['GET'])
def eliminar_diagnostico(cliente_id, detalle_id):
    detalle = Detalles.query.get_or_404(detalle_id)
    db.session.delete(detalle)
    db.session.commit()
    return redirect(url_for('editar_cliente', id=cliente_id))

# Eliminar cliente
@app.route('/clientes/<int:id>/eliminar', methods=['POST'])
def eliminar_cliente(id):
    cliente = Clientes.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('clientes')) 

# Nuevo vehiculo
@app.route('/clientes/<int:cliente_id>/nuevo_vehiculo', methods=['POST'])
def nuevo_vehiculo(cliente_id):
    if request.method == 'POST':
        # Obtener los datos del formulario
        modelo = request.form.get('modelo')
        placa = request.form.get('placa')
        marca = request.form.get('marca')
        vin = request.form.get('vin')  # Asegúrate de capturar el campo 'vin' correctamente
        ano_del_carro = request.form.get('ano_del_carro')
        vencimiento_placa = request.form.get('vencimiento_placa')

        # Crear un nuevo vehículo para el cliente dado
        nuevo_vehiculo = Vehiculos(
            id_cliente=cliente_id,
            modelo=modelo,
            placa=placa,
            marca=marca,
            vin=vin,  # Asegúrate de incluir 'vin' en la creación del objeto Vehiculos
            ano_del_carro=ano_del_carro,
            vencimiento_placa=vencimiento_placa
        )

        # Guardar el nuevo vehículo en la base de datos
        db.session.add(nuevo_vehiculo)
        db.session.commit()

        # Redirigir de vuelta a la página de edición del cliente
        return redirect(url_for('editar_cliente', id=cliente_id))

    # Si la solicitud no es POST, manejar según tu lógica de aplicación (por ejemplo, mostrar un error)
    return "Error: Método no permitido", 405

# Editar vehiculo
@app.route('/clientes/<int:cliente_id>/editar_vehiculo/<int:vehiculo_id>', methods=['GET', 'POST'])
def editar_vehiculo(cliente_id, vehiculo_id):
    cliente = Clientes.query.get_or_404(cliente_id)
    vehiculo = Vehiculos.query.get_or_404(vehiculo_id)

    if request.method == 'GET':
        return render_template('editar_vehiculo.html', cliente=cliente, vehiculo=vehiculo)
    elif request.method == 'POST':
        vehiculo.modelo = request.form['modelo']
        vehiculo.placa = request.form['placa']
        vehiculo.marca = request.form['marca']
        vehiculo.ano_del_carro = request.form['ano_del_carro']
        vehiculo.vencimiento_placa = request.form['vencimiento_placa']
        vehiculo.vin = request.form['vin']  # Asegúrate de manejar el campo VIN adecuadamente

        db.session.commit()
        return redirect(url_for('editar_cliente', id=cliente_id))


# Eliminar vehiculo
@app.route('/clientes/<int:cliente_id>/eliminar_vehiculo/<int:vehiculo_id>', methods=['GET'])
def eliminar_vehiculo(cliente_id, vehiculo_id):
    vehiculo = Vehiculos.query.get_or_404(vehiculo_id)
    db.session.delete(vehiculo)
    db.session.commit()
    return redirect(url_for('editar_cliente', id=cliente_id))



if __name__ == '__main__':
    app.run(debug=True, port=8000)
