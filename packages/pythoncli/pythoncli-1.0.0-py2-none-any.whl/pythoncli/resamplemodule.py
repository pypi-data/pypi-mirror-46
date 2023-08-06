import os 
# dir_path = os.path.dirname(os.path.realpath(__file__))
import pydub 
from pydub import AudioSegment

cwd = os.getcwd()
import wave
import contextlib



def upsample(cmnd):
    print ("upsampling to 48000 Hz")
    print(cwd)
    text_to_file = cmnd[1]
    
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    # # initialize portaudio
    # p = pyaudio.PyAudio()
    # stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=CHUNKSIZE)

    # # do this as long as you want fretsh samples
    # data = stream.read(CHUNKSIZE)
    # numpydata = np.fromstring(data, dtype=np.int16)

    # close stream
    # stream.stop_stream()
    # stream.close()
    # p.terminate()
    CHANNELS = 2
    swidth = 2
    spf = wave.open(input_name, 'rb')
    RATE=spf.getframerate()
    print( " Current frame rate is ")
    print(RATE)
    signal = spf.readframes(-1)
    if (RATE == 48000):
        return
    else:
        wf = wave.open('changed.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(swidth)
        Change_RATE = 1 + (1- RATE / 48000 )
        wf.setframerate(RATE*Change_RATE)
        wf.writeframes(signal)
        wf.close()

def getrate(cmnd):
    
    print ("Getting frame rate")
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
  
    CHANNELS = 2
    spf = wave.open(input_name, 'rb')
    RATE=spf.getframerate()
    print (" Current frame rate is ")
    print(RATE)

def getduration(cmnd):
    print ("The file duration of")
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    # CHANNELS = 2
    # spf = wave.open(input_name, 'rb')
    # RATE=spf.getframerate()
    # file_size =os.path.getsize(input_name)
    # # time = FileLength / (Sample Rate * Channels * Bits per sample /8)
    # time = file_size / (RATE * CHANNELS * 2)
    # print(time)
    with contextlib.closing(wave.open(input_name,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        print(duration)

def returnduration(input_name):
    
    print(input_name)
   
    with contextlib.closing(wave.open(input_name,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        print(duration)
        return duration
    return -1

def getsize(cmnd):
    print ("The file size of")
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    file_size =os.path.getsize(input_name)
    # + 0.0 to make size a float number
    siz = file_size + 0.0
    cu = 0
    while(siz > 1024):
        siz= siz/1024
        cu = cu + 1
    if(cu == 1):
        print (siz , " KB")
    elif(cu ==2):
        print (siz , " MB")
    elif(cu ==3):
        print (siz , " GB")

def getlength(cmnd):
    print ("The track length")
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    
    sound1 = AudioSegment.from_file(input_name, format="wav")
    duration_in_milliseconds = len(sound1)
    millis = duration_in_milliseconds
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24
    
    print ("%d:%d:%d" % (hours, minutes, seconds))

def downsample(cmnd):
    
    print ("upsampling to 8000 Hz")
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    # initialize portaudio
    CHANNELS = 2
    swidth = 2
    spf = wave.open(input_name, 'rb')
    RATE=spf.getframerate()
    print( " Current frame rate is ")
    print(RATE)
    signal = spf.readframes(-1)
    if (RATE == 8000):
        return
    else:
        wf = wave.open('changed.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(swidth)
        Change_RATE = ( RATE / 8000 ) -1
        wf.setframerate(RATE*Change_RATE)
        wf.writeframes(signal)
        wf.close()


