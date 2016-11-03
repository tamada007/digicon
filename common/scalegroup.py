import common
import sys

class DigiGroup:
	def __init__(self):
		self.groupScaleList = {}
		self.scaleGroupList = {}
	def get_scale_list_by_mgno(self, mgNo):
		return self.groupScaleList.get(mgNo, [])

	def get_mgno_from_scale(self, scale):
		return self.scaleGroupList.get(scale, -1)

	def read_from_config_file(self, fmtJsonFilePath):
		self.groupScaleList.clear()
		self.scaleGroupList.clear()
		json_data = common.get_json_from_file(fmtJsonFilePath, sys.getdefaultencoding())

		#if json_data and type(json_data) is list:
		if isinstance(json_data, list):
			for data_line in json_data:
				vScales = []
				iMGNo = data_line.get("MGNo", 0)
				scaleList = data_line.get("Scales", [])
				for scale in scaleList:
					#if type(scale) in (str, unicode):
					if isinstance(scale, (str, unicode)):
						vScales.append(scale)
						self.scaleGroupList[scale] = iMGNo
				self.groupScaleList[iMGNo] = vScales

