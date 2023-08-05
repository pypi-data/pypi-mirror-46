import os 
# dir_path = os.path.dirname(os.path.realpath(__file__))
import pydub 
from pydub import AudioSegment
import pyaudio
import numpy as np
cwd = os.getcwd()



def pan(cmnd):
    print "increasing volume"
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    val = cmnd [2]
    song = AudioSegment.from_wav(input_name)
    vl= 0 - val
    panned_right = song.pan(+0.15)

    # pan the sound 50% to the left
    panned_left = song.pan(-0.50)
    
    # save the output
    song.export("leftpan.wav", "wav")


def slicefront(cmnd):
    print " Slicing first section from the audio "
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    val=cmnd [2]
    
    song = AudioSegment.from_wav(input_name)
    
    f_song = song[:val*1000]
    
    
    # save the output
    f_song.export("first.wav", "wav")


def repeat_audio(cmnd):
    print "repeating audio file"
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print "file 1"
    print(input_name)
    # repeated times can be tf 
    # tf = cmnd[2]
    # tf_name= cwd +'/'+ tf
    # print (tf_name)
    sound1 = AudioSegment.from_file(input_name, format="wav")
    # sound2 = AudioSegment.from_file(tf_name, format="wav")
    repeated = sound1 * 2
    repeated.export("repeated.wav", "wav")

def slice_back(cmnd):
    print " Slicing back section from the audio "
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    val=cmnd [2]
    
    song = AudioSegment.from_wav(input_name)
    
    b_song = song[val*1000:]
    
    
    # save the output
    b_song.export("last.wav", "wav")
    
def slice_song(cmnd):
    print " Slicing a section from the audio "
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    val = cmnd [2]
    valt = cmnd [3]
    song = AudioSegment.from_wav(input_name)
    
    s_song = song[val*1000:valt*1000]
    
    
    # save the output
    s_song.export("sliced.wav", "wav")

def file_reverse(cmnd):
    
    print "reversing track"
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    song = AudioSegment.from_wav(input_name)
    
    backwards = song.reverse()

    # save the output
    backwards.export("reversed.wav", "wav")

def posgain(cmnd):
    
    print "increasing volume"
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    val = cmnd [2]
    song = AudioSegment.from_wav(input_name)
    
    song = song + val

    # save the output
    song.export("higher.wav", "wav")


def negain(cmnd):
    
    print "decreasing volume"
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    val = cmnd [2]
    song = AudioSegment.from_wav(input_name)
    
    song = song - val

    # save the output
    song.export("quiter.wav", "wav")