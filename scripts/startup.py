from io import StringIO
import sys
from threading import Thread
from flask import Flask, jsonify, render_template, request
from autofirmware import autofirmware_daemon, force_autofirmware, get_logs, get_last_error, get_current_toolhead, get_current_firmware_available, get_forced
from setup import update_config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', firmware_available=get_current_firmware_available())

@app.route('/get_logs')
def json_logs():
    return jsonify({"logs": get_logs()})

@app.route('/last_error')
def last_error():
    return jsonify(error=get_last_error())

@app.route('/toolhead')
def toolhead():
    return jsonify(toolhead=get_current_toolhead(), forced=get_forced())

@app.route('/firmware_available')
def firmware_available():
    return jsonify(firmware_available=get_current_firmware_available())

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/updatemachine')
def updatemachine():
    tmp = sys.stdout

    result = StringIO()
    sys.stdout = result
    update_config()

    sys.stdout = tmp
    return result.getvalue()

@app.route('/forcefirmware', methods=['POST'])
def force_firmware():
    try:
        data = request.get_json()
        firmware = data.get('firmware')

        if firmware:
            force_autofirmware(firmware)
            return jsonify({"message": f"Firmware {firmware} was forced with success!"}), 200
        else:
            return jsonify({"message": "No firmware specified."}), 400

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    autofirmware_daemon_thread = Thread(target = autofirmware_daemon)
    autofirmware_daemon_thread.daemon = True
    autofirmware_daemon_thread.start()
    app.run(host="0.0.0.0", port=8000)

