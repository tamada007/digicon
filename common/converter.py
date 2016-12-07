#encoding=gbk
import sys

import libsm110.smtws
import libsm120.digiscale

import libsm110.entity
import libsm120.entity

import common
import datafilter
import csvreader
import strparser
# import time
import traceback
import unicodedata
import csv,StringIO
from inspect import isfunction
from threading import Thread


class StatementConvert:
	@staticmethod
	def convertInfoForSm120(cur_line_no, csv_values, cbSetValueList):
		tableNamePLU = "Plu"
		tableNamePLA = "Pla"
		tableNameSPM = "Spm"
		tableNameING = "Ing"
		tableNameTEX = "Tex"
		tableNameMUB = "Mub"
		tableNameTBT = "Tbt"
		
		# PLU
		cbSetValueList(tableNamePLU, "PLUNo", csv_values.get("PLUNo") or '')
		# 单价
		cbSetValueList(tableNamePLU, "UnitPrice", csv_values.get("UnitPrice") or "0")
		# 称重标志
		cbSetValueList(tableNamePLU, "WeightingFlag", csv_values.get("WeightingFlag") or "0")
		# F1F2
		cbSetValueList(tableNamePLU, "BarcodeFlagOfEanData", csv_values.get("BarcodeFlag") or "0")
		# 单价覆盖
		cbSetValueList(tableNamePLU, "UnitPriceOverrideFlag", csv_values.get("PriceOverride") or "0")
		# ItemCode
		cbSetValueList(tableNamePLU, "ItemCode", csv_values.get("ItemCode") or "0000000000")
		
		# 产地
		tmp_placecode = csv_values.get("PlaCode")
		if tmp_placecode:
			# PlaceNo
			cbSetValueList(tableNamePLU, "PlaceNo", tmp_placecode)
	
			tmp_placename = csv_values.get("PlaceName") 
			if tmp_placename:
				cbSetValueList(tableNamePLA, "Code",		line_no = -1, value = tmp_placecode)
				cbSetValueList(tableNamePLA, "LineNo",		line_no = -1, value = "1")
				cbSetValueList(tableNamePLA, "DeleteFlag",	line_no = -1, value = "2")
				cbSetValueList(tableNamePLA, "PlaceFlag",	line_no = -1, value = "0")
				
				cbSetValueList(tableNamePLA, "Code",		line_no = 1, value = tmp_placecode)
				cbSetValueList(tableNamePLA, "LineNo",		line_no = 1, value = "1")
				cbSetValueList(tableNamePLA, "PlaceFlag",	line_no = 1, value = csv_values.get("PlaceFont") or "21")
				cbSetValueList(tableNamePLA, "PlaceName",	line_no = 1, value = tmp_placename)
				
		# 品名
		if csv_values.get("Commodity"):
			#自动分行的处理
			max_length = 23
			font = 20
			max_line = 4
			try: max_length = int(csv_values.get("CommodityMaxLength"))
			except:	pass
			try: font = int(csv_values.get("CommodityFont"))
			except:	pass
			try: max_line = int(csv_values.get("CommodityMaxLine"))
			except:	pass
			
			data_lines = StatementConvert.wrap_text_block(csv_values.get("Commodity"), max_length).split('\n')
			
			for index, value in enumerate(data_lines[:max_line]):
				cbSetValueList(tableNamePLU, "CommodityName%d" % (index+1),	value.replace('"','""'))
				cbSetValueList(tableNamePLU, "CommodityFont%d" % (index+1),	str(font))
			
		else:
			if csv_values.get("Commodity1"):
				cbSetValueList(tableNamePLU, "CommodityName1", csv_values.get("Commodity1").replace('"','""'))
				cbSetValueList(tableNamePLU, "CommodityFont1", csv_values.get("Commodity1Font") or '0')
			if csv_values.get("Commodity2"):
				cbSetValueList(tableNamePLU, "CommodityName2", csv_values.get("Commodity2").replace('"','""'))
				cbSetValueList(tableNamePLU, "CommodityFont2", csv_values.get("Commodity2Font") or '0')
			if csv_values.get("Commodity3"):
				cbSetValueList(tableNamePLU, "CommodityName3", csv_values.get("Commodity3").replace('"','""'))
				cbSetValueList(tableNamePLU, "CommodityFont3", csv_values.get("Commodity3Font") or '0')
			if csv_values.get("Commodity4"):
				cbSetValueList(tableNamePLU, "CommodityName4", csv_values.get("Commodity4").replace('"','""'))
				cbSetValueList(tableNamePLU, "CommodityFont4", csv_values.get("Commodity4Font") or '0')
			
		# 条码格式
		cbSetValueList(tableNamePLU, "BarcodeFormat", csv_values.get("BarcodeFormat") or '0')
		# 标签格式
		cbSetValueList(tableNamePLU, "LabelFormat1", csv_values.get("LabelFormat1") or '17')
		
		# 保质期
		if csv_values.get("UsedByDate"):
			cbSetValueList(tableNamePLU, "UsedByDateFlag", "1")
			cbSetValueList(tableNamePLU, "UsedByDate", csv_values.get("UsedByDate"))
			
		# 销售日期
		if csv_values.get("SellByDate"):
			cbSetValueList(tableNamePLU, "SellByDateFlag", "1")
			cbSetValueList(tableNamePLU, "SellByDate", csv_values.get("SellByDate"))

		# 包装日期
		if csv_values.get("PackedByDate"):
			cbSetValueList(tableNamePLU, "PackedDateFlag", "1")
			cbSetValueList(tableNamePLU, "PackedDate", csv_values.get("PackedByDate"))

		# 包装时间
		if csv_values.get("PackedByTime"):
			cbSetValueList(tableNamePLU, "PackedTimeFlag", "1")
			cbSetValueList(tableNamePLU, "PackedTime", csv_values.get("PackedByTime"))

		# 销售时间
		if csv_values.get("SellByTime"):
			cbSetValueList(tableNamePLU, "SellByTimeFlag", "1")
			cbSetValueList(tableNamePLU, "SellByTime", csv_values.get("SellByTime"))
			
		# 主组
		cbSetValueList(tableNamePLU, "MGNo", csv_values.get("MGNo") or "997")
		
		# BarcodeType (EAN or ITF)
		tmp_bartype = csv_values.get("BarcodeType") or "EAN"
		cbSetValueList(tableNamePLU, "BarcodeTypeOfEanData", "9" if tmp_bartype == "ITF" else "0")
		#追溯码开关
		cbSetValueList(tableNamePLU, "TraceabilityFlag", csv_values.get("TraceabilityFlag") or "0")
		# 追溯码编号
		cbSetValueList(tableNamePLU, "TraceabilityNo", csv_values.get("TraceabilityNo") or "0")
		
		# 特殊信息
		cbSetValueList(tableNamePLU, "SpecialMessageNo", csv_values.get("SpmCode") or str(cur_line_no))
		cbSetValueList(tableNameSPM, "Code",		line_no = -1, value = csv_values.get("SpmCode") or str(cur_line_no))
		cbSetValueList(tableNameSPM, "LineNo",		line_no = -1, value = "1")
		cbSetValueList(tableNameSPM, "DeleteFlag",	line_no = -1, value = "2")
		if csv_values.get("SpecialMessage"):
			#自动分行的处理
			max_length = 23
			font = 20
			max_line = 10
			try: max_length = int(csv_values.get("SpecialMessageMaxLength"))
			except:	pass
			try: font = int(csv_values.get("SpecialMessageFont"))
			except:	pass
			try: max_line = int(csv_values.get("SpecialMessageMaxLine"))
			except:	pass
			
			data_lines = StatementConvert.wrap_text_block(csv_values.get("SpecialMessage"), max_length).split('\n')
			
			for index, value in enumerate(data_lines[:max_line]):
				cbSetValueList(tableNameSPM, "Code",		line_no = index+1, value = csv_values.get("SpmCode") or str(cur_line_no))
				cbSetValueList(tableNameSPM, "LineNo",		line_no = index+1, value = str(index+1))
				cbSetValueList(tableNameSPM, "Flag",		line_no = index+1, value = str(font))
				cbSetValueList(tableNameSPM, "Data",		line_no = index+1, value = value.replace('"','""'))
		else:
			for index in xrange(10):
				if csv_values.get("SpecialMessage%d" % (index+1)):
					cbSetValueList(tableNameSPM, "Code",	line_no = index+1, value = csv_values.get("SpmCode") or str(cur_line_no))
					cbSetValueList(tableNameSPM, "LineNo",	line_no = index+1, value = str(index+1))
					cbSetValueList(tableNameSPM, "Flag",	line_no = index+1, value = csv_values.get("SpecialMessage%dFont" % (index+1)) or "0")
					cbSetValueList(tableNameSPM, "Data",	line_no = index+1, value = csv_values.get("SpecialMessage%d" % (index + 1)).replace('"','""'))
			
		# 成份
		cbSetValueList(tableNamePLU, "IngredientNo", csv_values.get("IngCode") or str(cur_line_no))
		cbSetValueList(tableNameING, "Code",		line_no = -1, value = csv_values.get("IngCode") or str(cur_line_no))
		cbSetValueList(tableNameING, "LineNo",		line_no = -1, value = "1")
		cbSetValueList(tableNameING, "DeleteFlag",	line_no = -1, value = "2")
		if csv_values.get("Ingredient"):
			#自动分行的处理
			max_length = 23
			font = 20
			max_line = 10
			try: max_length = int(csv_values.get("IngredientMaxLength"))
			except:	pass
			try: font = int(csv_values.get("IngredientFont"))
			except:	pass
			try: max_line = int(csv_values.get("IngredientMaxLine"))
			except:	pass
			
			data_lines = StatementConvert.wrap_text_block(csv_values.get("Ingredient"), max_length).split('\n')
			
			for index, value in enumerate(data_lines[:max_line]):
				cbSetValueList(tableNameING, "Code",		line_no = index+1, value = csv_values.get("IngCode") or str(cur_line_no))
				cbSetValueList(tableNameING, "LineNo",		line_no = index+1, value = str(index+1))
				cbSetValueList(tableNameING, "Flag",		line_no = index+1, value = str(font))
				cbSetValueList(tableNameING, "Data",		line_no = index+1, value = value.replace('"','""'))
		else:
			for index in xrange(10):
				if csv_values.get("Ingredient%d" % (index+1)):
					cbSetValueList(tableNameING, "Code",	line_no = index+1, value = csv_values.get("IngCode") or str(cur_line_no))
					cbSetValueList(tableNameING, "LineNo",	line_no = index+1, value = str(index+1))
					cbSetValueList(tableNameING, "Flag",	line_no = index+1, value = csv_values.get("Ingredient%dFont" % (index+1)) or "0")
					cbSetValueList(tableNameING, "Data",	line_no = index+1, value = csv_values.get("Ingredient%d" % (index+1)).replace('"','""'))
	
		# 文本
		for index in xrange(10):
			if csv_values.get("Text%d" % (index+1)):
				cbSetValueList(tableNamePLU, "TextNo%d" % (index+1),	csv_values.get("TexCode%d" % (index+1)) or str(cur_line_no))
				cbSetValueList(tableNameTEX, "Code",		line_no = -1, value = csv_values.get("TexCode%d" % (index+1)) or str(cur_line_no))
				cbSetValueList(tableNameTEX, "LineNo",		line_no = -1, value = "1")
				cbSetValueList(tableNameTEX, "DeleteFlag",	line_no = -1, value = "2")
				cbSetValueList(tableNameTEX, "Code",		line_no = 1, value = csv_values.get("TexCode%d" % (index+1)) or str(cur_line_no))
				cbSetValueList(tableNameTEX, "LineNo",		line_no = 1, value = "1")
				cbSetValueList(tableNameTEX, "Flag",		line_no = 1, value = csv_values.get("Text%dFont" % (index+1)) or "0")
				cbSetValueList(tableNameTEX, "Data",		line_no = 1, value = csv_values.get("Text%d" % (index+1)).replace('"','""'))
			
		# MultiBarcode 1
		if csv_values.get("Multibarcode1"):
			cbSetValueList(tableNamePLU, "Multibarcode1No", csv_values.get("MubCode1") or str(cur_line_no))
			cbSetValueList(tableNameMUB, "Code",				line_no = 1, value = csv_values.get("MubCode1") or str(cur_line_no))
			cbSetValueList(tableNameMUB, "MultiBarcodeType",	line_no = 1, value = "2")
			cbSetValueList(tableNameMUB, "BarcodeType",			line_no = 1, value = "1")
			cbSetValueList(tableNameMUB, "Data",				line_no = 1, value = csv_values.get("Multibarcode1"))
			
		# MultiBarcode 2
		if csv_values.get("Multibarcode2"):
			tmp_mubcode2 = csv_values.get("MubCode2") or str(cur_line_no)
			cbSetValueList(tableNamePLU, "Multibarcode2No", tmp_mubcode2)
			
			cbSetValueList(tableNameTBT, "Code",					line_no = -1, value = tmp_mubcode2)
			cbSetValueList(tableNameTBT, "LineNo",					line_no = -1, value = "1")
			cbSetValueList(tableNameTBT, "DeleteFlag",				line_no = -1, value = "2")
			
			cbSetValueList(tableNameMUB, "Code",					line_no = 2, value = tmp_mubcode2)
			cbSetValueList(tableNameMUB, "MultiBarcodeType",		line_no = 2, value = "2" if csv_values.get("NoLinkTo2DBarcodeText") else "3")
			cbSetValueList(tableNameMUB, "BarcodeType",				line_no = 2, value = "5")
				
			if csv_values.get("NoLinkTo2DBarcodeText"):
				cbSetValueList(tableNameMUB, "Data",				line_no = 2, value = csv_values.get("Multibarcode2"))
			else:
				cbSetValueList(tableNameMUB, "Link2DBarcodeTextNo", line_no = 2, value = csv_values.get("TbtCode") or str(cur_line_no))
				try:
					mul2_data_list = csv.reader(StringIO.StringIO(csv_values.get("Multibarcode2"))).next()
					for mul2_index, mul2_data in enumerate(mul2_data_list[:10]):
						cbSetValueList(tableNameTBT, "Code",		line_no = mul2_index+1, value = csv_values.get("TbtCode") or str(cur_line_no))
						cbSetValueList(tableNameTBT, "LineNo",		line_no = mul2_index+1, value = str(mul2_index+1))
						cbSetValueList(tableNameTBT, "Data",		line_no = mul2_index+1, value = mul2_data)
				except Exception:
					pass
				
		# Extra Processing
		execfile("plugin.py")
	
	@staticmethod
	def convertInfoForSm110(cur_line_no, csv_values, cbSetValueList):
		
		tableNamePLU = "Plu"
		tableNamePLA = "Pla"
		tableNameTBT = "Tbt"
		tableNameTEX = "Tex"

		# PLU
		cbSetValueList(tableNamePLU, "PLUNo", csv_values.get("PLUNo") or '')
		
		# Status1
		cbSetValueList(tableNamePLU, "PLUStatus1", "0000000%s 000%s0000" % (csv_values.get("WeightingFlag") or '0', csv_values.get("PriceOverride") or '0'))
		# EAN Data
		cbSetValueList(tableNamePLU, "EANData", "%s,%s,%s" % (
				csv_values.get("ItemCode") or '0000000000', 
				csv_values.get("BarcodeType") or 'EAN',
				csv_values.get("BarcodeX") or '0')
			)
		# 产地
		tmp_placecode = csv_values.get("PlaCode")
		if tmp_placecode:
			cbSetValueList(tableNamePLU, "PlaceNumber", tmp_placecode)
			tmp_placename = csv_values.get("PlaceName")
			if tmp_placename:
				cbSetValueList(tableNamePLA, "Code", tmp_placecode)
				cbSetValueList(tableNamePLA, "PlaceName", '%s,"%s"' % (csv_values.get("PlaceFont") or '21', tmp_placename.replace('"','""')))


		# 单价
		cbSetValueList(tableNamePLU, "UnitPrice", csv_values.get("UnitPrice") or "0")
		# F1F2
		cbSetValueList(tableNamePLU, "F1F2", csv_values.get("BarcodeFlag") or "00")
		# BarcodeFormat
		cbSetValueList(tableNamePLU, "BarcodeFormat", csv_values.get("BarcodeFormat") or "0")
		# LabelFormat1
		cbSetValueList(tableNamePLU, "LabelFormat1", csv_values.get("LabelFormat1") or "17")
		# 保质期
		cbSetValueList(tableNamePLU, "UsedByDate", csv_values.get("UsedByDate") or "")
		# 销售日期
		cbSetValueList(tableNamePLU, "SellByDate", csv_values.get("SellByDate") or "")
		# 销售时间
		cbSetValueList(tableNamePLU, "SellByTime", csv_values.get("SellByTime") or "")
		# 包装日期
		cbSetValueList(tableNamePLU, "PackedDate", csv_values.get("PackedByDate") or "")
		# 包装时间
		cbSetValueList(tableNamePLU, "PackedTime", csv_values.get("PackedByTime") or "")
		# 主组号
		cbSetValueList(tableNamePLU, "MGCode", csv_values.get("MGNo") or "997")
		
		# MultiBarcode 1
		if csv_values.get("Multibarcode1"):
			cbSetValueList(tableNamePLU, "MultiBarcode1", "1,%s,2" % csv_values.get("Multibarcode1"))

		# MultiBarcode 2 
		if csv_values.get("Multibarcode2"):
			if csv_values.get("NoLinkTo2DBarcodeText"):
				cbSetValueList(tableNamePLU, "MultiBarcode2", "5,%s,2" % csv_values.get("Multibarcode2"))
			else:
				cbSetValueList(tableNamePLU, "MultiBarcode2", "5,%s,3" % csv_values.get("MubCode2") or str(cur_line_no))
				#2D Barcode
				cbSetValueList(tableNameTBT, "Code", csv_values.get("MubCode2") or str(cur_line_no))
				try:
					cbSetValueList(tableNameTBT, "Data", "\n".join(['21,"%s"' % ent.replace('"','""') for ent in csv.reader(StringIO.StringIO(csv_values.get("Multibarcode2"))).next()]))
				except: pass
		
		# Text1
		if csv_values.get("Text1"):
			cbSetValueList(tableNamePLU, "LinkedText1No", csv_values.get("TexCode1") or str(cur_line_no))
			cbSetValueList(tableNameTEX, "Code", line_no = 1, value = csv_values.get("TexCode1") or str(cur_line_no))
			cbSetValueList(tableNameTEX, "Name", line_no = 1, value = '%s,"%s"' % (csv_values.get("Text1Font") or '21', csv_values.get("Text1").replace('"','""')))

		# Text2
		if csv_values.get("Text2"):
			cbSetValueList(tableNamePLU, "LinkedText2No", csv_values.get("TexCode2") or str(cur_line_no))
			cbSetValueList(tableNameTEX, "Code", line_no = 2, value = csv_values.get("TexCode2") or str(cur_line_no))
			cbSetValueList(tableNameTEX, "Name", line_no = 2, value = '%s,"%s"' % (csv_values.get("Text2Font") or '21', csv_values.get("Text2").replace('"','""')))

		# Text3
		if csv_values.get("Text3"):
			cbSetValueList(tableNamePLU, "LinkedText3No", csv_values.get("TexCode3") or str(cur_line_no))
			cbSetValueList(tableNameTEX, "Code", line_no = 3, value = csv_values.get("TexCode3") or str(cur_line_no))
			cbSetValueList(tableNameTEX, "Name", line_no = 3, value = '%s,"%s"' % (csv_values.get("Text3Font") or '21', csv_values.get("Text3").replace('"','""')))

		# Text4
		if csv_values.get("Text4"):
			cbSetValueList(tableNamePLU, "LinkedText4No", csv_values.get("TexCode4") or str(cur_line_no))
			cbSetValueList(tableNameTEX, "Code", line_no = 4, value = csv_values.get("TexCode4") or str(cur_line_no))
			cbSetValueList(tableNameTEX, "Name", line_no = 4, value = '%s,"%s"' % (csv_values.get("Text4Font") or '21', csv_values.get("Text4").replace('"','""')))

		# Text5
		if csv_values.get("Text5"):
			cbSetValueList(tableNamePLU, "LinkedText5No", csv_values.get("TexCode5") or str(cur_line_no))
			cbSetValueList(tableNameTEX, "Code", line_no = 5, value = csv_values.get("TexCode5") or str(cur_line_no))
			cbSetValueList(tableNameTEX, "Name", line_no = 5, value = '%s,"%s"' % (csv_values.get("Text5Font") or '21', csv_values.get("Text5").replace('"','""')))

		# 追溯码开关
		cbSetValueList(tableNamePLU, "Traceability", csv_values.get("TraceabilityFlag") or "0")
		# 追溯码编号
		cbSetValueList(tableNamePLU, "TraceabilityLink", csv_values.get("TraceabilityNo") or "0")
		
		# 品名
		if csv_values.get("Commodity"):
			#自动分行的处理
			max_comm_length = 23
			comm_font = 20
			max_comm_line = 4
			try: max_comm_length = int(csv_values.get("CommodityMaxLength"))
			except:	pass
			try: comm_font = int(csv_values.get("CommodityFont"))
			except:	pass
			try: max_comm_line = int(csv_values.get("CommodityMaxLine"))
			except:	pass
			
			comm_data_lines = StatementConvert.wrap_text_block(csv_values.get("Commodity"), max_comm_length).split('\n')
			cbSetValueList(tableNamePLU, "Commodity", 
				"\n".join(['%d,"%s"' % (comm_font,comm_data_line.replace('"','""')) for comm_data_line in comm_data_lines[:max_comm_line]])
				)
		else:
			#上层软件已分行
			j = -1
			for i in reversed(xrange(4)):
				commName = "Commodity%d" % (i+1)
				if csv_values.get(commName): j = i + 1; break
			comm_array_data = []
			for i in xrange(j):
				commName = "Commodity%d" % (i+1)
				commNameFont = commName + "Font"
				cur_font = 20
				try: cur_font = int(csv_values.get(commNameFont))
				except: pass
				
				valCommName = csv_values.get(commName) or ""
				comm_array_data.append('%d,"%s"' % (cur_font, valCommName.replace('"', '""')))
			cbSetValueList(tableNamePLU, "Commodity", "\n".join(comm_array_data))
		
		
		# 特殊信息
		if csv_values.get("SpecialMessage"):
			#自动分行的处理
			max_spm_length = 23
			spm_font = 20
			max_spm_line = 10
			try: max_spm_length = int(csv_values.get("SpecialMessageMaxLength"))
			except:	pass
			try: spm_font = int(csv_values.get("SpecialMessageFont"))
			except:	pass
			try: max_spm_line = int(csv_values.get("SpecialMessageMaxLine"))
			except:	pass
			
			spm_data_lines = StatementConvert.wrap_text_block(csv_values.get("SpecialMessage"), max_spm_length).split('\n')
			cbSetValueList(tableNamePLU, "SpecialMessage", 
				"\n".join(['%d,"%s"' % (spm_font,spm_data_line.replace('"','""')) for spm_data_line in spm_data_lines[:max_spm_line]])
				)
		else:
			#上层软件已分行
			j = -1
			for i in reversed(xrange(10)):
				spmName = "SpecialMessage%d" % (i+1)
				if csv_values.get(spmName):	j = i + 1; break
			spm_array_data = []
			for i in xrange(j):
				spmName = "SpecialMessage%d" % (i+1)
				spmNameFont = spmName + "Font"
				cur_font = 20
				try: cur_font = int(csv_values.get(spmNameFont))
				except: pass
				valSpmName = csv_values.get(spmName) or ""
				spm_array_data.append('%d,"%s"' % (cur_font, valSpmName.replace('"', '""')))
			cbSetValueList(tableNamePLU, "SpecialMessage", "\n".join(spm_array_data))

		# 成分
		if csv_values.get("Ingredient"):
			#自动分行的处理
			max_ing_length = 23
			ing_font = 20
			max_ing_line = 10
			try: max_ing_length = int(csv_values.get("IngredientMaxLength"))
			except:	pass
			try: ing_font = int(csv_values.get("IngredientFont"))
			except:	pass
			try: max_ing_line = int(csv_values.get("IngredientMaxLine"))
			except:	pass
			
			ing_data_lines = StatementConvert.wrap_text_block(csv_values.get("Ingredient"), max_ing_length).split('\n')
			cbSetValueList(tableNamePLU, "Ingredient", 
				"\n".join(['%d,"%s"' % (ing_font,ing_data_line.replace('"','""')) for ing_data_line in ing_data_lines[:max_ing_line]])
				)
		else:
			#上层软件已分行
			j = -1
			for i in reversed(xrange(10)):
				ingName = "Ingredient%d" % (i+1)
				if csv_values.get(ingName): j = i + 1; break
			ing_array_data = []
			for i in xrange(j):
				ingName = "Ingredient%d" % (i+1)
				ingNameFont = ingName + "Font"
				cur_font = 20
				try: cur_font = int(csv_values.get(ingNameFont))
				except: pass
				valIngName = csv_values.get(ingName) or ""
				ing_array_data.append('%d,"%s"' % (cur_font, valIngName.replace('"', '""')))
			cbSetValueList(tableNamePLU, "Ingredient", "\n".join(ing_array_data))

		# Extra Processing
		execfile("plugin.py")
		

	@staticmethod
	def split(txt,sp):
		return txt.split(sp)

	@staticmethod
	def get_hz_string_width(text):  
		""" 
		获取可能包含汉字的字符串的长度（1个汉字算2个字符长） 
		"""  
		s = 0  
		for ch in text:  
			if isinstance(ch, unicode):  
				if unicodedata.east_asian_width(ch)!= 'Na':   
					s += 2  
				else:  
					s += 1  
			else:  
				s += 1  
		return s  

	@staticmethod
	def get_hz_sub_string(text,startat,sub_len=None):  
		""" 
		获取可能包含汉字的字符串的子串（计算长度时，1个汉字算2个字符长） 
	
		用法： 
		get_hz_sub_string(record,0,44)  #取子串，位置为0至43 
		get_hz_sub_string(record,44)	#取子串，位置为44至末尾 
		"""  
		s = []  
		pos = 0  
		for ch in text:  
			if pos >= startat:  
				s.append(ch)  
			if isinstance(ch, unicode):  
				if unicodedata.east_asian_width(ch)!= 'Na':   
					pos += 2  
				else:  
					pos += 1  
			else:  
				pos += 1  
			if sub_len!=None and StatementConvert.get_hz_string_width(''.join(s))>=sub_len:  
				break	 
		return ''.join(s)  

	@staticmethod
	def insert_line_feed(my_str,interval,line_feed="\n"):  
		"""隔指定长度插入一个\n符号(一个汉字处理为2个字符长度）"""  
		if len(my_str)==0:   
			return ""  
	
		n = int((StatementConvert.get_hz_string_width(my_str)-1)/interval)+1  
		str_list = []  
		k = 1  
		pos_start = 0  
		while k <= n:  
			sub_str = StatementConvert.get_hz_sub_string(my_str,pos_start,interval)   
			str_list.append(sub_str)  
			k = k + 1  
			pos_start = pos_start + StatementConvert.get_hz_string_width(sub_str)  
	
		return line_feed.join(str_list)	  

	@staticmethod
	def wrap_text_block(text,line_length,do_trim=True):  
		if do_trim:  
			str_list = StatementConvert.split(text.rstrip(),'\n')  
		else:	  
			str_list = StatementConvert.split(text,'\n')  
	
		#检测末尾空行的开始位置  
		text_to_line = -1  
		if do_trim:  
			i = len(str_list)-1  
			while i > 0:  
				line_str = str_list[i]  
				if len(line_str.strip())==0:  
					text_to_line = i  
					i -= 1  
				else:  
					break	   
	
		new_str_list = []  
		i = 0  
		for obj in str_list:  
			if do_trim and i == text_to_line:  
				break  
			new_str_list += StatementConvert.split(StatementConvert.insert_line_feed(obj,line_length),'\n')  
			i += 1  
	
		#不加 u'' 就出错“'unicode' object is not callable”！？  
		return u''+'\n'.join(new_str_list)	


		


