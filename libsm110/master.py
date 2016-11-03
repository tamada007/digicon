#encoding=gbk

import traceback
import sys
import csv
import StringIO
from common import common
import const

def get_length_of_ascii(cell_data, max_length):
	total_length = 0
	while cell_data:
		#font_size = cell_data[:2]
		length = common.hex2int(cell_data[2:4])
		last_pos = 4 + length * 2
		total_length += last_pos
		if last_pos >= min(max_length, len(cell_data)): break
		if cell_data[ last_pos : last_pos+2 ] == "0C":
			total_length += 2
			break
		
		#while last_pos < min(max_length, len(cell_data)) and cell_data[last_pos : last_pos+2] == "00":
		while last_pos < min(max_length, len(cell_data)) and cell_data[last_pos : last_pos+2] in ("00", "0D"):
			total_length += 2
			last_pos += 2
			
		if last_pos >= min(max_length, len(cell_data)): break
		#cell_data = cell_data[last_pos + 2:] 
		cell_data = cell_data[last_pos:]
	return total_length

'''
def get_length_of_ascii(cell_data):
	total_length = 0
	while cell_data:
		font_size = cell_data[:2]
		length = common.hex2int(cell_data[2:4])
		last_pos = 4 + length * 2
		total_length += last_pos + 2
		if cell_data[ last_pos : last_pos+2 ] == "0C": break
		cell_data = cell_data[last_pos + 2:] 
	return total_length
'''

class TWSReader():
	#dat格式转结构体格式
	def dat_to_cell(self, arg0, arg1, arg2):
		return arg0
	#结构体格式转dat
	def cell_to_dat(self, arg0, arg1, arg2):
		return arg0
	#csv转结构体
	def csv_to_cell(self, arg0, arg1, arg2):
		return arg0
	#结构体转csv
	def cell_to_csv(self, arg0, arg1, arg2):
		return arg0
	#csv转dat
	def csv_to_dat(self, arg0, arg1, arg2):
		return arg0
	#dat转csv
	def dat_to_csv(self, arg0, arg1, arg2):
		return arg0

		
class F1F2Reader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		return arg0.rjust(arg1, '0')
		
class HEXReader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try: return common.int2hex(arg0, length = arg1)
		except Exception,e:
			return common.int2hex(0, length = arg1)
	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			return common.hex2int(arg0)
		except Exception, e:
			return 0
	def cell_to_dat(self, arg0, arg1, arg2):
		return self.csv_to_dat(arg0, arg1, arg2)
	def dat_to_cell(self, arg0, arg1, arg2):
		return self.dat_to_csv(arg0, arg1, arg2)

		
class BYTESReader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try: return arg0.encode(sys.getdefaultencoding()).encode("hex").ljust(arg1, '0')
		except Exception, e:
			return "0".ljust(arg1, '0')
	def dat_to_csv(self, arg0, arg1, arg2):
		try: return arg0.decode("hex").rstrip('\x00').decode(sys.getdefaultencoding(), errors='ignore')
		except Exception, e:
			return ""
	def cell_to_dat(self, arg0, arg1, arg2):
		try: return arg0.encode(sys.getdefaultencoding()).encode("hex").ljust(arg1, '0')
		except Exception, e:
			return "0".ljust(arg1, '0')
	def dat_to_cell(self, arg0, arg1, arg2):
		try: return arg0.decode("hex").rstrip('\x00').decode(sys.getdefaultencoding(), errors='ignore')
		except Exception, e:
			return ""

		
class BCDReader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try: return str(arg0).rjust(arg1, '0')
		except Exception, e:
			return "0".rjust(arg1, '0')

	def dat_to_csv(self, arg0, arg1, arg2):
		try: return int(arg0)
		except Exception, e:
			return 0

	def cell_to_dat(self, arg0, arg1, arg2):
		try: return str(arg0).rjust(arg1, '0')
		except Exception, e:
			return "0".rjust(arg1, '0')
	def dat_to_cell(self, arg0, arg1, arg2):
		try: return int(arg0)
		except Exception, e:
			return 0
		
class ASCIIReader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			dst_data = []
			for row in csv.reader(StringIO.StringIO(arg0)):
				dst_oneline = []
				text_data = row[1].encode(sys.getdefaultencoding()).encode("hex").upper()
				text_len = len(text_data) // 2 
				dst_oneline.append( common.int2hex(int(row[0])) )
				dst_oneline.append( common.int2hex(text_len) )
				dst_oneline.append( text_data )
				dst_data.append("".join(dst_oneline))
			return "0D".join(dst_data) + "0C"
		except Exception, e:
			return "00000C"
		
	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, list):
			return arg0
		try:
			dst_data = []
			for row in csv.reader(StringIO.StringIO(arg0)):
				dst_oneline = {}
				text_data = row[1].decode(sys.getdefaultencoding(), errors='ignore')
				text_len = len(text_data) // 2 
				dst_oneline = {
					"font_size":  int(row[0]),
					"text": text_data
				}
				dst_data.append(dst_oneline)

			return dst_data
		except Exception, e:
			return [{"font_size": 0, "text": ""}]

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			cell_data = arg0.decode("hex").rstrip("\x0c\x00")
			dst_lines = []
			while cell_data:
				cell_data = cell_data.lstrip("\x0d")
				font_size = ord(cell_data[0])
				length    = ord(cell_data[1])
				text      = cell_data[2:2+length].decode(sys.getdefaultencoding(), errors='ignore')
				#dst_lines.append( ",".join([str(font_size), "\"" + text + "\""]) )
				dst_lines.append( ",".join([str(font_size), "\"" + text.replace('"','""') + "\""]) )
				cell_data = cell_data[2+length:]
			return "\n".join(dst_lines)
		except Exception, e:
			common.log_err( "error:" + arg0 )
			common.log_err( traceback.format_exc() )
			return ""


	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			cell_data = arg0.decode("hex").rstrip("\x0c\x00")
			dst_lines = []
			while cell_data:
				cell_data = cell_data.lstrip("\x0d")
				font_size = ord(cell_data[0])
				length    = ord(cell_data[1])
				text      = cell_data[2:2+length].decode(sys.getdefaultencoding(), errors='ignore')
				dst_lines.append({
					"font_size":   font_size,
					"text":        text
				})
				cell_data = cell_data.rstrip[2+length:]
			return dst_lines
		except Exception, e:
			print e, ":", cell_data
			return ""


	def cell_to_dat(self, arg0, arg1, arg2):
		try:
			dst_data = []
			for row in arg0:
				dst_oneline = []
				text_data = row["text"].encode(sys.getdefaultencoding()).encode("hex").upper()
				text_len = len(text_data) // 2 
				dst_oneline.append( common.int2hex( row["font_size"]) )
				dst_oneline.append( common.int2hex(text_len) )
				dst_oneline.append( text_data )
				dst_data.append("".join(dst_oneline))
			return "0D".join(dst_data) + "0C"
		except:
			return "00000C"

	def cell_to_csv(self, arg0, arg1, arg2):
		try:
			dst_data = []
			#print arg0
			for row in arg0:
				#dst_data.append(",".join([ str(row["font_size"]), "\"" + row["text"] + "\"" ]))
				dst_data.append(",".join([ str(row["font_size"]), "\"" + row["text"].replace('"','""') + "\"" ]))

			return "\n".join(dst_data)
		except Exception, e:
			return ""

class BarcodeDataReader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try: return arg0.encode(sys.getdefaultencoding()).encode("hex").upper()
		except Exception, e:
			return "00"
	def dat_to_csv(self, arg0, arg1, arg2):
		try: return arg0.decode("hex").decode(sys.getdefaultencoding())
		except Exception, e:
			return ""
	def dat_to_cell(self, arg0, arg1, arg2):
		return self.dat_to_csv(arg0, arg1, arg2)
	def cell_to_dat(self, arg0, arg1, arg2):
		return self.csv_to_dat(arg0, arg1, arg2)

