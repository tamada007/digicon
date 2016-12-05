#encoding:utf-8

import os,sys
import getopt

#默认为gbk,在encode.txt可设置编码
current_encoding = 'gbk'
if os.path.isfile('encode.txt'):
	with open('encode.txt') as fp:
		current_encoding = fp.readline()
		

VERSION="3.1"

sys.getdefaultencoding()
reload(sys)
#sys.setdefaultencoding("utf-8")
sys.setdefaultencoding(current_encoding)  # @UndefinedVariable

#import common.common
from common import common
# from common.converter import ScaleConverter
from common.converter import ScalesConverter
from common import converter

import libsm120.easy
import libsm110.easy
#from libsm120.const import report_list
import libsm120.const
import libsm110.const
#import argparse

#from smftp import smftp
#import master,entity


def print_usage():
	print """%s [Options]
Options:
    -h                       This Help
    -d                       Delete Master On Scale (Plu,Mgp...)
    -P                       Import Plu generally (Both sm110 and sm120)
    -T                       Import Trace generally (Both sm110 and sm120)
    -L                       Import Flexibarcode generally (Both sm110 and sm120)
    -H                       Title Line In CSV
    -c Json File             Send Commodity information by Json
    -t Json File             Send Traceability information by Json
    -f Json File             Send Label Format information by Json
    -G Json File             Receive Label Format information by Json
    -F Json File             Csv Filter File
    -m Json File             Import/Export Template Json File
    -R Report File Name      Export Pre-defined Report file
    -s Scale List            Scale List Separated by "," for example "192.168.1.2, 192.168.1.3"
    -S Scale File            File where scale list is
    -g Scale Group List      Scale Group list File
    -i Csv File              Import Csv File
    -o Csv File              Export Csv File
""" % sys.argv[0]

if __name__ == '__main__':

	exitCode = 0

	json_plu_file = ""
	json_label_file = ""
	json_trace_file = ""
	out_csv_file = ""
	in_csv_file = ""
	template_file = ""
	delete_file = ""
	report_file = ""
	group_file = ""
	filter_file = ""
	scale_list = []
	scale_file = ""
	
	dat_file = ""

	get_label = False

	general_plu = False
	general_trace = False
	general_flb = False
	general_kas = False
	titling = False

	#init log module
	common.log_init()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "HvPTKLhd:F:g:G:c:t:s:S:m:f:t:R:i:o:", ["dat=","help"])

		if not opts:
			print_usage()
			sys.exit(0)

		for o, v in opts:
			if o in ("-h", "--help"):
				print_usage()
			elif o == "--dat":
				dat_file = v
			elif o in ("-c"):
				json_plu_file = v
			elif o in ("-t"):
				json_trace_file = v
			elif o in ("-f"):
				json_label_file = v
			elif o in ("-s"):
				scale_list = v.split(",")
			elif o =="-S":
				scale_file = v
			elif o == "-o":
				out_csv_file = v
			elif o == "-F":
				filter_file = v
			elif o == "-i":
				in_csv_file = v
			elif o == "-d":
				delete_file = v
			elif o == "-m":
				template_file = v
			elif o == "-R":
				report_file = v
			elif o == "-g":
				group_file = v
			elif o == "-H":
				titling = True
			elif o == "-P":
				general_plu = True
			elif o == '-K':
				general_kas = True
			elif o == "-L":
				general_flb = True
			elif o == "-T":
				general_trace = True
			elif o == "-G":
				json_label_file = v
				get_label = True
			elif o == '-v':
				print "version: " + VERSION
				sys.exit(0)
			else:
				sys.exit(1)

	except getopt.GetoptError as err:
		common.log_err( "Parameters Error:", err )

	file_list = []

	common.set_title_onoff(titling)

	#Checking Confliction
	conflict_check_list = []

	#Template File conflict with Report File
	if template_file:
		conflict_check_list.append(template_file)
	if report_file:
		conflict_check_list.append(report_file)
	if len(conflict_check_list) == 2:
		common.log_err( "Template File and Report File conflict!!!" )
		sys.exit(6)

	if report_file and not out_csv_file:
		common.log_err( "No enough Parameters For exporting Files" )
		sys.exit(4)

	if template_file and not in_csv_file and not out_csv_file:
		common.log_err( "No enough Parameters For exporting Files" )
		sys.exit(4)
		
	if scale_list and scale_file:
		common.log_err( "Cannot process both scale list and scale file" )
		sys.exit(4)


	if in_csv_file and out_csv_file:
		common.log_err( "-i and -o cannot be Process Together!!!" )
		sys.exit(4)

	if os.path.exists(json_plu_file):
		file_list.append(json_plu_file)

	if os.path.exists(json_trace_file):
		file_list.append(json_trace_file)

	if get_label or os.path.exists(json_label_file):
		file_list.append(json_label_file)

#	if report_file and report_file not in libsm120.const.report_list.keys():
#		common.log_err( "Report File not Exist!!!" )
#		sys.exit(5)

	if len(conflict_check_list) == 0 and not file_list and not delete_file and not dat_file:
		common.log_err( "No enough Parameters" )
		sys.exit(2)

	if not scale_list and not scale_file and not dat_file:
		common.log_err( "Scale List is EMPTY!" )
		sys.exit(3)


	if scale_file:
		with open(scale_file) as fp:
			scale_list = [line for line in fp.readlines() if line and line.strip()]
