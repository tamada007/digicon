# encoding:utf-8

import os
import sys
import getopt
import datetime
import re
from threading import Thread

VERSION = "5.5.10.1"

LOGFILE_ERROR = "digicon_failed_scale.log"
LOGFILE_SUCCEED = "digicon_succeeded_scale.log"

# 默认为gbk,在encode.txt可设置编码
current_encoding = 'gbk'
if os.path.isfile('encode.txt'):
    with open('encode.txt') as fp:
        current_encoding = fp.readline().strip()

# print("encoding: " + current_encoding)

sys.getdefaultencoding()
reload(sys)
# sys.setdefaultencoding("utf-8")
sys.setdefaultencoding(current_encoding)  # @UndefinedVariable

from common import common
from common.converter import ScalesConverter
from common import converter
from common import globalspec

import libsm120.easy
import libsm110.easy
# from libsm120.const import report_list
import libsm120.const
import libsm110.const


# import argparse
# from smftp import smftp
# import master,entity


def print_usage():
    print """%s [Options]
Options:
    -h                       This Help
    -d                       Delete Master On Scale (Plu,Mgp...)
    -P                       Import Plu (work with sm80/sm110/sm120)
    -M                       Import DateTime (work with sm80/sm110/sm120)
    -T                       Import Trace (work with sm80/sm110/sm120)
    -L                       Import Flexi-barcode (work with sm80/sm110/sm120)
    -A                       Import Password (work with sm80/sm110/sm120)
    -E                       Import Text (work with sm80/sm110/sm120)
    -f Json File             Send Label Format information by Json
    -G Json File             Receive Label Format information by Json
    -m Json File             Import/Export Template Json File
    -R Report File Name      Export Pre-defined Report file
    -s Scale List            Scale List Separated by "," for example "192.168.1.2, 192.168.1.3"
    -S Scale File            File where scale list is
    -i Csv File              Import Csv File
    -o Csv File              Export Csv File
    --check_connection       Check Connecting to the Scales
    --syncdate               Synchronizing datetime to Scale
    --noverifytype           no verify scale type of sm100/sm110
    
    Examples:
        Download Plu to Scale:
            digicon -P -s 192.168.68.197:sm110,192.168.68.215 -i plu_import.csv -m plu_template.json
    
        Check Connection:
            digicon -s 192.168.68.111,192.168.68.112 --check_connection 
    
""" % sys.argv[0]


