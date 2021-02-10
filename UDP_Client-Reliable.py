import socket
import sys

a = sys.argv

if len(a) != 2:
	print("NO TEXT FILE GIVEN OR TOO MANY ARGUMENTS")
	quit()

f = None

try:
	f = open(a[1], "r")
except:
	print("INVALID TEXT FILE")
	quit()
data = f.read()
data = data.splitlines()
arr = []
end = len(data)
if len(data) > 7:
	end = 7
for i in range(0,end):
	arr.append(data[i].split())

serverAddressPort   = ("127.0.0.1", 65432)
bufferSize          = 1024

if len(arr) < 7:
	print("INVALID TEXT FILE: AT LEAST 7 LINES NEEDED")
	quit()
for i in arr:
	if len(i) != 3:
		print("INVALID TEXT FILE: A LINE DOES NOT CONTAIN EXACTLY 3 VALUES")
		quit()


for i in arr:

	UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

	temp = str(i[0]) + " " + str(i[1]) + " " + str(i[2])

	UDPClientSocket.sendto(temp.encode(), serverAddressPort)
	data = UDPClientSocket.recvfrom(bufferSize)
	data = data[0]
	data = data.decode()
	if data[0:3] == "200":
		cur = (data[5:len(data)])
		print("The result of " + str(i[1]) + " " + str(i[0]) + " " + str(i[2]) + " is " + cur)
	else:
		print("ERROR: " + str(i[1]) + " " + str(i[0]) + " " + str(i[2]) + " is an INVALID INPUT")
	UDPClientSocket.close()