class BINReader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		if isinstance(arg0, str):
			arg0 = self.cell_to_csv(arg0, arg1, arg2)
		#dst_hexs = [ hex(int(byte, 2))[2:].upper().rjust(2, '0') for byte in arg0.split(' ') ]
		dst_hexs = [ common.bin2hex(byte) for byte in arg0.split(' ') ]
		if len(dst_hexs) != len(arg2["detail"]): raise Exception("Wrong Data")
		return "".join(dst_hexs)

	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, list):
			return arg0
		if not arg0:
			return arg0

		dst_ints = [ common.bin2int(byte) for byte in arg0.split(' ') ]
		field_detail = arg2["detail"]
		byte_count = len(field_detail)
		dst_jsons = []
		#if not dst_ints: return dst_jsons
		if len(dst_ints) != byte_count: raise Exception("Wrong Data")
		for indx, detail in enumerate(field_detail):
			dst_json_line = {}
			for detail_name, detail_value in detail.items():
				if dst_ints[indx] & (1 << detail_value) != 0:
					dst_json_line[detail_name] = 1
				else:
					dst_json_line[detail_name] = 0
			dst_jsons.append(dst_json_line)

		return dst_jsons

	def dat_to_csv(self, arg0, arg1, arg2):
		hex_data = arg0.decode("hex")
		if len(hex_data) != len(arg2["detail"]):
			raise Exception("Wrong Data")
	
		entire_val = []
		for indx, detail in enumerate(arg2["detail"]):
			item = {}
			byte = ord(hex_data[indx])
			for key, val in detail.items():
				res = byte & (1 << val) != 0
				if res : item[key] = 1
				else: item[key] = 0
			entire_val.append(item)

		dst_bytes = [0] * len(arg2["detail"])
		for indx, detail in enumerate(arg2["detail"]):
			for detail_key, detail_value in detail.items():
				if entire_val[indx][detail_key] == 1:
					dst_bytes[indx] |= 1 << detail_value
		dst_data = " ".join([ "{0:b}".format(dst_byte).rjust(8,'0') for dst_byte in dst_bytes ])

		return dst_data

	def dat_to_cell(self, arg0, arg1, arg2):
		csv_data = self.dat_to_csv(arg0, arg1, arg2)
		return self.csv_to_cell(csv_data, arg1, arg2)

	def cell_to_csv(self, arg0, arg1, arg2):
		json_value = arg0
		dst_bytes = [0] * len(arg2["detail"])

		for indx, detail in enumerate(arg2["detail"]):
			for detail_key, detail_value in detail.items():
				if json_value[indx][detail_key] == 1:
					dst_bytes[indx] |= 1 << detail_value

		dst_data = " ".join([ "{0:08b}".format(dest_byte) for dest_byte in dst_bytes ])

		return dst_data

	def cell_to_dat(self, arg0, arg1, arg2):
		json_value = arg0
		dst_bytes = [0] * len(arg2["detail"])
		try:
			for indx, detail in enumerate(arg2["detail"]):
				for detail_key, detail_value in detail.items():
					if json_value[indx][detail_key] == 1:
						dst_bytes[indx] |= 1 << detail_value
	
			dst_data = "".join([ "{0:02X}".format(dest_byte) for dest_byte in dst_bytes ])
			return dst_data
		except:
			dst_data = "".join([ "{0:02X}".format(dest_byte) for dest_byte in dst_bytes ])
			return dst_data

		
class EANReader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			dst_data = []
			line = csv.reader(StringIO.StringIO(arg0)).next()
			#ean
			dst_data.append(line[0].ljust(10, '0'))
			#type
			if line[1] == "EAN":
				dst_data.append('0')
			else:
				dst_data.append('9')
	
			#last byte
			dst_data.append( line[2] ) 
			return "".join(dst_data)
		except:
			return "00000000000000"

		
	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, dict):
			return arg0
		#dst_data = []
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			return {
				"ean_data": line[0],
				"type":     line[1],
				"last_byte":line[2],
			}
		except Exception, e:
			return {
				"ean_data": "",
				"type":     "EAN",
				"last_byte":0,
			}

	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			ean_data = arg0[:10]
			if arg0[10] == '9':
				typ = "ITF"
			else:
				typ = "EAN"
			last_byte     = int(arg0[11])
			return {
				"ean_data":   ean_data,
				"type":       typ,
				"last_byte":  last_byte,
			}
		except Exception, e:
			return {
				"ean_data":   "",
				"type":       "EAN",
				"last_byte":  0,
			}

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			ean_data = arg0[:10]
			if arg0[10] == '9':
				typ = "ITF"
			else:
				typ = "EAN"
			last_byte     = int(arg0[11])
	
			return ",".join([str(val) for val in [ean_data, typ, last_byte]])
		except Exception, e:
			return ""

	def cell_to_csv(self, arg0, arg1, arg2):
		if not isinstance(arg0, dict):
			return arg0
		try:
			return ",".join([str(val) for val in [arg0["ean_data"], arg0["type"], arg0["last_byte"]]])
		except Exception, e:
			return ""

	def cell_to_dat(self, arg0, arg1, arg2):
		csv_data = self.cell_to_csv(arg0, arg1, arg2)
		return self.csv_to_dat(csv_data, arg1, arg2)


class MultiBarcodeReader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			dst_data = []
			line = csv.reader(StringIO.StringIO(arg0)).next()
			#dst_data.append( hex(int(line[0]))[2:].upper().rjust(2, '0') )
			dst_data.append( common.int2hex(int(line[0])) )
			dst_data.append( line[1].encode("hex").upper().ljust(arg1 - 2 * 2, '0') )
			dst_data.append( line[2].rjust(2, '0') )
	
			return "".join(dst_data)
		except Exception, e:
			return "0" * arg1

	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, dict):
			return arg0
		dst_data = []
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			return {
				"fnc1": line[0],
				"data": line[1],
				"code": line[2]
			}
		except Exception, e:
			return {
				"fnc1": 86,
				"data": "",
				"code": 2
			}

	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			fnc1 = common.hex2int(arg0[:2])
			data = arg0[2:100].decode('hex').rstrip('\x00')
			code = common.hex2int(arg0[-2:])
	
			return {
				"fnc1": fnc1,
				"data": data,
				"code": code
			}
		except Exception, e:
			return {
				"fnc1": 86,
				"data": "",
				"code": 2
			}

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			fnc1 = common.hex2int(arg0[:2])
			data = arg0[2:100].decode('hex').rstrip('\x00')
			code = common.hex2int(arg0[-2:])
			return ",".join([ str(fnc1), "\"" + data + "\"", str(code) ])
		except Exception, e:
			return ""

	def cell_to_csv(self, arg0, arg1, arg2):
		if not isinstance(arg0, dict):
			return ""
		try:
			return ",".join([ str(arg0["fnc1"]), "\"" + arg0["data"] + "\"", str(arg0["code"]) ])
		except Exception, e:
			return ""

	def cell_to_dat(self, arg0, arg1, arg2):
		try:
			csv_data = self.cell_to_csv(arg0, arg1, arg2)
			return self.csv_to_dat(csv_data, arg1, arg2)
		except:
			return "0" * arg1


class N1Reader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			dst_data = [
				common.int2hex(int(line[0]), 4),
				common.int2hex(int(line[1]), 4),
				common.int2hex(int(line[2]), 4),
				common.int2hex(int(line[3]), 2),
				common.int2hex(int(line[4]), 2),
			]
	
			return "".join(dst_data)
		except Exception, e:
			return "0" * arg1

	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, dict):
			return arg0
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			return {
				"x":         int(line[0]),
				"y":         int(line[1]),
				"status":    int(line[2]),
				"char_size": int(line[3]),
				"digit_num": int(line[4]),
			}
		except Exception, e:
			return {
				"x":         0,
				"y":         0,
				"status":    0,
				"char_size": 0,
				"digit_num": 0,
			}

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			x         = common.hex2int(arg0[:4])
			y         = common.hex2int(arg0[4:8])
			stat      = common.hex2int(arg0[8:12])
			char_size = common.hex2int(arg0[12:14])
			digit_num = common.hex2int(arg0[14:16])
			return ",".join([ str(val) for val in [x,y,stat,char_size,digit_num] ])
		except Exception, e:
			return ""

	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			x         = common.hex2int(arg0[:4])
			y         = common.hex2int(arg0[4:8])
			stat      = common.hex2int(arg0[8:12])
			char_size = common.hex2int(arg0[12:14])
			digit_num = common.hex2int(arg0[14:16])
			return  {
				"x": x,
				"y": y,
				"status": stat,
				"char_size": char_size,
				"digit_num": digit_num
			}
		except Exception, e:
			return  {
				"x": 0,
				"y": 0,
				"status": 0,
				"char_size": 0,
				"digit_num": 0,
			}

	def cell_to_csv(self, arg0, arg1, arg2):
		if not arg0: return arg0
		try:
			retval = ",".join(
				[str(val) for val in 
					[
						arg0["x"],
						arg0["y"],
						arg0["status"],
						arg0.get("char_size", 0),
						arg0.get("digit_num", 0),
					]
				])
			return retval
		except Exception, e:
			return ""

	def cell_to_dat(self, arg0, arg1, arg2):
		try:
			csv_data = self.cell_to_csv(arg0, arg1, arg2)
			return self.csv_to_dat(csv_data, arg1, arg2)
		except Exception, e:
			return "0" * arg1

	