ConvertDesc_FLEXIBARCODE = {
	"sm110": [
		{ "source": "isnull($(BarcodeCode),$(CurLineNo))",   "target": "Flb.Code" },
		{ "source": "$(BarcodeFlagType)",                    "target": "Flb.FlagType" },
		{ "source": "$(ItemCodeLength)",                     "target": "Flb.ItemCodeDigitNum" },
		{ "source": "$(Data1Length)",                        "target": "Flb.ProgramData1DigitNum" },
		{ "source": "$(Data2Length)",                        "target": "Flb.ProgramData2DigitNum" },
		{
			"source": "iif(equals($(BarcodeType),EAN),1,0)0isnull($(IndiaCode128LastByte),0)00isnull($(IndiaCode128),0)isnull($(LastCD),0)isnull($(MidCD),0)",
			"target": "Flb.CheckDigit"
		},
		{ "source": "$(Data1)",                              "target": "Flb.ProgramData1" },
		{ "source": "$(Data2)",                              "target": "Flb.ProgramData2" },
		{ "source": "$(Data1Shift)",                         "target": "Flb.ProgramData1Shift" },
		{ "source": "$(Data2Shift)",                         "target": "Flb.ProgramData2Shift" }
	],
	"sm120": [
		{ "source": "isnull($(BarcodeCode),$(CurLineNo))",   "target": "Flb.Code" },
		{ "source": "$(BarcodeFlagType)",                    "target": "Flb.FlagType" },
		{ "source": "$(ItemCodeLength)",                     "target": "Flb.ItemCodeDigitNumber" },
		{ "source": "$(Data1Length)",                        "target": "Flb.ProgramData1DigitNumber" },
		{ "source": "$(Data2Length)",                        "target": "Flb.ProgramData2DigitNumber" },
		{ "source": "isnull($(MidCD),0)",                    "target": "Flb.FlagOfMiddleCheckDigit" },
		{ "source": "isnull($(LastCD),0)",                   "target": "Flb.FlagOfLastCheckDigit" },
		{ "source": "iif(equals($(BarcodeType),EAN),1,0)",   "target": "Flb.FlagOfBarcodeType" },
		{ "source": "isnull($(IndiaCode128),0)",             "target": "Flb.FlagOfIndiaCode128" },
		{ "source": "isnull($(IndiaCode128LastByte),0)",     "target": "Flb.FlagOfIndiaCode128LastByte" },
		{ "source": "$(Data1)",                              "target": "Flb.ProgramData1Type" },
		{ "source": "$(Data2)",                              "target": "Flb.ProgramData2Type" },
		{ "source": "$(Data1Shift)",                         "target": "Flb.ProgramData1Shift" },
		{ "source": "$(Data2Shift)",                         "target": "Flb.ProgramData2Shift" }
	]
}

