import sys
import fire

from .classmodule import MyClass
from .funcmodule import my_function

#loading methods

from .resamplemodule import getlength
from .resamplemodule import getsize
from .resamplemodule import getduration
from .resamplemodule import downsample
from .resamplemodule import getrate
from .resamplemodule import upsample


from .effectsmodule import file_reverse
from .effectsmodule import slice_back
from .effectsmodule import slice_song
from .effectsmodule import slice_front
from .effectsmodule import posgain
from .effectsmodule import negain
from .effectsmodule import repeat_audio
from .effectsmodule import playback_audio
from .effectsmodule import get_max

from .supereffectmodule import overlay_audio
from .supereffectmodule import normalize_audio
from .supereffectmodule import dynamic_overlay
from .supereffectmodule import combine_audio
from .supereffectmodule import calc_pan

from .loadingmodule import load_mp3
from .loadingmodule import load_wav
from .loadingmodule import load_any
from .loadingmodule import convert_all_mp3
from .loadingmodule import convert_all_wav
from .loadingmodule import change_bit_rate

version = "beta 1.0.0"
info = "A Python Command Line Interface (CLI) that performs Digital Audio Workstations (DAW) actions using Digital Signal Processing (DSP) Techinques and algorithms "
def main():

    args = sys.argv[1:]
    togller = True
    i = 0
    al = len(args)
    
    if(al == 0):
        print ("Welcome to Python CLI a tool to replace DAW using DSP ")
        togller =False
    
    if(al > 0):
        print('Welcome to GUC CLI ')
        print('count of args :: {}'.format(len(args)))
        a_string = args[0]
        first_letter = a_string[:1]
        
        # if( a_string == '-info'):
        #     fire.Fire(info)
        # elif( a_string == '-v'):
        #     fire.Fire(version)
        
    #filter arguments to know which method are we gonna use 
    while(i< al and (togller ==True)):
        
        arg= args[i]
        if( i==0 ):
            if(arg == "loadwav"):
                load_wav(args)
            elif (arg == "loadmp"):
                load_mp3(args)
            elif (arg == "gain"):
                posgain(args)
            elif (arg == "negain"):
                negain(args)
            elif (arg == "upsample"):
                upsample(args)
            elif (arg == "getrate"):
                getrate(args)
            elif (arg == "downsample"):
                downsample(args)
            elif (arg == "getduration"):
                getduration(args)
            elif (arg == "getsize"):
                getsize(args)
            elif (arg == "getlength"):
                getlength(args)
            elif (arg == "reverse"):
                file_reverse(args)
            elif ( arg == "combine"):
                combine_audio(args)
            elif ( arg == "repeat"):
                repeat_audio(args)
            elif ( arg == "slice"):
                slice_song(args)
            elif ( arg == "overlay"):
                overlay_audio(args)
            elif ( arg == "expertoverlay"):
                dynamic_overlay(args)
            elif ( arg == "backslice"):
                slice_back(args)
            elif ( arg == "normalize"):
                normalize_audio(args)
            elif ( arg == "play"):
                playback_audio(args)
            elif ( arg == "wavconvert"):
                convert_all_wav(args)
            elif ( arg == "mp3convert"):
                convert_all_mp3(args)
            elif( arg == "cbr" ):
                change_bit_rate(args)
            elif ( arg == "getmax" ):
                get_max(args)
            else:
                print ("Command is not found or incorrect please try again ")
        print('input argument :: {}'.format(arg))
        i = i+1
    my_function('Operations complete ')
    
    # my_object = MyClass('Peter')
    # my_object.say_name()

if __name__ == '__main__':
    # main()
    fire.Fire()