class B1Reader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			dst_data = [
				common.int2hex(int(line[0]), 4),
				common.int2hex(int(line[1]), 4),
				common.int2hex(int(line[2]), 4),
				common.int2hex(int(line[3]), 4),
				common.int2hex(int(line[4]), 4),
				common.int2hex(int(line[5]), 4),
			]
			return "".join(dst_data)
		except Exception, e:
			return "0" * arg1

	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, dict):
			return arg0
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			return {
				"x":         int(line[0]),
				"y":         int(line[1]),
				"status":    int(line[2]),
				"h":         int(line[3]),
				"w":         int(line[4]),
				"status2":   int(line[5]),
			}
		except Exception, e:
			return {
				"x":         0, 
				"y":         0,
				"status":    0,
				"h":         0,
				"w":         0,
				"status2":   0,
			}

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			x     = common.hex2int(arg0[:4])
			y     = common.hex2int(arg0[4:8])
			stat  = common.hex2int(arg0[8:12])
			h     = common.hex2int(arg0[12:16])
			w     = common.hex2int(arg0[16:20])
			stat2 = common.hex2int(arg0[20:24])

			return ",".join([str(val) for val in [x,y,stat,h,w,stat2]])
		except Exception, e:
			return ""


	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			x     = common.hex2int(arg0[:4])
			y     = common.hex2int(arg0[4:8])
			stat  = common.hex2int(arg0[8:12])
			h     = common.hex2int(arg0[12:16])
			w     = common.hex2int(arg0[16:20])
			stat2 = common.hex2int(arg0[20:24])

			return {
				"x": x,
				"y": y,
				"status": stat,
				"h": h,
				"w": w,
				"status2": stat2,
			}
		except Exception, e:
			return {
				"x": 0,
				"y": 0,
				"status": 0,
				"h": 0,
				"w": 0,
				"status2": 0,
			}

	def cell_to_csv(self, arg0, arg1, arg2):
		if not arg0: return arg0
		try:
			return ",".join(
				[str(val) for val in 
					[
						arg0["x"],
						arg0["y"],
						arg0["status"],
						arg0["w"],
						arg0["h"],
						arg0.get("status2", 0)
					]
				])
		except Exception, e:
			return ""


	def cell_to_dat(self, arg0, arg1, arg2):
		try:
			csv_data = self.cell_to_csv(arg0, arg1, arg2)
			return self.csv_to_dat(csv_data, arg1, arg2)
		except Exception, e:
			return "0" * arg1
		

class B2Reader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			dst_data = [
				common.int2hex(int(line[0]), 4),
				common.int2hex(int(line[1]), 4),
				common.int2hex(int(line[2]), 4),
				common.int2hex(int(line[3]), 4),
				common.int2hex(int(line[4]), 4),
				common.int2hex(int(line[5]), 4),
			]
			return "".join(dst_data)
		except Exception, e:
			return "0" * arg1

	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, dict):
			return arg0
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			return {
				"x":         int(line[0]),
				"y":         int(line[1]),
				"status":    int(line[2]),
				"h":         int(line[3]),
				"w":         int(line[4]),
				"logo_size": int(line[5]),
			}
		except Exception, e:
			return {
				"x":         0,
				"y":         0,
				"status":    0,
				"h":         0,
				"w":         0,
				"logo_size": 0,
			}

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			x         = common.hex2int(arg0[:4])
			y         = common.hex2int(arg0[4:8])
			stat      = common.hex2int(arg0[8:12])
			h         = common.hex2int(arg0[12:16])
			w         = common.hex2int(arg0[16:20])
			logo_size = common.hex2int(arg0[20:24])

			return ",".join([str(val) for val in [x,y,stat,h,w,logo_size]])
		except Exception, e:
			return ""

	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			x         = common.hex2int(arg0[:4])
			y         = common.hex2int(arg0[4:8])
			stat      = common.hex2int(arg0[8:12])
			h         = common.hex2int(arg0[12:16])
			w         = common.hex2int(arg0[16:20])
			logo_size = common.hex2int(arg0[20:24])

			return {
				"x": x,
				"y": y,
				"status": stat,
				"h": h,
				"w": w,
				"status2": logo_size,
			}
		except Exception, e:
			return {
				"x": 0,
				"y": 0,
				"status": 0,
				"h": 0,
				"w": 0,
				"status2": 0,
			}

	def cell_to_csv(self, arg0, arg1, arg2):
		if not arg0: return arg0
		try:
			return ",".join(
				[str(val) for val in 
					[
						arg0["x"],
						arg0["y"],
						arg0["status"],
						arg0["w"],
						arg0["h"],
						arg0.get("logo_size", 0),
					]
				])
		except Exception, e:
			return ""

	def cell_to_dat(self, arg0, arg1, arg2):
		try:
			csv_data = self.cell_to_csv(arg0, arg1, arg2)
			return self.csv_to_dat(csv_data, arg1, arg2)
		except Exception, e:
			return "0" * arg1


class B3Reader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			dst_data = [
				common.int2hex(int(line[0]), 4),
				common.int2hex(int(line[1]), 4),
				common.int2hex(int(line[2]), 4),
				common.int2hex(int(line[3]), 4),
				common.int2hex(int(line[4]), 4),
				common.int2hex(int(line[5]), 4),
			]
			return "".join(dst_data)
		except Exception, e:
			return "0" * arg1

	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, dict):
			return arg0
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			return {
				"x":         int(line[0]),
				"y":         int(line[1]),
				"status":    int(line[2]),
				"h":         int(line[3]),
				"w":         int(line[4]),
				"thick":     int(line[5]),
			}
		except Exception, e:
			return {
				"x":         0,
				"y":         0,
				"status":    0,
				"h":         0,
				"w":         0,
				"thick":     0,
			}

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			x     = common.hex2int(arg0[:4])
			y     = common.hex2int(arg0[4:8])
			stat  = common.hex2int(arg0[8:12])
			h     = common.hex2int(arg0[12:16])
			w     = common.hex2int(arg0[16:20])
			thick = common.hex2int(arg0[20:24])
	
			return ",".join([str(val) for val in [x,y,stat,h,w,thick]])
		except Exception, e:
			return ""

	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			x     = common.hex2int(arg0[:4])
			y     = common.hex2int(arg0[4:8])
			stat  = common.hex2int(arg0[8:12])
			h     = common.hex2int(arg0[12:16])
			w     = common.hex2int(arg0[16:20])
			thick = common.hex2int(arg0[20:24])
			return {
				"x": x,
				"y": y,
				"status": stat,
				"h": h,
				"w": w,
				"thick": thick,
			}
		except Exception, e:
			return {
				"x": 0,
				"y": 0,
				"status": 0,
				"h": 0,
				"w": 0,
				"thick": 0,
			}

	def cell_to_csv(self, arg0, arg1, arg2):
		if not arg0: return arg0
		try:
			return ",".join(
				[str(val) for val in
					[
						arg0["x"],
						arg0["y"],
						arg0["status"],
						arg0["w"],
						arg0["h"],
						arg0.get("thick", 0),
					]
				])
		except Exception, e:
			return ""

	def cell_to_dat(self, arg0, arg1, arg2):
		try:
			csv_data = self.cell_to_csv(arg0, arg1, arg2)
			return self.csv_to_dat(csv_data, arg1, arg2)
		except Exception, e:
			return "0" * arg1

class B4Reader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			dst_data = [
				common.int2hex(int(line[0]), 4),
				common.int2hex(int(line[1]), 4),
				common.int2hex(int(line[2]), 4),
				common.int2hex(int(line[3]), 4),
				common.int2hex(int(line[4]), 4),
				line[5].upper().rjust(4,'0'),
			]
			return "".join(dst_data)
		except Exception, e:
			return "0" * arg1

	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, dict):
			return arg0
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			return {
				"x":         int(line[0]),
				"y":         int(line[1]),
				"status":    int(line[2]),
				"h":         int(line[3]),
				"w":         int(line[4]),
				"image_num": int(line[5]),
			}
		except Exception, e:
			return {
				"x":         0,
				"y":         0,
				"status":    0,
				"h":         0,
				"w":         0,
				"image_num": 0,
			}

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			x         = common.hex2int(arg0[:4])
			y         = common.hex2int(arg0[4:8])
			stat      = common.hex2int(arg0[8:12])
			h         = common.hex2int(arg0[12:16])
			w         = common.hex2int(arg0[16:20])
			image_num = common.hex2int(arg0[20:24])
			return ",".join([str(val) for val in [x,y,stat,h,w,image_num]])
		except Exception, e:
			return ""

	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			x         = common.hex2int(arg0[:4])
			y         = common.hex2int(arg0[4:8])
			stat      = common.hex2int(arg0[8:12])
			h         = common.hex2int(arg0[12:16])
			w         = common.hex2int(arg0[16:20])
			image_num = common.hex2int(arg0[20:24])
			return {
				"x": x,
				"y": y,
				"status": stat,
				"h": h,
				"w": w,
				"image_num": image_num,
			}
		except Exception, e:
			return {
				"x": 0,
				"y": 0,
				"status": 0,
				"h": 0,
				"w": 0,
				"image_num": 0,
			}

	def cell_to_csv(self, arg0, arg1, arg2):
		if not arg0: return arg0
		try:
			return ",".join(
				[str(val) for val in 
					[
						arg0["x"],
						arg0["y"],
						arg0["status"],
						arg0["w"],
						arg0["h"],
						arg0.get("image_num", 0),
					]
				])
		except Exception, e:
			return ""

	def cell_to_dat(self, arg0, arg1, arg2):
		try:
			csv_data = self.cell_to_csv(arg0, arg1, arg2)
			return self.csv_to_dat(csv_data, arg1, arg2)
		except Exception, e:
			return "0" * arg1
		