ConverterDesc_TRACE = {
	"sm110": [
		{ "source": "$(TraceabilityNo)",                 "target": "Trg.Code" },
		{ "source": "$(TraceReferenceCode)",             "target": "Trg.ReferenceCode" },
		{ "source": "1",                                 "target": "Trg.ReferenceType" },
		{
			"condition": "isnotempty($(TrbCode))",
			"statements": [
				{ "source": "$(TrbCode)", "target": "Trg.BarcodeNo" },
				{ "source": "$(TrbCode)", "target": "Trb.Code" },
				{ "source": "$(TraceBarcode)", "target": "Trb.Data" }
			]			
		}
		
	],
	"sm120": [
		{ "source": "$(TraceabilityNo)",                "target": "Trg.Code" },
		{ "source": "$(TraceReferenceCode)",            "target": "Trg.ReferenceCode" },
		{ "source": "1",                                "target": "Trg.ReferenceType" },
		{
			"condition": "isnotempty($(TrbCode))",
			"statements": [
				{ "source": "$(TrbCode)",                       "target": "Trg.TraceBarcodeNo" },
				{ "source": "$(TrbCode)",                       "target": "Trb.Code" },
				{ "source": "$(TraceBarcode)",                  "target": "Trb.Data" }
			]
		}
	]
}