# 			for line in fp.readlines():
# 				if line and line.strip(): scale_list.append(line)

	if out_csv_file and os.path.isfile(out_csv_file):
		os.remove(out_csv_file)


	if template_file and in_csv_file:
		if general_plu or general_trace or general_flb or general_kas:
			if general_plu:
				scales_converter = ScalesConverter()
			elif general_trace:
				scales_converter = ScalesConverter(converter.TRACE_converter)
			elif general_flb:
				scales_converter = ScalesConverter(converter.FLEXIBARCODE_converter)
			elif general_kas:
				scales_converter = ScalesConverter(converter.PRESETKEY_converter)
			
			if not scales_converter.easyImportMaster(scale_list, in_csv_file, template_file):
				exitCode = 8


	#处理直接下发的DAT文件(只支持SM110)
	if dat_file:
		try:
			import re
			#匹配192.168.68.125.25.DAT这样的格式
			pat = re.compile("(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})\.(\d+)\.dat")
			m = pat.match(dat_file.lower())
			if m:
				scale_ip = m.group(1)
				file_no = int(m.group(2),16)
				sm110_scale = libsm110.smtws.smtws(scale_ip)
				if not sm110_scale.upload_file(file_no, dat_file):
					raise Exception('Error On Sending Data File')
			else:
				raise Exception("Incorrect File Name")
		except Exception, e:
			common.log_err( e )
			exitCode = 8
			#print dir(e)
		else:
			common.log_info( "Finished Sending Dat File To Scale!" )
			
	

	for index, scale in enumerate(scale_list):
		scale = scale.strip()
		if not scale:
			common.log_err( "scale %d empty" % index )
			continue

		scale_info = scale.split(':')
		scale = scale_info[0]
		if len(scale_info) > 1:
			scale_type = scale_info[1]
		else:
			scale_type = "sm120"

		#import common.common

		if scale_type.lower() == "sm120":
			#sm120
			ease = libsm120.easy.Easy(scale)
			common.clear_all_tables(libsm120.const.db_name)
			
		else:
			#sm110
			ease = libsm110.easy.Easy(scale)
			common.clear_all_tables(libsm110.const.db_name)


		if delete_file:
			if ease.easyDeleteFile(delete_file):
				common.log_info( "Delete Master %s Successfully!" % delete_file )
			else:
				common.log_err( "Delete Master Failed!" )

		if json_plu_file:
			ease.easySendPlu(json_plu_file)
		if json_trace_file:
			ease.easySendTrace(json_trace_file)
		if json_label_file:
			try:
				if get_label:
					ease.easyRecvPrintFormat(json_label_file)
				else:
					ease.easySendPrintFormat(json_label_file)
			except Exception, e:
				common.log_err( "Label Format Error:", e )

		#common.clear_all_tables(libsm120.const.db_name)
		if template_file:
			if out_csv_file:
				ease.exportCSV(
					export_template_file = template_file, 
					export_template_info = "",
					export_csv_file = out_csv_file,
					title = True)
			elif in_csv_file:
				#import
				if general_plu or general_trace or general_flb or general_kas:
					#scale_converter.easyImportMaster(in_csv_file, template_file)
					pass
				else:
					ease.easyImportMaster(
						in_csv_file, 
						template_file, 
						json_scale_group_file = group_file,
						json_filter_file = filter_file)
		if report_file:
			if scale_type.lower() == "sm120":
				ease.exportCSV(
					export_template_file = "",
					export_template_info = libsm120.const.report_list[report_file],
					export_csv_file = out_csv_file,
					title = True)
			else:
				ease.exportCSV(
					export_template_file = "",
					export_template_info = libsm110.const.report_list[report_file],
					export_csv_file = out_csv_file,
					title = True)

	sys.exit(exitCode)

#	m = KageTest()
#	m.test()

	#m = master.MgpMaster('mgp.json')
	#m = entity.MgpMaster()

	#csvreader.SmCsvReader().read('m.csv', lambda x : m.add_rows(x))
	#m.from_csv('m.csv')
	#m.to_json("m.json")

	#m.to_csv('koko.csv', True)

	'''
	with open('m.csv', 'r') as fp:
		cr = csv.reader(fp)
		header = cr.next()
		#print header
		rows_list = []
		for cur_row in cr:
			row_dic = []
			#print cur_row
			for i,col in enumerate(header):
				#print '%d, %s' % (i, col)
				row_dic.append( { col: cur_row[i] } )
			#m.add_row(cur_row)
			#print rows
			#m.add_row(row_dic);
			rows_list.append(row_dic);
		m.add_rows(rows_list)

	'''

	#scale = digiscale.DigiSm120('S0501')
	#scale.send(m)
	#m.to_csv('aa.csv')
	

	#rootdir_local   = '.'                       # local folder
	#rootdir_remote  = '.'                       # remote folder
	#ftp = smftp('192.168.100.22', 'anonymous', '')
	#ftp = smftp('S0501', 'admin', 'admin')
	#ftp.login()
	#ftp.download_file(rootdir_local + '/' + 'plu0uall.csv', 'plu0uall.csv')
	#time.sleep(5);
	#conn = open_sqlite_db('kage.sqlite')

	#cursor = conn.cursor()
	#cursor.execute('CREATE TABLE IF NOT EXISTS t1(f1 int primary key, f2 text)')
	#cursor.execute('REPLACE INTO t1 VALUES (1, "abc")');
	#cursor.execute('REPLACE INTO t1 VALUES (2, "def")');
	#conn.commit()

	#cursor.execute('select * from t1');
	#for row in cursor:
		#print row['f2']

#	with open('mgp.json', 'r') as f:
#		data = json.load(f)
#		for k, v in data.items():
#			print 'k:%s v:%s' % (k, v)
