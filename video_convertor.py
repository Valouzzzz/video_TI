import os
import subprocess

def convertor(name_input:str):
    input_video = name_input
    output_video = "video_108p.mp4"

    if os.path.exists(output_video):
        os.remove(output_video)
        print(f"{output_video} supprimé.")

    subprocess.run([
        "ffmpeg",
        "-i", input_video,
        "-vf", "scale=166:120",
        "-c:v", "libx264",
        "-crf", "30",
        "-c:a", "aac",
        output_video
    ])

    #print("Vidéo convertie !")
