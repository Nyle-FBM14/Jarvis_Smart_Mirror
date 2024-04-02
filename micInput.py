import os
import struct
import wave
import pyaudio
import requests
import pvporcupine
import threading
from os import getenv
from dotenv import load_dotenv
load_dotenv()

WHISPER_API_KEY = getenv("WHISPER_API_KEY")
PORCUPINE_API_KEY = getenv("PORCUPINE_API_KEY")

#values taken from Nyle's headset microphone
samplingRate = 48000
numChannels = 2
samplingWidth = 2
chunk = 48000 * 5 #num of frames to record at a time, it is multiplied by number of seconds
silence_threshold = 10000

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

def checkSilence(audio_data):
    global command_unfinished
    energy = sum(abs(sample) ** 2 for sample in audio_data) / len(audio_data)
    print(energy)
    print(energy > silence_threshold)
    command_unfinished = energy > silence_threshold
def getVoiceCommand():
    global command_unfinished
    p =  pyaudio.PyAudio()
    activeListening = p.open(rate = samplingRate, channels = numChannels, format = p.get_format_from_width(samplingWidth), input = True)
    wf = wave.open("command.wav", 'wb')
    wf.setframerate(samplingRate)
    wf.setnchannels(numChannels)
    wf.setsampwidth(samplingWidth)

    print("Recording")
    '''
    command_unfinished = True
    audio_buffer = b""
    stop_flag = threading.Event()
    
    while(command_unfinished):
        audio_data = activeListening.read(chunk)
        m = threading.Thread(target=checkSilence, kwargs={"audio_data": list(audio_data)})
        m.start()
        audio_buffer += audio_data
        m.join()
    wf.writeframes(audio_buffer)'''

    audio_data = activeListening.read(chunk)
    print("Done")
    wf.writeframes(audio_data)

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