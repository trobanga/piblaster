#!/usr/bin/env python
# -*- coding: utf-8 -*-


# class for handling a bluetooth connection with the phones


import bluetooth
from Queue import Queue
import threading
import logging
import subprocess

class BlueberryServer(object):

    uuid = "00001101-0000-1000-8000-00805F9B34FB"

    max_bytes = 1024 # max bytes per bluetooth packet


    def __init__(self):
        self.connected = False
        self.messages = Queue()


    def connect(self):
        try:
            s = subprocess.call("sudo service bluetooth restart", shell=True) # evil hack, fix it
            logging.debug('Bluetooth service restarted retval %d', s)
            self.server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
            self.server_sock.bind(("", bluetooth.PORT_ANY))
            self.server_sock.listen(1)
            self.port = self.server_sock.getsockname()[1]

            bluetooth.advertise_service( self.server_sock, "BlueberryServer",
                                         service_id = self.uuid,
                                         service_classes = [ self.uuid, bluetooth.SERIAL_PORT_CLASS ],
                                         profiles = [ bluetooth.SERIAL_PORT_PROFILE ], 
                                         )

            logging.info('Waiting for connection on RFCOMM channel %d', self.port)
            print("Waiting for connection on RFCOMM channel %d" % self.port)
            self.client_sock, self.client_info = self.server_sock.accept()
            print("Accepted connection from ", self.client_info)
            logging.info("Accepted connection from ", self.client_info)
            self.connected = True
            self.receive(daemon=True)
        except Exception as e:
            print e


    def send(self, s, daemon=False):
        """
        Sends string s
        """        
        if daemon:
            t = threading.Thread(target=self.send, args=(s))
            t.daemon = True
            t.start()
        else:
            self.client_sock.send(s)

    
    def receive(self, daemon=False):
        """Waits for message and saves it in self.messages"""
        if daemon:
            t = threading.Thread(target=self.receive)
            t.daemon = True
            t.start()
        else:
            while self.connected:
                try:
                    msg = self.client_sock.recv(self.max_bytes)
                    self.messages.put(msg)
                except Exception as e:
                    print e
                    self.connected = False
                    self.connect() # try to reconnect


    def close(self):
        """Close all connections."""
        bluetooth.stop_advertising(self.server_sock)
        self.client_sock.close()
        self.server_sock.close()
