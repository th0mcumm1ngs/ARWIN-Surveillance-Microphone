import pyaudio, wave, datetime, json, random, os

# configure settings
chunk = 1024 # set the chunk size of 1024 samples
FORMAT = pyaudio.paInt16 # sample format
channels = 1
sample_rate = 44100 # 44100 samples per second
record_seconds = 5 # set the record time in seconds

# open json system settings file
systemSettings = json.load(open('settings.json', 'r'))

# initialize objects
p = pyaudio.PyAudio() # initialize PyAudio object
stream = p.open(format=FORMAT, channels=channels, rate=sample_rate, input=True, output=True, frames_per_buffer=chunk) # open stream object as input & output

def generate_file_name():
    fileName = ""

    for i in range(10):
        fileName += str(random.randint(0, 9))

    if f'{fileName}.wav' in os.listdir("recordings"):
        generate_file_name()
    else:
        return fileName

# save audio file
def save_file(startTime, endTime, channels, FORMAT, sample_rate, frames):

    fileName = generate_file_name()

    # save the actual audio file
    wf = wave.open(f'recordings/{str(fileName)}.wav', "wb") # open the file in 'write bytes' mode
    wf.setnchannels(channels) # set the channels
    wf.setsampwidth(p.get_sample_size(FORMAT)) # set the sample format
    wf.setframerate(sample_rate) # set the sample rate
    wf.writeframes(b"".join(frames)) # write the frames as bytes
    wf.close() # close the file

    # save the start and end times with a file name to map to the audio file
    fileData = {
        'startTime': startTime.strftime("%Y-%m-%d %H:%M:%S"),
        'endTime': endTime.strftime("%Y-%m-%d %H:%M:%S"),
        'fileName': f'{fileName}.wav'
    }

    json.dump(fileData, open(f'file_data/{fileName}.json', 'w'), indent = 4)

while True:
    try:
        frames = []

        startTime = datetime.datetime.now()
        for i in range(int(sample_rate / chunk * record_seconds)):
            data = stream.read(chunk, exception_on_overflow = False)
            frames.append(data)
        endTime = datetime.datetime.now()

        save_file(startTime, endTime, channels, FORMAT, sample_rate, frames)
    except:
        pass

stream.stop_stream() # stop the stream
stream.close() # close the stream object
p.terminate() # terminate pyaudio object