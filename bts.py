#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bluetooth

class BlueberryServer(object):

    uuid = "00001101-0000-1000-8000-00805F9B34FB"


    def __init__(self):
        pass

    def connect(self):
        self.server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)
        self.port = self.server_sock.getsockname()[1]



        bluetooth.advertise_service( self.server_sock, "BlueberryServer",
                           service_id = self.uuid,
                           service_classes = [ self.uuid, bluetooth.SERIAL_PORT_CLASS ],
                           profiles = [ bluetooth.SERIAL_PORT_PROFILE ], 
                           )

        
        print("Waiting for connection on RFCOMM channel %d" % self.port)
        self.client_sock, self.client_info = self.server_sock.accept()
        print("Accepted connection from ", self.client_info)



    def send(self, s, eol='\n'):
        s = s.replace(eol, '') # remove existing eol characters because only exactly one must be sent
        self.client_sock.send("{}{}".format(s, eol))

            
    def receive(self):
        return self.client_sock.recv(1024)



    def close(self):
        """Close all connections"""
        bluetooth.stop_advertising()
        self.client_sock.close()
        self.server_sock.close()
        

if __name__ == "__main__":

    import time

    # musikliste is a file where each line is a piece of good music - just take a random file...
    with open('musikliste', 'r') as f:
        musikliste = f.readlines()





    b = BlueberryServer()
    b.connect()




    t = time.clock()

    try:
        while True:
            data = b.receive()
            if len(data) == 0: 
                break
            print time.clock()
            if time.clock() - t > 20: # watchdog
                break
            print("received [%s]" % data)
            print 'sending data...'
            for m in musikliste:
                b.send(m)
            print 'sent'
    except IOError as e:
        print e


    b.close()
    print("exiting")
