#encoding=gbk
# import math
import csv, StringIO
import re
import datetime
import decimal


def eval_trim(expr, vlist, mlist, glist):
	return expr.strip()

def eval_isempty(expr, vlist, mlist, glist):
	if expr.strip() == '':
		return 'TRUE'
	else:
		return 'FALSE'

def eval_and(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	for col in col_list:
		if col != 'TRUE':
			return 'FALSE'
	return 'TRUE'
		

def eval_isnotempty(expr, vlist, mlist, glist):
	if expr.strip() == '':
		return 'FALSE'
	else:
		return 'TRUE'

def eval_isnull(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if col_list and len(col_list) == 2:
		if col_list[0].strip() == "":
			return col_list[1]
		return col_list[0]
	return ""

def eval_iszero(expr, vlist, mlist, glist):
	try:
		col_list = csv.reader(StringIO.StringIO(expr)).next()
		if isinstance(col_list, list) and len(col_list) == 1:
			if int(col_list[0]) == 0:
				return "TRUE"
			else:
				return "FALSE"
		else:
			return "TRUE"
	except:
		return "TRUE"

def eval_isnotzero(expr, vlist, mlist, glist):
	try:
		col_list = csv.reader(StringIO.StringIO(expr)).next()
		if isinstance(col_list, list) and len(col_list) == 1:
			if int(col_list[0]) == 0:
				return "FALSE"
			else:
				return "TRUE"
		else:
			return "FALSE"
	except:
		return "FALSE"
	

def eval_isnotnull(expr, vlist, mlist, glist):
	#print "expr:", expr
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	#print "col_list:", col_list
	if col_list and len(col_list) == 2:
		if col_list[0].strip() == "":
			return ""
		return col_list[1]
	return ""

def eval_hex(expr, vlist, mlist, glist):
	return str(int(expr, 16))

def eval_int(expr, vlist, mlist, glist):
	return hex(int(expr))[2:].upper()


def eval_join(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	#for col in col_list: print col
	if len(col_list) >= 3:
		first  = col_list[0]
		second = col_list[1]
		third  = col_list[2]

		return first.join([second, third])

	return ""

def eval_div(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) >= 2:
# 		first  = float(col_list[0])
# 		second = float(col_list[1])
 		first  = decimal.Decimal(col_list[0])
 		second = decimal.Decimal(col_list[1])
		return str(first / second)
	return ""

def eval_mod(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) >= 2:
		first  = int(col_list[0])
		second = int(col_list[1])
		return str(first % second)
	return ""


def eval_rtnindex(expr, vlist, mlist, glist):
	if not expr: return ""
	tmp_data = expr.split(',')
	if len(tmp_data) >= 2:
		index = int(tmp_data[0])
		data = ','.join(tmp_data[1:])
		li = data.split('\n')
		if index - 1 >= len(li): return ""
		return li[index - 1]
	else:
		return ""

def eval_csvformat(expr, vlist, mlist, glist):
	return expr.replace('"','""')

def eval_csvformat4(expr, vlist, mlist, glist):
	return expr.replace('"','""""')

def eval_twsascii(expr, vlist, mlist, glist):
	#print "expr:",expr
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) < 2: return ""
	data_list = col_list[1]
	font_list = col_list[0]
	#print "data_list:",data_list
	#print "font_list:",font_list
	lst_data = csv.reader(StringIO.StringIO(data_list)).next()
	lst_font = csv.reader(StringIO.StringIO(font_list)).next()
	#search for not empty reversed
	j = -1
	for i in reversed(xrange(len(lst_data))):
		if lst_data[i]:
			j=i+1
			break
	lst_data = lst_data[:j]
	lst_data = [ d.replace('"','""') for d in lst_data ]
	lst_font = lst_font[:j]

	all_data = zip(lst_font, lst_data)
	all_data_2 = ["%s,\"%s\"" % (d[0], d[1]) for d in all_data]

	#for all_cell in all_data_2:
	#	u = csv.reader(StringIO.StringIO(all_cell)).next()
	#	print u[0], ":", u[1]

	result = "\n".join(all_data_2)
	#print "result:", result
	return result

def eval_csv2tws_autoindent(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) >= 2:
		col_data = col_list[0]
		font = col_list[1]

		from font import font_num_table
		import sys
		data_un = list(col_data.decode(sys.getdefaultencoding()))
		
		k = []
		c = ""
		font_max_size = font_num_table[int(font)]
		for d in data_un:
			if ord(d) >= 0x4e00 and ord(d) <= 0x9fa5:
				if len(c.encode(sys.getdefaultencoding())) + 2 > font_max_size:
					k.append(c.encode(sys.getdefaultencoding()))
					c = ""
				c += d
			else:
				if len(c.encode(sys.getdefaultencoding())) + 1 > font_max_size:
					k.append(c.encode(sys.getdefaultencoding()))
					c = ""
				c += d

		if c:
			k.append(c.encode('gbk'))
			c = ""
		
		#print k
		
		k = k[:10]

		#all_data = zip(lst_font, lst_data)
		#all_data_2 = ["%s,\"%s\"" % (d[0], d[1]) for d in all_data]
		#result = "\n".join(all_data_2)
		result = ""
		return result
	return ""
	

def eval_csv2twsascii(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) >= 2:
		col_data = col_list[0]
		font = col_list[1]
		col_delimiter = ','
		if len(col_list) > 2:
			col_delimiter = col_list[2]
		lst_data = csv.reader(StringIO.StringIO(col_data), delimiter=col_delimiter).next()
		lst_font = [font] * len(lst_data)
		
		all_data = zip(lst_font, lst_data)
		all_data_2 = ["%s,\"%s\"" % (d[0], d[1]) for d in all_data]
		result = "\n".join(all_data_2)
		return result
	return ""

def eval_rtncount(expr, vlist, mlist, glist):
	if not expr:
		return 0
	return len(expr.split('\n'))

def eval_csvindex(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) >= 2:
		index = int(col_list[0])
		if index >= len(col_list): return ""
		return col_list[index]
	return ""

def eval_csvcount(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if col_list:
		return str(len(col_list))
	return 0

def eval_substr(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	#col_list = expr.split(',')
	if len(col_list) >= 2:
		orig = col_list[0]
		first = int(col_list[1])
		if len(col_list) > 2:
			second = int(col_list[2])
			return orig[first : first+second]
		return orig[first:]
	return ""

def eval_notequals(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	#col_list = expr.split(',')
	if len(col_list) == 2:
		return 'FALSE' if col_list[0] == col_list[1] else 'TRUE'
	else:
		return 'TRUE'

def eval_equals(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	#col_list = expr.split(',')
	if len(col_list) == 2:
		return 'TRUE' if col_list[0] == col_list[1] else 'FALSE'
	else:
		return 'FALSE'

def eval_lessthan(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	#col_list = expr.split(',')
	if len(col_list) == 2:
		return 'TRUE' if int(col_list[0]) < int(col_list[1]) else 'FALSE'
	else:
		return 'FALSE'

def eval_greatthan(expr, vlist, mlist, glist):
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	#col_list = expr.split(',')
	if len(col_list) == 2:
		return 'TRUE' if int(col_list[0]) > int(col_list[1]) else 'FALSE'
	else:
		return 'FALSE'

def eval_iif(expr, vlist, mlist, glist):
	#col_list = expr.split(',')
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) == 3:
		if "TRUE" == col_list[0]: return col_list[1]
		return col_list[2]

def eval_case(expr, vlist, mlist, glist):
	#col_list = expr.split(',')
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) % 2 == 0:
		sName = col_list[0].strip()
		cp = 1
		while (True):
			sVal = col_list[cp].strip()
			if sVal == sName:
				break
			cp += 2
			if cp >= len(col_list): break
			if cp == len(col_list) - 1: return col_list[cp]
		if cp < len(col_list): return col_list[cp + 1]
	return ""

def eval_lfill(expr, vlist, mlist, glist):
	#col_list = expr.split(',')
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) in (2, 3):
		orig = col_list[0]
		fill_what = '0'
		length = int(col_list[1])
		if len(col_list) == 3:
			fill_what = col_list[2]
		return fill_what * (length - len(orig)) + orig
	return ""

def eval_rfill(expr, vlist, mlist, glist):
	#col_list = expr.split(',')
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) in (2, 3):
		orig = col_list[0]
		fill_what = '0'
		length = int(col_list[1])
		if len(col_list) == 3:
			fill_what = col_list[2]
		return orig + fill_what * (length - len(orig))

def eval_dec(expr, vlist, mlist, glist):
	#col_list = expr.split(',')
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) == 2:
# 		opt1 = int(col_list[0])
# 		opt2 = int(col_list[1])
 		opt1 = decimal.Decimal(col_list[0])
 		opt2 = decimal.Decimal(col_list[1])
		return str(opt1 - opt2) 
	return ""


def eval_add(expr, vlist, mlist, glist):
	#col_list = expr.split(',')
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) == 2:
# 		opt1 = int(col_list[0])
# 		opt2 = int(col_list[1])
 		opt1 = decimal.Decimal(col_list[0])
 		opt2 = decimal.Decimal(col_list[1])
		return str(opt1 + opt2) 
	return ""

def eval_mul(expr, vlist, mlist, glist):
	#col_list = expr.split(',')
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) == 2:
		#opt1 = float(col_list[0])
		#opt2 = float(col_list[1])
		opt1 = decimal.Decimal(col_list[0])
		opt2 = decimal.Decimal(col_list[1])
		return str(int(opt1 * opt2))
	return ""

