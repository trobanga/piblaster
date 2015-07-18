#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mp3database as db
import blueberry
import threading


music_db_file = '/home/pi/piblaster/music.db' # where store mp3 tag data
music_directories = ['/home/pi/music'] # list of directories filled with the finest music


if __name__ == '__main__':

    import sys
    import argparse
    parser = argparse.ArgumentParser(prog='piblaster.py')
    parser.add_argument("--debug", "-d", action='store_true',
                        help="debug, set if not running on raspberry pi")
    parser.add_argument(
        "--scan", "-s", action='store_true', help='scan music directory')
    args = parser.parse_args()

    music_db = db.MusicDB(music_db_file)
    if args.scan:
        try:
            music_db.scan_library(music_directories)
        except Exception, e:
            print e
            print 'bye bye'
            exit(1)
    else:
        music_db.load_db()

    # list artists
    print sorted(music_db.artist_db.keys())
