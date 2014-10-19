gatling-web
===========

A tiny flask app that one can use to trigger Gatling simulations via HTTP
- Note: This is not yet fully functional/tested

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

