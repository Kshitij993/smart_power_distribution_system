# Smart Power Distribution System

This is a Flask application that manages devices and their consumption data. It allows users to add, configure, turn on/off, and remove devices. The application also displays real-time data such as voltage, current, power, energy, and frequency for each device.

## Project Structure

```
my-flask-app
├── app
│   ├── __init__.py
│   ├── cli.py
│   ├── models.py
│   ├── routes.py
│   ├── static
│   │   └── styles.css
│   └── templates
│       ├── devices.html
│       └── index.html
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd my-flask-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To initialize the database and start the scheduler, run the following commands:
```
flask init_db
flask start_scheduler
```

To run the application, execute the following command:
```
python run.py
```

The application will start on `http://127.0.0.1:5000/`.

## Features

- **Add Device**: Add a new device with a name and wattage rating.
- **Configure Device**: Configure the name and wattage rating of an existing device.
- **Turn On/Off Device**: Turn on or off a device. When a device is turned on, it starts recording consumption data.
- **Remove Device**: Remove an existing device.
- **Real-time Data**: Display real-time data such as voltage, current, power, energy, and frequency for each device.
- **Consumption Data**: View total consumption data and top power-consuming devices.

## Contributing

Feel free to submit issues or pull requests for any improvements or features you'd like to see!