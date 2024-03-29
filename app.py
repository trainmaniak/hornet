#!./venv/bin/python3

from flask import Flask, jsonify
import subprocess
from models import Task, TaskData, CmdData, PingData
from wakeonlan import send_magic_packet

app = Flask(__name__)

deviceList = {
    'localhost': '192.168.0.5',
    'oxygen': '192.168.0.2',
    'cobalt': '192.168.0.3',
    'thrain': '192.168.0.7'}

deviceMACList = {
    'oxygen': '70.85.C2.D1.21.F3',
    'thrain': '0c.dd.24.33.30.56'}

commandList = ['wol', 'suspend', 'testssh']

@app.route('/')
def index():
    return "Nothing interest here. Go to /help"

@app.route('/cmd/<device>/<command>')
def cmd(device, command):
    response = Task('cmd', 'fail', CmdData(device, command))

    if (not device in deviceList) or (not command in commandList):
        return response.serialize()

    returnBool = \
            (command == 'wol' and wol(device)) \
            or (command == 'suspend' and suspend(device)) \
            or (command == 'testssh' and test_ssh(device))

    response.status = 'ok' if returnBool else 'fail'
    
    return response.serialize()

@app.route('/ping/<device>')
def ping(device):
    response = Task('ping', 'fail', PingData(device))

    if not device in deviceList:
        return response.serialize()

    cmd = ['ping', '-c', '2', deviceList[device]]
    response.status = 'ok' if subprocess.call(cmd) == 0 else 'fail'

    return response.serialize()

def wol(device):
    if not device in deviceMACList:
        return False

    send_magic_packet(deviceMACList[device])
    return True

def test_ssh(device):
    cmd = ['ssh', '-oStrictHostKeyChecking=no', 'cerebro@' + deviceList[device], '\'uname\'']
    return subprocess.call(cmd) == 0

def suspend(device):
    cmd = ['ssh', '-oStrictHostKeyChecking=no', 'cerebro@' + deviceList[device], '\'bin/suspend\'']
    return subprocess.call(cmd) == 0

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

