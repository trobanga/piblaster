#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mp3database as db
from blueberry_server import BlueberryServer
import threading
import logging
import md5

class Piblaster(object):

    music_db_file = '/home/pi/piblaster/music.db' # where store mp3 tag data
    music_directories = ['/home/pi/music'] # list of directories filled with the finest music

    music_db_file = '/home/trobanga/Workspace/projects/piblaster/music.db' # where store mp3 tag data
    music_directories = ['/mnt/Banca/Music'] # list of directories filled with the finest music



    # command lists:
    # general command format: cmd,num-id,payload\n
    # num-id is a (random?) identifier, used for splitting messages and as response code


    # command list receiving:
    # SEND_MUSIC_DB_VERSION: send version
    # SEND_MUSIC_DB: send song database to phone
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
    
    # command list sending:
    # ACK: send ack
    # MUSIC_DB_DATA: data chung of music DB
    # DB_SIZE: length of DB string, poor man's checksum
    # DB_PACKET_COUNT: number of packets that will be send for transferring the DB
    # SONG_DB_VERSION
    cmd_snd_list = ['ACK', 'MUSIC_DB_DATA', 'DB_SIZE', 'DB_PACKET_COUNT', 'MUSIC_DB_VERSION']
    
    
    def __init__(self):
        logging.info('Starting')
        
        self.cmd_recv_list = {'SEND_MUSIC_DB_VERSION': self.send_music_db_version, 'SEND_MUSIC_DB': self.send_music_db,
                              'SEND_PLAYLIST': None, 'APPEND_SONG': None, 'APPEND_ALBUM': None, 'APPEND_ARTIST': None, 
                              'PLAY_SONG': None, 'PLAY_ALBUM': None, 'PLAY_ARTIST': None, 
                              'PREPEND_SONG': None, 'PREPEND_ALBUM': None, 'PREPEND_ARTIST': None}

        self.music_db = db.MusicDB(self.music_db_file) # load music db
        self.music_db.load_db()
        # self.bt = BlueberryServer()
        # self.bt.connect()
        self.max_payload = 1000
        self.run()

    def music_db_version(self):
        return md5.md5(self.music_db.json_repr()).hexdigest()

    def create_music_db(self):
        """(Re)creates music db and checksum/music_db_version."""
        try:
            self.music_db.scan_library(self.music_directories)
            logging.info('Successfully scanned %s', self.music_directories)
        except Exception, e:
            logging.error("Could not create music db from %s, error msg: %s", self.music_db_file, e)

    def send_music_db(self, *args):
        db_str = self.music_db.json_repr()
        len_db = len(db_str)
        num_pkt = len_db / self.max_payload + int(len_db % self.max_payload != 0)

        logging.info("Sending %d packets to client", num_pkt)
        
        for p in xrange(num_pkt):
            logging.debug('sending string %d of %d', p, num_pkt)
            self.send('', db_str[p * self.max_payload:(p+1) * self.max_payload])
            

        
        
    def send_music_db_version(self, *args):
        """Send music_db_version to client."""
        self.send('MUSIC_DB_VERSION', self.music_db_version())


    def send(self, cmd, payload):
        """Sends cmd and payload via bluetooth."""
        if self.bt.connected and cmd in cmd_snd_list:
            self.bt.send("{},{}".format(cmd, payload))
            return True
        else:
            return False


    def receive(self):
        """
        Checks bt queue for new messages.
        Packets are split into command and payload.
        Corresponding function is called with payload as parameter.
        
        """
        if not self.bt.messages.empty():
            # received new message
            m = self.bt.messages.get()
            cmd, payload = m.split(',', 1) # split at first comma
            if cmd in self.cmd_recv_list.keys():
                logging.info('cmd: %s, payload: %s', cmd, payload)
                self.cmd_recv_list[cmd](payload)
                



    def run(self):
        """Main loop"""

        self.send_music_db()
        return
        while True:
            # self.receive()
            self.send_music_db()



if __name__ == '__main__':

    import sys
    import argparse
    parser = argparse.ArgumentParser(prog='piblaster.py')
    parser.add_argument("--debug", "-d", action='store_true',
                        help="debug, set if not running on raspberry pi")
    parser.add_argument(
        "--scan", "-s", action='store_true', help='scan music directory')
    args = parser.parse_args()


    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    logging.basicConfig(filename='piblaster.log',level=loglevel, format='%(levelname)s: %(asctime)s %(message)s')
    
    piblaster = Piblaster()
    