def eval_trunc(expr, vlist, mlist, glist):
	#col_list = expr.split(',')
	col_list = csv.reader(StringIO.StringIO(expr)).next()
	if len(col_list) == 1:
# 		return str(int(float(col_list[0])))
 		return str(int(decimal.Decimal(col_list[0])))
	return ""

def eval_len(expr, vlist, mlist, glist):
	if expr:
		return str(len(expr))
	return "0"

def eval_now(expr, vlist, mlist, glist):
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def eval_dola(expr, vlist, mlist, glist):
	try:
		col = int(expr)
	except ValueError:
		col = 0 
	if col > 0 and col <= len(vlist):
		return vlist[col - 1]
	else:
		if mlist and mlist.has_key(expr):
			return mlist[expr]
		if glist and glist.has_key(expr):
			return glist[expr]
		#return expr
		return ""
	
	
	
funcList = {
	"trim":	        eval_trim,
	"substr":       eval_substr,
	"equals":       eval_equals,
	"notequals":    eval_notequals,
	"less":         eval_lessthan,
	"great":        eval_greatthan,
	"iif":          eval_iif,
	"case":         eval_case,
	"lfill":        eval_lfill,
	"rfill":        eval_rfill,
	"div":          eval_div,
	"mod":          eval_mod,
	"csvindex":     eval_csvindex,
	"csvcount":     eval_csvcount,
	"rtnindex":     eval_rtnindex,
	"rtncount":     eval_rtncount,
	"twsascii":     eval_twsascii,
#	"csv2twsascii": eval_csv2twsascii,
	"csv2tws":      eval_csv2tws_autoindent,
	"csvformat":    eval_csvformat,
	"csvformat4":   eval_csvformat4,
	"add":          eval_add,
	"dec":          eval_dec,
	"mul":          eval_mul,
	"trunc":        eval_trunc,
	"hex2int":      eval_hex,
	"int2hex":		eval_int,
	"isempty":      eval_isempty,
	"isnotempty":   eval_isnotempty,
	"isnull":       eval_isnull,
	"isnotnull":    eval_isnotnull,
	"iszero":       eval_iszero,
	"isnotzero":    eval_isnotzero,
	"now":          eval_now,
	"len":          eval_len,
	"and":          eval_and,
	"$":            eval_dola
}

