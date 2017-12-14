# opentrans.py
# python3
# transopen.py
import os

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

def get_open_card_list(filename):
	ul = []
	workbook = None
	try:
		import xlrd
		workbook = xlrd.open_workbook(filename)
	except Exception as e:
		print('open file error')
		print(e)
		exit(0)
	sheets = workbook.sheets()
	sheet0 = sheets[0]
	rows = sheet0.nrows
	cols = sheet0.ncols
	for i in range(1,rows):
		ul.append([sheet0.cell(i, j).value for j in range(cols) if 1 < j < 5])
	return ul


def get_reg_mbk_sql(ul):
	sql = 'select user_real_name,main_accno,cif_idno,cif_cellno,reg_sts,sign_type from eci_cif_register where main_accno in ('
	for i in ul:
		sql += "'%s'," % (i[0])
	return sql[:-1]+');'


def mksendfile(opl):
	mod = ''
	with open('xlsx/1001.xml', 'r', encoding='utf-8') as fd:
		mod = fd.read()
	for i in opl:
		msg = mod % (i[0], i[1], i[2], i[3])
		with open('target/'+i[3]+'.xml', 'w', encoding='gbk') as fd:
			fd.write(msg)

def tarsendfile(srcdir, basedir):
	import tarfile
	tar = tarfile.open(os.path.join(basedir, 'sendxml.tar.gz'), 'w:gz')
	for root, _, files in os.walk(srcdir):
		for file in files:
			fullpath = os.path.join(root, file)
			tar.add(fullpath)
			os.remove(fullpath)
	tar.close()

def putsendxml(fielname):
	from ftplib import FTP
	ftp=None
	try:
		ftp = FTP(host='127.0.0.1', user='eci', passwd='eci')
		ftp.cwd('/home/eci/')
	except Exception as e:
		print(e)
		exit(0)
	print('[FTP]  User workdir:', ftp.pwd())
	try:
		with open(fielname, 'rb') as fd:
			print('[FTP] ', ftp.storbinary('STOR sendxml.tar.gz', fd))
	except Exception as e:
		print(e)
	print('[FTP] ', ftp.quit())
	ftp.close()
	os.remove(fielname)

def main(date):
	cardfile='xlsx/%s.xls' % (date)
	regfile ='xlsx/%s' % (date)
	target='./'
	ul = get_open_card_list(cardfile)
	sql = get_reg_mbk_sql(ul)
	if os.path.exists(regfile):
		regl = flist(regfile)
		mksendfile(regl)
		tarsendfile('target', target)
		print('sendxml.tar.gz created successfuly in', target)
		putsendxml(os.path.join(target, 'sendxml.tar.gz'))
		print('sendxml.tar.gz put eci successfuly')
	else:
		print('please select cif reg info from oecis:\n\n\n')
		print(sql)
		print('\n\n\n')

if __name__ == '__main__':
	# xlsx:20171212.xlsx
	# do transopen.py
	# select sql
	# xlsx:20171212
	# redo transopen.py
	# send sendxml.tar.gz

	# main('20171212')
	pass