ConvertDesc_PRESETKEY = {
	"sm110": [
		{ "source": "add($(KasCode),mul(256,isnull($(PageNo),0)))", "target": "Kas.Code" },
		{ "source": "$(PluCode)", "target": "Kas.SwitchNo" },
		{ "source": "0",		  "target": "Kas.Status" }
	],
	"sm120": [
		{ "source": "isnull($(PageNo),0)", "target": "Kas.PageNo" },
		{ "source": "$(KasCode)", "target": "Kas.KeyNo" },
		{ "source": "$(PluCode)", "target": "Kas.SwitchNo" },
		{ "source": "0", "target": "Kas.Status" }
	]
}


ConvertDesc_PLU = {
	"sm110": [
		{
# 			"condition": "isnotempty($(SpecialMessage))",
			"statement": StatementConvert.convertInfoForSm110
		},
# 		{"source": "$(PLUNo)",                         "target": "Plu.PLUNo"},
# 		{"source": "$(UnitPrice)",                     "target": "Plu.UnitPrice"},
# 		{
# 			"source": "0000000isnull($(WeightingFlag),0) 000isnull($(PriceOverride),0)0000",
# 			"target": "Plu.PLUStatus1"
# 		},
# 		{"source": "isnull($(BarcodeFlag),00)",        "target": "Plu.F1F2"},
# 		{
# 			"source": "isnull($(ItemCode),0000000000),isnull($(BarcodeType),EAN),isnull($(BarcodeX),0)",
# 			"target": "Plu.EANData"
# 		},
# 		{
# 			"condition": "isnotempty($(PlaCode))",
# 			"statements": [
# 				{
# 					"source": "$(PlaCode)",
# 					"target": "Plu.PlaceNumber"
# 				},
# 				{
# 					"condition": "isnotempty($(PlaceName))",
# 					"statements": [
# 						{ "source": "$(PlaCode)",      "target": "Pla.Code",	},
# 						{ "source": 'isnull($(PlaceFont),21),"csvformat($(PlaceName))"',    "target": "Pla.PlaceName" }
# 					]
# 				}
# 			]
# 		},
# 		{
# 			#"sourceold": "twsascii(\"$(Commodity1Font),$(Commodity2Font),$(Commodity3Font),$(Commodity4Font)\",\"csvformat($(Commodity1)),csvformat($(Commodity2)),csvformat($(Commodity3)),csvformat($(Commodity4))\")",
# 			"source": 'twsascii("$(Commodity1Font),$(Commodity2Font),$(Commodity3Font),$(Commodity4Font)","""csvformat4($(Commodity1))"",""csvformat4($(Commodity2))"",""csvformat4($(Commodity3))"",""csvformat4($(Commodity4))""")',
# 			"target": "Plu.Commodity"
# 		},
# 		{"source": "isnull($(BarcodeFormat),0)",       "target": "Plu.BarcodeFormat"},
# 		{"source": "isnull($(LabelFormat1),17)",       "target": "Plu.LabelFormat1"},
# 		{"source": "$(UsedByDate)",                    "target": "Plu.UsedByDate"},
# 		{"source": "$(SellByDate)",                    "target": "Plu.SellByDate"},
# 		{"source": "$(PackedByDate)",                  "target": "Plu.PackedDate"},
# 		{"source": "$(SellByTime)",                    "target": "Plu.SellByTime"},
# 		{"source": "$(PackedByTime)",                  "target": "Plu.PackedTime"},
# 		{"source": "$(MGNo)",                          "target": "Plu.MGCode"},
# 		{
# 			"condition": "isempty($(SpecialMessage))",
# 			#"sourceold": "twsascii(\"$(SpecialMessage1Font),$(SpecialMessage2Font),$(SpecialMessage3Font),$(SpecialMessage4Font),$(SpecialMessage5Font),$(SpecialMessage6Font),$(SpecialMessage7Font),$(SpecialMessage8Font),$(SpecialMessage9Font),$(SpecialMessage10Font)\",\"csvformat($(SpecialMessage1)),csvformat($(SpecialMessage2)),csvformat($(SpecialMessage3)),csvformat($(SpecialMessage4)),csvformat($(SpecialMessage5)),csvformat($(SpecialMessage6)),csvformat($(SpecialMessage7)),csvformat($(SpecialMessage8)),csvformat($(SpecialMessage9)),csvformat($(SpecialMessage10))\")",
# 			"source": 'twsascii("$(SpecialMessage1Font),$(SpecialMessage2Font),$(SpecialMessage3Font),$(SpecialMessage4Font),$(SpecialMessage5Font),$(SpecialMessage6Font),$(SpecialMessage7Font),$(SpecialMessage8Font),$(SpecialMessage9Font),$(SpecialMessage10Font)","""csvformat4($(SpecialMessage1))"",""csvformat4($(SpecialMessage2))"",""csvformat4($(SpecialMessage3))"",""csvformat4($(SpecialMessage4))"",""csvformat4($(SpecialMessage5))"",""csvformat4($(SpecialMessage6))"",""csvformat4($(SpecialMessage7))"",""csvformat4($(SpecialMessage8))"",""csvformat4($(SpecialMessage9))"",""csvformat4($(SpecialMessage10))""")',
# 			"target": "Plu.SpecialMessage"
# 		},
# 		{
# 			"condition": "isempty($(Ingredient))",
# 			#"sourceold": "twsascii(\"$(Ingredient1Font),$(Ingredient2Font),$(Ingredient3Font),$(Ingredient4Font),$(Ingredient5Font),$(Ingredient6Font),$(Ingredient7Font),$(Ingredient8Font),$(Ingredient9Font),$(Ingredient10Font)\",\"csvformat($(Ingredient1)),csvformat($(Ingredient2)),csvformat($(Ingredient3)),csvformat($(Ingredient4)),csvformat($(Ingredient5)),csvformat($(Ingredient6)),csvformat($(Ingredient7)),csvformat($(Ingredient8)),csvformat($(Ingredient9)),csvformat($(Ingredient10))\")",			
# 			"source": 'twsascii("$(Ingredient1Font),$(Ingredient2Font),$(Ingredient3Font),$(Ingredient4Font),$(Ingredient5Font),$(Ingredient6Font),$(Ingredient7Font),$(Ingredient8Font),$(Ingredient9Font),$(Ingredient10Font)","""csvformat4($(Ingredient1))"",""csvformat4($(Ingredient2))"",""csvformat4($(Ingredient3))"",""csvformat4($(Ingredient4))"",""csvformat4($(Ingredient5))"",""csvformat4($(Ingredient6))"",""csvformat4($(Ingredient7))"",""csvformat4($(Ingredient8))"",""csvformat4($(Ingredient9))"",""csvformat4($(Ingredient10))""")',			
# 			"target": "Plu.Ingredient"
# 		},
# 		{
# 			"condition": "isnotempty($(Multibarcode1))",
# 			"source": "1,$(Multibarcode1),2",
# 			"target": "Plu.MultiBarcode1"
# 		},
# 		{
# 			"condition": "isnotempty($(Multibarcode2))",
# 			"statements": [
# 				{
# 					"condition": "isnotempty($(NoLinkTo2DBarcodeText))",
# 					"source": "5,$(Multibarcode2),2",
# 					"target": "Plu.MultiBarcode2"
# 				},
# 				{
# 					"condition": "isempty($(NoLinkTo2DBarcodeText))",
# 					"source": "5,isnull($(MubCode2),$(CurLineNo)),3", 
# 					"target": "Plu.MultiBarcode2"
# 				},
# 				{
# 					"condition": "isempty($(NoLinkTo2DBarcodeText))",
# 					"source": "isnull($(MubCode2),$(CurLineNo))",
# 					"target": "Tbt.Code"
# 				},
# 				{
# 					"comment": "isnotnull(\"csvindex(1,$(Multibarcode2))\",\"21,\"\"csvindex(1,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(2,$(Multibarcode2))\",\"\n21,\"\"csvindex(2,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(3,$(Multibarcode2))\",\"\n21,\"\"csvindex(3,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(4,$(Multibarcode2))\",\"\n21,\"\"csvindex(4,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(5,$(Multibarcode2))\",\"\n21,\"\"csvindex(5,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(6,$(Multibarcode2))\",\"\n21,\"\"csvindex(6,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(7,$(Multibarcode2))\",\"\n21,\"\"csvindex(7,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(8,$(Multibarcode2))\",\"\n21,\"\"csvindex(8,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(9,$(Multibarcode2))\",\"\n21,\"\"csvindex(9,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(10,$(Multibarcode2))\",\"\n21,\"\"csvindex(10,$(Multibarcode2))\"\"\")",
# 					"condition": "isempty($(NoLinkTo2DBarcodeText))", 
# 					"source": 'twsascii("21,21,21,21,21,21,21,21,21,21","csvindex(1,csvformat($(Multibarcode2))),csvindex(2,csvformat($(Multibarcode2))),csvindex(3,csvformat($(Multibarcode2))),csvindex(4,csvformat($(Multibarcode2))),csvindex(5,csvformat($(Multibarcode2))),csvindex(6,csvformat($(Multibarcode2))),csvindex(7,csvformat($(Multibarcode2))),csvindex(8,csvformat($(Multibarcode2))),csvindex(9,csvformat($(Multibarcode2))),csvindex(10,csvformat($(Multibarcode2)))")',
# 					"target": "Tbt.Data"
# 				}
# 			]
# 		},

# 		{
# 			"condition": "isnotempty($(Text1))",
# 			"statements": [
# 				{"source": "isnull($(TexCode1),$(CurLineNo))",               "target": "Plu.LinkedText1No"},
# 				{"source": "isnull($(TexCode1),$(CurLineNo))",               "target": "Tex.Code.1"},
# 				{"source": 'isnull($(Text1Font),0),"$(Text1)"',              "target": "Tex.Name.1"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text2))",
# 			"statements": [
# 				{"source": "isnull($(TexCode2),$(CurLineNo))",               "target": "Plu.LinkedText2No"},
# 				{"source": "isnull($(TexCode2),$(CurLineNo))",               "target": "Tex.Code.2"},
# 				{"source": 'isnull($(Text2Font),0),"$(Text2)"',              "target": "Tex.Name.2"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text3))",
# 			"statements": [
# 				{"source": "isnull($(TexCode3),$(CurLineNo))",               "target": "Plu.LinkedText3No"},
# 				{"source": "isnull($(TexCode3),$(CurLineNo))",               "target": "Tex.Code.3"},
# 				{"source": 'isnull($(Text3Font),0),"$(Text3)"',              "target": "Tex.Name.3"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text4))",
# 			"statements": [
# 				{"source": "isnull($(TexCode4),$(CurLineNo))",               "target": "Plu.LinkedText4No"},
# 				{"source": "isnull($(TexCode4),$(CurLineNo))",               "target": "Tex.Code.4"},
# 				{"source": 'isnull($(Text4Font),0),"$(Text4)"',              "target": "Tex.Name.4"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text5))",
# 			"statements": [
# 				{"source": "isnull($(TexCode5),$(CurLineNo))",               "target": "Plu.LinkedText5No"},
# 				{"source": "isnull($(TexCode5),$(CurLineNo))",               "target": "Tex.Code.5"},
# 				{"source": 'isnull($(Text5Font),0),"$(Text5)"',              "target": "Tex.Name.5"}
# 			]
# 		},
			
# 		{
# 			"condition": "isnotempty($(Text6))",
# 			"statements": [
# 				{"source": "isnull($(TexCode6),$(CurLineNo))",               "target": "Plu.LinkedText6No"},
# 				{"source": "isnull($(TexCode6),$(CurLineNo))",               "target": "Tex.Code.6"},
# 				{"source": 'isnull($(Text6Font),0),"$(Text6)"',              "target": "Tex.Name.6"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text7))",
# 			"statements": [
# 				{"source": "isnull($(TexCode7),$(CurLineNo))",               "target": "Plu.LinkedText7No"},
# 				{"source": "isnull($(TexCode7),$(CurLineNo))",               "target": "Tex.Code.7"},
# 				{"source": 'isnull($(Text7Font),0),"$(Text7)"',              "target": "Tex.Name.7"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text8))",
# 			"statements": [
# 				{"source": "isnull($(TexCode8),$(CurLineNo))",               "target": "Plu.LinkedText8No"},
# 				{"source": "isnull($(TexCode8),$(CurLineNo))",               "target": "Tex.Code.8"},
# 				{"source": 'isnull($(Text8Font),0),"$(Text8)"',              "target": "Tex.Name.8"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text9))",
# 			"statements": [
# 				{"source": "isnull($(TexCode9),$(CurLineNo))",               "target": "Plu.LinkedText9No"},
# 				{"source": "isnull($(TexCode9),$(CurLineNo))",               "target": "Tex.Code.9"},
# 				{"source": 'isnull($(Text9Font),0),"$(Text9)"',              "target": "Tex.Name.9"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text10))",
# 			"statements": [
# 				{"source": "isnull($(TexCode10),$(CurLineNo))",               "target": "Plu.LinkedText10No"},
# 				{"source": "isnull($(TexCode10),$(CurLineNo))",               "target": "Tex.Code.10"},
# 				{"source": 'isnull($(Text10Font),0),"$(Text10)"',             "target": "Tex.Name.10"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(TraceabilityFlag))",
# 			"source": "$(TraceabilityFlag)",
# 			"target": "Plu.Traceability"
# 		},
# 		{
# 			"condition": "isnotempty($(TraceabilityNo))",
# 			"source": "$(TraceabilityNo)",
# 			"target": "Plu.TraceabilityLink"
# 		}
	],
	"sm120": [
		{
			"statement": StatementConvert.convertInfoForSm120
		},
			
# 		{"source": "$(PLUNo)",          "target": "Plu.PLUNo"},
# 		{"source": "$(UnitPrice)",      "target": "Plu.UnitPrice"},
# 		{
# 			"source": "isnull($(WeightingFlag),0)",
# 			"target": "Plu.WeightingFlag"
# 		},
# 		{
# 			"source": "isnull($(BarcodeFlag),0)",
# 			"target": "Plu.BarcodeFlagOfEanData"
# 		},
# 		{
# 			"source": "isnull($(PriceOverride),0)",
# 			"target": "Plu.UnitPriceOverrideFlag"
# 		},
# 		{
# 			"source": "isnull($(ItemCode),0000000000",
# 			"target": "Plu.ItemCode"
# 		},
			
# 		{
# 			"condition": "isnotempty($(PlaCode))",
# 			"statements": [
# 				{ "source": "$(PlaCode)",					"target": "Plu.PlaceNo" 	},
# 				{
# 					"condition": "isnotempty($(PlaceName))",
# 					"statements": [
# 						{"source": "$(PlaCode)",        "target": "Pla.Code.-1"},
# 						{"source": "1",                 "target": "Pla.LineNo.-1"},
# 						{"source": "2",                 "target": "Pla.DeleteFlag.-1"},
# 						{"source": "0",                 "target": "Pla.PlaceFlag.-1"},
# 						
# 						{"source": "$(PlaCode)",        "target": "Pla.Code.1",	},
# 						{"source": "1",                 "target": "Pla.LineNo.1"},
# 						{"source": 'isnull($(PlaceFont),21)',    "target": "Pla.PlaceFlag.1" },
# 						{"source": '$(PlaceName)',      "target": "Pla.PlaceName.1" }
# 					]
# 				}
# 			]
# 		},
			
# 		{
# 			"condition": "isnotempty($(Commodity1))",
# 			"statements": [
# 				{"source": '"csvformat($(Commodity1))"',   "target": "Plu.CommodityName1"},
# 				{"source": "isnull($(Commodity1Font),0)",  "target": "Plu.CommodityFont1"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Commodity2))",
# 			"statements": [
# 				{"source": '"csvformat($(Commodity2))"',   "target": "Plu.CommodityName2"},
# 				{"source": "isnull($(Commodity2Font),0)",  "target": "Plu.CommodityFont2"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Commodity3))",
# 			"statements": [
# 				{"source": '"csvformat($(Commodity3))"',   "target": "Plu.CommodityName3"},
# 				{"source": "isnull($(Commodity3Font),0)",  "target": "Plu.CommodityFont3"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Commodity4))",
# 			"statements": [
# 				{"source": '"csvformat($(Commodity4))"',   "target": "Plu.CommodityName4"},
# 				{"source": "isnull($(Commodity4Font),0)",  "target": "Plu.CommodityFont4"}
# 			]
# 		},

# 		{
# 			"source": "isnull($(BarcodeFormat),0)",
# 			"target": "Plu.BarcodeFormat"
# 		},
# 		{
# 			"source": "isnull($(LabelFormat1),0)",
# 			"target": "Plu.LabelFormat1"
# 		},
# 		{
# 			"condition": "isnotempty($(UsedByDate))",
# 			"statements": [
# 				{ "source": "1",             "target": "Plu.UsedByDateFlag" },
# 				{ "source": "$(UsedByDate)", "target": "Plu.UsedByDate" }
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(SellByDate))",
# 			"statements": [
# 				{ "source": "1",             "target": "Plu.SellByDateFlag" },
# 				{ "source": "$(SellByDate)", "target": "Plu.SellByDate" }
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(PackedByDate))",
# 			"statements": [
# 				{ "source": "1",               "target": "Plu.PackedDateFlag" },
# 				{ "source": "$(PackedByDate)", "target": "Plu.PackedDate" }
# 			]
# 		},
# 
# 		{
# 			"condition": "isnotempty($(PackedByTime))",
# 			"statements": [
# 				{ "source": "1",               "target": "Plu.PackedTimeFlag" },
# 				{ "source": "$(PackedByTime)", "target": "Plu.PackedTime" }
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(SellByTime))",
# 			"statements": [
# 				{ "source": "1",               "target": "Plu.SellByTimeFlag" },
# 				{ "source": "$(SellByTime)",   "target": "Plu.SellByTime" }
# 			]
# 		},
		
