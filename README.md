gatling-web
===========

A tiny flask app that one can use to trigger Gatling simulations via HTTP

config
------
To use a custom config file, you need to export a variable CONFIG_FILE with the path to the file. E.g.:
```
export CONFIG_FILE="/opt/gatling-web/app.conf"
```

start the app
-------------
```
python /path/to/gatling-web/app.py
```

check status of simulation
--------------------------
http://ip:8080/gatling/{simulation_name}

Returns JSON with status, e.g.:
```json
{"status": "running"}
```
```json
{"status": "stopped"}
```

start a simulation
------------------
http://ip:8080/gatling/{simulation_name}/start

Returns JSON with status, e.g.:
```json
{"status": "success", "details": "true"}
```

stop a simulation
------------------
http://ip:8080/gatling/{simulation_name}/stop

Returns JSON with status, e.g.:
```json
{"status": "failed", "details": "x"}
```

list reports/results
--------------------
http://ip:8080/gatling/{simulation_name}/reports

Lists reports in JSON format:
```json
{"reports": [] }
```
```json
{"reports": ["sim-123456", "sim-123457"] }
```

download report
--------------------
http://ip:8080/gatling/{simulation_name}/reports/report-ID

This will download a zipped up report.