class B5Reader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			dst_data = [
				common.int2hex(int(line[0]), 4),
				common.int2hex(int(line[1]), 4),
				common.int2hex(int(line[2]), 4),
				common.int2hex(int(line[3]), 4),
				common.int2hex(int(line[4]), 4),
				common.int2hex(int(line[5]), 2),
				common.int2hex(int(line[6]), 2),
			]
			return "".join(dst_data)
		except Exception, e:
			return "0" * arg1

	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, dict):
			return arg0
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			return {
				"x":         int(line[0]),
				"y":         int(line[1]),
				"status":    int(line[2]),
				"h":         int(line[3]),
				"w":         int(line[4]),
				"status2":   int(line[5]),
				"digit_num": int(line[6]),
			}
		except Exception, e:
			return {
				"x":         0,
				"y":         0,
				"status":    0,
				"h":         0,
				"w":         0,
				"status2":   0,
				"digit_num": 0,
			}

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			x           = common.hex2int(arg0[:4])
			y           = common.hex2int(arg0[4:8])
			stat        = common.hex2int(arg0[8:12])
			h           = common.hex2int(arg0[12:16])
			w           = common.hex2int(arg0[16:20])
			stat2       = common.hex2int(arg0[20:22])
			digit_num   = common.hex2int(arg0[22:24])
			return ",".join([str(val) for val in [x,y,stat,h,w,stat2,digit_num]])
		except Exception, e:
			return ""

	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			x           = common.hex2int(arg0[:4])
			y           = common.hex2int(arg0[4:8])
			stat        = common.hex2int(arg0[8:12])
			h           = common.hex2int(arg0[12:16])
			w           = common.hex2int(arg0[16:20])
			stat2       = common.hex2int(arg0[20:22])
			digit_num   = common.hex2int(arg0[22:24])
	
			return {
				"x": x,
				"y": y,
				"status": stat,
				"h": h,
				"w": w,
				"status2": stat2,
				"digit_num": digit_num,
			}
		except Exception, e:
			return {
				"x": 0,
				"y": 0,
				"status": 0,
				"h": 0,
				"w": 0,
				"status2": 0,
				"digit_num": 0,
			}

	def cell_to_csv(self, arg0, arg1, arg2):
		if not arg0: return arg0
		try:
			return ",".join(
				[str(val) for val in 
					[
						arg0["x"],
						arg0["y"],
						arg0["status"],
						arg0["w"],
						arg0["h"],
						arg0.get("status2", 0),
						arg0.get("digit_num", 0),
					]
				])
		except Exception, e:
			return ""

	def cell_to_dat(self, arg0, arg1, arg2):
		try:
			csv_data = self.cell_to_csv(arg0, arg1, arg2)
			return self.csv_to_dat(csv_data, arg1, arg2)
		except Exception, e:
			return "0" * arg1

class C1Reader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			dst_data = [
				common.int2hex(int(line[0]), 4),
				common.int2hex(int(line[1]), 4),
				common.int2hex(int(line[2]), 4),
				common.int2hex(int(line[3]), 4),
				common.int2hex(int(line[4]), 4),
				common.int2hex(int(line[5]), 2),
				common.int2hex(int(line[6]), 2),
				common.int2hex(int(line[7]), 2),
				common.int2hex(int(line[8]), 2),
			]
	
			return "".join(dst_data)
		except Exception, e:
			return "0" * arg1

	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, dict):
			return arg0
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			return {
				"x":            int(line[0]),
				"y":            int(line[1]),
				"status":       int(line[2]),
				"h":            int(line[3]),
				"w":            int(line[4]),
				"char_size1":   int(line[5]),
				"char_size2":   int(line[6]),
				"char_size3":   int(line[7]),
				"char_size4":   int(line[8]),
			}
		except Exception, e:
			return {
				"x":            0,
				"y":            0,
				"status":       0,
				"h":            0,
				"w":            0,
				"char_size1":   0,
				"char_size2":   0,
				"char_size3":   0,
				"char_size4":   0,
			}

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			x          = common.hex2int(arg0[:4])
			y          = common.hex2int(arg0[4:8])
			stat       = common.hex2int(arg0[8:12])
			h          = common.hex2int(arg0[12:16])
			w          = common.hex2int(arg0[16:20])
			char_size1 = common.hex2int(arg0[20:22])
			char_size2 = common.hex2int(arg0[22:24])
			char_size3 = common.hex2int(arg0[24:26])
			char_size4 = common.hex2int(arg0[26:28])
			return ",".join([str(val) for val in [x,y,stat,h,w,char_size1,char_size2,char_size3,char_size4]])
		except Exception, e:
			return ""

	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			x          = common.hex2int(arg0[:4])
			y          = common.hex2int(arg0[4:8])
			stat       = common.hex2int(arg0[8:12])
			h          = common.hex2int(arg0[12:16])
			w          = common.hex2int(arg0[16:20])
			char_size1 = common.hex2int(arg0[20:22])
			char_size2 = common.hex2int(arg0[22:24])
			char_size3 = common.hex2int(arg0[24:26])
			char_size4 = common.hex2int(arg0[26:28])
	
			return {
				"x": x,
				"y": y,
				"status": stat,
				"h": h,
				"w": w,
				"char_size1": char_size1,
				"char_size2": char_size2,
				"char_size3": char_size3,
				"char_size4": char_size4,
			}
		except Exception, e:
			return {
				"x": 0,
				"y": 0,
				"status": 0,
				"h": 0,
				"w": 0,
				"char_size1": 0,
				"char_size2": 0,
				"char_size3": 0,
				"char_size4": 0,
			}

	def cell_to_csv(self, arg0, arg1, arg2):
		if not arg0: return arg0
		try:
			return ",".join(
				[str(val) for val in 
					[
						arg0["x"],
						arg0["y"],
						arg0["status"],
						arg0["w"],
						arg0["h"],
						arg0.get("char_size1", 0),
						arg0.get("char_size2", 0),
						arg0.get("char_size3", 0),
						arg0.get("char_size4", 0),
					]
				])
		except Exception, e:
			return ""

	def cell_to_dat(self, arg0, arg1, arg2):
		try:
			csv_data = self.cell_to_csv(arg0, arg1, arg2)
			return self.csv_to_dat(csv_data, arg1, arg2)
		except Exception, e:
			return "0" * arg1

class C2Reader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			dst_data = [
				common.int2hex(int(line[0]), 4),
				common.int2hex(int(line[1]), 4),
				common.int2hex(int(line[2]), 4),
				common.int2hex(int(line[3]), 4),
				common.int2hex(int(line[4]), 4),
				common.int2hex(int(line[5]), 2),
				line[6].upper().rjust(2,'0'),
			]
			return "".join(dst_data)
		except Exception, e:
			return "0" * arg1

	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, dict):
			return arg0
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			return {
				"x":            int(line[0]),
				"y":            int(line[1]),
				"status":       int(line[2]),
				"h":            int(line[3]),
				"w":            int(line[4]),
				"char_size1":   int(line[5]),
				"char_size2":   int(line[6]),
			}
		except Exception, e:
			return {
				"x":            0,
				"y":            0,
				"status":       0,
				"h":            0,
				"w":            0,
				"char_size1":   0,
				"char_size2":   0,
			}

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			x          = common.hex2int(arg0[:4])
			y          = common.hex2int(arg0[4:8])
			stat       = common.hex2int(arg0[8:12])
			h          = common.hex2int(arg0[12:16])
			w          = common.hex2int(arg0[16:20])
			char_size1 = common.hex2int(arg0[20:22])
			char_size2 = int(arg0[22:24])
			return ",".join([str(val) for val in [x,y,stat,h,w,char_size1,char_size2]])
		except Exception, e:
			return ""

	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			x          = common.hex2int(arg0[:4])
			y          = common.hex2int(arg0[4:8])
			stat       = common.hex2int(arg0[8:12])
			h          = common.hex2int(arg0[12:16])
			w          = common.hex2int(arg0[16:20])
			char_size1 = common.hex2int(arg0[20:22])
			char_size2 = int(arg0[22:24])
			return {
				"x": x,
				"y": y,
				"status": stat,
				"h": h,
				"w": w,
				"char_size1": char_size1,
				"char_size2": char_size2,
			}
		except Exception, e:
			return {
				"x": 0,
				"y": 0,
				"status": 0,
				"h": 0,
				"w": 0,
				"char_size1": 0,
				"char_size2": 0,
			}

	def cell_to_csv(self, arg0, arg1, arg2):
		if not arg0: return arg0
		try:
			return ",".join(
				[str(val) for val in 
					[
						arg0["x"],
						arg0["y"],
						arg0["status"],
						arg0["w"],
						arg0["h"],
						arg0.get("char_size1", 0),
						arg0.get("char_size2", 0),
					]
				])
		except Exception, e:
			return ""

	def cell_to_dat(self, arg0, arg1, arg2):
		try:
			csv_data = self.cell_to_csv(arg0, arg1, arg2)
			return self.csv_to_dat(csv_data, arg1, arg2)
		except Exception, e:
			return "0" * arg1