if __name__ == '__main__':

    iExitCode = 0

    # json_plu_file = ""
    # json_trace_file = ""
    json_label_file = ""
    out_csv_file = ""
    in_csv_file = ""
    template_file = ""
    delete_file = ""
    report_file = ""
    delete_report_file = ""
    group_file = ""
    filter_file = ""
    scale_list = []
    scale_file = ""

    dat_file = ""

    get_label = False

    optImportForPlu = False
    optImportForTrace = False
    optImportForFlexibarcode = False
    optImportForPresetKey = False
    optImportForPassword = False
    optImportForText = False
    optImportForDateTime = False
    optTitling = False
    optCheckConnection = False    # 检测秤是否连接
    optSyncDate = False           # 同步本机时间到秤

    file_write = None
    file_read = None
    access_file_name = ""

    # 日志模块功能
    common.log_init()

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "vHEPMTKLAhvd:G:c:t:s:S:m:f:t:R:i:o:D:",
            [
                "dat=",
                "read=",
                "write=",
                "access_file_name=",
                "check_connection",
                # "check_type",
                "syncdate",
                "noverifytype",
                "complex"
                "help"])

        if not opts:
            print_usage()
            sys.exit(0)

        for o, v in opts:
            if o in ("-h", "--help"):
                print_usage()
            elif o == "--dat":
                dat_file = v
            elif o == "--write":
                file_write = v
            elif o == "--read":
                file_read = v
            elif o == "--access_file_name":
                access_file_name = v
            elif o == '--noverifytype':
                globalspec.setVerifyScaleType(False)
            elif o == "--check_connection":
                optCheckConnection = True
            # elif o =="--check_type":
            #     common.set_check_scale_type_sm110(True)
            elif o == "--syncdate":
                optSyncDate = True
            # elif o == "-c":
            #     json_plu_file = v
            # elif o == "-t":
            #     json_trace_file = v
            elif o == "-f":
                json_label_file = v
            elif o == "-s":
                scale_list = v.split(",")
            elif o == "-S":
                scale_file = v
            elif o == "-o":
                out_csv_file = v
            # elif o == "-F":
            #     filter_file = v
            # elif o == "-g":
            #     group_file = v
            elif o == "-H":
                optTitling = True
            elif o == "-i":
                in_csv_file = v
            elif o == "-d":
                delete_file = v
            elif o == "-m":
                template_file = v
            elif o == "-R":
                report_file = v
            elif o == "-D":
                delete_report_file = v
            elif o == "-P":
                optImportForPlu = True
            elif o == "-M":
                optImportForDateTime = True
            elif o == "-A":
                optImportForPassword = True
            elif o == '-K':
                optImportForPresetKey = True
            elif o == "-L":
                optImportForFlexibarcode = True
            elif o == "-T":
                optImportForTrace = True
            elif o == "-E":
                optImportForText = True
            elif o == "-G":
                json_label_file = v
                get_label = True
            elif o == '-v':
                print "version: " + VERSION
                print "Shanghai Teraoka Co,. Ltd"
                sys.exit(0)
            else:
                sys.exit(1)

    except getopt.GetoptError as err:
        common.log_err("Parameters Error: %s" % err)

    file_list = []

    common.set_title_onoff(optTitling)

    # Checking Confliction
    conflict_check_list_file = []

    conflict_check_list_import = []

    if optImportForPlu:
        conflict_check_list_import.append(optImportForPlu)
    if optImportForDateTime:
        conflict_check_list_import.append(optImportForDateTime)
    if optImportForTrace:
        conflict_check_list_import.append(optImportForTrace)
    if optImportForFlexibarcode:
        conflict_check_list_import.append(optImportForFlexibarcode)
    if optImportForPresetKey:
        conflict_check_list_import.append(optImportForPresetKey)
    if optImportForPassword:
        conflict_check_list_import.append(optImportForPassword)
    if optImportForText:
        conflict_check_list_import.append(optImportForText)
    if optCheckConnection:
        conflict_check_list_import.append(optCheckConnection)
    if optSyncDate:
        conflict_check_list_import.append(optSyncDate)

    if len(conflict_check_list_import) >= 2:
        common.log_err("Multiple Import Options!!!")
        sys.exit(6)

    # Template File conflict with Report File
    if template_file:
        conflict_check_list_file.append(template_file)
    if report_file:
        conflict_check_list_file.append(report_file)
    if delete_report_file:
        conflict_check_list_file.append(delete_report_file)
    if len(conflict_check_list_file) >= 2:
        common.log_err("Template File and Report File conflict!!!")
        sys.exit(6)

    if report_file and not out_csv_file:
        common.log_err("No enough Parameters For exporting Files")
        sys.exit(4)

    if delete_report_file and not in_csv_file:
        common.log_err("No enough Parameters For importing Files")
        sys.exit(4)

    if template_file and not in_csv_file and not out_csv_file:
        common.log_err("No enough Parameters For exporting Files")
        sys.exit(4)

    if scale_list and scale_file:
        common.log_err("Cannot process both scale list and scale file")
        sys.exit(4)

    if in_csv_file and out_csv_file:
        common.log_err("-i and -o cannot be Process Together!!!")
        sys.exit(4)

    # if os.path.exists(json_plu_file):
    #     file_list.append(json_plu_file)
    #
    # if os.path.exists(json_trace_file):
    #     file_list.append(json_trace_file)

    if get_label or os.path.exists(json_label_file):
        file_list.append(json_label_file)

    #	if report_file and report_file not in libsm120.const.report_list.keys():
    #		common.log_err( "Report File not Exist!!!" )
    #		sys.exit(5)

    if len(conflict_check_list_file) == 0 and \
            not optCheckConnection and \
            not optSyncDate and \
            not file_list and \
            not delete_file and \
            not dat_file and \
            not file_write and \
            not file_read:
        common.log_err("No enough Parameters")
        sys.exit(2)

    if (file_write or file_read) and not access_file_name:
        common.log_err("No enough Parameters")
        sys.exit(2)

    if not scale_list and not scale_file and not dat_file:
        common.log_err("Scale List is EMPTY!")
        sys.exit(3)

    if scale_file:
        with open(scale_file) as fp:
            scale_list = [line for line in fp.readlines() if line and line.strip()]
        # 			for line in fp.readlines():
        # 				if line and line.strip(): scale_list.append(line)

    if out_csv_file and os.path.isfile(out_csv_file):
        os.remove(out_csv_file)

    ##########################################
    # 基本导入下发功能
    ##########################################
    if template_file and in_csv_file:
        b_import_flg = False
        # if optImportForPlu or \
        #         optImportForTrace or \
        #         optImportForFlexibarcode or \
        #         optImportForPresetKey or \
        #         optImportForPassword or \
        #         optImportForDateTime or \
        #         optImportForText:
        if optImportForPlu:
            scales_converter = ScalesConverter()
            b_import_flg = True
        elif optImportForTrace:
            scales_converter = ScalesConverter(converter.ConvertDesc_TRACE)
            b_import_flg = True
        elif optImportForFlexibarcode:
            scales_converter = ScalesConverter(converter.ConvertDesc_FLEXIBARCODE)
            b_import_flg = True
        elif optImportForPresetKey:
            scales_converter = ScalesConverter(converter.ConvertDesc_PRESETKEY)
            b_import_flg = True
        elif optImportForPassword:
            scales_converter = ScalesConverter(converter.ConvertDesc_PAS)
            b_import_flg = True
        elif optImportForText:
            scales_converter = ScalesConverter(converter.ConvertDesc_TEXT)
            b_import_flg = True
        elif optImportForDateTime:
            scales_converter = ScalesConverter(converter.ConvertDesc_DAT)
            b_import_flg = True

        # 集成下发功能
        if b_import_flg:
            if not scales_converter.easyImportMaster(scale_list, in_csv_file, template_file):
                iExitCode = 8

    ##########################################
    # 其它处理
    ##########################################

    if optSyncDate:
        # 生成同步时间用json
        json_sync_date = """[
            { "source_expr": "255", "target_field": "DateTimeCode"},
            { "source_expr": "$(1)", "target_field": "Year"},
            { "source_expr": "$(2)", "target_field": "Month"},
            { "source_expr": "$(3)", "target_field": "Day"},
            { "source_expr": "$(4)", "target_field": "Hour"},
            { "source_expr": "$(5)", "target_field": "Minute"}
        ]"""

        dat_json_file = "temp_dat_template.json"
        open(dat_json_file, "w").write(json_sync_date)

        # 生成同步用csv
        dat_csv_file = "temp_dat_import.csv"
        nowtime = datetime.datetime.now()
        strtime = "%s,%02d,%02d,%02d,%02d" % (str(nowtime.year)[2:], nowtime.month, nowtime.day, nowtime.hour, nowtime.minute)
        open(dat_csv_file, "w").write(strtime)

        scales_converter = ScalesConverter(converter.ConvertDesc_DAT)
        if not scales_converter.easyImportMaster(scale_list, dat_csv_file, dat_json_file):
            iExitCode = 8

        os.remove(dat_json_file)
        os.remove(dat_csv_file)

    arr_check_connection = []
    list_success_scale_connection = []
    list_failed_scale_connection = []

    for index, scale in enumerate(scale_list):
        scale = scale.strip()
        if not scale:
            common.log_err("scale %d empty" % index)
            continue

        scale_info = scale.split(':')
        scale = scale_info[0]
        if len(scale_info) > 1:
            scale_type = scale_info[1]
        else:
            scale_type = "sm120"

        # 清除内存表中数据，以防与下次下发冲突
        if scale_type.lower() == "sm120":
            # sm120
            ease = libsm120.easy.Easy(scale)
            common.clear_all_tables(libsm120.const.db_name)

        else:
            # sm110
            ease = libsm110.easy.Easy(scale)
            common.clear_all_tables(libsm110.const.db_name)

        if delete_file:
            if ease.easyDeleteFile(delete_file):
                common.log_info("Delete Master %s Successfully!" % delete_file)
                list_success_scale_connection.append(scale)
            else:
                common.log_err("Delete Master Failed!")
                list_failed_scale_connection.append(scale)

        if file_read:
            # if ease.easyReceiveFile(file_read, access_file_name):
            #     common.log_info("Receive Master %s to %s Successfully!" % (file_read, access_file_name))
            # else:
            #     common.log_err("Receive Master Failed!")
            try:
                file_data_list = []
                file_failed_list = []
                for master_name in file_read.split(','):
                    temp_file_name = "temp1_" + scale + "_" + master_name + "_.dat"
                    result = ease.easyReceiveFile(master_name, temp_file_name)
                    if result:
                        try:
                            temp_file_data = ""
                            with open(temp_file_name, 'r') as fp:
                                temp_file_data = fp.read()
                            os.remove(temp_file_name)

                            for line_data in temp_file_data.split("\n"):
                                if line_data.strip(' \r'):
                                    file_data_list.append(master_name + ":" + line_data.rstrip(" \r"))
                        except Exception, ex:
                            common.log_err(ex)
                            file_failed_list.append(master_name)
                file_data = "\n".join(file_data_list)
                with open(access_file_name, "w") as fp2:
                    fp2.write(file_data)

                if len(file_failed_list) > 0:
                    raise Exception("Receive from %s Masters %s Failed" % (scale, ",".join(file_failed_list)))

            except Exception, e:
                common.log_err(e)
                list_failed_scale_connection.append(scale)
            else:
                common.log_info("Receive from %s Masters (%s) to %s Successfully!" % (scale, file_read, access_file_name))
                list_success_scale_connection.append(scale)

        if file_write:
            # if ease.easySendFile(file_write, access_file_name):
            #     common.log_info("Send Master %s to %s Successfully!" % (file_write, access_file_name))
            # else:
            #     common.log_err("Send Master Failed!")
            file_failed_list = []
            file_total_list = []
            dict_data = {}
            try:
                with open(access_file_name, "r") as fp2:
                    file_data = fp2.read()
                    for line_data in file_data.split("\n"):
                        line_data = line_data.rstrip(" \r")
                        pat = re.compile("(\w+):(.+)")
                        m = pat.match(line_data)
                        if m:
                            if not m.group(1) in dict_data:
                                dict_data[m.group(1)] = ""
                            dict_data[m.group(1)] += m.group(2) + "\n"

                for scale_file, scale_file_data in dict_data.items():
                    temp_file_name = "temp2_" + scale + "_" + scale_file + "_" + ".dat"
                    with open(temp_file_name, "w") as fp2:
                        fp2.write(scale_file_data)
                    file_total_list.append(scale_file)
                    if not ease.easySendFile(scale_file, temp_file_name):
                        file_failed_list.append(scale_file)

                    os.remove(temp_file_name)

                if len(file_failed_list) > 0:
                    raise Exception("Send Masters (%s) to %s failed" % (",".join(file_failed_list), scale))

            except Exception, e:
                common.log_err(e)
                list_failed_scale_connection.append(scale)
            else:
                common.log_info("Send Masters (%s) to %s Successfully!" % (",".join(file_total_list), scale))
                list_success_scale_connection.append(scale)

        # if json_plu_file:
        #     ease.easySendPlu(json_plu_file)
        # if json_trace_file:
        #     ease.easySendTrace(json_trace_file)
        if json_label_file:
            try:
                if get_label:
                    ease.easyRecvPrintFormat(json_label_file)
                else:
                    ease.easySendPrintFormat(json_label_file)
            except Exception, e:
                common.log_err("Label Format Error:", e)

        # common.clear_all_tables(libsm120.const.db_name)
        if template_file and out_csv_file:
            if not ease.exportCSV(
                    export_template_file=template_file,
                    export_template_info="",
                    export_csv_file=out_csv_file,
                    # title=True):
                    title=common.get_title_onoff()):
                        list_failed_scale_connection.append(scale)
            else:
                        list_success_scale_connection.append(scale)

        if report_file:
            if scale_type.lower() == "sm120":
                if not ease.exportCSV(
                        export_template_file="",
                        export_template_info=libsm120.const.report_list[report_file],
                        export_csv_file=out_csv_file,
                        # title=True):
                        title=common.get_title_onoff()):
                            list_failed_scale_connection.append(scale)
                else:
                            list_success_scale_connection.append(scale)
            else:
                if not ease.exportCSV(
                        export_template_file="",
                        export_template_info=libsm110.const.report_list[report_file],
                        export_csv_file=out_csv_file,
                        # title=True):
                        title=common.get_title_onoff()):
                            list_failed_scale_connection.append(scale)
                else:
                            list_success_scale_connection.append(scale)

        if delete_report_file:
            if not ease.deleteFromCSV(
                    delete_report_file,
                    in_csv_file,
                    with_title=common.get_title_onoff()):
                iExitCode = 9
                list_failed_scale_connection.append(scale)
            else:
                list_success_scale_connection.append(scale)

        def check_conn(p_scale_ip, p_scale_type, p_result):
            if p_scale_type.lower() == "sm120":
                o_scale = libsm120.digiscale.DigiSm120(p_scale_ip)
            else:
                o_scale = libsm110.smtws.smtws(p_scale_ip)

            if isinstance(p_result, list) and len(p_result) > 0:
                p_result[0] = 0 if o_scale.check_connection() else -1

        if optCheckConnection:
            result = [-1]
            thd_check = Thread(target=check_conn, args=(scale, scale_type, result))
            arr_check_connection.append((thd_check, scale, result))
            thd_check.start()

    for entry_check_connection in arr_check_connection:
        entry_check_connection[0].join()
        scale_ip = entry_check_connection[1]
        if entry_check_connection[2][0] == 0:  # connection OK
            list_success_scale_connection.append(scale_ip)
            common.log_info("%s Connection OK..." % scale_ip)
            common.log2_info("%s Connection OK..." % scale_ip)
        else:
            list_failed_scale_connection.append(scale_ip)
            common.log_info("%s Connecting Failed..." % scale_ip)
            common.log2_info("%s Connecting Failed..." % scale_ip)

    if len(list_success_scale_connection) > 0 or len(list_failed_scale_connection) > 0:
        try:
            if len(list_failed_scale_connection) > 0:
                iExitCode = 10
            else:
                iExitCode = 0
            with open(LOGFILE_ERROR, 'w') as fp1:
                fp1.write('\r\n'.join(list_failed_scale_connection))
            with open(LOGFILE_SUCCEED, 'w') as fp2:
                fp2.write('\r\n'.join(list_success_scale_connection))
        except Exception, e:
            common.log_err(e)

    # 处理直接下发的单个DAT文件(仅支持SM110)
    if dat_file:
        try:
            import re

            # 匹配192.168.68.125.25.DAT这样的格式
            pat = re.compile("(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})\.(\w+)\.dat")
            m = pat.match(dat_file.lower())
            if m:
                scale_ip = m.group(1)
                file_no = int(m.group(2), 16)
                sm110_scale = libsm110.smtws.smtws(scale_ip)
                if not sm110_scale.upload_file(file_no, dat_file):
                    raise Exception('Error On Sending Data File')
            else:
                raise Exception("Incorrect File Name")
        except Exception, e:
            common.log_err(e)
            iExitCode = 8
            # print dir(e)
        else:
            common.log_info("Finished Sending Dat File To Scale!")

    sys.exit(iExitCode)

