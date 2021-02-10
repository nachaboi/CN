import socket
import sys
import select

a = sys.argv

if len(a) != 2:
	print("NO TEXT FILE GIVEN OR TOO MANY PARAMETERS")
	quit()

d = 0.1

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


i = 0

while i <= 6:
	# print(i, d)
	UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	temp = str(arr[i][0]) + " " + str(arr[i][1]) + " " + str(arr[i][2])

	UDPClientSocket.sendto(temp.encode(), serverAddressPort)
	UDPClientSocket.settimeout(d)
	restart = False
	passBy = False
	try:
		data = UDPClientSocket.recvfrom(bufferSize)
	except:
		# print(temp)
		d = 2*d
		if d>2:
			print("ERROR: FAILURE SERVER IN TROUBLE... " + str(arr[i][1]) + " " + str(arr[i][0]) + " " + str(arr[i][2]) + " NOT CALCULATED")
			passBy = True
		else:
			print("ERROR: WAITTIME | REATTEMPTING REQUEST...")
			restart = True
	if restart:
		continue
	if not passBy:
		data = data[0]
		data = data.decode()
		if data[0:3] == "200":
			cur = (data[5:len(data)])
			print("The result of " + str(arr[i][1]) + " " + str(arr[i][0]) + " " + str(arr[i][2]) + " is " + cur)
		else:
			print("ERROR: " + str(arr[i][1]) + " " + str(arr[i][0]) + " " + str(arr[i][2]) + " is an INVALID INPUT")
		UDPClientSocket.close()
	i+=1

