from glob import glob
from pydub import AudioSegment


from pydub.generators import WhiteNoise

from random import *

import math
import os 

from .resamplemodule import returnduration

from .loadingmodule import load_any

cwd = os.getcwd()

def write_script(cmnd):
    print (" Write the Commands following the block diagram instructions ")
    script_list = raw_input("Please abide to syntax ")

    print (script_list)

def normalize_audio(cmnd):
    print ("Normalizing audio file ")
    output_name = "normalized.wav"
    sound = load_any(cmnd)

    file_type = "wav"
    if ( len(cmnd) == 3):
        
        tmp = cmnd[2]
        output_name = str(tmp)
        tmpf = output_name[-3:]
        file_type = str(tmpf)

    normalized_sound = sound.apply_gain(-sound.max_dBFS)

    normalized_sound.export(output_name, file_type)

def fftnoise(f):
    f = np.array(f, dtype='complex')
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1:Np+1] *= phases
    f[-1:-1-Np:-1] = np.conj(f[1:Np+1])
    return np.fft.ifft(f).real

def band_limited_noise(min_freq, max_freq, samples=1024, samplerate=1):
    freqs = np.abs(np.fft.fftfreq(samples, 1/samplerate))
    f = np.zeros(samples)
    idx = np.where(np.logical_and(freqs>=min_freq, freqs<=max_freq))[0]
    f[idx] = 1
    return fftnoise(f)

def generate_noise(cmnd):
    # get the 4 args from the command 
    x = band_limited_noise(200, 2000, 44100, 44100)
    y = np.int16(x * (2**15 - 1))
    y.export("noise.wav","wav")

def calc_pan(index):
    print ("getting song index")

    return cos(radians(index))

def dynamic_overlay(cmnd):
    #gets the largest file duration first and places it the first file in the over lay 
    print ("Overlaying  audio files")
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print ("file 1")
    print(input_name)
    tf = cmnd[2]
    tf_name= cwd +'/'+ tf
    print (tf_name)
    #determining the larger file 
    dur1 = returnduration(input_name)
    dur2 = returnduration(tf_name)
    
    sound1 = load_any(input_name)
    sound2 = load_any(tf_name)

    if( dur1 > dur2 ):
        combined = sound1.overlay(sound2)
    else:
        combined = sound2.overlay(sound1)
        
    combined.export("expertover.wav", format='wav')

def overlay_audio(cmnd):
    print ("Overlaying 2 audio files")
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print ("file 1")
    print(input_name)
    tf = cmnd[2]
    tf_name= cwd +'/'+ tf
    print (tf_name)
    sound1 = AudioSegment.from_file(input_name, format="wav")
    sound2 = AudioSegment.from_file(tf_name, format="wav")
    combined = sound1.overlay(sound2)

    combined.export("over.wav", format='wav')
    

def combine_audio(cmnd):
    
    print ("combining 2 audio file")
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print ("file 1")
    print(input_name)
    tf = cmnd[2]
    tf_name= cwd +'/'+ tf
    print (tf_name)
    sound1 = AudioSegment.from_file(input_name, format="wav")
    sound2 = AudioSegment.from_file(tf_name, format="wav")
    combined = sound1 + sound2
    combined.export("combined.wav", "wav")


def cross_fade(cmnd):
    
    print ("Cross fading")
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    val = cmnd [2]
    
    song_duration = returnduration(input_name)
    song = AudioSegment.from_wav(input_name)
    
    first = song_duration - val
    
    end = song[val *-1000:]
    beginning = song[:first*1000]

    with_style = beginning.append(end, crossfade=val *1000)
    # save the output
    with_style.export("crossfaded.wav", "wav")

def fade_in(cmnd):
    print ("fading in")
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    val = cmnd [2]
    song = AudioSegment.from_wav(input_name)
    awesome = song.fade_in(val)
    # save the output
    awesome.export("fadein.wav", "wav")

def fade_out(cmnd):
    print ("fading out")
    print(cwd)
    text_to_file = cmnd[1]
    input_name= cwd +'/'+ text_to_file
    print(input_name)
    val = cmnd [2]
    song = load_any(cmnd)
    awesome = song.fade_out(val)
    # save the output
    awesome.export("fadeout.wav", "wav")

def eight(cmnd):

    #playlist_songs = [AudioSegment.from_mp3(mp3_file) for mp3_file in glob("mp3/*.mp3")]

    #first_song = playlist_songs.pop(0)
    interval = 0.2 * 1000  # sec

    song = AudioSegment.from_mp3('mp3/castle-of-glass.mp3')
    song_inverted = song.invert_phase()
    song.overlay(song_inverted)

    splitted_song = splitted_song_inverted = []
    song_start_point = 0

    print ("split song in part")
    while song_start_point + interval < len(song):
        splitted_song.append(song[song_start_point:song_start_point + interval])
        #splitted_song_inverted.append(song_inverted[song_start_point:song_start_point+interval])
        song_start_point += interval

    if song_start_point < len(song):
        splitted_song.append(song[song_start_point:])
        #splitted_song_inverted.append(song[song_start_point:])

    print ("end splitting")
    print ("total pieces: " + str(len(splitted_song)))

    ambisonics_song = splitted_song.pop(0)
    pan_index = 0
    #left_db_index = 45
    #right_db_index = 45
    index = 0
    for piece in splitted_song:
        print( "start panning pieces: " + str(index))
        pan_index += 5
        piece = piece.pan(calc_pan(pan_index))
        #WN = WhiteNoise().to_audio_segment(interval).apply_gain(-10.5).pan(-calc_pan(pan_index))
        #piece.overlay(splitted_song_inverted[index].pan(-calc_pan(pan_index)))
        ambisonics_song = ambisonics_song.append(piece, crossfade=interval / 50)
        index += 1
        #left_db_index = calc_left(left_db_index, right_db_index)
        #right_db_index = calc_right(right_db_index, left_db_index)

    # lets save it!
    out_f = open("compiled/castle-of-glass.mp3", 'wb')

    ambisonics_song.export(out_f, format='mp3')