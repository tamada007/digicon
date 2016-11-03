import csv,sys

class test2():
	def gogo(self, p1, p2, encoding=sys.getdefaultencoding()):
		print encoding
		
		with open("xyyc.csv", "r") as fp:
			cr = csv.reader(fp)
			line = cr.next()
			for row in cr:
				for cell in row:
					#print cell.decode(sys.getdefaultencoding())
					pass