#	m = KageTest()
#	m.test()

# m = master.MgpMaster('mgp.json')
# m = entity.MgpMaster()

# csvreader.SmCsvReader().read('m.csv', lambda x : m.add_rows(x))
# m.from_csv('m.csv')
# m.to_json("m.json")

# m.to_csv('koko.csv', True)

# scale = digiscale.DigiSm120('S0501')
# scale.send(m)
# m.to_csv('aa.csv')


# rootdir_local   = '.'                       # local folder
# rootdir_remote  = '.'                       # remote folder
# ftp = smftp('192.168.100.22', 'anonymous', '')
# ftp = smftp('S0501', 'admin', 'admin')
# ftp.login()
# ftp.download_file(rootdir_local + '/' + 'plu0uall.csv', 'plu0uall.csv')
# time.sleep(5);
# conn = open_sqlite_db('kage.sqlite')

# cursor = conn.cursor()
# cursor.execute('CREATE TABLE IF NOT EXISTS t1(f1 int primary key, f2 text)')
# cursor.execute('REPLACE INTO t1 VALUES (1, "abc")');
# cursor.execute('REPLACE INTO t1 VALUES (2, "def")');
# conn.commit()

# cursor.execute('select * from t1');
# for row in cursor:
# print row['f2']

#	with open('mgp.json', 'r') as f:
#		data = json.load(f)
#		for k, v in data.items():
#			print 'k:%s v:%s' % (k, v)
