#! /usr/bin/python
# python 2
# sendxml.py
import socket
import sys
import os

class msg_sender():
	host = '127.0.0.1'
	port = 12302

	def __init__(self):
		if len(sys.argv) < 2:
			print 'Usage: tsend msg[file] [ip][port]'
			return None
		elif len(sys.argv) == 3:
			self.port = int(sys.argv[2])
		elif len(sys.argv) == 4:
			self.host = sys.argv[2]
			self.port = int(sys.argv[3])

		print 'Remote:', self.host, self.port
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.host, self.port))

		if os.path.exists(sys.argv[1]):
			file_size = os.stat(sys.argv[1]).st_size
			fd = open(sys.argv[1], 'r')
			buf = fd.read()
			buf = str(file_size).zfill(8) + buf
			fd.close()
			print 'File Name', sys.argv[1]
			print 'Data Size', file_size
		else:
			buf = sys.argv[1]		

		print 'Send Date', buf
		s.send(buf)
		print 'Send Total', len(buf)

		print 'Receiving ...'

		msg = s.recv(2*1024)
		print 'Received Date:', msg
		print 'Received Total:', len(msg)
		if len(msg) > 0:
			print 'Data Size:', int(msg[0:8])
		else:
			print 'Data Size:', 0
			
		s.close()

if __name__ == '__main__':
	try:
		msg_sender()
	except:
		print 'error'
