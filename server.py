import os
import duckduckgo
import bleach, re
from flask import Flask, abort, Response, request, jsonify
from tts import TextToSpeech
from manage_json import JSONManager

app = Flask(__name__)

# start text to speech
tts = TextToSpeech('en-GB', female=True, max_audio_files=5)
filename = None

# initialize json manager
json_manager = JSONManager()

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):
    src = os.path.join(root_dir(), filename)
    if os.path.exists(src):
        return open(src).read()
    return None


def get_audio_response(text):
    global filename
    filename = None
    filename = tts.get_audio(text)


def get_content_data(content):
    data = content['data']
    audio = content['speak']
    return data, audio


@app.route('/')
@app.route('/home')
def index():
    return app.send_static_file('index.html')


@app.route('/data', methods=['POST'])
def add_data():
    content = request.get_json(silent=True)
    if content is not None:
        data, audio = get_content_data(content)
        result = json_manager.add(data)
        text = 'Data saved with ID ' + str(result)
        if audio:
            get_audio_response(text)
        return jsonify(data=text)
    else:
        return jsonify(data='Nothing to process.')


@app.route('/data/<int:data_id>', methods=['GET'])
def get_data(data_id):
    speak = True if request.args.get('speak') == 'true' else False
    result = json_manager.get(data_id)
    if result is not None:
        text = result['data']
    else:
        text = 'No data found.'
    if speak:
        get_audio_response(text)
    return jsonify(data=text)


@app.route('/data/<int:data_id>', methods=['DELETE'])
def delete_data(data_id):
    speak = True if request.args.get('speak') == 'true' else False
    result = json_manager.delete(data_id)
    if result:
        text = 'Data deleted successfully.'
    else:
        text = 'No data to delete.'
    if speak:
        get_audio_response(text)
    return jsonify(data=text)


@app.route('/data/<int:data_id>', methods=['PUT'])
def put_data(data_id):
    content = request.get_json(silent=True)
    if content is not None:
        data, audio = get_content_data(content)
        result = json_manager.edit(data_id, data)
        if result:
            text = 'Data edited successfully.'
        else:
            text = 'No data to edit with ID - ' + str(data_id) + '.'

        if audio:
            get_audio_response(text)
        return jsonify(data=text)
    else:
        return jsonify(data='Nothing to process.')


@app.route('/capitalize', methods=['POST'])
def capitalize():
    content = request.get_json(silent=True)
    if content is not None:
        data, audio = get_content_data(content)
        response = data.upper()
        if audio:
            get_audio_response(response)
        return jsonify(data=response), 200
    return jsonify(data='Nothing to process.'), 401


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        query = request.args.get('q')
        audio = True if request.args.get('speak') == 'true' else False
    else:
        content = request.get_json(silent=True)
        query, audio = get_content_data(content)
    result = duckduckgo.get_zci(query)
    if result is not None:
        if audio:
            text = re.sub(r'(?:\@|https?\://)\S+', '', str(result).strip(), flags=re.MULTILINE)
            print(text)
            if not bool(text and text.strip()):
                text = query
            print(text)
            get_audio_response(text)
        result = bleach.linkify(result)
        return jsonify(data=result), 200

    return jsonify(data='No search results.'), 200


@app.route('/voicelist', methods=['GET'])
def voice_list():
    voicelist = tts.get_voice_list()
    return jsonify(data=voicelist), 200


@app.route('/voice', methods=['POST'])
def set_voice():
    content = request.get_json(silent=True)
    if content is not None:
        data = content['data']
        language, gender = data.split('#')
        gender = True if gender == 'Female' else False
        res = tts.update_settings(language_code=language, female=gender)
        get_audio_response(res)
        return jsonify(data=res), 200


@app.route('/voice', methods=['GET'])
def get_voice():
    code, gender = tts.get_voice_settings()
    return jsonify(data={'language':code, 'gender':gender}), 200


@app.route('/audio_response')
def audio():
    # will send the saved file if exists
    global filename
    if filename is not None:
        content = get_file(filename)
        if content is not None:
            return Response(content, mimetype='audio/mpeg')
    abort(404)


@app.route('/get-audio', methods=['GET', 'POST'])
def speak_input():
    query = None
    content = None
    if request.method == 'GET':
        query = request.args.get('q')
    else:
        content = request.get_json(silent=True)
        query = content['data']
    if query is not None:
        get_audio_response(query)
        global filename
        if filename is not None:
            content = get_file(filename)
    return Response(content, mimetype='audio/mpeg')
            
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = False)
