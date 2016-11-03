#encoding=utf-8

import os,sys
import json
import sqlite3

#sys.getdefaultencoding()
reload(sys)
#sys.setdefaultencoding("utf-8")
sys.setdefaultencoding("gbk")  # @UndefinedVariable
#import libsm120.csvreader
#test2.test2().gogo(1,2)
#libsm120.csvreader.SmCsvReader().read_line_by_line(
	#"xyyc.csv",
	#None)
	
from common.converter import ScalesConverter

import common.common

import time
count = 700000
while count > 0:
	print ScalesConverter().easyImportMaster("192.168.68.125:sm110", "plu_import.csv", "plu_template.json")
	#print ScalesConverter().easyImportMaster("192.168.175.1:sm110", "plu_import.csv", "plu_template.json")
 	#print ScalesConverter().easyImportMaster("192.168.175.1", "plu_import.csv", "plu_template.json")
	#print ScalesConverter().easyImportMaster("192.168.68.194", "plu_import.csv", "plu_template.json")
	count -= 1
	common.common.close_all_sqlite_db()
	time.sleep(0.01)
	

sys.exit(3)








from common import common

def get_length_of_ascii(cell_data, max_length):
	total_length = 0
	pos = 0
	while pos < min(max_length, len(cell_data)):
		d = common.hex2int(cell_data[pos : pos+2])
		pos += 2
		print "d,pos:", d, pos
		if d == 12:
			break
	return pos

#a = "4150504C45BBBBACDBB9EF"
#b = a.decode('hex').decode('gbk', errors='replace')
#b = a.decode('hex').decode('gbk', 'ignore').encode('gbk')
#print b
#print get_length_of_ascii("0601610D0601620C", 26)
#sys.exit(0)
'''
class GoGo():
	def gogotest(self):
		for i in range(2):
			def gogotest2():
				print i
			gogotest2()

GoGo().gogotest()
sys.exit(0)
'''

'''
import logging
import logging.handlers

logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt='%a, %d %b %Y %H:%M:%S',
		#filename='myapp.log',
		filemode='w')
    
#����һ��StreamHandler����INFO������ߵ���־��Ϣ��ӡ����׼���󣬲�������ӵ���ǰ����־�������#
#console = logging.StreamHandler()
#console.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
#console.setFormatter(formatter)
#logging.getLogger('').addHandler(console)

Rthandler = logging.handlers.RotatingFileHandler('myapp.log', maxBytes=10*1024*1024,backupCount=5)
Rthandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)


logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')


from nosqlite.nosqlite import client, server
s = server(directory='c:/tmp/a')
c = client(s.port)
database = c.db
collection = database.foo; collection
collection.insert({'a':123, 'b':'hello'})
list(collection)
collection.insert([{'a':i} for i in range(5)])
len(collection)
collection.find_one(a=4)
collection.find_one(a=123)
list(collection.find('a<3'))
collection.insert({'a':-1, 'foo':[1,(2,3),set([3,4])]})
collection.find_one(a=-1)

def ktest():
	yield 1
	yield 'a'
	yield 'ccc'

k = ktest()
v = k.next()
while v:
	print v
	try:
		v = k.next()
	except StopIteration, e:
		break

'''

#sys.exit(0)

'''
def open_sqlite_db(fileName):
	conn = sqlite3.connect(fileName)
	conn.row_factory = sqlite3.Row
	return conn


#print "c p 3:", "bfbcb7f2".decode("hex").decode("gbk").encode("hex")
#print "c p 4:", [byte for byte in "\xd6\xd0\xb9\xfa".decode("gbk")]
#print "c p 5:", "\xd6\xd0\xb9\xfa".encode("utf-8").encode("hex")
conn = open_sqlite_db("aa.sqlite")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS t1(f1 text)")
text = "bfbcb7f2".decode("hex").decode(sys.getdefaultencoding()) + ",aaa"
#text = '23, \xe8\x80\x83\xe5\xa4\xab'.encode("utf-8")
#text = "23, \xbf\xbc\xb7\xf2".decode("gbk")
text = "23, abc".decode("gbk")
text = unicode(text)
cursor.execute("INSERT INTO t1 VALUES(?)", [text])
conn.commit()
sys.exit(0)
'''
#text = "bfbcb7f2".decode("hex").decode(sys.getdefaultencoding())
#print unicode(text).encode("hex")

