import pygame
from pygame.locals import *
import playlists
import threading

class Play(object):
    """
    Does all the stuff a good fool does. Plays a song or another.
    Plays louder or shuts up if needs to, but cannot juggle.
    """

    def __init__(self):

        pygame.init()
        

        
        self.cur_playlist = None
        self.is_playing = False
        self.vol = pygame.mixer.music.get_volume()
        self.dvol = 0.10
        self.muted = False

        
    def load_playlist(self, pl):
        print 'set playlist', pl
        self.cur_playlist = pl
        # self.cur_playlist.first()

                
    def vol_up(self):
        self.vol += self.dvol
        if self.vol > 1:
            self.vol = 1
        pygame.mixer.music.set_volume(self.vol)

        
    def vol_down(self):
        self.vol -= self.dvol
        if self.vol < 0:
            self.vol = 0
        pygame.mixer.music.set_volume(self.vol)

        
    def mute(self):
        if self.muted:
            self.muted = False
            pygame.mixer.music.set_volume(self.vol)
        else:
            self.muted = True
            pygame.mixer.music.set_volume(0)

                    
    def next_song(self):
        try:
            self.cur_playlist.next_song()
            if self.cur_playlist.cur_song:
                self.start()
            else:
                self.is_playing = False
        except Exception, e:
            print e

            
    def prev_song(self):
        try:
            self.cur_playlist.prev_song()
            self.start()
        except Exception, e:
            print e

            
    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing = False

        
    def unpause(self):
        pygame.mixer.music.unpause()
        self.is_playing = True

                
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

                
    def start(self):
        """
        Starts playing of self.cur_playlist.cur_song
        """
        if not self.cur_playlist.cur_song:
            self.cur_playlist.first()
        self.is_playing = True
        print 'now playing:',  self.cur_playlist.cur_song
        pygame.mixer.music.load(
            self.cur_playlist.cur_song['path'].encode('utf-8'))
        pygame.mixer.music.play()
        self.play(daemon=True)
        
        
    def play(self, daemon=False):
        """
        Checks if song has finished and starts next from playlist
        """
        if daemon:
            t = threading.Thread(target=self.play)
            t.daemon = True
            t.start()
        else:
            while self.is_playing:
                if not pygame.mixer.music.get_busy() \
                       and self.cur_playlist \
                       and not self.cur_playlist.is_empty() \
                       and self.is_playing:
                    self.next_song()
