from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='Off')
    consumption = db.Column(db.Float, nullable=False, default=0.0)
    rating = db.Column(db.Float, nullable=False)
    history = db.relationship('ConsumptionHistory', backref='device', cascade="all, delete-orphan", lazy=True)

class ConsumptionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    voltage = db.Column(db.String(10), nullable=False)
    current = db.Column(db.String(10), nullable=False)
    power = db.Column(db.String(10), nullable=False)
    energy = db.Column(db.String(10), nullable=False)
    frequency = db.Column(db.String(10), nullable=False)
    pf = db.Column(db.String(10), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)