'''
kstr = "140D323334343434343434343434350D14036162630C"
while kstr:
	print "kstr:" , kstr
	font_size = kstr[:2]
	length = int(kstr[2:4], 16)
	text = kstr[4:4+length * 2]
	print text, length
	kstr = kstr[4+length * 2+2:] 
'''

#import libsm110.entity
#tbtmt = libsm110.entity.TbtMaster()

#tbtmt.find_records("SELECT * FROM tbt 


#sys.exit(0)

class tes1():
	def tes1(self, *b):
		print "tes1"

class tes2(tes1):
	def tes1(self, *b):
		print "tes2"
#		print b
		
#tes2().tes1(9,8,7)
dic1={
	"f1": lambda: tes2(),
	"f2": lambda: tes1()
}

def va1(**args):
	print args["name"]

#va1(name='kage', age=31)
#sys.exit(0)


#dic1["f2"]().tes1()
#sys.exit(0)

class base():
	def test(self):
		print "base.test"
	def test2(self):
		print "base.test2"

class derive(base):
	def test2(self):
		print "derive.test2"
	def test3(self):
		print "test3"
		
#derive().test2()
		
#sys.exit(0)



def printf(x): print x

def test(cb):
	if cb is not None: cb(1)

import re
#p = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
p = re.compile(r"(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})")
m = p.match("127.0.1.3")

#if m:
	#print m.groups()
	#print len(m.groups())
	#print m.group(3)
	#for i in m.groups():
		#print i

#test(lambda x : printf(x))


t = type(0.2)
#print t()


aaa = {
	"k1" : 2,
	"k2" : 4
}

#print aaa.get('k3', -1)

bbb = {
1: 'abc',
'2': 'def',
3: "ghi",
'4':"aaa",
'5':"bbb"
}

#iii = {"1":1, "2": 2}
#print [ "ok" for k,v in iii.items()]

#a = u"中国"
#b = "aaa"

#with open("kkk.txt", "wb") as fp:
	#fp.write(a.encode("utf-8"))

#c = a.encode("cp936")
#print [a, c]
#print c.decode("cp936")
#print [a, c]
#print a.decode("CP936")

#with open('tt.txt', 'r') as fp: b = fp.read()


#print reduce(lambda x,y: x and y, [1, 1, 1])

#with open("S0501_ing0uall.csv", "r") as fp:
	#print fp.read()


import csv
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        #yield line.encode('utf-8')
        yield line.decode('gbk')


def test2():
	return 1,2,5


x,y,z = test2()

#obj = {"name": "kage"}
#print x,y,z
#conn = open_sqlite_db("kage2.sqlite")
#cursor = conn.cursor()
#cursor.execute("CREATE TABLE IF NOT EXISTS ko (t text)")
#cursor.execute("INSERT INTO ko VALUES( %s )" % obj)
#conn.commit()
#sys.exit(0)
#cursor.execute("SELECT * FROM spm");
#for row in cursor:
#	print row["Data"], row[4]

#print dict( (str(v), v) for v in range(1,100) )

a = {"name": "kage"}
b = {"age": 35}

c = a.copy()
c.update(b)

#print c



a = "中国"
b =  unicode(a, "utf-8")

#print type(b) in (str, unicode)

#print type(b)
c = b.encode("gbk")
#print c

#print type(a) == unicode


#print map(lambda x: x * 2, [1,2,4])

#print reduce(lambda x,y : x* 100 + y,  [11, 30, 20])

#a = b"\xf1\x32\x33"

class ReqData:
	Read_File    = 1
	Read_Record  = 2
	Write_File   = 3
	Del_Record   = 4
	Del_File     = 5
	def create_request_data(self, method, file_no, record_no):
		return {
			ReqData.Read_File:     "F7%02x%08d" % (file_no, record_no),
			ReqData.Write_File:    "F1%02x" % file_no,
			ReqData.Read_Record:   "F0%02x%08d" % (file_no, record_no),
			ReqData.Del_File:      "F2%02x" % file_no,
			ReqData.Del_Record:    "F3%02x%08d" % (file_no, record_no),
		}.get(method, "")

