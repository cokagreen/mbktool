#! /usr/bin/python
# python 2
# mtt.py
import os
import sys
import socket

WORKDIR = sys.path[0]
ULIST = os.path.join(WORKDIR, 'ulist')
TLIST = os.path.join(WORKDIR, 'tlist')
MLIST = os.path.join(WORKDIR, 'mlist')

class mbstest():
	def __init__(self, host, port):
		print 'Hi'
		self.open(host, port)
		self.ul = []
		self.tl = []
		self.usr = []
		self.td = {}
		self.conf()

	def __del__(self):
		self.close()
		print 'Bye'

	def __getd(self, filename):
                with open(filename, 'r') as fd:
                        return fd.read()

	def __getl(self, filename):
		llist = []
		dstr = self.__getd(filename)
		for i in dstr.split('\n'):
			if len(i) == 0:
				continue
			llist.append([j for j in i.split()])
		return llist

	def __geti(self, llist, info):
		for i in llist:
			if info in i:
				return i

	def open(self, host, port):
		print 'Remote:', host, port
		self.cfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print 'Connecting'
		self.cfd.connect((host, port))

	def send(self, data):
		print 'Send Date:', data
		self.cfd.send(data)
		print 'Send Total:', len(data)

	def recv(self, size=2*1024):
		print 'Receiving ...'
		msg = self.cfd.recv(size)
		print 'Received Date:', msg[:1024]
		print 'Received Total:', len(msg)
		return msg

	def close(self):
		print 'Disconnecting'
		self.cfd.close()

	def conf(self):
		self.ul = self.__getl(ULIST)
		self.tl = self.__getl(TLIST)
	
	def getu(self, uinfo):
		self.usr = self.__geti(self.ul, uinfo)

	def gett(self, tinfo):
		tlist = self.__geti(self.tl, tinfo)
		tmod = self.__geti(self.tl, 'TXCODE')
		for i in range(len(tlist)):
			self.td[tmod[i]] = tlist[i]

	def getm(self, code, info):
		self.getu(info)
		self.gett(code)
		txdef = []
		if 'TXDEF' not in self.td:
			txdef = []
		else:
			txdef = [self.usr[int(i)] for i in self.td['TXDEF']]
		model = self.__getd(os.path.join(MLIST, self.td['TXCODE'] + '.xml'))
		xml = model % tuple(txdef)
		return str(len(xml)).zfill(8) + xml

	def log(self, filename, date):
		with open(filename, 'a') as fd:
			fd.write(date)

	def test(self, code, info):
		sbuf = self.getm(code, info)
		self.send(sbuf)
		rbuf = self.recv(10*1024)
		self.log(os.path.join(WORKDIR, 'mbstest.log'), sbuf)
		self.log(os.path.join(WORKDIR, 'mbstest.log'), rbuf)
	def showuser(self, start=0, end=20):
		for i in range(len(self.ul)):
			if i >= start and i < end:
				print(i)
			else:
				break

if __name__ == '__main__':
	print 'Workdir:', WORKDIR
	args = sys.argv
	if len(args) == 4:
		host = '127.0.0.1'
		port = int(args[1])
		test = mbstest(host, port)
		test.test(args[2], args[3])
        else:
                print 'Usage: %s port [txcode usrinfo]' % (args[0])
