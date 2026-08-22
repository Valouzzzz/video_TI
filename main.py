import time

from video_convertor import convertor
from color import convertor_Ti

name_file = str(input("Video file name (place in the folder) : "))

convertor(name_file)
time.sleep(2)
convertor_Ti(name_file)