#print "%02x" % 10
#sys.exit(0)

#import socket
#try:
	#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#socket.setdefaulttimeout(3)
	##sock.settimeout(2)
	#sock.connect(("192.168.175.1", 2003))
	#print sock.recv(1)
#except socket.error, e:
	#print e

def trunc(num, digits):
   sp = str(num).split('.')
   return '.'.join([sp[0], sp[:digits]])
#print trunc("3.2", 1)
#import libsm110.master
#import libsm110.const




#class base():
#	def __init__(self, info):
#		self.info = info
#class derive(base):
#	def __init__(self, info, data):
#		base.__init__(self, info)
#		#print self.info

#derive({"name":"kage"}, 15)

#print "31616263D6D0B9FA".decode("HEX")
#print "d6d0b9fa".decode('hex').decode( sys.getdefaultencoding() )

'''
with open("xyyc.csv", "r") as fp:
	cr = csv.reader(fp)
	line = cr.next()
	print sys.getdefaultencoding()
	for row in cr:
		for cell in row:
			print cell.decode(sys.getdefaultencoding())
'''


#libsm110.master.Master("mgp", libsm110.const.mgp_struct)
from common import common
from libsm110.smtws import smtws
import libsm110.entity

#import traceback
common.log_init()

sm110 = smtws("192.168.68.137")
prfmt = libsm110.entity.PrfMaster()
sm110.download_master(prfmt)


if len(sys.argv) >= 2:
	fileName = sys.argv[1]
	path, fileOnly = os.path.split(fileName)

	tmpData = fileOnly.split('.')
	if len(tmpData) == 6:
		ip		= ".".join(tmpData[:4])
		iFileNo = int(tmpData[4],16)
		
		sm110 = smtws(ip)
		
		sm110.upload_file(iFileNo, fileName)
		


#ip = "192.168.1.205"
# ip = "192.168.50.205"

#sm110.upload_file(0x23, "S0205.23.dat")
#sm110.upload_file(0x25, "S0205.25.dat")
#print sm110.download_file(0x23)
#sm110.delete_file(0x25)
# mgpmt = libsm110.entity.MgpMaster()
# plumt = libsm110.entity.PluMaster()
# prfmt = libsm110.entity.PrfMaster()

#sm110.delete_file(0x4d)

# kasmt = libsm110.entity.KasMaster()
# sm110.download_master(kasmt)


# sm110.upload_file(0x25, r"D:\develop\XiaoSHL\working\DIGI2005\trunk\Bin\192.168.50.205.25.DAT")



sys.exit(0)

import libsm110.easy


# from common.converter import ScaleConverter
# from common.converter import TRACE_converter 
# from common.converter import FLEXIBARCODE_converter 

# ScaleConverter("sm110", "192.168.1.205"  ).easyImportMaster("plu_import.csv", "comm_plu.json")
#ScaleDispatcher("sm110", "192.168.1.205", dispatcher=trace_dispatcher).easyImportMaster("plu_import.csv", "comm_trace.json")
#ScaleDispatcher("sm120", "192.168.68.200" ).easyImportMaster("plu_import.csv", "comm_plu.json")
#ScaleDispatcher("sm120", "192.168.68.200", dispatcher=trace_dispatcher).easyImportMaster("plu_import.csv", "comm_trace.json")
# ScaleConverter("sm110", "192.168.1.205", dispatcher = FLEXIBARCODE_converter ).easyImportMaster("plu_import.csv", "comm_flb.json")
#ScaleDispatcher("sm120", "192.168.68.200", dispatcher = flexibarcode_dispatcher ).easyImportMaster("plu_import.csv", "comm_flb.json")


'''
libsm110.easy.Easy(ip).easyImportMaster(
	"plu_import.csv",
	"sm110.it"
)

libsm110.easy.Easy(ip).easyImportMaster(
	"trace.csv",
	"tr.it"
)
'''

