import random
import logging
from datetime import datetime
from flask import Blueprint, render_template, jsonify, request, current_app
from app.models import db, Device, ConsumptionHistory

bp = Blueprint('main', __name__)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize serial connection with error handling
ser = None
# try:
#     ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
# except serial.SerialException as e:
#     ser = None
#     logger.error(f"Could not open serial port: {e}")

@bp.route('/')
def home():
    devices = Device.query.all()
    return render_template('index.html', devices=devices)

@bp.route('/devices')
def devices_page():
    devices = Device.query.all()
    return render_template('devices.html', devices=devices)

@bp.route('/turn_off/<int:device_id>', methods=['POST'])
def turn_off(device_id):
    device = Device.query.get(device_id)
    if device:
        device.status = 'Off'
        device.consumption = 0.0
        db.session.commit()
    return jsonify(success=True)

@bp.route('/turn_on/<int:device_id>', methods=['POST'])
def turn_on(device_id):
    device = Device.query.get(device_id)
    if device:
        device.status = 'On'
        voltage, current, power, energy, frequency, pf = read_sensor_data()
        device.voltage = f"{voltage}V"
        device.current = f"{current}A"
        device.power = f"{power}kW"
        device.energy = f"{energy}kWh"
        device.frequency = f"{frequency}Hz"
        db.session.commit()
    return jsonify(success=True)

@bp.route('/configure/<int:device_id>', methods=['POST'])
def configure(device_id):
    device = Device.query.get(device_id)
    if device:
        device.name = request.form.get('name')
        device.rating = float(request.form.get('rating'))
        db.session.commit()
    return jsonify(success=True)

@bp.route('/add_device', methods=['POST'])
def add_device():
    name = request.form.get('name')
    rating = float(request.form.get('rating'))
    new_device = Device(name=name, rating=rating)
    db.session.add(new_device)
    db.session.commit()
    return jsonify(success=True, device=new_device.id)

@bp.route('/remove_device/<int:device_id>', methods=['POST'])
def remove_device(device_id):
    device = Device.query.get(device_id)
    if device:
        db.session.delete(device)
        db.session.commit()
    return jsonify(success=True)

@bp.route('/consumption_data')
def consumption_data():
    devices = Device.query.all()
    total_consumption = {
        "labels": [],
        "data": []
    }
    top_devices = {
        "labels": [],
        "data": []
    }

    # Collect total consumption data
    for device in devices:
        history = ConsumptionHistory.query.filter_by(device_id=device.id).all()
        for entry in history:
            timestamp = entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            power = float(entry.power.replace('W', ''))
            if timestamp not in total_consumption['labels']:
                total_consumption['labels'].append(timestamp)
                total_consumption['data'].append(power)
            else:
                index = total_consumption['labels'].index(timestamp)
                total_consumption['data'][index] += power

    # Collect top 3 power consuming devices
    device_consumptions = [(device.name, float(ConsumptionHistory.query.filter_by(device_id=device.id).order_by(ConsumptionHistory.timestamp.desc()).first().power.replace('W', ''))) for device in devices if ConsumptionHistory.query.filter_by(device_id=device.id).first()]
    device_consumptions.sort(key=lambda x: x[1], reverse=True)
    top_3_devices = device_consumptions[:3]

    for device_name, power in top_3_devices:
        top_devices['labels'].append(device_name)
        top_devices['data'].append(power)

    return jsonify(success=True, totalConsumption=total_consumption, topDevices=top_devices)

@bp.route('/device_data/<int:device_id>')
def device_data(device_id):
    device = Device.query.get(device_id)
    if device:
        latest_history = ConsumptionHistory.query.filter_by(device_id=device.id).order_by(ConsumptionHistory.timestamp.desc()).first()
        if latest_history:
            return jsonify(success=True, device={
                'id': device.id,
                'name': device.name,
                'status': device.status,
                'voltage': latest_history.voltage,
                'current': latest_history.current,
                'power': latest_history.power,
                'energy': latest_history.energy,
                'frequency': latest_history.frequency,
                'rating': device.rating
            })
    return jsonify(success=False)

# Schedule the update_device_history function to run every second
from threading import Timer

def read_sensor_data():
    # if ser is None:
    #     return None, None, None, None, None, None
    # ser.write(b'\xB0\xC0\xA8\x01\x01\x00\x1A')  # Example command to read data from PZEM-004T
    # data = ser.read(7)  # Read 7 bytes of data
    # if len(data) == 7:
    #     voltage = data[0] + data[1] / 10.0
    #     current = data[2] + data[3] / 100.0
    #     power = data[4] + data[5] / 10.0
    #     energy = data[6] / 100.0
    #     frequency = 50.0  # Assuming a fixed frequency
    #     pf = 1.0  # Assuming a fixed power factor
    #     return voltage, current, power, energy, frequency, pf
    voltage = round(random.uniform(220.0, 240.0), 2)
    current = round(random.uniform(0.0, 10.0), 2)
    power = round(voltage * current / 1000.0, 2)  # Power in kW
    energy = round(random.uniform(0.0, 100.0), 2)
    frequency = 50.0  # Assuming a fixed frequency
    pf = round(random.uniform(0.8, 1.0), 2)  # Power factor
    return voltage, current, power, energy, frequency, pf

def update_device_history(app):
    with app.app_context():
        devices = Device.query.all()
        for device in devices:
            if device.status == 'On':  # Only update history if the device is on
                voltage, current, power, energy, frequency, pf = read_sensor_data()
                timestamp = datetime.now()
                history_entry = ConsumptionHistory(
                    timestamp=timestamp,
                    voltage=f"{voltage}V",
                    current=f"{current}A",
                    power=f"{power}kW",
                    energy=f"{energy}kWh",
                    frequency=f"{frequency}Hz",
                    pf=f"{pf}",
                    device_id=device.id
                )
                db.session.add(history_entry)
        db.session.commit()

def schedule_update(app):
    update_device_history(app)
    Timer(1, schedule_update, args=[app]).start()