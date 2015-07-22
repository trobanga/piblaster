#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mp3database as db
from blueberry_server import BlueberryServer
import threading


class Piblaster(object):

    music_db_file = '/home/pi/piblaster/music.db' # where store mp3 tag data
    music_directories = ['/home/pi/music'] # list of directories filled with the finest music



    # command lists:
    # general command format: cmd,num-id,payload\n
    # num-id is a (random?) identifier, used for splitting messages and as response code


    # command list receiving:
    # SEND_SONG_DB_VERSION: send version
    # SEND_SONG_DB: send song database to phone
    #    including artist names and albums with songs
    # SEND_PLAYLIST: send current playlist to phone
    # APPEND_SONG: append song to playlist
    # APPEND_ALBUM: append album to playlist
    # APPEND_ARTIST: append all albums from artist to playlist
    # PLAY_SONG: play song, new playlist
    # PLAY_ALBUM: play album, new playlist
    # PLAY_ARTIST: play all albums from artist, new playlist
    # PREPEND_SONG: prepend song to playlist
    # PREPEND_ALBUM: prepend album to playlist
    # PREPEND_ARTIST: prepend all albums from artist to playlist
    cmd_recv_list = ['SEND_SONG_DB_VERSION', 'SEND_SONG_DB', 'SEND_PLAYLIST', 
                     'APPEND_SONG', 'APPEND_ALBUM', 'APPEND_ARTIST', 
                     'PLAY_SONG', 'PLAY_ALBUM', 'PLAY_ARTIST', 
                     'PREPEND_SONG', 'PREPEND_ALBUM', 'PREPEND_ARTIST']

    # command list sending:
    # ACK: send ack
    # DB_DATA: data chung of music DB
    # DB_SIZE: length of DB string, poor man's checksum
    # DB_PACKET_COUNT: number of packets that will be send for transferring the DB
    # SONG_DB_VERSION
    cmd_snd_list = ['ACK', 'DB_DATA', 'DB_SIZE', 'DB_PACKET_COUNT', 'SONG_DB_VERSION']
    
    
    def __init__(self):
        self.bt = BlueberryServer()
        self.bt.connect()
        self.run()




    def send(self, cmd, payload):
        if self.bt.connected and cmd in cmd_snd_list:
            self.bt.send("{},{}".format(cmd, payload))
            return True
        else:
            return False


    def receive(self):
        if not self.bt.messages.empty():
            # received new message
            m = self.bt.messages.get()
            for c in m:
                print c, ord(c)




    def run(self):
        """Main loop"""
        while True:
            self.receive()            
                    
            





if __name__ == '__main__':

    import sys
    import argparse
    parser = argparse.ArgumentParser(prog='piblaster.py')
    parser.add_argument("--debug", "-d", action='store_true',
                        help="debug, set if not running on raspberry pi")
    parser.add_argument(
        "--scan", "-s", action='store_true', help='scan music directory')
    args = parser.parse_args()

    # music_db = db.MusicDB(music_db_file)
    # if args.scan:
    #     try:
    #         music_db.scan_library(music_directories)
    #     except Exception, e:
    #         print e
    #         print 'bye bye'
    #         exit(1)
    # else:
    #     music_db.load_db()

    # # list artists
    # print sorted(music_db.artist_db.keys())



    piblaster = Piblaster()
    
