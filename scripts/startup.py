import html
from threading import Thread
from flask import Flask, render_template
from autofirmware import autofirmware_daemon, get_error, get_current_toolhead

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/error')
def error():
    return "{ \"error\": \"" + html.escape(get_error()).replace("\n", "<br>") + "\"}"

@app.route('/toolhead')
def toolhead():
    return "{ \"toolhead\": \"" + html.escape(get_current_toolhead()) + "\"}"

if __name__ == '__main__':
    autofirmware_daemon_thread = Thread(target = autofirmware_daemon)
    autofirmware_daemon_thread.daemon = True
    autofirmware_daemon_thread.start()
    app.run(port=8000)

