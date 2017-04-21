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
    """Get the root directory of the current file"""
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):
    """Get the inputed file
        
    filename -- the file to get
    
    @return file, None if it does not exist
    """
    src = os.path.join(root_dir(), filename)
    if os.path.exists(src):
        return open(src).read()
    return None


def get_audio_response(text):
    """Generate the audio response file and get the filename
        
    text -- text to be converted to speech
    """
    global filename
    filename = None
    filename = tts.get_audio(text)


def get_content_data(content):
    """Get data from the json object
        
    content -- the json object
    
    @return data, audio values
    """
    data = content['data']
    audio = content['speak']
    return data, audio


@app.route('/')
@app.route('/home')
def index():
    """Get the home page
    
    @return home page    
    """
    return app.send_static_file('index.html')


@app.route('/data', methods=['POST'])
def add_data():
    """Add new data
    
    @return json with the result    
    """
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
    """Get data with inputed id
    
    data_id -- data id

    @return json, with the result    
    """
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
    """Delete data with inputed id

    data_id -- data id

    @return json, with the result    
    """
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
    """Update data with id inputed

    data_id -- data id

    @return json, with the result    
    """
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
    """Do a search

    @return json, with the result    
    """
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
    """Get the list of available voices
    
    @return json, with the result    
    """
    voicelist = tts.get_voice_list()
    return jsonify(data=voicelist), 200


@app.route('/voice', methods=['POST'])
def set_voice():
    """Set the voice

    @return json, with the result    
    """
    content = request.get_json(silent=True)
    if content is not None:
        data = content['data']
        language, gender = data.split('#')
        gender = True if gender == 'Female' else False
        res = tts.update_settings(language_code=language, female=gender)
        get_audio_response(res)
        return jsonify(data=res), 200
    abort(400) 


@app.route('/voice', methods=['GET'])
def get_voice():
    """Get the current voice settings

    @return json, with the result    
    """
    code, gender = tts.get_voice_settings()
    return jsonify(data={'language':code, 'gender':gender}), 200


@app.route('/audio_response')
def audio():
    """Get the audio file

    @return audio file or 404 if no audio available    
    """
    # will send the saved file if exists
    global filename
    if filename is not None:
        content = get_file(filename)
        if content is not None:
            return Response(content, mimetype='audio/mpeg')
    abort(404)


@app.route('/get-audio', methods=['GET', 'POST'])
def speak_input():
    """Get the audio file

    @return audio file    
    """
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
