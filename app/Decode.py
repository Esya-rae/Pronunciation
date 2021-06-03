from os import environ, path, listdir
import soundfile as sf
import librosa

import pocketsphinx
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from app.Phonemes import Phonemes
from app.Word import Word

class To_phonemes():

    def __init__(self) -> None:
        #Find Directories
        directory = "/usr/local/lib/python3.8/dist-packages/pocketsphinx/"
        model_directory = directory + "model"
        data_directore = '/home/ubuntu/Pronunciation/app/'
        self.raw_path = path.join(directory, 'temp.raw')

        #Make a configuration
        config = Decoder.default_config()
        config.set_float('-lw', 2.0)
        config.set_float('-beam', 1e-20)
        config.set_float('-pbeam', 1e-20)
        config.set_string('-hmm', path.join(model_directory, 'en-us'))
        config.set_string('-allphone', path.join(model_directory, 'en-us/en-us-phone.lm.dmp'))
        config.set_string('-logfn', 'nul')

        #Make a decoder on the configuration
        self.decoder = Decoder(config)

    def decode(self, path):
        # Convert into '.wav' file into '.raw' file
        y, sr = librosa.load(path, sr=16000, mono=True)
        sf.write(file=self.raw_path, data=y, samplerate=sr, subtype='PCM_16', format='RAW')
        print(self.raw_path, 2)
        #Decode data
        self.decoder.start_utt()
        stream = open(self.raw_path, 'rb')
        while True:
            buffer = stream.read(1024)
            if buffer:
                self.decoder.process_raw(buffer, False, False)
            else:
                break
        self.decoder.end_utt()
        #Make decoded data in right format
        phonemes = Phonemes(self.decoder.seg())
        phonemes.delete_silence()
        phonemes.delete_repetitions()
        phonemes.change_format()
        return phonemes


