import os 
# dir_path = os.path.dirname(os.path.realpath(__file__))
import pydub 
from pydub import AudioSegment

cwd = os.getcwd()
 
from .loadingmodule import load_any


def playback_audio(cmnd):
    print ("Playing an audio file ")
    sound = load_any(cmnd)
    play(sound)
    
def pan(cmnd):
    print ("increasing volume")
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


def get_max(cmnd):
    print ("getting max amplitude of an audio file ")
    sound = load_any(cmnd)
    peak_amplitude = sound.max
    print (peak_amplitude)

def repeat_audio(cmnd):
    print ("repeating audio file")
    output_name = "repeated.wav"
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print "file 1"
    print(input_name)

    repeated_times = 2
    file_type ="wav"
    
    if ( len(cmnd) == 3 ):
        repeated_times = cmnd[2]
    
    if ( len(cmnd) == 4):
        tmp = cmnd[3]
        output_name = str(tmp)
        tmpf = output_name[-3:]
        file_type = str(tmpf)

    sound1 = AudioSegment.from_file(input_name, format="wav")
    # sound2 = AudioSegment.from_file(tf_name, format="wav")
    repeated = sound1 * repeated_times
    repeated.export("repeated.wav", "wav")
    
def slice_front(cmnd):
    print (" Slicing first section from the audio ")

    output_name = "firstslice.wav"
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    
    val=cmnd [2]
    
    file_type = "wav"
    if ( len(cmnd) == 4):
        
        tmp = cmnd[3]
        output_name = str(tmp)
        tmpf = output_name[-3:]
        file_type = str(tmpf)

    song = AudioSegment.from_wav(input_name)
    
    f_song = song[:val*1000]
    
    
    # save the output
    f_song.export(output_name, file_type)

def slice_back(cmnd):
    print (" Slicing back section from the audio ")
    output_name = "lastslice.wav"
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    val=cmnd [2]
    
    file_type = "wav"
    if ( len(cmnd) == 4):
        tmp = cmnd[3]
        output_name = str(tmp)
        tmpf = output_name[-3:]
        file_type = str(tmpf)

    song = AudioSegment.from_wav(input_name)
    
    b_song = song[val*1000:]
    
    # save the output
    b_song.export(output_name, file_type)
    
def slice_song(cmnd):
    print (" Slicing a section from the audio ")
    output_name =  "sliced.wav"
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)

    file_type = "wav"

    if ( len(cmnd) == 5):
        tmp = cmnd[4]
        output_name = str(tmp)
        tmpf = output_name[-3:]
        file_type = str(tmpf)

    val = cmnd [2]
    valt = cmnd [3]
    song = AudioSegment.from_wav(input_name)
    
    s_song = song[val*1000:valt*1000]
    
    
    # save the output
    s_song.export(output_name, file_type)

def file_reverse(cmnd):
    
    print ("reversing track")
    output_name =  "reversed.wav"
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    file_type = "wav"
    
    if ( len(cmnd) == 3):
        tmp = cmnd[2]
        output_name = str(tmp)
        tmpf = output_name[-3:]
        file_type = str(tmpf)

    song = AudioSegment.from_wav(input_name)
    
    backwards = song.reverse()

    # save the output
    backwards.export(output_name, file_type)

def posgain(cmnd):
    
    print ("increasing volume")
    output_name =  "higher.wav"
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    val = cmnd [2]
    file_type = "wav"

    if ( len(cmnd) == 4):
        tmp = cmnd[3]
        output_name = str(tmp)
        tmpf = output_name[-3:]
        file_type = str(tmpf)

    # song = AudioSegment.from_wav(input_name)
    song = load_any(cmnd)
    
    song = song + val

    # save the output
    song.export(output_name, file_type)


def negain(cmnd):
    
    print ("decreasing volume")
    output_name = "quiter.wav"
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    val = cmnd [2]
    file_type = "wav"
    
    if ( len(cmnd) == 4 ):
        tmp = cmnd[3]
        output_name = str(tmp)
        tmpf = output_name[-3:]
        file_type = str(tmpf)

    song = AudioSegment.from_wav(input_name)
    
    song = song - val

    # save the output
    song.export(output_name, file_type)