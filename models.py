from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    codigo = db.Column(db.String(20))
    vehiculos = db.relationship('Vehiculos', backref='cliente', lazy=True)

    @staticmethod
    def generate_codigo(mapper, connection, target):
            last_client = db.session.query(Clientes).order_by(Clientes.id.desc()).first()
            if last_client:
                last_id = int(last_client.codigo[2:])  # Extrae el número de la cadena del último código
                new_id = last_id + 1
                target.codigo = f"AU{new_id:04}"  # Formatea el nuevo código con relleno de ceros
            else:
                target.codigo = "AU0001"  # En caso de que sea el primer cliente

# Escuchar el evento 'before_insert' para generar automáticamente el código
event.listen(Clientes, 'before_insert', Clientes.generate_codigo)

class Detalles(db.Model):
    __tablename__ = 'detalles'
    id = db.Column(db.Integer, primary_key=True)
    id_maestro = db.Column(db.Integer, db.ForeignKey('maestro.id'))
    fecha = db.Column(db.Date)
    encargado = db.Column(db.String(100))
    area = db.Column(db.String(100))
    servicios = db.Column(db.String(100))
    codigo_diag = db.Column(db.String(50))
    comentario = db.Column(db.Text)
    horas = db.Column(db.Time)
    cotizar = db.Column(db.Boolean)
    maestro = db.relationship('Maestro', backref='detalles')

class Maestro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    id_vehiculo = db.Column(db.Integer, db.ForeignKey('vehiculos.id', ondelete='CASCADE'))
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
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)

