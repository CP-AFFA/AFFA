from bcast_socket import *

def main():
 	sock = Socket(5554)
	while(1):
 		sock.send("how")


if __name__ == '__main__':
	main()