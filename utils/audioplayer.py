import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSoundEffect
from PyQt5.QtWidgets import QApplication
import threading

class SoundManager(threading.Thread):
    def __init__(self):
        # needed to run multimedia functions
        if not hasattr(self, "initialized"):
            self.initialized = True  # Prevent re-initialization
            super().__init__()
            self.app = QApplication(sys.argv)
            
            # Set up BGM player
            self.bgm_player = QMediaPlayer()
            self.bgm_player.setVolume(50)  # Set the initial volume (0-100)
            self.current_bgm = None
            
            # Set up SFX player
            self.sfx_player = QSoundEffect()
            self.sfx_player.setVolume(1.0)  # Full volume for SFX

            # Connect to mediaStatusChanged signal to loop BGM
            self.bgm_player.mediaStatusChanged.connect(self.check_bgm_status)
        
    def run(self): # this is a threading subclass thingy that just gets called wwhen the thread starts
        self.app.exec_()
    def get_sound_player_thread(): # Obtain single instance of sound player thread
        instance = SoundManager()
        if not instance.is_alive():
            instance.start()
        return instance
    

    def play_bgm(self, bgm_file):
        """Play background music, interrupt only by calling this method again"""
        if self.current_bgm != bgm_file:  # Check if the same bgm is not playing
            self.current_bgm = bgm_file
            url = QUrl.fromLocalFile(bgm_file)
            content = QMediaContent(url)
            self.bgm_player.setMedia(content)
            self.bgm_player.play()
        
    def stop_bgm(self):
        """Stop the background music"""
        self.bgm_player.stop()
        self.current_bgm = None
        
    def play_sfx(self, sfx_file):
        """Play sound effect without interrupting the BGM"""
        self.sfx_player.setSource(QUrl.fromLocalFile(sfx_file))
        self.sfx_player.play()

    def check_bgm_status(self, status):
        """Check the status of the BGM to loop it"""
        if status == QMediaPlayer.EndOfMedia and self.current_bgm:
            self.play_bgm(self.current_bgm)

# Example:
'''
# Play BGM
SoundManager().play_bgm("./assets/sounds/space_lv1.wav")
# Play sound effect
SoundManager().play_sfx("./assets/sounds/menu_main.wav")
# To stop BGM or change to another one
SoundManager().stop_bgm()
SoundManager().play_bgm("./assets/sounds/space_lv2.wav")
'''
