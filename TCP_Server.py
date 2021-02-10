import socket

HOST = '127.0.0.1'  
PORT = 65432        

OC = ['+','-','*','/']

def RepresentsInt(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	correctResponse = True
	print("SERVER RUNNING ON " + HOST + ":" + str(PORT))
	while correctResponse:
		try:
			s.listen()
			conn, addr = s.accept()
			with conn:
				print('Connected by', addr)
				err = False
				while True:
					data = conn.recv(1024)
					if not data:
						break
					curReq = data.decode()
					curReq = curReq.split()
					if curReq[0] not in OC:
						conn.sendall(b"300")
						print("SENT SC 300")
					elif not RepresentsInt(curReq[1]):
						conn.sendall(b"300")
						print("SENT SC 300")
					elif not RepresentsInt(curReq[2]):
						conn.sendall(b"300")
						print("SENT SC 300")
					elif curReq[0] == '/' and int(curReq[2]) == 0:
						conn.sendall(b"300")
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
						conn.sendall(str(theTuple).encode())
						print("SENT SC 200")
						# correctResponse = False
		except (KeyboardInterrupt, SystemExit):
			s.close()