class C3Reader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			dst_data = [
				common.int2hex(int(line[0]), 4),
				common.int2hex(int(line[1]), 4),
				common.int2hex(int(line[2]), 4),
				common.int2hex(int(line[3]), 4),
				common.int2hex(int(line[4]), 4),
				common.int2hex(int(line[5]), 2),
				common.int2hex(int(line[6]), 2),
				common.int2hex(int(line[7]), 2),
				common.int2hex(int(line[8]), 2),
				common.int2hex(int(line[9]), 2),
				common.int2hex(int(line[10]), 2),
				common.int2hex(int(line[11]), 2),
				common.int2hex(int(line[12]), 2),
				common.int2hex(int(line[13]), 2),
				common.int2hex(int(line[14]), 2),
				common.int2hex(int(line[15]), 2),
				common.int2hex(int(line[16]), 2),
				common.int2hex(int(line[17]), 2),
				common.int2hex(int(line[18]), 2),
				common.int2hex(int(line[19]), 2),
				common.int2hex(int(line[20]), 2),
			]
			return "".join(dst_data)
		except Exception, e:
			return "0" * arg1
		
	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, dict):
			return arg0
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			return {
				"x":            int(line[0]),
				"y":            int(line[1]),
				"status":       int(line[2]),
				"h":            int(line[3]),
				"w":            int(line[4]),
				"char_size1":   int(line[5]),
				"char_size2":   int(line[6]),
				"char_size3":   int(line[7]),
				"char_size4":   int(line[8]),
				"char_size5":   int(line[9]),
				"char_size6":   int(line[10]),
				"char_size7":   int(line[11]),
				"char_size8":   int(line[12]),
				"char_size9":   int(line[13]),
				"char_size10":  int(line[14]),
				"char_size11":  int(line[15]),
				"char_size12":  int(line[16]),
				"char_size13":  int(line[17]),
				"char_size14":  int(line[18]),
				"char_size15":  int(line[19]),
				"dummy":        int(line[20]),
			}
		except Exception, e:
			return {
				"x":            0,
				"y":            0,
				"status":       0,
				"h":            0,
				"w":            0,
				"char_size1":   0,
				"char_size2":   0,
				"char_size3":   0,
				"char_size4":   0,
				"char_size5":   0,
				"char_size6":   0,
				"char_size7":   0,
				"char_size8":   0,
				"char_size9":   0,
				"char_size10":  0,
				"char_size11":  0,
				"char_size12":  0,
				"char_size13":  0,
				"char_size14":  0,
				"char_size15":  0,
				"dummy":        0,
			}

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			x           = common.hex2int(arg0[:4])
			y           = common.hex2int(arg0[4:8])
			stat        = common.hex2int(arg0[8:12])
			h           = common.hex2int(arg0[12:16])
			w           = common.hex2int(arg0[16:20])
			char_size1  = common.hex2int(arg0[20:22])
			char_size2  = common.hex2int(arg0[22:24])
			char_size3  = common.hex2int(arg0[24:26])
			char_size4  = common.hex2int(arg0[26:28])
			char_size5  = common.hex2int(arg0[28:30])
			char_size6  = common.hex2int(arg0[30:32])
			char_size7  = common.hex2int(arg0[32:34])
			char_size8  = common.hex2int(arg0[34:36])
			char_size9  = common.hex2int(arg0[36:38])
			char_size10 = common.hex2int(arg0[38:40])
			char_size11 = common.hex2int(arg0[40:42])
			char_size12 = common.hex2int(arg0[42:44])
			char_size13 = common.hex2int(arg0[44:46])
			char_size14 = common.hex2int(arg0[46:48])
			char_size15 = common.hex2int(arg0[48:50])
			dummy       = common.hex2int(arg0[50:52])
			retval = ",".join([str(val) for val in [ 
				x,y,stat,h,w,
				char_size1,
				char_size2,
				char_size3,
				char_size4,
				char_size5,
				char_size6,
				char_size7,
				char_size8,
				char_size9,
				char_size10,
				char_size11,
				char_size12,
				char_size13,
				char_size14,
				char_size15,
				dummy,
				]])
			return retval
		except Exception, e:
			return ""

	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			x           = common.hex2int(arg0[:4])
			y           = common.hex2int(arg0[4:8])
			stat        = common.hex2int(arg0[8:12])
			h           = common.hex2int(arg0[12:16])
			w           = common.hex2int(arg0[16:20])
			char_size1  = common.hex2int(arg0[20:22])
			char_size2  = common.hex2int(arg0[22:24])
			char_size3  = common.hex2int(arg0[24:26])
			char_size4  = common.hex2int(arg0[26:28])
			char_size5  = common.hex2int(arg0[28:30])
			char_size6  = common.hex2int(arg0[30:32])
			char_size7  = common.hex2int(arg0[32:34])
			char_size8  = common.hex2int(arg0[34:36])
			char_size9  = common.hex2int(arg0[36:38])
			char_size10 = common.hex2int(arg0[38:40])
			char_size11 = common.hex2int(arg0[40:42])
			char_size12 = common.hex2int(arg0[42:44])
			char_size13 = common.hex2int(arg0[44:46])
			char_size14 = common.hex2int(arg0[46:48])
			char_size15 = common.hex2int(arg0[48:50])
			dummy       = common.hex2int(arg0[50:52])

			return {
				"x": x,
				"y": y,
				"status": stat,
				"h": h,
				"w": w,
				"char_size1":  char_size1,
				"char_size2":  char_size2,
				"char_size3":  char_size3,
				"char_size4":  char_size4,
				"char_size5":  char_size5,
				"char_size6":  char_size6,
				"char_size7":  char_size7,
				"char_size8":  char_size8,
				"char_size9":  char_size9,
				"char_size10": char_size10,
				"char_size11": char_size11,
				"char_size12": char_size12,
				"char_size13": char_size13,
				"char_size14": char_size14,
				"char_size15": char_size15,
				"dummy":       dummy,
			}
		except Exception, e:
			return {
				"x": 0,
				"y": 0,
				"status": 0,
				"h": 0,
				"w": 0,
				"char_size1":  0,
				"char_size2":  0,
				"char_size3":  0,
				"char_size4":  0,
				"char_size5":  0,
				"char_size6":  0,
				"char_size7":  0,
				"char_size8":  0,
				"char_size9":  0,
				"char_size10": 0,
				"char_size11": 0,
				"char_size12": 0,
				"char_size13": 0,
				"char_size14": 0,
				"char_size15": 0,
				"dummy":       0,
			}

	def cell_to_csv(self, arg0, arg1, arg2):
		if not arg0: return arg0
		try:
			return ",".join(
				[str(val) for val in [
						arg0["x"],
						arg0["y"],
						arg0["status"],
						arg0["w"],
						arg0["h"],
						arg0.get("char_size1", 0),
						arg0.get("char_size2", 0),
						arg0.get("char_size3", 0),
						arg0.get("char_size4", 0),
						arg0.get("char_size5", 0),
						arg0.get("char_size6", 0),
						arg0.get("char_size7", 0),
						arg0.get("char_size8", 0),
						arg0.get("char_size9", 0),
						arg0.get("char_size10", 0),
						arg0.get("char_size11", 0),
						arg0.get("char_size12", 0),
						arg0.get("char_size13", 0),
						arg0.get("char_size14", 0),
						arg0.get("char_size15", 0),
						arg0.get("dummy", 0),
					]
				])
		except Exception, e:
			return ""
	
	def cell_to_dat(self, arg0, arg1, arg2):
		try:
			csv_data = self.cell_to_csv(arg0, arg1, arg2)
			return self.csv_to_dat(csv_data, arg1, arg2)
		except Exception, e:
			return "0" * arg1
		