# 		{"source": "$(MGNo)",           "target": "Plu.MGNo"},
# 		{
# 			"source": "iif(equals($(BarcodeType),EAN),0,9",
# 			"target": "Plu.BarcodeTypeOfEanData"
# 		},
# 		{
# 			"condition": "isnotempty($(TraceabilityFlag))",
# 			"source": "$(TraceabilityFlag)",
# 			"target": "Plu.TraceabilityFlag"
# 		},
# 		{
# 			"condition": "isnotempty($(TraceabilityNo))",
# 			"source": "$(TraceabilityNo)",
# 			"target": "Plu.TraceabilityNo"
# 		},
# 		{"source": "isnull($(SpmCode),$(CurLineNo))",        "target": "Plu.SpecialMessageNo"},
# 		{"source": "isnull($(IngCode),$(CurLineNo))",        "target": "Plu.IngredientNo"},
# 		{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.-1"},
# 		{"source": "1",                                 "target": "Spm.LineNo.-1"},
# 		{"source": "2",                                 "target": "Spm.DeleteFlag.-1"},
# 		{
# 			"condition": "isnotempty($(SpecialMessage1))",
# 			"statements": [
# 				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.1"},
# 				{"source": "1",                                 "target": "Spm.LineNo.1"},
# 				{"source": '"csvformat($(SpecialMessage1))"',   "target": "Spm.Data.1"},
# 				{"source": "isnull($(SpecialMessage1Font),0)",  "target": "Spm.Flag.1"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(SpecialMessage2))",
# 			"statements": [
# 				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.2"},
# 				{"source": "2",                                 "target": "Spm.LineNo.2"},
# 				{"source": '"csvformat($(SpecialMessage2))"',   "target": "Spm.Data.2"},
# 				{"source": "isnull($(SpecialMessage2Font),0)",  "target": "Spm.Flag.2"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(SpecialMessage3))",
# 			"statements": [
# 				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.3"},
# 				{"source": "3",                                 "target": "Spm.LineNo.3"},
# 				{"source": '"csvformat($(SpecialMessage3))"',   "target": "Spm.Data.3"},
# 				{"source": "isnull($(SpecialMessage3Font),0)",  "target": "Spm.Flag.3"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(SpecialMessage4))",
# 			"statements": [
# 				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.4"},
# 				{"source": "4",                                 "target": "Spm.LineNo.4"},
# 				{"source": '"csvformat($(SpecialMessage4))"',   "target": "Spm.Data.4"},
# 				{"source": "isnull($(SpecialMessage4Font),0)",  "target": "Spm.Flag.4"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(SpecialMessage5))",
# 			"statements": [
# 				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.5"},
# 				{"source": "5",                                 "target": "Spm.LineNo.5"},
# 				{"source": '"csvformat($(SpecialMessage5))"',   "target": "Spm.Data.5"},
# 				{"source": "isnull($(SpecialMessage5Font),0)",  "target": "Spm.Flag.5"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(SpecialMessage6))",
# 			"statements": [
# 				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.6"},
# 				{"source": "6",                                 "target": "Spm.LineNo.6"},
# 				{"source": '"csvformat($(SpecialMessage6))"',   "target": "Spm.Data.6"},
# 				{"source": "isnull($(SpecialMessage6Font),0)",  "target": "Spm.Flag.6"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(SpecialMessage7))",
# 			"statements": [
# 				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.7"},
# 				{"source": "7",                                 "target": "Spm.LineNo.7"},
# 				{"source": '"csvformat($(SpecialMessage7))"',   "target": "Spm.Data.7"},
# 				{"source": "isnull($(SpecialMessage7Font),0)",  "target": "Spm.Flag.7"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(SpecialMessage8))",
# 			"statements": [
# 				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.8"},
# 				{"source": "8",                                 "target": "Spm.LineNo.8"},
# 				{"source": '"csvformat($(SpecialMessage8))"',   "target": "Spm.Data.8"},
# 				{"source": "isnull($(SpecialMessage8Font),0)",  "target": "Spm.Flag.8"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(SpecialMessage9))",
# 			"statements": [
# 				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.9"},
# 				{"source": "9",                                 "target": "Spm.LineNo.9"},
# 				{"source": '"csvformat($(SpecialMessage9))"',   "target": "Spm.Data.9"},
# 				{"source": "isnull($(SpecialMessage9Font),0)",  "target": "Spm.Flag.9"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(SpecialMessage10))",
# 			"statements": [
# 				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.10"},
# 				{"source": "10",                                "target": "Spm.LineNo.10"},
# 				{"source": '"csvformat($(SpecialMessage10))"',  "target": "Spm.Data.10"},
# 				{"source": "isnull($(SpecialMessage10Font),0)", "target": "Spm.Flag.10"}
# 			]
# 		},
# 		{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.-1"},
# 		{"source": "1",                                 "target": "Ing.LineNo.-1"},
# 		{"source": "2",                                 "target": "Ing.DeleteFlag.-1"},
# 		{
# 			"condition": "isnotempty($(Ingredient1))",
# 			"statements": [
# 				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.1"},
# 				{"source": "1",                                 "target": "Ing.LineNo.1"},
# 				{"source": '"csvformat($(Ingredient1))"',       "target": "Ing.Data.1"},
# 				{"source": "isnull($(Ingredient1Font),0)",      "target": "Ing.Flag.1"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Ingredient2))",
# 			"statements": [
# 				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.2"},
# 				{"source": "2",                                 "target": "Ing.LineNo.2"},
# 				{"source": '"csvformat($(Ingredient2))"',       "target": "Ing.Data.2"},
# 				{"source": "isnull($(Ingredient2Font),0)",      "target": "Ing.Flag.2"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Ingredient3))",
# 			"statements": [
# 				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.3"},
# 				{"source": "3",                                 "target": "Ing.LineNo.3"},
# 				{"source": '"csvformat($(Ingredient3))"',       "target": "Ing.Data.3"},
# 				{"source": "isnull($(Ingredient3Font),0)",      "target": "Ing.Flag.3"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Ingredient4))",
# 			"statements": [
# 				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.4"},
# 				{"source": "4",                                 "target": "Ing.LineNo.4"},
# 				{"source": '"csvformat($(Ingredient4))"',       "target": "Ing.Data.4"},
# 				{"source": "isnull($(Ingredient4Font),0)",      "target": "Ing.Flag.4"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Ingredient5))",
# 			"statements": [
# 				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.5"},
# 				{"source": "5",                                 "target": "Ing.LineNo.5"},
# 				{"source": '"csvformat($(Ingredient5))"',       "target": "Ing.Data.5"},
# 				{"source": "isnull($(Ingredient5Font),0)",      "target": "Ing.Flag.5"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Ingredient6))",
# 			"statements": [
# 				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.6"},
# 				{"source": "6",                                 "target": "Ing.LineNo.6"},
# 				{"source": '"csvformat($(Ingredient6))"',       "target": "Ing.Data.6"},
# 				{"source": "isnull($(Ingredient6Font),0)",      "target": "Ing.Flag.6"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Ingredient7))",
# 			"statements": [
# 				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.7"},
# 				{"source": "7",                                 "target": "Ing.LineNo.7"},
# 				{"source": '"csvformat($(Ingredient7))"',       "target": "Ing.Data.7"},
# 				{"source": "isnull($(Ingredient7Font),0)",      "target": "Ing.Flag.7"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Ingredient8))",
# 			"statements": [
# 				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.8"},
# 				{"source": "8",                                 "target": "Ing.LineNo.8"},
# 				{"source": '"csvformat($(Ingredient8))"',       "target": "Ing.Data.8"},
# 				{"source": "isnull($(Ingredient8Font),0)",      "target": "Ing.Flag.8"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Ingredient9))",
# 			"statements": [
# 				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.9"},
# 				{"source": "9",                                 "target": "Ing.LineNo.9"},
# 				{"source": '"csvformat($(Ingredient9))"',       "target": "Ing.Data.9"},
# 				{"source": "isnull($(Ingredient9Font),0)",      "target": "Ing.Flag.9"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Ingredient10))",
# 			"statements": [
# 				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.10"},
# 				{"source": "10",                                "target": "Ing.LineNo.10"},
# 				{"source": '"csvformat($(Ingredient10))"',      "target": "Ing.Data.10"},
# 				{"source": "isnull($(Ingredient10Font),0)",     "target": "Ing.Flag.10"}
# 			]
# 		},

