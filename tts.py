import pyvona
import ConfigParser
import json
import io, os
import time, random, string

from operator import itemgetter
from texttable import Texttable

class TextToSpeech():


    def __init__(self, language_code="en-GB", female=False, max_audio_files=10):
        """Initialize Text To Speech
        
        language_code -- string, the language code, default -> 'en-GB'
        female -- bool, if the voice gender,  default -> False
        max_audio_file -- int, the maximum number of audio files to keep stored in the folder audio folder, default -> 10
        """
        self.max_audio_files = max_audio_files
        # create directory if it does not exist
        self.directory = './audio'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.voice = self.__load_voice()
        self.voice.codec = 'mp3'
        self.voices_list = self.__get_all_voices()
        self.language_code = language_code
        self.gender = "Female" if female else "Male"
        valid, settings = self.__get_valid_settings(self.language_code, self.gender)
        self.__set_settings(valid, settings)


    def __rand_name(self):
        """Returns a random string with text and numbers."""
        part_one = int(time.time())
        part_two = "".join([random.choice(string.letters) for i in xrange(6)])
        return str(part_one) + '-' + part_two


    def __get_all_voices(self):
        """Returns a dict with the valid voices."""
        with io.open('voices.json', 'r', encoding='utf8') as json_data:
            voices = json.load(json_data)

        return voices
    
    
    def show_supported_voices(self):
        """Prints supported languages and voices."""
        t = Texttable()
        voices = [None] * len(self.voices_list) 
        for index, voice_data in enumerate(self.voices_list):
            voice = [None] * 4
            voice[0] = voice_data["voice_language"]
            voice[1] = voice_data["language"]
            voice[2] = voice_data["gender"]
            voice[3] = voice_data["voice_name"]
            voices[index] = voice
        voices = sorted(voices, key=itemgetter(0))
        voices.insert(0, ['LANGUAGE', 'LANGUAGE CODE',  'GENDER', 'NAME'])
        t.add_rows(voices)
        print(t.draw())


    def get_voice_list(self):
        """Returns the list of voice settings."""
        return self.voices_list
        
        
    def get_voice_settings(self):
        """Returns the language and gender that were setup."""
        return self.language_code, self.gender
        
        
    def __load_voice(self):
        """Loads the keys configuration file and returns pyvona voice object."""
        # get configuration
        configParser = ConfigParser.RawConfigParser()
        configFilePath = r'config.cfg'
        configParser.read(configFilePath)

        access_key = configParser.get('main', 'access_key')
        secret_key = configParser.get('main', 'secret_key')
        # create pyvona voice
        return pyvona.create_voice(access_key, secret_key)


    def __get_valid_settings(self, language, gender):
        """
        Validates the inputed languange and gender.
        
        language -- string
        gender -- string

        Returns a tuple with (True or False, settings or None)
        """
        found = None
        backup = None
        for voice in self.voices_list:
            if voice["language"] == language and voice["gender"] == gender:
                found = voice
            elif voice["language"] == language:
                backup = voice
        if found is not None:
            return (True, found)
        elif backup is not None:
            return (False, backup)
        return (False, None)


    def __set_settings(self, valid, settings):
        """
        Sets the inputed settings if valid or the default ones if not valid.
        
        valid -- boolean, result of get valid settings function
        settings -- dict, settings found by get valid settings function
        """
        if valid:
            self.voice.voice_name = settings["voice_name"]
            self.voice.language = settings["language"]
            self.voice.gender = settings["gender"]
        else:
            if settings is not None:
                print("Couldn't find the inputed gender for the selected " + \
                    "language. \nUsing the " + settings["gender"] + " voice.")
                self.voice.voice_name = settings["voice_name"]
                self.voice.language = settings["language"]
                self.voice.gender = settings["gender"]
            else:
                print("Couldn't find the inputed language. " + \
                   "\nUsing the default values.")
                self.voice.voice_name = "Brian"
                self.voice.language = "en-GB"
                self.voice.gender = "Male"


    def get_audio(self, text):
        """
        Gets the audio for the inputed text and saves it.
        Return the file path.
        
        text -- string
        """
        filename = 'voice_answer_' + self.__rand_name() + '.mp3'
        filepath = os.path.join(self.directory, filename)
        
        self.voice.fetch_voice(text, filepath)
        print('Audiofile ' + filename + ' saved to ' + self.directory)

        # check if files count is bigger than the allowed storage then remove
        sorted_list = sorted(os.listdir(self.directory))
        if len(sorted_list) > self.max_audio_files:
            print('Files count is bigger than the allowed amount.') 
            path = os.path.join(self.directory, sorted_list[0])
            if os.path.exists(path):
               os.remove(path)
               print('File ' + path + ' has been deleted.') 
        return filepath
        
        
    def update_settings(self, language_code="en-GB", female=False):
        self.gender = "Female" if female else "Male"
        self.language_code = language_code
        valid, settings = self.__get_valid_settings(self.language_code, self.gender)
        self.__set_settings(valid, settings)
        if settings is not None:
            result = "Voice set to " + settings["voice_name"]
        else:            
            result = "Voice set to default values"
        return result


if __name__ == '__main__':
    tts = TextToSpeech("en-GB", female=True)
    tts.show_supported_voices()
    tts.get_audio('''
        I see trees of green, red roses too
        I see them bloom, for me and you
        And I think to myself
        What a wonderful world
        ''')