class C4Reader(TWSReader):
	def csv_to_dat(self, arg0, arg1, arg2):
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			dst_data = [
				common.int2hex(int(line[0]), 4),
				common.int2hex(int(line[1]), 4),
				common.int2hex(int(line[2]), 4),
				common.int2hex(int(line[3]), 4),
				common.int2hex(int(line[4]), 4),
				common.int2hex(int(line[5]), 2),
				common.int2hex(int(line[6]), 2),
				common.int2hex(int(line[7]), 2),
				common.int2hex(int(line[8]), 2),
				common.int2hex(int(line[9]), 2),
				common.int2hex(int(line[10]), 2),
				common.int2hex(int(line[11]), 2),
				common.int2hex(int(line[12]), 2),
			]
			return "".join(dst_data)
		except Exception, e:
			return "0" * arg1
		
	def csv_to_cell(self, arg0, arg1, arg2):
		if isinstance(arg0, dict):
			return arg0
		try:
			line = csv.reader(StringIO.StringIO(arg0)).next()
			return {
				"x":         int(line[0]),
				"y":         int(line[1]),
				"status":    int(line[2]),
				"h":         int(line[3]),
				"w":         int(line[4]),
				"char_size1":int(line[5]),
				"char_size2":int(line[6]),
				"char_size3":int(line[7]),
				"char_size4":int(line[8]),
				"char_size5":int(line[9]),
				"char_size6":int(line[10]),
				"char_size7":int(line[11]),
				"char_size8":int(line[12]),
			}
		except Exception, e:
			return {
				"x":         0,
				"y":         0,
				"status":    0,
				"h":         0,
				"w":         0,
				"char_size1":0,
				"char_size2":0,
				"char_size3":0,
				"char_size4":0,
				"char_size5":0,
				"char_size6":0,
				"char_size7":0,
				"char_size8":0,
			}

	def dat_to_csv(self, arg0, arg1, arg2):
		try:
			x           = common.hex2int(arg0[:4])
			y           = common.hex2int(arg0[4:8])
			stat        = common.hex2int(arg0[8:12])
			h           = common.hex2int(arg0[12:16])
			w           = common.hex2int(arg0[16:20])
			char_size1  = common.hex2int(arg0[20:22])
			char_size2  = common.hex2int(arg0[22:24])
			char_size3  = common.hex2int(arg0[24:26])
			char_size4  = common.hex2int(arg0[26:28])
			char_size5  = common.hex2int(arg0[28:30])
			char_size6  = common.hex2int(arg0[30:32])
			char_size7  = common.hex2int(arg0[32:34])
			char_size8  = common.hex2int(arg0[34:36])
			return ",".join([str(val) for val in [
				x,y,stat,h,w,
				char_size1,
				char_size2,
				char_size3,
				char_size4,
				char_size5,
				char_size6,
				char_size7,
				char_size8,
				]])
		except Exception, e:
			return ""

	def dat_to_cell(self, arg0, arg1, arg2):
		try:
			x           = common.hex2int(arg0[:4])
			y           = common.hex2int(arg0[4:8])
			stat        = common.hex2int(arg0[8:12])
			h           = common.hex2int(arg0[12:16])
			w           = common.hex2int(arg0[16:20])
			char_size1  = common.hex2int(arg0[20:22])
			char_size2  = common.hex2int(arg0[22:24])
			char_size3  = common.hex2int(arg0[24:26])
			char_size4  = common.hex2int(arg0[26:28])
			char_size5  = common.hex2int(arg0[28:30])
			char_size6  = common.hex2int(arg0[30:32])
			char_size7  = common.hex2int(arg0[32:34])
			char_size8  = common.hex2int(arg0[34:36])
			return {
				"x": x,
				"y": y,
				"status": stat,
				"h": h,
				"w": w,
				"char_size1": char_size1,
				"char_size2": char_size2,
				"char_size3": char_size3,
				"char_size4": char_size4,
				"char_size5": char_size5,
				"char_size6": char_size6,
				"char_size7": char_size7,
				"char_size8": char_size8,
			}
		except Exception, e:
			return {
				"x": 0,
				"y": 0,
				"status": 0,
				"h": 0,
				"w": 0,
				"char_size1": 0,
				"char_size2": 0,
				"char_size3": 0,
				"char_size4": 0,
				"char_size5": 0,
				"char_size6": 0,
				"char_size7": 0,
				"char_size8": 0,
			}

	def cell_to_csv(self, arg0, arg1, arg2):
		if not arg0: return arg0
		try:
			return ",".join(
				[str(val) for val in [
						arg0["x"],
						arg0["y"],
						arg0["status"],
						arg0["w"],
						arg0["h"],
						arg0.get("char_size1", 0),
						arg0.get("char_size2", 0),
						arg0.get("char_size3", 0),
						arg0.get("char_size4", 0),
						arg0.get("char_size5", 0),
						arg0.get("char_size6", 0),
						arg0.get("char_size7", 0),
						arg0.get("char_size8", 0),
					]
				])
		except Exception, e:
			return ""

	def cell_to_dat(self, arg0, arg1, arg2):
		try:
			csv_data = self.cell_to_csv(arg0, arg1, arg2)
			return self.csv_to_dat(csv_data, arg1, arg2)
		except Exception, e:
			return "0" * arg1


call_list = {
	"BCD":          lambda: BCDReader(),
	"F1F2":         lambda: F1F2Reader(),
	"EAN":          lambda: EANReader(),
	"HEX":          lambda: HEXReader(),
	"MULTIBARCODE": lambda: MultiBarcodeReader(),
	"BIN":          lambda: BINReader(),
	"ASCII":        lambda: ASCIIReader(),
	"BARCODEDATA":  lambda: BarcodeDataReader(),
	"BYTES":        lambda: BYTESReader(),
	"B1":           lambda: B1Reader(),
	"B2":           lambda: B2Reader(),
	"B3":           lambda: B3Reader(),
	"B4":           lambda: B4Reader(),
	"B5":           lambda: B5Reader(),
	"C1":           lambda: C1Reader(),
	"C2":           lambda: C2Reader(),
	"C3":           lambda: C3Reader(),
	"C4":           lambda: C4Reader(),
	"N1":           lambda: N1Reader(),
}


