import os 
# dir_path = os.path.dirname(os.path.realpath(__file__))
import pydub 
import glob
from pydub import AudioSegment
# import pyaudio
# import numpy as np
cwd = os.getcwd()



def convert_all_mp3(cmnd):
    video_dir = cwd
    extension_list = ('*.mp4', '*.flv')
    os.chdir(video_dir)
    for extension in extension_list:
        for video in glob.glob(extension):
            mp3_filename = os.path.splitext(os.path.basename(video))[0] + '.mp3'
            AudioSegment.from_file(video).export(mp3_filename, format='mp3')

def convert_all_wav(cmnd):
    video_dir = cwd
    extension_list = ('*.mp4', '*.flv')
    os.chdir(video_dir)
    for extension in extension_list:
        for video in glob.glob(extension):
            wav_filename = os.path.splitext(os.path.basename(video))[0] + '.wav'
            AudioSegment.from_file(video).export(wav_filename, format='wav')
    
def load_any(cmnd):
    
    print ("Loading file and converting it to wav ")
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    file_type = input_name[-3:]
    print(file_type)
    version = AudioSegment.from_file(input_name, str(file_type) )
    print("The returned type",type(version))
    return version
    # version.export("temporary.wav",format="wav")
    #remember to delete file after operation is called
    #os.remove(cwd +'/temporary.wav')
    # send flag to all functions whether to perform a delete or not 

def load_txt(cmnd, counter):
    print ("Loading file and converting it to wav ")
    print(cwd)
    #text file name
    text_file = cmnd[1]
    i_file=open(text_file,'r')
    for i in range(6):
        i_file.readline() 
        items=i_file.readline().split()
    #input name deducted from file
    input_name= items[counter]
    print(input_name)
    file_type = input_name[-3:]
    print(file_type)
    version = AudioSegment.from_file(input_name, str(file_type) )
    print("The returned type",type(version))
    return version


def change_bit_rate(cmnd):
    print ("Loading file and converting it to wav ")
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    file_type = input_name[-3:]
    val = cmnd [2]
    version = AudioSegment.from_file(input_name, file_type)
    version.export('bitrate'+'.'+file_type,format=file_type , bitrate= val+'k')

def export_with_tags(cmnd):
    print ("Loading file")
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    sound = AudioSegment.from_mp3(input_name)
    sound.export("mashup.mp3", format="mp3", tags={'artist': 'Various artists', 'album': 'Best of 2011', 'comments': 'This album is awesome!'})

def load_wav(cmnd):
    print ("Loading wave") 
    print(cwd)
    text_to_file = cmnd[1]
    
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    # initialize portaudio
    # p = pyaudio.PyAudio()
    # stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=CHUNKSIZE)

    # # do this as long as you want fretsh samples
    # data = stream.read(CHUNKSIZE)
    # numpydata = np.fromstring(data, dtype=np.int16)


    # # close stream
    # stream.stop_stream()
    # stream.close()
    # p.terminate()
    sound = AudioSegment.from_mp3(input_name)
    sound.export(cwd+"/file.wav", format="wav")

def load_mp3(cmnd):
    print "Loading mp3"
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    
    sound = AudioSegment.from_wav(input_name)
    sound.export(cwd+"/outputfile.mp3", format="mp3")