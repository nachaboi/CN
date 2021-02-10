import socket
import sys

a = sys.argv

if len(a) != 2:
	print("NO TEXT FILE GIVEN OR TOO MANY ARGUMENTS")
	quit()

HOST = '127.0.0.1'
PORT = 65432

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

if len(arr) < 7:
	print("INVALID TEXT FILE: AT LEAST 7 LINES NEEDED")
	quit()
for i in arr:
	if len(i) != 3:
		print("INVALID TEXT FILE: A LINE DOES NOT CONTAIN EXACTLY 3 VALUES")
		quit()

for i in arr:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		temp = str(i[0]) + " " + str(i[1]) + " " + str(i[2])
		s.sendall(temp.encode())
		data = s.recv(1024)
		data = repr(data)
		if data[2:5] == "200":
			cur = (data[7:len(data)-1])
			print("The result of " + str(i[1]) + " " + str(i[0]) + " " + str(i[2]) + " is " + cur)
		else:
			print("ERROR: " + str(i[1]) + " " + str(i[0]) + " " + str(i[2]) + " is an INVALID INPUT")
		s.close()