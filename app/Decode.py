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
        directory = "/usr/local/lib/python3.8/dist-packages/pocketsphinx/"
        model_directory = directory + "model"
        data_directore = '/home/ubuntu/Pronunciation/app/'
        self.raw_path = path.join(directory, 'temp.raw')
        print(self.raw_path)
        config = Decoder.default_config()
        config.set_string('-hmm', path.join(model_directory, 'en-us'))
        config.set_string('-allphone', path.join(model_directory, 'en-us/en-us-phone.lm.dmp'))
        config.set_string('-logfn', 'nul')
        config.set_string('-logfn', 'nul')
        config.set_float('-lw', 2.0)
        config.set_float('-beam', 1e-20)
        config.set_float('-pbeam', 1e-20)

        # Decode streaming data.
        self.decoder = Decoder(config)

    def decode(self, path):
        # Convert into 16KHz mono '.raw' file
        print(path)
        y, sr = librosa.load(path, sr=16000, mono=True)
        sf.write(file=self.raw_path, data=y, samplerate=sr, subtype='PCM_16', format='RAW')
        print(self.raw_path, 2)
        self.decoder.start_utt()
        stream = open(self.raw_path, 'rb')
        while True:
            buf = stream.read(1024)
            if buf:
                self.decoder.process_raw(buf, False, False)
            else:
                break
        self.decoder.end_utt()
        #print('Best hypothesis segments: ', [seg.word for seg in self.decoder.seg()])
        phonemes = Phonemes(self.decoder.seg())
        phonemes.delete_silence()
        phonemes.delete_repetitions()
        phonemes.change_format()
        print(phonemes)
        return phonemes


