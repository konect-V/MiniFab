import html
from threading import Thread
from flask import Flask, jsonify, render_template, request
from autofirmware import autofirmware_daemon, force_autofirmware, get_error, get_current_toolhead, get_current_firmware_available, get_forced

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', firmware_available=get_current_firmware_available())

@app.route('/error')
def error():
    return "{ \"error\": \"" + html.escape(get_error()).replace("\n", "<br>") + "\"}"

@app.route('/toolhead')
def toolhead():
    return "{ \"toolhead\": \"" + html.escape(get_current_toolhead()) + "\", \"forced\": \"" + str(get_forced()) + "\"}"

@app.route('/firmware_available')
def firmware_available():
    return "{ \"firmware_available\": \"" + html.escape(get_current_firmware_available()) + "\"}"

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
    app.run(port=8000)