pat = "^"
pat_list = ["\$" if key=='$' else key for key, value in funcList.items()]
pat += "(" + "|".join(pat_list) + ")" + "\("
pat = re.compile(pat)

class StrParser:
	def __init__(self, expr = "", vlist = None, mlist = None, glist = None):
		self.expr = expr
		#self.vlist = vlist
		self.curPos = 0
		self.fieldByIndex = vlist
		self.fieldByName = mlist
		self.globalName = glist
		


	def is_function(self, expr):
		m = pat.match(expr)
		if m:
			data = m.group()[:-1]
			return len(data), funcList.get(data)
		return -1, None
				
	"""
	def is_function2(self, expr):
		funcList = {
			"$":	self.eval_dola
		}
		
		fn, fc = '', None
		for func_name, func_cb in funcList.items():
			tmpStr = func_name + "("
			if expr.startswith(tmpStr):
				fn, fc = func_name, func_cb
				break
		if len(fn) == 0: return -1, None
		return len(fn), fc

	def eval2(self, level):
		left_string = ''
		while (self.curPos < len(self.expr)):
			curStr = self.expr[self.curPos:]
			if not curStr:
				return left_string
			if level > 0 and curStr[0] == ')':
				self.curPos += 1
				return left_string

			size, funcCallBack = self.is_function2(curStr)
			if size == -1:
				left_string += curStr[0]
				self.curPos+=1
				curStr = curStr[1:]
			else:
				self.curPos += size + 1
				left_string += funcCallBack(self.eval2(level + 1), self.fieldByIndex, self.fieldByName, self.globalName)
		return str(eval(left_string))
	"""

	def eval(self, level, expr=None, fieldByIndex=None,fieldByName=None,globalName=None,resetPos=False):
		if resetPos: self.curPos = 0
		if not expr: expr = self.expr
		if not fieldByIndex: fieldByIndex = self.fieldByIndex
		if not fieldByName: fieldByName = self.fieldByName
		if not globalName: globalName = self.globalName
		
		left_string = ''
		while (self.curPos < len(expr)):
			curStr = expr[self.curPos:]
			if not curStr:
				return left_string
			if level > 0 and curStr[0] == ')':
				self.curPos += 1
				return left_string

			size, funcCallBack = self.is_function(curStr)
			if size == -1:
				left_string += curStr[0]
				self.curPos+=1
				curStr = curStr[1:]
			else:
				self.curPos += size + 1
				left_string += funcCallBack(self.eval(level + 1, expr, fieldByIndex, fieldByName, globalName), fieldByIndex, fieldByName, globalName)
		return left_string
			

