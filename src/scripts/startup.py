from io import BytesIO, StringIO
import sys
import os
from threading import Thread
from flask import Flask, jsonify, render_template, request, send_file
from autofirmware import autofirmware_daemon, force_autofirmware, get_logs, get_last_error, get_current_toolhead, get_current_firmware_available, get_forced, get_reload_allowed_firmware, allow_firmware_reload
from setup import update_config

# Create Flask app with correct template and static paths
script_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, 
            template_folder=os.path.join(script_dir, "templates"),
            static_folder=os.path.join(script_dir, "static"))

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
    return jsonify(toolhead=get_current_toolhead(), forced=get_forced(), reload_allowed_firmware=get_reload_allowed_firmware())

@app.route('/firmware_available')
def firmware_available():
    return jsonify(firmware_available=get_current_firmware_available())

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/download_logs')
def download_logs():
    buffer = BytesIO()
    buffer.write('\n'.join(get_logs()).encode('utf-8'))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name='log.txt',
        mimetype='text/plain'
    )

@app.route('/allowfirmwarereload')
def allow_firmware_reload_entry():
    if allow_firmware_reload():
        return jsonify({"message": "Firmware reload allowed."}), 200
    else:
        return jsonify({"message": "Failed to allow firmware reload."}), 500

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
    autofirmware_daemon_thread = Thread(target=autofirmware_daemon)
    autofirmware_daemon_thread.daemon = True
    autofirmware_daemon_thread.start()
    app.run(host="0.0.0.0", port=8000)