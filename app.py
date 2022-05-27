import json
from flask import Flask, session,render_template
from pywebostv.connection import WebOSClient
from pywebostv.controls import InputControl, SourceControl

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.secret_key = '90234jkfn08s8ejS'

@app.before_first_request
def before_first_request_func():
    store = {}
    client = WebOSClient("192.168.1.89")
    client.connect()
    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")
        elif status == WebOSClient.REGISTERED:
            print("Registration successful!")

    session['store'] = store

@app.context_processor
def inject_input_sources():
    sources = get_sources()
    return dict(sources=enumerate(map(lambda s: s.label, sources)))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hdmi/<id>')
def hdmi(id):
    sc = get_source_control()
    sc.set_source(sc.list_sources()[id])
    return json.dumps('success')


@app.route('/home')
def home():
    run_input('home')
    return "Pressed."

@app.route('/settings')
def settings():
    run_input('menu')
    return "Pressed."

@app.route('/back')
def back():
    run_input('back')
    return "Pressed."

@app.route('/guide')
def dash():
    run_input('dash')
    return "Pressed."

def run_input(command):
    client = get_client()

    inp = InputControl(client)
    inp.connect_input()
    getattr(inp, command)()
    inp.disconnect_input()

def get_sources(client=False):
    client = client or get_client()
    return get_source_control(client).list_sources()

def get_source_control(client=False):
    client = client or get_client()
    return SourceControl(client)

def get_client():
    print('gettingclient')
    store = session.get('store', {})
    client = WebOSClient("192.168.1.89")
    client.connect()
    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")
        elif status == WebOSClient.REGISTERED:
            print("Registration successful!")

    return client

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')