if __name__ == '__main__':
	#print '|' + StrParser('iif(equals($(2),33),10,11)', ['abcde','32']).eval(0) + '|'
	#print '|' + StrParser('$(1)', ['abcde','32']).eval(0) + '|'
	#print '|' + StrParser('case(1,2,a,1,b,d)', ['abcde','32']).eval(0) + '|'
	#print StrParser('$(1)', ['3', ' apple', ' 12', ' 0', ' 23', ' 5', ' 17', ' 181', ' 1aaaa', ' 2bbbb ']).eval(0)
	#print StrParser("join(\"\n\",'3,4','5,6')", []).eval(0)
	#dic = {"m": 'kage,"kage2,kage3"'}
	sdic = r'''
		{
			"m": "kage,\"kage2,kage3\""
		}
	'''
	sdic2 = r'''
		{"v": "isnotnull(\"csvindex(2,$(m))\",\"21,\"\"csvindex(2,$(m))\"\"\")isnotnull(\"csvindex(2,$(m))\",\"\n21,\"\"csvindex(2,$(m))\"\"\")"}
	'''
	import json
	dic = json.loads(sdic)
	dic2 = json.loads(sdic2)
	#print dic2["v"]
	#for row in csv.reader(StringIO.StringIO(dic["m"]), quotechar="\""): print row
	#for row in csv.reader(StringIO.StringIO(dic["m"])): print row
	#print StrParser('isnotnull("csvindex(2,$(m))","csvindex(2,$(m))"', [], dic).eval(0)
	#print StrParser(dic2["v"], [], dic).eval(0)
# 	print StrParser("mod(8,3)", [], {}).eval(0)
# 	print StrParser("iszero(substr(10,1))", [], {}, {}).eval(0)
 	#print StrParser("rfill(1234,10)", [], {}, {}).eval(0)
 	#print StrParser("len(abc)", [], {}, {}).eval(0)
	data = '""abc,def"",ghi'
	
	data = "中b国人567777"
	#print len(data)
	
	#print StrParser('add(1.2,3)',[],{},{}).eval(0)
	print StrParser('hex2int(substr(lfill(int2hex(3232253053),8),0,2))',[],{},{}).eval(0)

 	#StrParser("csv2tws(12345中国国国国国国国国国国国国国国国国国国国国,21)", [], {}, {}).eval(0)
					
	#for l in k: print l
			
	
# 	from re import compile as _Re
# 	_unicode_chr_splitter = _Re( '(?s)((?:[\ud800-\udbff][\udc00-\udfff])|.)' ).split
# 	def split_unicode_chrs( text ):
# 		return [ chr for chr in _unicode_chr_splitter( text ) if chr ]
#  	print split_unicode_chrs(data)
	
	#m = re.sub("[\x80-\xFF]{2}", '00', data)
	
	#x=5
	#for y in range(10):
	#    print data.decode('utf-8')[x*y:x*(y+1)].encode('utf-8')
	#print data.decode('gbk')[:5].encode('gbk')
	
	
	#jdata = json.loads(jstr)
	#k = 'ab"c,def'

	
	
	#print jdata["name"]
 	#print StrParser("twsascii(\"21,22,23,24,25\",\"\"\"csvformat4(%s)\"\",\"\"ghi,jkl\"\"\")" % k, [], {}, {}).eval(0)
 	#print StrParser("and(FALSE,FALSE)", [], {}, {}).eval(0);
 	#print StrParser("add(1,mul(256,isnull(1,0)))", [], {}, {}).eval(0);
 	#print StrParser("csv2twsascii(\"abc|def|中国\",21,|)", [], {}, {}).eval(0);

	
	#print '|' + StrParser('"$(2)" + (6 - len("$(2)")) * "0"', ['abcde', '123']).eval2(0) + '|'