# 		{
# 			"condition": "isnotempty($(Text1))",
# 			"statements": [
# 				{"source": "isnull($(TexCode1),$(CurLineNo))",  "target": "Tex.Code.-1"},
# 				{"source": "1",                                 "target": "Tex.LineNo.-1"},
# 				{"source": "2",                                 "target": "Tex.DeleteFlag.-1"},
# 				{"source": "isnull($(TexCode1),$(CurLineNo))",  "target": "Plu.TextNo1"},
# 				{"source": "isnull($(TexCode1),$(CurLineNo))",  "target": "Tex.Code.1"},
# 				{"source": "1",                                 "target": "Tex.LineNo.1"},
# 				{"source": '"csvformat($(Text1))"',             "target": "Tex.Data.1"},
# 				{"source": "isnull($(Text1Font),0)",            "target": "Tex.Flag.1"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text2))",
# 			"statements": [
# 				{"source": "isnull($(TexCode2),$(CurLineNo))",  "target": "Tex.Code.-2"},
# 				{"source": "1",                                 "target": "Tex.LineNo.-2"},
# 				{"source": "2",                                 "target": "Tex.DeleteFlag.-2"},
# 				{"source": "isnull($(TexCode2),$(CurLineNo))",  "target": "Plu.TextNo2"},
# 				{"source": "isnull($(TexCode2),$(CurLineNo))",  "target": "Tex.Code.2"},
# 				{"source": "1",                                 "target": "Tex.LineNo.2"},
# 				{"source": '"csvformat($(Text2))"',             "target": "Tex.Data.2"},
# 				{"source": "isnull($(Text2Font),0)",            "target": "Tex.Flag.2"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text3))",
# 			"statements": [
# 				{"source": "isnull($(TexCode3),$(CurLineNo))",  "target": "Tex.Code.-3"},
# 				{"source": "1",                                 "target": "Tex.LineNo.-3"},
# 				{"source": "2",                                 "target": "Tex.DeleteFlag.-3"},
# 				{"source": "isnull($(TexCode3),$(CurLineNo))",  "target": "Plu.TextNo3"},
# 				{"source": "isnull($(TexCode3),$(CurLineNo))",  "target": "Tex.Code.3"},
# 				{"source": "1",                                 "target": "Tex.LineNo.3"},
# 				{"source": '"csvformat($(Text3))"',             "target": "Tex.Data.3"},
# 				{"source": "isnull($(Text3Font),0)",            "target": "Tex.Flag.3"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text4))",
# 			"statements": [
# 				{"source": "isnull($(TexCode4),$(CurLineNo))",  "target": "Tex.Code.-4"},
# 				{"source": "1",                                 "target": "Tex.LineNo.-4"},
# 				{"source": "2",                                 "target": "Tex.DeleteFlag.-4"},
# 				{"source": "isnull($(TexCode4),$(CurLineNo))",  "target": "Plu.TextNo4"},
# 				{"source": "isnull($(TexCode4),$(CurLineNo))",  "target": "Tex.Code.4"},
# 				{"source": "1",                                 "target": "Tex.LineNo.4"},
# 				{"source": '"csvformat($(Text4))"',             "target": "Tex.Data.4"},
# 				{"source": "isnull($(Text4Font),0)",            "target": "Tex.Flag.4"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text5))",
# 			"statements": [
# 				{"source": "isnull($(TexCode5),$(CurLineNo))",  "target": "Tex.Code.-5"},
# 				{"source": "1",                                 "target": "Tex.LineNo.-5"},
# 				{"source": "2",                                 "target": "Tex.DeleteFlag.-5"},
# 				{"source": "isnull($(TexCode5),$(CurLineNo))",  "target": "Plu.TextNo5"},
# 				{"source": "isnull($(TexCode5),$(CurLineNo))",  "target": "Tex.Code.5"},
# 				{"source": "1",                                 "target": "Tex.LineNo.5"},
# 				{"source": '"csvformat($(Text5))"',             "target": "Tex.Data.5"},
# 				{"source": "isnull($(Text5Font),0)",            "target": "Tex.Flag.5"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text6))",
# 			"statements": [
# 				{"source": "isnull($(TexCode6),$(CurLineNo))",  "target": "Tex.Code.-6"},
# 				{"source": "1",                                 "target": "Tex.LineNo.-6"},
# 				{"source": "2",                                 "target": "Tex.DeleteFlag.-6"},
# 				{"source": "isnull($(TexCode6),$(CurLineNo))",  "target": "Plu.TextNo6"},
# 				{"source": "isnull($(TexCode6),$(CurLineNo))",  "target": "Tex.Code.6"},
# 				{"source": "1",                                 "target": "Tex.LineNo.6"},
# 				{"source": '"csvformat($(Text6))"',             "target": "Tex.Data.6"},
# 				{"source": "isnull($(Text6Font),0)",            "target": "Tex.Flag.6"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text7))",
# 			"statements": [
# 				{"source": "isnull($(TexCode7),$(CurLineNo))",  "target": "Tex.Code.-7"},
# 				{"source": "1",                                 "target": "Tex.LineNo.-7"},
# 				{"source": "2",                                 "target": "Tex.DeleteFlag.-7"},
# 				{"source": "isnull($(TexCode7),$(CurLineNo))",  "target": "Plu.TextNo7"},
# 				{"source": "isnull($(TexCode7),$(CurLineNo))",  "target": "Tex.Code.7"},
# 				{"source": "1",                                 "target": "Tex.LineNo.7"},
# 				{"source": '"csvformat($(Text7))"',             "target": "Tex.Data.7"},
# 				{"source": "isnull($(Text7Font),0)",            "target": "Tex.Flag.7"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text8))",
# 			"statements": [
# 				{"source": "isnull($(TexCode8),$(CurLineNo))",  "target": "Tex.Code.-8"},
# 				{"source": "1",                                 "target": "Tex.LineNo.-8"},
# 				{"source": "2",                                 "target": "Tex.DeleteFlag.-8"},
# 				{"source": "isnull($(TexCode8),$(CurLineNo))",  "target": "Plu.TextNo8"},
# 				{"source": "isnull($(TexCode8),$(CurLineNo))",  "target": "Tex.Code.8"},
# 				{"source": "1",                                 "target": "Tex.LineNo.8"},
# 				{"source": '"csvformat($(Text8))"',             "target": "Tex.Data.8"},
# 				{"source": "isnull($(Text8Font),0)",            "target": "Tex.Flag.8"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text9))",
# 			"statements": [
# 				{"source": "isnull($(TexCode9),$(CurLineNo))",  "target": "Tex.Code.-9"},
# 				{"source": "1",                                 "target": "Tex.LineNo.-9"},
# 				{"source": "2",                                 "target": "Tex.DeleteFlag.-9"},
# 				{"source": "isnull($(TexCode9),$(CurLineNo))",  "target": "Plu.TextNo9"},
# 				{"source": "isnull($(TexCode9),$(CurLineNo))",  "target": "Tex.Code.9"},
# 				{"source": "1",                                 "target": "Tex.LineNo.9"},
# 				{"source": '"csvformat($(Text9))"',             "target": "Tex.Data.9"},
# 				{"source": "isnull($(Text9Font),0)",            "target": "Tex.Flag.9"}
# 			]
# 		},
# 		{
# 			"condition": "isnotempty($(Text10))",
# 			"statements": [
# 				{"source": "isnull($(TexCode10),$(CurLineNo))", "target": "Tex.Code.-10"},
# 				{"source": "1",                                 "target": "Tex.LineNo.-10"},
# 				{"source": "2",                                 "target": "Tex.DeleteFlag.-10"},
# 				{"source": "isnull($(TexCode10),$(CurLineNo))", "target": "Plu.TextNo10"},
# 				{"source": "isnull($(TexCode10),$(CurLineNo))", "target": "Tex.Code.10"},
# 				{"source": "1",                                 "target": "Tex.LineNo.10"},
# 				{"source": '"csvformat($(Text10))"',            "target": "Tex.Data.10"},
# 				{"source": "isnull($(Text10Font),0)",           "target": "Tex.Flag.10"}
# 			]
# 		},

