from flask import Flask, render_template
from threading import Thread
from autofirmware import autofirmware_daemon, get_error, get_current_toolhead

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', error=get_error(), toolhead=get_current_toolhead())

if __name__ == '__main__':
    autofirmware_daemon_thread = Thread(target = autofirmware_daemon)
    autofirmware_daemon_thread.daemon = True
    autofirmware_daemon_thread.start()
    app.run(port=8000)
    
