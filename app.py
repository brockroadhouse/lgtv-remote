import json
from flask import Flask, session,render_template
from os import environ
from pywebostv.connection import WebOSClient
from pywebostv.controls import InputControl, SourceControl, MediaControl

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.secret_key = '90234jkfn08s8ejS'
TV_IP=environ.get('TV_IP')

@app.before_first_request
def before_first_request_func():
    get_client()

@app.context_processor
def inject_input_sources():
    hdmi = get_hdmi_labels()
    return dict(sources=enumerate(hdmi))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hdmi/<id>')
def hdmi(id):
    sc = get_source_control()
    hdmis = list(get_hdmi_inputs())
    sc.set_source(hdmis[int(id)])
    return json.dumps('success')

@app.route('/volUp')
def volUp():
    mc = get_media_control()
    mc.volume_up()
    return 'Volume up.'

@app.route('/volDown')
def volDown():
    mc = get_media_control()
    mc.volume_down()
    return 'Volume down.'

@app.route('/mute')
def mute():
    mc = get_media_control()
    muted = mc.get_volume()['volumeStatus']['muteStatus']
    mc.mute(not muted)
    return mc.get_volume()

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

@app.route('/button/<command>')
def button(command):
    # DANGEROURS
    run_input(command)
    return "Pressed."

def run_input(command):
    client = get_client()

    inp = InputControl(client)
    inp.connect_input()
    getattr(inp, command)()
    inp.disconnect_input()

def get_hdmi_labels():
    sources = get_hdmi_inputs()
    return list(source['label'] for source in sources)

def get_hdmi_inputs():
    sources = get_sources()
    return (source for source in sources if(source['id'].startswith('HDMI')))    

def get_sources(client=False):
    client = client or get_client()
    return get_source_control(client).list_sources()

def get_media_control():
    return MediaControl(get_client())

def get_source_control(client=False):
    client = client or get_client()
    return SourceControl(client)

def get_client():
    store = session.get('store', {})
    client = WebOSClient(TV_IP)
    client.connect()
    for status in client.register(store):
        print(status)
        # if status == WebOSClient.PROMPTED:
        #     #log prompted
        # elif status == WebOSClient.REGISTERED:
        #     #log registrers
    session['store'] = store
    return client

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')