#libsm110.easy.Easy(ip).easySendPlu("easyplu.json")
#libsm110.easy.Easy(ip).easySendTrace("easytrace.json")
#libsm110.easy.Easy(ip).easyRecvPrintFormat("ooo.json")
#libsm110.easy.Easy(ip).easySendPrintFormat("ooo.json")


#sm110.download_file(0x51)
#sm110.download_file(0x52)
#sm110.download_master(plumt)
#plumt.add_rows("192.168.68.205.25.dat")
#plumt.add_rows("25.dat")
#sm110.upload_master(plumt)
#plumt.to_datfile("out.dat")
#sm110.delete_master(plumt)

#sm110.download_master(prfmt)
#sm110.upload_master(prfmt)

#print plumt.get_all_data()
#mgpmt.add_rows("192.168.68.205.23.dat")
#mgpmt.add_rows("mgp.dat")
#mgpmt.to_dat("22.dat")
#sm110.upload_master(mgpmt)

sys.exit(0)


'''
import time
socket.setdefaulttimeout(3)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_read = ""
record_no = 0
#a = ReqData().create_request_data(ReqData.Read_File, 0x25, record_no).decode("hex")
#a = ReqData().create_request_data(ReqData.Write_File, 0x25, record_no)
sock.connect(("192.168.68.205", 2205))

a = ReqData().create_request_data(ReqData.Del_Record, 0x25, 1).decode("hex")

sock.send(a)
data_received = sock.recv(1)
if data_received:
	print ord(data_received[0])

a = ReqData().create_request_data(ReqData.Del_File, 0x25, record_no).decode("hex")
sock.send(a)
data_received = sock.recv(1)
if data_received:
	print ord(data_received[0])
'''


'''
a = ReqData().create_request_data(ReqData.Read_Record, 0x2E, 1).decode("hex")
sock.send(a)
data_received = sock.recv(1460)
data_received = data_received.encode("hex").upper()
print data_received
'''

#with open("ooo", "r") as fp:
#	for line in fp:
#		line = line.rstrip()

'''
with open("ooo", "r") as fp:
	for line in fp:
		line = line.rstrip()
		data_send = a + line
		data_send = data_send.decode("hex")
		sock.send(data_send)
		ack = sock.recv(1)
		if not ack:
			print "no ack"
			break
		i_ack = ord(ack[0])
		if i_ack == 0xE1:
			print "E1"
			break #Write Error
		if i_ack == 0xE0: 
			print "E0"
			break #No Data
		if i_ack == 0xE3:
			print "E3"
			break #No Free Space
		if i_ack == 0x06:
			print "06"
			continue
		else:
			print "other:%d" % i_ack
			break
'''

'''
with open("ooo", "w") as fp:
	while True:
		sock.send(a)
		data_read = sock.recv(1460)
		if len(data_read) == 1:
			if data_read[0] == 0xE0: break #Read Error
			if data_read[0] == 0xE2: break #No Data
		data_read = data_read.encode("hex").upper()
		record_no = int(data_read[:8])
		fp.write(data_read + "\r\n")
		a = ReqData().create_request_data(ReqData.Read_File, 0x25, record_no).decode("hex")
'''

#sock.close()

'''
with open("ooo", "r") as fp:
	uu = fp.read()
	print uu.encode("hex").upper()
'''



#u = u'中国'
#r = u.encode("gbk").encode("hex")
#print r.upper()



#a = [0xd6,0xd0]
#a = "d6d0"
#import codecs
#with open("kkk.dat", "wb") as fp:
#with codecs.open("kkk.txt", "wb", "gbk") as fp:
	#d = a.decode("hex")
	#pass
	#print [e for e in d]
	#fp.write(d)


	#kkk = a.decode("hex")
	#pass
	#fp.write(a)

sys.exit(-1)

#print dict(a.items()+ b.items())

#print type(a) is dict

#for k,v in bbb.iteritems():
	#print k, v

#filtered_dict = {k:v for k,v in bbb.items() if type(k) == int}
#l = list(filtered_dict.iteritems())
#print l[0][1]