# 		{
# 			"condition": "isnotempty($(Multibarcode1))",
# 			"statements": [
# 				{"source": "isnull($(MubCode1),$(CurLineNo))", "target": "Plu.Multibarcode1No"},
# 				{"source": "isnull($(MubCode1),$(CurLineNo))", "target": "Mub.Code.1"},
# 				{"source": "2",                                "target": "Mub.MultiBarcodeType.1"},
# 				{"source": "1",                                "target": "Mub.BarcodeType.1"},
# 				{"source": "$(Multibarcode1)",                 "target": "Mub.Data.1"}
# 			]
# 		},

# 		{
# 			"condition": "isnotempty($(Multibarcode2))",
# 			"statements": [
# 				{"source": "isnull($(TbtCode),$(CurLineNo))",   "target": "Tbt.Code.-1"},
# 				{"source": "1",                                 "target": "Tbt.LineNo.-1"},
# 				{"source": "2",                                 "target": "Tbt.DeleteFlag.-1"},
# 
# 				{"source": "isnull($(MubCode2),$(CurLineNo))", "target": "Plu.Multibarcode2No"},
# 				{"source": "isnull($(MubCode2),$(CurLineNo))", "target": "Mub.Code.2"},
# 				{"source1": "3",                               "target1": "Mub.MultiBarcodeType.2"},
# 				{
# 					"source": "iif(isempty($(NoLinkTo2DBarcodeText)),3,2)",
# 					"target": "Mub.MultiBarcodeType.2"
# 				},
# 				{"source": "5",                                "target": "Mub.BarcodeType.2"},
# 				{
# 					"condition": "isempty($(NoLinkTo2DBarcodeText))",
# 					"source": "isnull($(TbtCode),$(CurLineNo))",
# 					"target": "Mub.Link2DBarcodeTextNo.2"
# 				},
# 				{
# 					"condition": "isnotempty($(NoLinkTo2DBarcodeText))",
# 					"source": "$(Multibarcode2)",
# 					"target": "Mub.Data.2"
# 				},
# 				{
# 					"condition1": "great(csvcount($(Multibarcode2)), 0)",
# 					"condition": "and(isempty($(NoLinkTo2DBarcodeText)),great(csvcount($(Multibarcode2)),0))",
# 					"statements": [
# 						{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.1"},
# 						{"source": "1",                                "target": "Tbt.LineNo.1"},
# 						{"source": '"csvindex(1,$(Multibarcode2))"',   "target": "Tbt.Data.1"},
# 						{
# 							"condition": "great(csvcount($(Multibarcode2)), 1)",
# 							"statements": [
# 								{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.2"},
# 								{"source": "2",                                "target": "Tbt.LineNo.2"},
# 								{"source": '"csvindex(2,$(Multibarcode2))"',   "target": "Tbt.Data.2"},
# 								{
# 									"condition": "great(csvcount($(Multibarcode2)), 2)",
# 									"statements": [
# 										{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.3"},
# 										{"source": "3",                                "target": "Tbt.LineNo.3"},
# 										{"source": '"csvindex(3,$(Multibarcode2))"',   "target": "Tbt.Data.3"},
# 										{
# 											"condition": "great(csvcount($(Multibarcode2)), 3)",
# 											"statements": [
# 												{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.4"},
# 												{"source": "4",                                "target": "Tbt.LineNo.4"},
# 												{"source": '"csvindex(4,$(Multibarcode2))"',   "target": "Tbt.Data.4"},
# 												{
# 													"condition": "great(csvcount($(Multibarcode2)), 4)",
# 													"statements": [
# 														{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.5"},
# 														{"source": "5",                                "target": "Tbt.LineNo.5"},
# 														{"source": '"csvindex(5,$(Multibarcode2))"',   "target": "Tbt.Data.5"},
# 														{
# 															"condition": "great(csvcount($(Multibarcode2)), 5)",
# 															"statements": [
# 																{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.6"},
# 																{"source": "6",                                "target": "Tbt.LineNo.6"},
# 																{"source": '"csvindex(6,$(Multibarcode2))"',   "target": "Tbt.Data.6"},
# 																{
# 																	"condition": "great(csvcount($(Multibarcode2)), 6)",
# 																	"statements": [
# 																		{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.7"},
# 																		{"source": "7",                                "target": "Tbt.LineNo.7"},
# 																		{"source": '"csvindex(7,$(Multibarcode2))"',   "target": "Tbt.Data.7"},
# 																		{
# 																			"condition": "great(csvcount($(Multibarcode2)), 7)",
# 																			"statements": [
# 																				{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.8"},
# 																				{"source": "8",                                "target": "Tbt.LineNo.8"},
# 																				{"source": '"csvindex(8,$(Multibarcode2))"',   "target": "Tbt.Data.8"},
# 																				{
# 																					"condition": "great(csvcount($(Multibarcode2)), 8)",
# 																					"statements": [
# 																						{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.9"},
# 																						{"source": "9",                                "target": "Tbt.LineNo.9"},
# 																						{"source": '"csvindex(9,$(Multibarcode2))"',   "target": "Tbt.Data.9"},
# 																						{
# 																							"condition": "great(csvcount($(Multibarcode2)), 9)",
# 																							"statements": [
# 																								{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.10"},
# 																								{"source": "10",                               "target": "Tbt.LineNo.10"},
# 																								{"source": '"csvindex(10,$(Multibarcode2))"',  "target": "Tbt.Data.10"}
# 																							]
# 																						}
# 																					]
# 																				}
# 																			]
# 																		}
# 																	]
# 																}
# 															]
# 														}
# 													]
# 												}
# 											]
# 										}
# 									]
# 								}
# 							]
# 						}
# 					]
# 				}
# 			]
# 		}

	]
}

