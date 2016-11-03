#encoding=gbk
import sys,csv

class SmCsvReader:
	def read_line_by_line(
		self,
		file_path,
		callback,
		encoding=sys.getdefaultencoding(),
		head = True):
		with open(file_path, "r") as fp: 
			cr = csv.reader(fp)
			if head: cr.next()
			all_data = \
			[
				[
					cur_cell.decode(encoding) for cur_cell in cur_row
				] for cur_row in cr
			]
		for i, cur_row in enumerate(all_data): 
			if callback is not None: callback(i, cur_row)
		
	def read_all_lines(self, file_path, callback, encoding=sys.getdefaultencoding()):
		rows_list = []
		with open(file_path, 'r') as fp: 
			cr = csv.reader(fp)
			header = cr.next()
			for cur_row in cr:
				#for i, col in enumerate(header): print col.strip(), cur_row[i].decode(encoding)
				row_dic = [{col.strip().decode(encoding): cur_row[i].decode(encoding)} for i, col in enumerate(header)]
				#print row_dic
				#for i,col in enumerate(header):
					#print '%d, %s' % (i, col)
				#	row_dic.append( { col: cur_row[i] } )
				rows_list.append(row_dic)
		if callback is not None: callback(rows_list)
		
