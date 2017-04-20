# API to Speech
An example to add speech responses to an API using Python, Flask and Pyvona

![screenshot](http://i.imgur.com/B2jvNfS.png)

## Installation

```
$ mkdir venv
$ export VENV='path_to_folder'/venv
$ virtualenv $VENV
$ . $VENV/bin/activate
$ $VENV/bin/pip install -U pyvona
$ $VENV/bin/pip install -U texttable
$ $VENV/bin/pip install -U flask
$ $VENV/bin/pip install -U duckduckgo2
$ $VENV/bin/pip install -U bleach
```

## Configuration
Get an [IVONA Speech Cloud Account](https://www.ivona.com/us/for-business/speech-cloud/) and generate credentials: Access and Secret Key

Create configuration file `config.cfg` (or just edit and rename the `config_example.cfg`)

```
[main]
access_key = IVONA_ACCESS_KEY
secret_key = IVONA_SECRET_KEY
```

## Run

```
$ $VENV/bin/python server.py
```

Open browser on printed URL, usually `http://0.0.0.0:5000`.
