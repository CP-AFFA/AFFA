# Standard Python imports
import netifaces
import socket
import struct

# Description: This class will give all the functionality to broadcast messages
# and receive messages. One of the things to consider here will be how to pack
# the data into binary format. There may be advantages to creating a custom packing method.
class Socket():
	
    def __init__(self, port=None, my_id=None, my_ip=None, bcast_ip=0xff, device='wlan0'):
		# Instance variables
        self._port = port			#UDP port for send/recv
        self._id   = my_id			# Local entity ID (0..255 currently)
        self._ip   = my_ip          # local entity ip address
        self._bcast= bcast_ip		# Broadcast IP address
        self._sock = None			# UDP socket
       
        # If user did not specify both addresses,
        # Attempt to look up network device addressing information
        if not my_ip or not bcast_ip:
            try:
                self._ip = netifaces.ifaddresses(device)[2][0]['addr']
                print self._ip
                self._bcast = netifaces.ifaddresses(device)[2][0]['broadcast']
            except Exception:
                raise Exception("Couldn't establish IP addressing information")

        # Build the socket
        try:
            # Setup a scket that uses UDP protocal
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Setup socket to broadcast
            # May want to change this to multicast eventually
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            # Bind to socket
            # TODO figure out what this actually means
            self._sock.bind((self._ip, self._port))
        except Exception:
            raise Exception("Couldn't establish network socket")


    def send(self, data):
        try:
            # Send it, return number of bytes sent (per sendto())
            return self._sock.sendto(data, (self._bcast, self._port))

        # Print any exception for user's awareness
        except Exception as ex:
            print ex.args[0]
            return False

    # Return values:
    #  - <Object> - valid received message object
    #  - False - A message arrived, but one to be ignored
    #  - None - No valid message arrived
    def recv(self, buffsize=1024):
        try:
            data, (ip, port) = self._sock.recvfrom(buffsize, socket.MSG_DONTWAIT)
            print(data)
            # Mostly likely due to no packets being available
            if not data:
                return None
        except Exception as ex:
            # Mostly likely due to no packets being available
            return None
      