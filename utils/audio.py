"""
Centralized Audio player
"""
import winsound
class Sounds():
    """
    Initialises variables
    """
    def __init__(self):   
        pass

    def play_bgm(self,file_path):
        winsound.PlaySound(file_path, winsound.SND_FILENAME + winsound.SND_ASYNC + winsound.SND_LOOP)
    def play_sfx(self,file_path):
        winsound.PlaySound(file_path, winsound.SND_FILENAME + winsound.SND_ASYNC)
    def play_none(self):
        winsound.PlaySound(None)

"""
How to Run Aduio Files
1. Aduio Wo interuppting code

from utils.audio import Sounds
Sounds().play_audio("./assets/sounds/sample_launch_able.wav", delay=1)

1.1 Play BG

Sounds().play_audio("bg_music.wav", background=True)

2. Aduio that INTERUPTS code

winsound.PlaySound("Welcome.wav",winsound.SND_FILENAME) #[Finish audio before stop (normal way)]

3. Sys Sounds 

winsound.PlaySound("SystemExit",0) #Exit Game Sound [Finish before continuing code]
"""