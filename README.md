# API to Speech
An example to add speech responses to an API using Python, Flask and Pyvona

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


## Usage

![screenshot](http://i.imgur.com/B2jvNfS.png)

- **Available Voices**
  - Select the voice you want the results to be spoken with.

- **Speak**
  - Turn *on* and *off* speech response
  - speak [ ]: audio feedback off
  - speak [x]: audio feedback on

- **Results**
  - The results will be showned here

- **Add Data**
  - Will create an entry with the inputed text and return the generated ID.
  - *Note:* The result returned is always in english.

- **Get Data**
  - Will get the data with the inputed ID (the inputed text) and show it in the Results and in the Edit Data sections.
  - *Note:* The result if nothing is found will be in english.

- **Edit Data**
  - Will edit the data fetched via Get Data with the new inputed text.
  - *Note:* The result returned (success|fail) is always in english.

- **Delete Data**
  - Will delete the data with the inputed ID.
  - *Note:*  The result returned (success|fail) is always in english.

- **Capitalize**
  - Will get a capitalized version of the inputed text.

- **Search**
  - Will search for the inputed term using duckduck go API and get the first available response (text and a URL or just a URL).
  - Example: Weather in [city name]

- **Get Audio**
  - Used to get an audio file with speech of the inputed text.
    - Request examples for command line using curl:
      - **GET Request**: will generate the curl GET command to get the audio file for the inputed text
      - **POST Request**: will generate the curl POST command to get the audio file for the inputed text