class Master:
	
	#DBConnection = common.open_sqlite_db(const.db_name)

	"""	
	def __del__(self):
		try:
			if self.conn:
				self.conn.close()
		except:
			pass
	"""

	def __init__(self, name, file_no, text):
		json_data = common.get_json_from_string(text)
		self.name = name
		self.file_no = file_no
		self.fieldKeys		= []
		self.fields_info    = []
		self.fields_info_dic= {}
		self.record_size_field_index = -1
		types = {
			"ASCII":         "text",
			"BARCODEDATA":   "text",
			"MULTIBARCODE":  "text",
			"EAN":           "text",
			"BCD":           "int",
			"BIN":           "text",
			"BYTES":         "text",
			"F1F2":          "text",
			"HEX":           "int",
			"B1":            "text",
			"B2":            "text",
			"B3":            "text",
			"B4":            "text",
			"B5":            "text",
			"C1":            "text",
			"C2":            "text",
			"C3":            "text",
			"C4":            "text",
			"N1":            "text"
		}
		type_entity = {
			"ASCII":         type(""),
			"BARCODEDATA":   type(""),
			"MULTIBARCODE":  type(""),
			"BCD":           type(0),
			"F1F2":          type(""),
			"BIN":           type(""),
			"BYTES":         type(""),
			"EAN":           type(""),
			"HEX":           type(0),
			"B1":            type(""),
			"B2":            type(""),
			"B3":            type(""),
			"B4":            type(""),
			"B5":            type(""),
			"C1":            type(""),
			"C2":            type(""),
			"C3":            type(""),
			"C4":            type(""),
			"N1":            type("")
		}
		field_text_arr = []
		for column_index, field in enumerate(json_data):
			field_name           = ""
			field_type           = "BYTES"
			field_detail         = {}
			field_visible        = None
			field_printable      = None
			field_related        = ""
			try:
				field_name       = field["Name"]
				field_len        = field["Length"]
				field_type       = field["Type"]
				sql_type         = types[field_type]
				is_record_size   = field.get("IsSize", 0)
				is_disabled      = field.get("Disable", 0)
				if field_type    == "BIN":
					field_detail = field.get("Detail", {})
				field_visible    = field.get("Visible", None)
				field_printable  = field.get("Printable", None)
				field_related    = field.get("Related", "")

			except Exception, e:
				common.log_err( traceback.format_exc() )
				return None


			if is_record_size == 1:
				self.record_size_field_index = column_index
		
			#primary key
			if field.get("Key", 0) == 1:
				self.fieldKeys.append(field_name)

			create_field = [field_name, sql_type]
			if field_name in self.fieldKeys:
				create_field.append("primary key")
			field_text_arr.append(" ".join(create_field))

			self.fields_info.append(
				{
					"index":      column_index,
					"len":        field_len,
					"name":       field_name,
					"type":       field_type,
					"instcreator":type_entity[field_type],
					"disable":    is_disabled,
					"detail":     field_detail,
					"visible":    field_visible,
					"printable":  field_printable,
					"related":    field_related,
				})

			self.fields_info_dic[field_name] = self.fields_info[-1]

		#self.conn = common.open_sqlite_db(const.db_name)
		#self.conn = Master.DBConnection
		self.conn = common.open_sqlite_db(const.db_name)
		#cursor = self.conn.cursor()

		#field_text = [ f["text"] for f in self.fields_info ]
		self.conn.execute("DROP TABLE IF EXISTS %s" % self.name)	#does not work when multiple call
		self.conn.execute("CREATE TABLE IF NOT EXISTS %s ( %s )" % (
				self.name, ",".join(field_text_arr)
			)
		)

	def create_row(self):
		dic_list = {}
		#print "fieldsinfo:", self.fields_info
		for i, field_info in enumerate(self.fields_info):
			#val_list.append(field_info["type"]())
			curNode = [ field_info["instcreator"]() ]
			dic_list[i + 1] = dic_list[field_info["name"]] = curNode
			#dic_list[i + 1] = dic_list[field_info["name"]] = [None]
			#val_list.append( {field_info["name"]: field_info["type"]()} )
		#return val_list
		return dic_list

	def import_line(self, new_row, is_struct = False, sync_status_bytes = True):
		try:
			#if not is_struct:
			#	self.conv_csv_to_cell(new_row, force_create = True)
			self.conv_csv_to_cell(new_row, force_create = True)


			fields_value = []
			fields_name  = []


			if sync_status_bytes:
				for field_info in reversed(self.fields_info):
					if field_info["disable"] == 1:
						continue
	
					field_name           = field_info["name"]
					field_visible        = field_info["visible"]
					field_printable      = field_info["printable"]
					field_type           = field_info["type"]
					field_value          = new_row[field_name][0]
	
	
					if field_visible:
						visible_field_name = field_visible["Name"]
						visible_field_byte = field_visible["Byte"]
						visible_field_bit  = field_visible["Bit"]
	
						#visible_field_info = self.fields_info_dic.get(visible_field_name, {})
	
						#print field_name, "depends on", visible_field_name
						#print "field_value:", field_value
	
						#if not new_row[visible_field_name][0]:
						#	new_row[visible_field_name][0] = self.init_status_byte(self.fields_info_dic.get(visible_field_name, {}))
	
						try:
							if field_value:
								new_row[visible_field_name][0][visible_field_byte-1][visible_field_bit] = 1
							else:
								new_row[visible_field_name][0][visible_field_byte-1][visible_field_bit] = 0

							#if field_name == 'LinkedText1No':
								#print "field_value, visible_field_name:", field_value, visible_field_name, visible_field_byte, visible_field_bit
								#print new_row[visible_field_name][0]
						except Exception, e:
							common.log_err( traceback.format_exc() )
	
	
					if field_printable:
						printable_field_name = field_printable["Name"]
						printable_field_byte = field_printable["Byte"]
						printable_field_bit  = field_printable["Bit"]
	
						#if not new_row[printable_field_name][0]:
						#	new_row[printable_field_name][0] = self.init_status_byte(self.fields_info_dic.get(printable_field_name, {}))
	
						#print field_name, "needs", printable_field_name, "to print"
						try:
							if field_value:
								new_row[printable_field_name][0][printable_field_byte-1][printable_field_bit] = 1
							else:
								new_row[printable_field_name][0][printable_field_byte-1][printable_field_bit] = 0
						except Exception, e:
							common.log_err( traceback.format_exc() )


			for field_info in self.fields_info:
				if field_info["disable"] == 1:
					continue

				field_name      = field_info["name"]
				field_visible   = field_info["visible"]
				field_type      = field_info["type"]
				field_length    = field_info["len"]

				#print "c p 10 processing", field_name

				field_value = new_row[field_name][0]
				#if field_type == "ASCII":
				#	print "ascii:", field_name, field_value, field_type
				try:
					#print "field name, field_value:", field_name, "null" if not field_value else field_value, call_list[field_type]().cell_to_csv(field_value, field_length, field_info)
					#print "field_name:", field_name, field_type
					fields_value.append( call_list[field_type]().cell_to_csv(field_value, field_length, field_info) )
				except Exception, e:
					common.log_err( "Field(%s) Error: %s" % (field_name, e) )
				else:
					fields_name.append(field_name)
				
				#print "field name, field_type:", field_name, field_type
				#fields_value.append(field_value)

			sql = "REPLACE INTO %s (%s) VALUES ( %s )" % (
						self.name,
						",".join(fields_name),
						",".join(['?'] * len(fields_value))
					)
					
			#print "fields_name:", fields_name
			#print "fields_value:", fields_value
					
			self.conn.cursor().execute(sql, fields_value)
			self.conn.commit()

			return True
		
		except Exception, e:
			common.log_err( traceback.format_exc() )
			return False
			
		
	def import_dat(self, line):
		new_row = self.create_row()
		#self.conv_csv_to_cell(new_row, force_create = True)
		#print new_row
		#self.conv_csv_to_cell(new_row)

		cur_line_pos = 0
		#print "line:", line
		try:
			fields_value = []
			fields_name = []
			for field_info in self.fields_info:
				if field_info["disable"] == 1:
					continue

				field_name      = field_info["name"]
				field_visible   = field_info["visible"]

				#print "field_name:", field_name

				#是否可见(即开关)
				visible = 0
				if field_visible:
					visible_field_name = field_visible["Name"]
					visible_field_byte = field_visible["Byte"]
					visible_field_bit  = field_visible["Bit"]
					visible_field_info = self.fields_info_dic.get(visible_field_name, {})

					#print field_name,"depends",visible_field_name
					#print "field_value:", new_row[visible_field_name][0]

					#print "name byte bit:", visible_field_name, visible_field_byte, visible_field_bit
					#print "new:", new_row[visible_field_name][0][visible_field_byte-1]
					#try: visible = new_row[visible_field_name][0][visible_field_byte-1][visible_field_bit]
					try:
						cellData = BINReader().csv_to_cell(new_row[visible_field_name][0], visible_field_info["len"] * 2, visible_field_info)
						#print field_name, "depend on", visible_field_name, visible_field_byte, visible_field_bit
						if cellData:
							visible = cellData[visible_field_byte-1][visible_field_bit]
					except Exception, e:
						common.log_err( "Field:%s Visible Field:%s Error: %s" % (field_name, visible_field_name, e) )
						common.log_err( traceback.format_exc() )

					#不可见跳过
					if not visible:
						continue

				fields_name.append(field_name)

				field_type = field_info["type"]
				field_length = field_info["len"] * 2

				#ASCII时到0C为结止
				if field_type == "ASCII":
					#length = line[cur_line_pos:].find("0C") + 2
					length = get_length_of_ascii(line[cur_line_pos:], field_length)
				elif field_type == "BARCODEDATA":
					length = len(line) - cur_line_pos
				else:
					length = field_info["len"] * 2

				cell_data = line[cur_line_pos : cur_line_pos+length]
				cur_line_pos += length
				#print "length, celldata:", length, cell_data

				new_row[field_name][0] = call_list[field_type]().dat_to_csv(cell_data, length, field_info) 
				fields_value.append(new_row[field_name][0])

			#print new_row
			return self.import_line(new_row)
		except Exception, e:
			common.log_err( traceback.format_exc() )
			return False

	def add_row(self, new_row, sync_status_bytes = True):
		return self.import_line(
			new_row,
			is_struct = True,
			sync_status_bytes = sync_status_bytes)
		
	def add_rows(self, dat_file):
		with open(dat_file, "rb") as fp:
			for line in fp.readlines():
				if not self.import_dat(line.rstrip()):
					return False
			self.conn.commit()
		return True

	def clear(self):
		cursor = self.conn.cursor()
		cursor.execute("DELETE FROM %s" % self.name)

	def get_all_keys(self):
		if len(self.fieldKeys) == 0: return []
		cursor = self.conn.cursor()
		sql = "SELECT %s FROM %s" % (self.fieldKeys[0], self.name)
		return [ int(row[0]) for row in cursor.execute(sql) ]
	
	def get_all_data(self, encoding=sys.getdefaultencoding()):
		cursor = self.conn.cursor()

		sql = "SELECT * FROM %s" % self.name
		cursor.execute(sql)
		names = [(index, desc[0]) for index, desc in enumerate(cursor.description)]
		rows = []
		for row in cursor:
			cells = [ cell for cell in row ]
			dic1 = {}; dic2 = {}
			for name in names:
				val = [row[name[0]]]
				dic1[name[1]] = dic2[int(str(name[0]+1))] = val
			dic3=dic1.copy()
			dic3.update(dic2)
			rows.append(dic3)

		for row in rows:
			#status byte转换成Json格式
			self.conv_csv_to_cell(row)
			#self.clear_status_byte(row)
			#根据有无Null设置Status2
			self.update_status_byte(row)

		return rows

	def init_status_byte(self, field_info):
		field_detail = field_info["detail"]
		byte_count = len(field_detail)
		dst_jsons = []
		for i in range(byte_count):
			dst_json_line = {}
			for indx, detail in enumerate(field_detail):
				for detail_name, detail_value in detail.items():
					dst_json_line[detail_name] = 0
			dst_jsons.append(dst_json_line)
		return dst_jsons
		


	#def conv_csv_to_cell(self, new_row, force_create = False):
	def conv_csv_to_cell(self, new_row, force_create = True):
		for field_info in self.fields_info:
			if field_info["disable"] == 1:  continue

			field_name      = field_info["name"]
			field_detail    = field_info["detail"]
			field_visible   = field_info["visible"]
			field_type      = field_info["type"]
			field_length    = field_info["len"]
			field_value     = new_row[field_name][0]
			field_related   = field_info["related"]
			#只处理STATUSBYTE
			if field_type == "BIN":
				#dst_jsons = []
				#byte_count = len(field_detail)

				#必须处理固定项
				if not field_value and (not field_visible or force_create):
					try: new_row[field_name][0] = self.init_status_byte(field_info)
					except Exception, e:
						common.log_err( traceback.format_exc() )
				elif field_value:
					try: new_row[field_name][0] = BINReader().csv_to_cell(field_value, field_info["len"] * 2, field_info)
					except Exception, e:
						common.log_err( traceback.format_exc() )
						pass
			else:
				if field_value:
					new_row[field_name][0] = call_list[field_type]().csv_to_cell(field_value, field_length, field_info) 

	'''
	def clear_status_byte(self, new_row):
		for field_info in self.fields_info:
			if field_info["disable"] == 1:  continue

			field_name      = field_info["name"]
			field_detail    = field_info["detail"]
			field_visible   = field_info["visible"]
			field_type      = field_info["type"]
			field_length    = field_info["len"]
			field_value     = new_row[field_name][0]
			field_related   = field_info["related"]
			#只处理STATUSBYTE
			if field_type == "BIN":
				try:
					new_row[field_name][0] = self.init_status_byte(field_info)
				except Exception, e:
					common.log_err( traceback.format_exc() )
	'''

	#如果该字段为空，且有依赖状态字，就关掉
	def update_status_byte(self, new_row):
		share = {}
		for field_info in self.fields_info:
			field_type      = field_info["type"]
			field_name      = field_info["name"]
			field_visible   = field_info["visible"]
			
			#BYTES不处理
			if field_type == "BYTES": continue

			if field_visible:
				visible_field_name = field_visible["Name"]
				visible_field_byte = field_visible["Byte"]
				visible_field_bit  = field_visible["Bit"]

				if field_type == "BIN":
					pass
					#print "field_name, visible_field_name", field_name, visible_field_name
					#print new_row[visible_field_name][0]
					
				#if field_name == "EANData":
				#	pass
					#print "name, value:", field_name, new_row[field_name][0]

				#是否有字段共享此标志
				if not share.has_key(visible_field_name):
					share[visible_field_name] = {}
				if not share[visible_field_name].has_key(visible_field_byte):
					share[visible_field_name][visible_field_byte] = {}
				if not share[visible_field_name][visible_field_byte].has_key(visible_field_bit):
					share[visible_field_name][visible_field_byte][visible_field_bit] = 0
				
				if share[visible_field_name][visible_field_byte][visible_field_bit] == 0:
					try:
						if not new_row[field_name][0]:
							new_row[visible_field_name][0][visible_field_byte-1][visible_field_bit] = 0
						else:
							new_row[visible_field_name][0][visible_field_byte-1][visible_field_bit] = 1
							share[visible_field_name][visible_field_byte][visible_field_bit] = 1
					except Exception, e: 
						common.log_err( traceback.format_exc() )
						#if field_type == "BIN": traceback.print_exc()

	def cell_to_data(self, new_row):
		try:
			dst_line_data = []
			#src_line_data = new_row

			#fp = open("log.txt", "wb")
			#print new_row

			for field_info in self.fields_info:
				field_type      = field_info["type"]
				field_name      = field_info["name"]
				field_length    = field_info["len"] * 2
				field_value     = new_row[field_name][0]
				field_visible   = field_info["visible"]

				if field_info["disable"] == 1:
					continue


				if field_visible:
					visible_field_name = field_visible["Name"]
					visible_field_byte = field_visible["Byte"]
					visible_field_bit  = field_visible["Bit"]
					visible_field_info = self.fields_info_dic.get(visible_field_name, {})

					#依赖的BYTE不存在，不处理
					if not new_row[visible_field_name][0]:
						continue

					#cellData = BINReader().csv_to_cell(new_row[visible_field_name][0], visible_field_info["len"] * 2, visible_field_info)

					#json_value = common.get_json_from_string(new_row[visible_field_name][0])
					#json_value = new_row[visible_field_name][0]
					#json_value = cellData[visible_field_name][0]
					json_value = new_row[visible_field_name][0]
					if json_value[visible_field_byte-1][visible_field_bit] == 0:
						continue

				#print field_value
				#print field_name, field_value
				dst_line_data.append( call_list[field_type]().cell_to_dat(field_value, field_length, field_info) )
				#print "ok"

				#fp.write("%s,%s\n" % (field_name, "".join(dst_line_data[-1])))
				
			#fp.close()

			entire_line_data = "".join(dst_line_data)
			record_size = len(entire_line_data) // 2

			recordsize_len = self.fields_info[self.record_size_field_index]["len"] * 2
			#dst_line_data[self.record_size_field_index] = hex(record_size)[2:].upper().rjust(recordsize_len, '0')
			dst_line_data[self.record_size_field_index] = common.int2hex(record_size, recordsize_len)

			#fp.write("".join(dst_line_data))
			#fp.write("\r\n")

			return "".join(dst_line_data)

		except Exception, e:
			common.log_err( traceback.format_exc() )
			return ""

	def to_dat_mem(self):
		src_all_data = self.get_all_data()
		data_to_return = ""
		for src_line_data in src_all_data:
			line_data = self.cell_to_data(src_line_data)
			if line_data:
