from flask import Flask
from flask import abort
from flask import render_template
from flask import request
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
import datetime
import json
import os
import subprocess
import time

app = Flask(__name__)
http_server = HTTPServer(WSGIContainer(app))

machines = {}
class Timestamps:
    def __init__(self):
        self.start_time = 0
        self.create_time = 0
        self.destroy_time = 0
        self.reset_time = 0

timestamps = Timestamps()

class Machine:
    def __init__(self, image_name, system_name,
        screenshot_filename, infections):
        self.creation_time = time.time()
        self.image_name = image_name
        self.system_name = system_name
        self.screenshot_filename = screenshot_filename
        self.infections = infections

@app.template_filter('gen_time')
def gen_time(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp)
    fdate = date.strftime('%Y-%m-%d at %H:%M:%S Eastern Time')
    return fdate


@app.template_filter('small')
def small(filename):
    filename = os.path.splitext(filename)[0]
    filename = filename + '_small.png'
    return filename


@app.route('/', methods = ['GET'])
def index():
    return render_template('index.tmpl', machines=machines,
        timestamps=timestamps)


@app.route('/about', methods = ['GET'])
def about():
    return render_template('about.tmpl')


@app.route('/vmhost/report_infection', methods = ['POST'])
def report():
    source_ip = request.remote_addr
    if source_ip.startswith('192.168.') is False:
        abort(403)

    target = None
    for machine in machines:
        image_name = machine.image_name
        proc = subprocess.Popen(['VBoxManage',
            'guestproperty', 'enumerate', image_name],
            stdout=subprocess.PIPE)

        data = proc.stdout.read()
        if source_ip in data:
            target = machine
            break

    if target is None:
        abort(500)

    infection_name = request.form['infection']
    if infection_name not in target.infections:
        target.infections.append(infection_name)

    return 'Success'


@app.route('/details/<vmname>', methods = ['GET'])
def details(vmname):
    if vmname not in machines:
        abort(404)

    machine = machines[vmname]
    return render_template('details.tmpl', machine=machine)


@app.route('/update', methods = ['POST'])
def update():
    source_ip = request.remote_addr
    if source_ip != '127.0.0.1':
        print('Rejected attempted update from ' + source_ip)
        abort(403)

    global machines
    machines = {}

    data = request.data.decode('utf-8')
    data = json.loads(data)

    for machine in data['machines']:
        image_name = machine['image_name']
        system_name = machine['system_name']
        capture_file = machine['screenshot_filename']
        infections = machine['infections']

        if capture_file is not None:
            capture_file = capture_file.rsplit('/', 1)[-1]

        machine = Machine(image_name, system_name,
            capture_file, infections)

        machines[image_name] = machine

    global timestamps
    timestamps.start_time = data['start_time']
    timestamps.create_time = data['create_time']
    timestamps.destroy_time = data['destroy_time']
    timestamps.reset_time = data['reset_time']

    return 'Success'

if __name__ == '__main__':
    print('Starting the HTTP server...')
    http_server.listen(5000)
    IOLoop.instance().start()
