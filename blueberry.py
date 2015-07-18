#!/usr/bin/env python
# -*- coding: utf-8 -*-


# class for handling a bluetooth connection with the phones

# command list
# 1: send song database to phone
#    including artist names and albums with songs

# 2: send current playlist to phone

# 3: append song to playlist
# 4: append album to playlist
# 5: append all albums from artist to playlist
# 6: play song, new playlist
# 7: play album, new playlist
# 8: play all albums from artist, new playlist
# 9: prepend song to playlist
# 10: prepend album to playlist
# 11: prepend all albums from artist to playlist


# command format: cmd,num-id,payload\n
# num-id is a (random?) identifier, used for response 


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
        """Send string s, multiple eol characters are removed from s."""
        s = s.replace(eol, '') # remove existing eol characters because only exactly one must be sent
        self.client_sock.send("{}{}".format(s, eol))

            
    def receive(self, b=1024):
        """Receive b bytes"""
        return self.client_sock.recv(b)



    def close(self):
        """Close all connections"""
        bluetooth.stop_advertising(self.server_sock)
        self.client_sock.close()
        self.server_sock.close()
        

if __name__ == "__main__":

    import time


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
            for m in range(500):
                b.send(str(m))
            b.send('stop')
            print 'sent'
    except IOError as e:
        print e


    b.close()
    print("exiting")