# 				fp.write(line_data); fp.write("\r\n")
				data_to_return += line_data+ "\r\n"
				
		return data_to_return
		

	def to_dat(self, file_path):
		src_all_data = self.get_all_data()
		with open(file_path, "wb") as fp:
			for src_line_data in src_all_data:
				line_data = self.cell_to_data(src_line_data)
				if line_data:
					fp.write(line_data); fp.write("\r\n")

	def find_records(self, sql, field_list):
		cursor = self.conn.cursor()
		#print "sql:", sql
		#print "field_list:", field_list
		cursor.execute(sql, field_list)
		names = [(index, desc[0]) for index, desc in enumerate(cursor.description)]
		rows = []
		for row in cursor:
			#yield [ (name[1], row[name[0]]) for name in names ]
			#cells = []
			dic1 = {}
			dic2 = {}
			for name in names:
				val = [row[name[0]]]
				dic1[name[1]] = dic2[str(name[0]+1)] = val
				#cells.append( {name[1]: val} ) 
				#cells.append( {str(name[0] + 1): val} )
			dic3=dic1.copy()
			dic3.update(dic2)
			rows.append(dic3)
			#rows.append(cells)
		return rows

	def get_max_value_of_key(self, strKeyField = ""):
		if not self.fieldKeys: return 0
		if not strKeyField:
			strKeyField = self.fieldKeys[0]

		sql = "SELECT IFNULL(MAX(%s), 0) FROM %s" % (strKeyField, self.name)
		cursor = self.conn.cursor()
		cursor.execute(sql)
		return cursor.fetchone()[0]


	def get_free_value_of_key(self):
		if not self.fieldKeys: return 1
		sql = '''
				SELECT (CASE WHEN EXISTS(SELECT 1 FROM %s WHERE %s=1) THEN MIN(%s+1) ELSE 1 END) 
				FROM %s
				WHERE %s not in(SELECT %s-1 FROM %s)	
			''' % (
			self.name, 
			self.fieldKeys[0], 
			self.fieldKeys[0], 
			self.name,
			self.fieldKeys[0], 
			self.fieldKeys[0], 
			self.name)
			
		cursor = self.conn.cursor()
		cursor.execute(sql)
		return cursor.fetchone()[0]
