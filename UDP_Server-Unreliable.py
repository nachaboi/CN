import socket
import random
import sys

a = sys.argv

if len(a) != 2:
	print("NO PROBABILITY GIVEN OR TOO MANY ARGUMENTS")
	quit()

p = a[1]

try:
	p = float(a[1])
except:
	print("PROBABILITY MUST BE A POSITIVE DECIMAL NUMBER")
	quit()
if p < 0 or p > 1:
	print("PROBABILITY MUST BE A POSITIVE DECIMAL NUMBER")
	quit()

localIP     = "127.0.0.1"
localPort   = 65432
bufferSize  = 1024

OC = ['+','-','*','/']

def RepresentsInt(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.bind((localIP, localPort))
print("SERVER RUNNING ON " + localIP + ":" + str(localPort))

while(True):
	try:
		bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
		currentPick = random.random()
		if currentPick > p:
			data = bytesAddressPair[0]
			address = bytesAddressPair[1]
			print('Connected by', address)
			
			curReq = data.decode()
			curReq = curReq.split()
			if curReq[0] not in OC:
				UDPServerSocket.sendto(b"300", address)
				print("SENT SC 300")
			elif not RepresentsInt(curReq[1]):
				UDPServerSocket.sendto(b"300", address)
				print("SENT SC 300")
			elif not RepresentsInt(curReq[2]):
				UDPServerSocket.sendto(b"300", address)
				print("SENT SC 300")
			elif curReq[0] == '/' and int(curReq[2]) == 0:
				UDPServerSocket.sendto(b"300", address)
				print("SENT SC 300")
			else:
				finalToSend = None
				if curReq[0] == '+':
					toSend = int(curReq[1]) + int(curReq[2])
					finalToSend = toSend
				elif curReq[0] == '-':
					toSend = int(curReq[1]) - int(curReq[2])
					finalToSend = toSend
				elif curReq[0] == '*':
					toSend = int(curReq[1]) * int(curReq[2])
					finalToSend = toSend
				elif curReq[0] == '/':
					toSend = int(curReq[1]) / int(curReq[2])
					finalToSend = toSend
				finalToSend = str(finalToSend)
				theTuple = "200" + ", " + finalToSend
				UDPServerSocket.sendto(str(theTuple).encode(), address)
				print("SENT SC 200")
		else:
			print('Packet Dropped from ' + str(bytesAddressPair[1]))

	except (KeyboardInterrupt, SystemExit):
			UDPServerSocket.close()

