# base.py
# python 3
def isnum(n):
	try:
		int(n)
		return True
	except:
		return False

def uline(s):
	l = ''
	for c in s:
		l += c if c is '_' or c.islower() else '_' + c.lower()
	l = l.replace('__', '_')
	return l

def hump(s):
	l = ''
	s = uline(s)
	for c in s.split('_'):
		l += c.capitalize()
	l = l[0].lower() + l[1:]
	return l

def llist(key_str):
	key_list = []
	for sub_str in key_str.split('\n'):
		if len(sub_str) == 0: continue
		key_list.append([key for key in sub_str.split()])
	return key_list

def flist(filename):
	key_list = []
	for line in open(filename, 'r', encoding='utf-8'):
		if len(line) == 0: continue
		key_list.append([key for key in line.split()])
	return key_list
