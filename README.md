# Pronunciation
For the installation of the project follow the steps

1. Start a virtual environment
    virtualenv env
2. Activate a virual environment
    source env/bin/activate
3. Install libraries
    pip3 install hypercorn
    pip3 install fastapi
    pip3 install pocketsphinx
    pip3 install soundfile
    pip3 install librosa
     pip3 install python-multipart
4. If you get this error "RuntimeError: new_Decoder returned -1":
        Please change the directory in Decode.py to the directory where is your pocketsphinx.

