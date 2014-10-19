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

start a simulation
------------------
http://ip:8080/gatling/{simulation_name}/start

stop a simulation
------------------
http://ip:8080/gatling/{simulation_name}/stop

