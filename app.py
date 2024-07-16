from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, Clientes, Vehiculos, Maestro, Detalles

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
    if request.method == 'GET':
        return render_template('editar_cliente.html', cliente=cliente)
    elif request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.telefono = request.form['telefono']
        cliente.direccion = request.form['direccion']
        cliente.codigo = request.form['codigo']
        db.session.commit()
        return redirect(url_for('clientes'))


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
