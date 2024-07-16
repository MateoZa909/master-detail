from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    codigo = db.Column(db.String(20))

class Detalles(db.Model):
    __tablename__ = 'detalles'
    id = db.Column(db.Integer, primary_key=True)
    id_maestro = db.Column(db.Integer, db.ForeignKey('maestro.id'))
    fecha = db.Column(db.Date)
    encargado = db.Column(db.String(100))
    area = db.Column(db.String(100))
    taller = db.Column(db.String(100))
    servicios = db.Column(db.String(100))
    codigo_diag = db.Column(db.String(50))
    comentarios = db.Column(db.Text)
    horas = db.Column(db.Float)
    cotizar = db.Column(db.Boolean)

    maestro = db.relationship('Maestro', backref='detalles')

class Maestro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    id_vehiculo = db.Column(db.Integer, db.ForeignKey('vehiculos.id'))
    cotizacion = db.Column(db.String)
    comentarios = db.Column(db.Text)
    cliente = db.relationship('Clientes', backref='maestro', cascade='all, delete')

class Vehiculos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    vin = db.Column(db.String(50))
    modelo = db.Column(db.String(100))
    placa = db.Column(db.String(20))
    vencimiento_placa = db.Column(db.Date)
    marca = db.Column(db.String(100))
    ano_del_carro = db.Column(db.Integer)