class ScalesConverter():
	def __init__(self, conv=ConvertDesc_PLU):
		if isinstance(conv, str):
			self.converter_node = common.get_json_from_string(conv)
		else:
			self.converter_node = conv
		self.strParser = strparser.StrParser()
		self.masterFactory = {
			"sm110": libsm110.entity.MasterFactory(),
			"sm120": libsm120.entity.MasterFactory(),
		}
		
	def easyImportMaster(
			self, 
			scale_list,
			csv_file_path, 
			json_fmt_file_path,
			str_mg_no="997",
			json_scale_group_file = "",
			json_filter_file = ""):

		self.lst_sm120 = []
		self.lst_sm110 = []

		if isinstance(scale_list, (str, unicode)):
			scale_list = scale_list.split(',')


		common.log_info("Scale List:" + ",".join(scale_list))

		for scale in scale_list:
			scale = scale.strip()
			if not scale:
				continue
			
			scale_info = scale.split(':')
			scale = scale_info[0]
			if len(scale_info) > 1:
				scale_type = scale_info[1]
			else:
				scale_type = "sm120"
				
			if scale_type=="sm120":
				self.lst_sm120.append(scale)
			else:
				self.lst_sm110.append(scale)


		try:
			json_data = common.get_json_from_file(json_fmt_file_path)
		except:
			common.log_err(traceback.format_exc())
			return False

		self.createMasterList = {}
		
		self.createMasterList["sm110"]={}
		self.createMasterList["sm120"]={}
		
		#过滤
		self.dataFilter = datafilter.DataFilter()
		globalVals = {"ScaleGroupNo": str_mg_no}
		self.dataFilter.set_glob_vars(globalVals)

		if json_filter_file:
			json_data2 = common.common.get_json_from_file(json_filter_file)  # @UndefinedVariable
			if isinstance(json_data2, list):
				self.dataFilter.set_expressions([dat for dat in json_data2])
				
		self.createMasterList["FromCSV"] = {}
		self.createMasterList["FromCSV"]["infos"] = []
		for fmt in json_data:
			source_expr  = fmt["source_expr"]
			target_field = fmt["target_field"]
			sp_data = target_field.split(".")
			fieldName = sp_data[0]
			if len(sp_data) > 1:
				lineNo = int(sp_data[1])
			else:
				lineNo = 0

			self.createMasterList["FromCSV"]["infos"].append(
				{
					"source_expression": source_expr,
					"full_field_name":   target_field,
					"field_name":        fieldName,
					"line_no":           lineNo,
				}
			)
		
		common.log_info("Start to parse %s ..." % csv_file_path)
		
		try:
			csvreader.SmCsvReader().read_line_by_line(
				csv_file_path,
				self.process_line,
				head = common.get_title_onoff())
		except:
			common.log_err(traceback.format_exc())
			return False

		common.log_info("End Parsing csv file...")
		
		success_scale_list = []
		failed_scale_list = []


		#多线程方法=======>
		def send_to_scale_sm120(scale, lst_data, result):
			common.log_info("Start to download file To %s" % scale.ip)
			
			scale.connect()
			if not scale.connected:
				common.log_err( "Failed To Connect To %s ..." % scale.ip)
				common.log2_err( "Failed To Connect To %s ..." % scale.ip)
				return
			
			has_error = False

			for sm120_data in lst_data:
				if not scale.send_file(sm120_data[0], sm120_data[1]):
					common.log_err( "Failed To Download %s To %s ..." % (sm120_data[1],scale.ip))
					common.log2_err( "Failed To Download %s To %s ..." % (sm120_data[1],scale.ip))
					has_error = True

			if isinstance(result, list) and len(result) > 0:
				if not has_error:
					result[0] = 0
				else:
					result[0] = 1
			

		sm120_results = []
		for scale_ip in self.lst_sm120:
			list_sm120_data = []
			scale = libsm120.digiscale.DigiSm120(scale_ip)
			for clsName, template_infos in self.createMasterList["sm120"].items():
				created_csv_file = scale.create_csv(template_infos["Master"])
				if created_csv_file:
					list_sm120_data.append((template_infos["Master"], created_csv_file))
					
			result = [-1]
			scl_thd = Thread(target=send_to_scale_sm120, args=(scale, list_sm120_data, result))
			sm120_results.append((scl_thd, scale_ip, result))
			scl_thd.start()
			
		for sm120_entry in sm120_results:
			sm120_entry[0].join()
			scale_ip = sm120_entry[1]
			if sm120_entry[2][0] == 0:	#send is ok
				allMasters = ",".join([clsName for clsName in self.createMasterList["sm120"]])
				common.log_info( "Downloading %s To %s Successfully..." % (allMasters, scale_ip) )
				common.log2_info( "Downloading %s To %s Successfully..." % (allMasters, scale_ip) )
				success_scale_list.append( scale_ip )
			else:
				failed_scale_list.append( scale_ip )

			
		def send_to_scale_sm110(scale, result):
			has_error = False
			for clsName, template_infos in self.createMasterList["sm110"].items():
				if not scale.upload_master(template_infos["Master"]):
					common.log_err( "Downloading %s To %s Failed..." % (clsName,scale.hostname))
					common.log2_err( "Downloading %s To %s Failed..." % (clsName,scale.hostname))
					has_error = True

			if isinstance(result, list) and len(result) > 0:
				if not has_error:
					result[0] = 0
				else:
					result[0] = 1
			
		sm110_results = []
		for scale_ip in self.lst_sm110:
			scale = libsm110.smtws.smtws(scale_ip)
			
			result = [-1]
			scl_thd = Thread(target=send_to_scale_sm110, args=(scale, result))
			sm110_results.append((scl_thd, scale_ip, result))
			scl_thd.start()
			
			
		for sm110_entry in sm110_results:
			sm110_entry[0].join()
			scale_ip = sm110_entry[1]
			if sm110_entry[2][0] == 0:	#send is ok
				allMasters = ",".join([clsName for clsName in self.createMasterList["sm110"]])
				common.log_info( "Downloading %s To %s Successfully..." % (allMasters, scale_ip) )
				common.log2_info( "Downloading %s To %s Successfully..." % (allMasters, scale_ip) )
				success_scale_list.append( scale_ip )
			else:
				failed_scale_list.append( scale_ip )

		try:				
			with open('digicon_failed_scale.log', 'w') as fp1:
				fp1.write('\r\n'.join(failed_scale_list))
		except Exception, e:
			common.log_err(e)
		#多线程方法<=========
			
		"""
		#单线程处理==========>
		for scale_ip in self.lst_sm120:
			list_sm120_data = []
			scale = libsm120.digiscale.DigiSm120(scale_ip)
			for clsName, template_infos in self.createMasterList["sm120"].items():
				created_csv_file = scale.create_csv(template_infos["Master"])
				if created_csv_file:
					list_sm120_data.append((template_infos["Master"], created_csv_file))

			common.log_info("Start to download file To %s" % scale_ip)
			scale.connect()
			if not scale.connected:
				#common.log_err("Failed to Connect to Scale %s!" % scale_ip)
				continue
			
			has_error = False
			for sm120_data in list_sm120_data:
				if not scale.send_file(sm120_data[0], sm120_data[1]):
					common.log_err( "Failed To Download %s To %s ..." % (sm120_data[1],scale_ip))
					common.log2_err( "Failed To Download %s To %s ..." % (sm120_data[1],scale_ip))
					has_error = True
			if not has_error:
				allMasters = ",".join([clsName for clsName in self.createMasterList["sm120"]])
				common.log_info( "Downloading %s To %s Successfully..." % (allMasters, scale_ip) )
				common.log2_info( "Downloading %s To %s Successfully..." % (allMasters, scale_ip) )
				success_scale_list.append( scale_ip )
		
		for scale_ip in self.lst_sm110:
			has_error = False
			scale = libsm110.smtws.smtws(scale_ip)
			for clsName, template_infos in self.createMasterList["sm110"].items():
				if not scale.upload_master(template_infos["Master"]):
					common.log_err( "Downloading %s To %s Failed..." % (clsName,scale_ip))
					common.log2_err( "Downloading %s To %s Failed..." % (clsName,scale_ip))
					has_error = True
			if not has_error:
				allMasters = ",".join([clsName for clsName in self.createMasterList["sm110"]])
				common.log_info( "Downloading %s To %s Successfully..." % (allMasters, scale_ip) )
				common.log2_info( "Downloading %s To %s Successfully..." % (allMasters, scale_ip) )
				success_scale_list.append( scale_ip )
		#单线程处理<==========
		"""
		

# 		if len(self.lst_sm110) > 0:
# 			for scalefile in self.createMasterList["sm110"]:
# 				del self.createMasterList["sm110"][scalefile]["Master"]
# 		if len(self.lst_sm120) > 0:
# 			for scalefile in self.createMasterList["sm120"]:
# 				del self.createMasterList["sm120"][scalefile]["Master"]

		if len(success_scale_list) == len(scale_list):
			return True
		else:
			return False
		#return True


	def process_line(self, curLineNo, cur_row):

		#1.导入csv
		#2.解析成秤的格式

		self.dataFilter.set_field_list(cur_row)
		if self.dataFilter.is_filtered(): return True
		gv = {"CurLineNo": str(curLineNo + 1)}

		#导入csv
		template_infos = self.createMasterList["FromCSV"]
		newLines = {}
		for template_info in template_infos["infos"]:
			iLineNo = int(template_info["line_no"])
			if not newLines.has_key(iLineNo):
				newLines[iLineNo] = {}
			result = self.strParser.eval(
				0, 
				expr=template_info["source_expression"], 
				fieldByIndex=cur_row, 
				fieldByName={}, 
				globalName=gv, 
				resetPos=True).decode(sys.getdefaultencoding())

			if not newLines[iLineNo].has_key(template_info["field_name"]):
				newLines[iLineNo][template_info["field_name"]] = [""]
			newLines[iLineNo][template_info["field_name"]][0] = result
				
		dic_data = dict((key, value[0]) for key, value in newLines[0].items() if isinstance(key, (str, unicode)) )
		value_list={
			"sm110": {},
			"sm120": {}
		}

		
		def setValueList(master_factory, master_list, scale_type, master_name, field_name, value = None, line_no = 0):
			if not master_list.has_key(master_name):
				master_list[master_name] = {}
				master_list[master_name]["Master"] = master_factory.createMaster(master_name)
			if not value_list[scale_type].has_key(master_name):
				value_list[scale_type][master_name] = {}
			if not value_list[scale_type][master_name].has_key(line_no):
				value_list[scale_type][master_name][line_no] = master_list[master_name]["Master"].create_row()
			value_list[scale_type][master_name][line_no][field_name][0] = value

		def append_line(src,dst,scale_type):
			result = self.strParser.eval(
				0, 
				expr=src, 
				fieldByIndex=[], 
				fieldByName=dic_data, 
				globalName=gv, 
				resetPos=True).decode(sys.getdefaultencoding())
				
			tgt = dst.split('.')
			tgt_table = tgt[0]
			tgt_field = tgt[1]
			tgt_lineno = 0
			if len(tgt) > 2:
				tgt_lineno = int(tgt[2])
				
# 			if not self.createMasterList[scale_type].has_key(tgt_table):
# 				self.createMasterList[scale_type][tgt_table] = {}
# 				self.createMasterList[scale_type][tgt_table]["Master"] = self.masterFactory[scale_type].createMaster(tgt_table)
# 		
# 			if not value_list[scale_type].has_key(tgt_table):
# 				value_list[scale_type][tgt_table] = {}
# 
# 			if not value_list[scale_type][tgt_table].has_key(tgt_lineno):
# 				value_list[scale_type][tgt_table][tgt_lineno] = self.createMasterList[scale_type][tgt_table]["Master"].create_row()
				
# 			value_list[scale_type][tgt_table][tgt_lineno][tgt_field][0] = result
			setValueList(
				master_factory = self.masterFactory[scale_type],
				master_list = self.createMasterList[scale_type],
				scale_type = scale_type,
				master_name = tgt_table,
				field_name = tgt_field,
				line_no = tgt_lineno,
				value = result)
			
		def parse_recur(curNode, scale_type):
			master_list = self.createMasterList[scale_type]
			master_factory = self.masterFactory[scale_type]
			
			def set_value_list(master_name, field_name, value = None, line_no = 0):
				setValueList(
					master_factory,
					master_list,
					scale_type, 
					master_name, 
					field_name, 
					value, 
					line_no)
			
			
			src       = curNode.get("source", None)
			dst       = curNode.get("target", None)
			cond      = curNode.get("condition", None)
			statments = curNode.get("statements", None)
			stmtcvt   = curNode.get("statement", None)
			if cond and "TRUE" != self.strParser.eval(
					0,
					expr=cond, 
					fieldByIndex=[], 
					fieldByName=dic_data, 
					globalName=gv,
					resetPos=True):
				return

			if src and dst:
				append_line(src, dst, scale_type)
			if isinstance(statments, list):
				for statement in statments:
					parse_recur(statement, scale_type)
			
			if isfunction(stmtcvt):
				stmtcvt(
					cur_line_no = curLineNo + 1,
					csv_values = dic_data,
					cbSetValueList = set_value_list
				)

#  		beg = time.time(); #testonly

		#统一格式分派给秤
		""
		if len(self.lst_sm110)>0:
			for value in self.converter_node["sm110"]:
				parse_recur(value, "sm110")
			for key, value in value_list["sm110"].items():
				sorted_line_no = sorted(value)
				for line_no in sorted_line_no:
					self.createMasterList["sm110"][key]["Master"].add_row(value[line_no])

		if len(self.lst_sm120)>0:
			for value in self.converter_node["sm120"]:
				parse_recur(value, "sm120")
			for key, value in value_list["sm120"].items():
				sorted_line_no = sorted(value)
				for line_no in sorted_line_no:
					self.createMasterList["sm120"][key]["Master"].add_row(value[line_no])



