# encoding=gbk
import os, sys, csv
import codecs, StringIO
from . import common

class SmCsvReader:
    def read_line_by_line(
            self,
            file_path,
            callback,
            encoding=sys.getdefaultencoding(),
            head=True):
        #		with open(file_path, "r") as fp:
        # 			cr = csv.reader(fp)
        # 			if head: cr.next()
        # 			all_data = \
        # 			[
        # 				[ cur_cell.decode(encoding) for cur_cell in cur_row ] for cur_row in cr
        # 			]
        with codecs.open(file_path, 'r', encoding) as fp:
            # dat = fp.read().replace('\x00','').decode(encoding) #去掉所有\x00
            # dat = fp.read().replace('\x00', '')  # 去掉所有\x00

            dat = ""
            lineCount = 0
            while True:
                lineCount += 1
                try:
                    line = fp.readline()
                except Exception, ex:
                    common.log_err("file: %s, line: %d, error: %s" % (file_path, lineCount, ex))
                    raise ex
                if not line:
                    break
                dat += line

            dat = dat.replace('\x00', '')

            cr = csv.reader(StringIO.StringIO(dat))
            # all_data = [  [ cur_cell for cur_cell in cur_row ] for cur_row in cr ]
            if head:
                cr.next()

            for i, cur_row in enumerate(cr):
                # if callback is not None:
                if callback is not None and len(cur_row) > 0:
                    callback(i, cur_row)

    def read_all_lines(self, file_path, callback, encoding=sys.getdefaultencoding()):
        rows_list = []
        with open(file_path, 'r') as fp:
            cr = csv.reader(fp)
            header = cr.next()
            for cur_row in cr:
                # for i, col in enumerate(header): print col.strip(), cur_row[i].decode(encoding)
                row_dic = [{col.strip().decode(encoding): cur_row[i].decode(encoding)} for i, col in enumerate(header)]
                # print row_dic
                # for i,col in enumerate(header):
                # print '%d, %s' % (i, col)
                #	row_dic.append( { col: cur_row[i] } )
                rows_list.append(row_dic)
        if callback is not None: callback(rows_list)
