import struct
import wave
import pyaudio
import requests
import pvporcupine
from os import getenv
from dotenv import load_dotenv
load_dotenv()

WHISPER_API_KEY = getenv("WHISPER_API_KEY")
PORCUPINE_API_KEY = getenv("PORCUPINE_API_KEY")

#values taken from Nyle's headset microphone
samplingRate = 48000
numChannels = 2
samplingWidth = 2

def transcribeCommand():
    url = "https://transcribe.whisperapi.com"
    headers = {
    'Authorization': WHISPER_API_KEY
    }
    file = {'file': open('command.wav', 'rb')}
    data = {
    "fileType": "wav",
    "diarization": "false",
    "numSpeakers": "1",
    "url": "",
    "initialPrompt": "",
    "language": "en",
    "task": "transcribe",
    "callbackURL": ""
    }
    response = requests.post(url, headers=headers, files=file, data=data)
    return(response.json())

def getVoiceCommand():
    p =  pyaudio.PyAudio()
    activeListening = p.open(rate = samplingRate, channels = numChannels, format = p.get_format_from_width(samplingWidth), input = True)
    wf = wave.open("command.wav", 'wb')
    wf.setframerate(samplingRate)
    wf.setnchannels(numChannels)
    wf.setsampwidth(samplingWidth)

    print("Recording")
    wf.writeframes(activeListening.read(250000)) #hardcoded number of frames - about 5s of input
    print("Done")

    activeListening.close()
    wf.close()
    p.terminate()

def listen():
    porcupine = pvporcupine.create(
    access_key= PORCUPINE_API_KEY,
    keywords=['jarvis']
    )
    p =  pyaudio.PyAudio()
    passiveListening = p.open(rate = porcupine.sample_rate, channels = 1, format = pyaudio.paInt16, input = True, frames_per_buffer = porcupine.frame_length)
    keywordFound = False
    while (not keywordFound):
        passiveRecording = passiveListening.read(porcupine.frame_length)
        passiveRecording = struct.unpack_from("h" * porcupine.frame_length, passiveRecording)
        keywordIndex = porcupine.process(passiveRecording)
        if(keywordIndex == 0):
            print("keyword detected")
            keywordFound = True
    
    passiveListening.close()
    p.terminate()
    porcupine.delete()
    return True