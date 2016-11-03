
import strparser

class DataFilter():
	def __init__(self):
		self.expression_list = []
		self.field_by_index  = []
		self.field_by_names  = {}
		self.global_vars     = {}
	def set_field_list(self, field_list):
		self.field_by_index = field_list
	def set_field_name(self, field_names):
		self.field_by_names = field_names
	def set_expressions(self, expr):
		self.expression_list = expr
	def set_glob_vars(self, gv):
		self.global_vars = gv
	def get_glob_vars(self):
		return self.global_vars

	def is_filtered(self):
		for expr in self.expression_list:
			
			strpar = strparser.StrParser(
				expr, 
				self.field_by_index, 
				self.field_by_names,
				self.global_vars)

			result = strpar.eval(0)	
			if "TRUE" != result: return True
		return False
