#! ../bin/python

from flask import Flask
from flask import url_for
from flask import redirect
import os.path
import json
import psutil
import subprocess


app = Flask(__name__, instance_relative_config=True)
app.config['GATLING_PATH'] = '/opt/gatling'
app.config['SIM_PATH'] = app.config['GATLING_PATH']+'/user-files/simulations/'
app.config['REPORT_PATH'] = app.config['GATLING_PATH']+'/results/'
app.config['DEBUG'] = False
app.debug = app.config['DEBUG']
app.config.from_envvar('CONFIG_FILE', silent=True)


_GATLING_PATH = app.config['GATLING_PATH']
_SIM_PATH = app.config['SIM_PATH']
_REPORT_PATH = app.config['REPORT_PATH']


def exists(simulation):
    """Function to check if the simulation actually exists
    and returns true or false"""
    app.logger.debug('Checking if file '
                     + _SIM_PATH + simulation + '.scala exits')
    return os.path.exists(_SIM_PATH + simulation + '.scala')


def check(simulation):
    """Checks if a simulation is currently running by
    listing processes"""
    app.logger.debug('Checking if ' + simulation + ' is running')
    procs = []
    _procs = psutil.process_iter()

    for proc in _procs:
        procs.append(proc.as_dict(attrs=['cmdline']))

    for pproc in procs:
        for item in pproc['cmdline']:
            if simulation in item:
                return True

    return False


def sim_action(simulation, action):
    """Starts or stopps a simulation"""
    app.logger.debug('Calling ' + action + ' on ' + simulation)
    if action == 'start' or action == 'stop':

        if action == 'start':
            p = subprocess.Popen([_GATLING_PATH + '/bin/gatling.sh', '-s',
                                 simulation])
            return True

        if action == 'stop':
            procs = []
            _procs = psutil.process_iter()
            for proc in _procs:
                procs.append(proc.as_dict(attrs=['pid', 'cmdline']))

            for pproc in procs:
                for item in pproc['cmdline']:
                    if simulation and 'java' in item:
                        app.logger.debug('Killing PID: ' + str(pproc['pid']))
                        p = subprocess.Popen(['kill', str(pproc['pid'])],
                                             stdout=subprocess.PIPE)
                        return p.communicate()[1]
    return False


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('gatling'), code=302)


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return ''


@app.route('/gatling', methods=['GET'])
@app.route('/gatling/', methods=['GET'])
def gatling():
    """Returns simple text with what url structure we expect"""
    return '<html><body><p style="margin: 20px; font-size: 12pt; font-family: Arial;">\
        Valid path to access a simulation is: /gatling/simulation_name/\
        </p></body></html>'


@app.route('/gatling/<simulation>', methods=['GET'])
@app.route('/gatling/<simulation>/', methods=['GET'])
def gatling_simulation(simulation):
    """Returns the status of a simulation in json format as
    {\"status\": \"running|stopped\"}"""
    if exists(simulation):
        _ret = check(simulation)

        if _ret is True:
            _retval = {"status": "running"}
        else:
            _retval = {"status": "stopped"}

        return json.dumps(_retval, indent=4)
    else:
        return("<h2>Simulation not found!</h2>", 404)


@app.route('/gatling/<simulation>/<action>', methods=['GET'])
def gatling_simulation_action(simulation, action):
    """Returns status of action for simulation, if the status is failed,
    it will try to also give failure details at a best effort basis"""

    _ret = {"status": "failed"}

    if exists(simulation):

        if action == 'start':
            if check(simulation) is True:
                _ret = {"status": "failed", "message": simulation +
                        " is already running"}
                return json.dumps(_ret, indent=4)

        if action == 'stop':
            if check(simulation) is False:
                _ret = {"status": "failed", "message": simulation +
                        " is not running"}
                return json.dumps(_ret, indent=4)

        ret = sim_action(simulation, action)
        if ret is None or True:
            _ret = {"status": "success", "details": ret}
        else:
            _ret = {"status": "failed", "details": ret}

    return json.dumps(_ret, indent=4)


@app.route('/gatling/<simulation>/reports', methods=['GET'])
@app.route('/gatling/<simulation>/reports/', methods=['GET'])
def gatling_simulation_reports(simulation):
    """Returns a list of reports for the simulation in json format as
    {\"reports\": \"['report1','report2',...]\"}"""

    _retval = {"reports": []}

    if exists(simulation):
        return json.dumps(_retval)

    return json.dumps(_retval)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
