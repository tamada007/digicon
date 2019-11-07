# encoding=gbk

import os
import sys
import smtws
import common.common
import common.scalegroup
import common.csvreader
import common.datafilter
import common.strparser
import master
import entity
import enum
import const
import traceback
import csv
import StringIO


class Easy:
    def __init__(self, ip):
        self.ip = ip

    # 导入的csv中删除秤上数据
    def deleteFromCSV(
            self,
            report_file_name,
            in_csv_file,
            with_title=True):
        with open(in_csv_file) as fp1:
            # key_lines = [x.rstrip("\n") for x in fp1.readlines()]
            key_lines = fp1.readlines()
            if with_title:
                key_lines = key_lines[1:]

            key_fields = []
            for key_line in key_lines:
                key_array = csv.reader(StringIO.StringIO(key_line.rstrip("\n"))).next()
                key_fields.append(key_array[0])

            key_lines = key_fields

            trans_table = {
                "Plu": "Plu",
                "PLU Transaction": "Ptr",
                "Real Time Total Buffer": "Rtt",
                "Real Time Buffer": "Rtb"
            }
            if report_file_name not in trans_table:
                common.common.log_err("%s is not supported" % report_file_name)
                return False
            rep_master = entity.MasterFactory().createMaster(trans_table[report_file_name])
            sm110 = smtws.smtws(self.ip)
            # return sm110.delete_records(rep_master.file_no, key_lines)
            delete_result = sm110.delete_records(rep_master.file_no, key_lines)
            if not delete_result:
                common.common.log_err("Failed to delete Report records from %s" % self.ip)
            else:
                common.common.log_info("Deleted Report records from %s" % self.ip)

            return delete_result

    def exportCSV(
            self,
            export_template_file="",
            export_template_info="",
            export_csv_file="",
            title=False,
            encoding=sys.getdefaultencoding(),
            append=True):

        json_data = {}
        if export_template_file:
            json_data = common.common.get_json_from_file(export_template_file)
        elif export_template_info:
            if isinstance(export_template_info, str):
                json_data = common.common.get_json_from_string(export_template_info)
            else:
                json_data = export_template_info

        sql = json_data.get("SQL", "")
        target_tables = json_data.get("Tables", "")
        target_fields = json_data.get("Fields", [])

        table_list = target_tables.split(",")

        sm110 = smtws.smtws(self.ip)
        master_list = map(lambda x: entity.MasterFactory().createMaster(x.strip()), table_list)

        for m in master_list:
            if not sm110.download_master(m):
                common.common.log_err("Retrieving %s From %s Failed" % (m.name, self.ip))
                return False

        conn = common.common.open_sqlite_db(const.db_name)
        cursor = conn.cursor()
        cursor.execute(sql)
        names = [(index, desc[0]) for index, desc in enumerate(cursor.description)]
        field_names = [data[1] for data in names]
        # print field_names
        if append:
            open_mode = "ab"
        else:
            open_mode = "wb"
        with open(export_csv_file, open_mode) as fp:
            if title:
                # 如果导出文件已经存在，且是append模式，就不加标题行了
                if append and os.path.isfile(export_csv_file) and os.path.getsize(export_csv_file) > 0:
                    pass
                else:
                    # fp.write(",".join(field_names) + "\r\n")
                    # fp.write(",".join(field_names).decode('utf8').encode(encoding) + "\r\n")
                    # 20191106
                    fp.write(",".join(field_names) + "\r\n")
            for row in cursor:
                # print row
                # cells = [unicode(cell).encode(encoding) for cell in row]
                # 20191106
                cells = [str(cell) for cell in row]

                target_cells = []
                for target_field in target_fields:
                    strpar = common.strparser.StrParser(target_field, cells)
                    target_cells.append(strpar.eval(0))

                fp.write(",".join(target_cells) + "\r\n")

        common.common.log_info("Exporting From %s To %s Successfully" % (self.ip, export_csv_file))
        return True

    def easyDeleteFile(self, mas_name):
        master_list = mas_name.split(',')
        sm110 = smtws.smtws(self.ip)
        for master_name in master_list:
            master = entity.MasterFactory().createMaster(master_name)
            if master:
                if not sm110.delete_master(master):
                    return False
            else:
                fileNo = int(master_name, 16)
                if not sm110.delete_file(fileNo):
                    return False
        return True

    def easyReceiveFile(self, mas_name, out_file_name):
        master_list = mas_name.split(',')
        sm110 = smtws.smtws(self.ip)
        for master_name in master_list:
            master = entity.MasterFactory().createMaster(master_name)
            if master:
                out_temp_file = sm110.download_file(master.file_no)
                if out_temp_file:
                    # print "rename", out_temp_file, "to", out_file_name
                    if os.path.exists(out_file_name):
                        os.remove(out_file_name)
                    os.rename(out_temp_file, out_file_name)
                else:
                    return False
            else:
                return False
        return True

    def easySendFile(self, mas_name, in_file_name):
        master_list = mas_name.split(',')
        sm110 = smtws.smtws(self.ip)
        result = True
        for master_name in master_list:
            master = entity.MasterFactory().createMaster(master_name)
            if master:
                result = result and sm110.upload_file(master.file_no, in_file_name)
            else:
                result = False
        return result


    def easyRecvPrintFormat(self, json_file_path):
        prfmt = entity.PrfMaster()
        sm110 = smtws.smtws(self.ip)

        if not sm110.download_master(prfmt):
            common.common.log_err("Error On receiving Data From Scale")
            return False

        prf_all_data = prfmt.get_all_data()
        prfJsonArray = []

        for prf_cur_row in prf_all_data:
            prf_code = prf_cur_row[enum.PRFField.CODE][0]
            prfJsonNode = {}
            prfJsonNode["Code"] = prf_code
            prfJsonNode["Width"] = prf_cur_row[enum.PRFField.PRINT_FORMAT_WIDTH][0]
            prfJsonNode["Height"] = prf_cur_row[enum.PRFField.PRINT_FORMAT_HEIGHT][0]

            pffJsonArray = []
            cur_pos_field = 1
            cur_pos_row = cur_pos_field + enum.PRFField.PRINT_FORMAT_STATUS
            while prf_cur_row.has_key(cur_pos_row):
                if prf_cur_row[cur_pos_row][0]:
                    pffJsonNode = {}
                    if const.printFormatIndexList.has_key(cur_pos_field):
                        pffJsonNode["Field"] = const.printFormatIndexList[cur_pos_field]
                        pffJsonNode["XPosition"] = prf_cur_row[cur_pos_row][0].get("x", 0)
                        pffJsonNode["YPosition"] = prf_cur_row[cur_pos_row][0].get("y", 0)
                        pffJsonNode["PrintStatus"] = prf_cur_row[cur_pos_row][0].get("status", 0)
                        pffJsonNode["Width"] = prf_cur_row[cur_pos_row][0].get("w", 0)
                        pffJsonNode["Height"] = prf_cur_row[cur_pos_row][0].get("h", 0)

                        pffJsonArray.append(pffJsonNode)

                cur_pos_field += 1
                cur_pos_row += 1

            prfJsonNode["Fields"] = pffJsonArray
            prfJsonArray.append(prfJsonNode)

        common.common.save_json_to_file(json_file_path, prfJsonArray)
        common.common.log_info("%s Created" % json_file_path)

    def easySendPrintFormat(self, fmt_json_file_path):
        prfmt = entity.PrfMaster()
        json_data = common.common.get_json_from_file(fmt_json_file_path)
        for prf in json_data:
            strCode = prf.get("Code", "0")
            strWidth = prf.get("Width", "0")
            strHeight = prf.get("Height", "0")
            strAngle = prf.get("Angle", "0")

            prf_new_row = prfmt.create_row()
            # prfmt.conv_csv_to_cell(prf_new_row, force_create = True)
            prf_new_row[enum.PRFField.CODE][0] = strCode
            prf_new_row[enum.PRFField.PRINT_FORMAT_WIDTH][0] = strWidth
            prf_new_row[enum.PRFField.PRINT_FORMAT_HEIGHT][0] = strHeight
            prf_new_row[enum.PRFField.PRINT_FORMAT_STATUS][0] = "00000000 00000010"

            for fieldNode in prf.get("Fields", []):
                strField = fieldNode.get("Field", "")
                iYPosition = fieldNode.get("YPosition", "0")
                iLabelType = fieldNode.get("LabelType", "0")
                iXPosition = fieldNode.get("XPosition", "0")
                iAngle = fieldNode.get("Angle", "0")
                iPrintStatus = fieldNode.get("PrintStatus", "0")
                iCharacterSize = fieldNode.get("YPosition", "0")
                iWidth = fieldNode.get("Width", "0")
                iHeight = fieldNode.get("Height", "0")
                iThickness = fieldNode.get("Thickness", "0")
                iX1Position = fieldNode.get("X1Position", "0")
                iY1Position = fieldNode.get("Y1Position", "0")
                iLinkedFileNo = fieldNode.get("LinkedFileNo", "0")
                iLinkedFileSouce = fieldNode.get("LinkedFileSource", "0")
                iCharacterSizex2x4 = fieldNode.get("CharacterSizex2x4", "0")
                iCentType = fieldNode.get("CentType", "0")
                iAutoSizing = fieldNode.get("AutoSizing", "0")

                iFieldNo = const.printFormatIndexListStringList.get(strField, -1)
                if iFieldNo == -1: continue
                base_pos = enum.PRFField.PRINT_FORMAT_STATUS
                if prf_new_row.has_key(iFieldNo + base_pos):
                    cur_pos = base_pos + iFieldNo
                    # if type(prf_new_row[cur_pos][0]) != dict:
                    if not isinstance(prf_new_row[cur_pos][0], dict):
                        prf_new_row[cur_pos][0] = {
                            "x": iXPosition,
                            "y": iYPosition,
                            "status": iPrintStatus,
                            "w": iWidth,
                            "h": iHeight,
                        }

            prfmt.add_row(prf_new_row, sync_status_bytes=False)

        sm110 = smtws.smtws(self.ip)
        if not sm110.upload_master(prfmt):
            common.common.log_err("Failed To Send Label Format")
            return False

        common.common.log_info("Sending Label Format To %s Successfully" % self.ip)
        return True

    def createDatForFlexibarcode(
            self,
            flexibarcodeMasterData,
            strBarcodeType,
            strBarcodeFormat):

        maxAvailbleNo = 0
        cdPos = -1
        barItemLength = {
            'F': 0,
            'C': 0,
            'W': 0,
            'P': 0
        }

        barItemPos = {
            'F': -1,
            'C': -1,
            'W': -1,
            'P': -1,
        }

        bar_formats = strBarcodeFormat.split(" ")

        tmpPosCount = 0
        for bar_format in bar_formats:
            if bar_format == "CD":
                tmpPosCount += 1
                cdPos = tmpPosCount
                continue

            bSame = True
            for i in range(len(bar_format)):
                if bar_format[i] != bar_format[i + 1]: bSame = False
            if not bSame: continue

            if bar_format and barItemPos.has_key(bar_format[0]):
                tmpPosCount += 1
                barItemPos[bar_format[0]] = tmpPosCount

            if bar_format and barItemLength.has_key(bar_format[0]):
                barItemLength[bar_format[0]] = len(bar_format)

        # if flbmt.from_json(flexiBarcodeJsonFile):
        flbmt = entity.FlbMaster()
        if True:
            flb_rows = flbmt.get_all_data()
            for flb_row in flb_rows:
                iCode = flb_row[enum.FLBField.CODE][0]
                if iCode > maxAvailbleNo: maxAvailbleNo = iCode
                if flb_row[enum.FLBField.CHECK_DIGIT][0] & 0x80 == 0:
                    iBarType = 0
                else:
                    iBarType = 1
                if iBarType == 0 and strBarcodeType == "ITF":
                    continue
                elif iBarType == 1 and strBarcodeType == "EAN":
                    continue

                osBarcode = ""
                osBarcodeArr = []
                iFlagType = flb_row[enum.FLBField.FLAG_TYPE][0]
                if iFlagType == 1:
                    osBarcode += "FF"
                    osBarcodeArr.append("FF")
                elif iFlagType == 0:
                    osBarcode += "F"
                    osBarcodeArr.append("F")

                osBarcode += " "
                iItemCodeDigitNum = flb_row[enum.FLBField.ITEM_CODE_DIGIT_NO][0]
                osBarcode += "C" * iItemCodeDigitNum
                osBarcodeArr.append("C" * iItemCodeDigitNum)
                osBarcode += " "
                iProgramData1DigitNum = flb_row[enum.FLBField.PROGRAM_DATA1_DIGIT_NO][0]
                iProgramData2DigitNum = flb_row[enum.FLBField.PROGRAM_DATA2_DIGIT_NO][0]

                iProgramData1Type = flb_row[enum.FLBField.PROGRAM_DATA1][0]
                if iProgramData1DigitNum > 0:
                    if iProgramData1Type == 3:
                        osBarcode += "W" * iProgramData1DigitNum
                        osBarcodeArr.append("W" * iProgramData1DigitNum)
                    elif iProgramData1Type == 4:
                        osBarcode += "P" * iProgramData1DigitNum
                        osBarcodeArr.append("P" * iProgramData1DigitNum)
                osBarcode += " "

                if flb_row[enum.FLBField.CHECK_DIGIT][0] and 0x01 == 0:
                    iMiddleCheckDigit = 0
                else:
                    iMiddleCheckDigit = 1

                if iMiddleCheckDigit:
                    osBarcode += "CD"
                    osBarcodeArr.append("CD")
                    osBarcode += " "

                iProgramData2Type = flb_row[enum.FLBField.PROGRAM_DATA2][0]
                if iProgramData2Type > 0:
                    if iProgramData2Type == 3:
                        osBarcode += "W" * iProgramData2DigitNum
                        osBarcodeArr.append("W" * iProgramData2DigitNum)
                    elif iProgramData2Type == 4:
                        osBarcode += "P" * iProgramData2DigitNum
                        osBarcodeArr.append("P" * iProgramData2DigitNum)

                osBarcode += " "

                if flb_row[enum.FLBField.CHECK_DIGIT][0] and 0x02 == 0:
                    iLastCheckDigit = 0
                else:
                    iLastCheckDigit = 1

                if iLastCheckDigit:
                    osBarcode += "CD"
                    osBarcodeArr.append("CD")
                    osBarcode += " "

                osBarcode = " ".join(osBarcodeArr)

                if osBarcode == strBarcodeFormat:
                    return True, iCode, ""

            newLineData = flbmt.create_row()
            if maxAvailbleNo + 1 > 9: maxAvailbleNo = 0
            newLineData[enum.FLBField.CODE][0] = maxAvailbleNo + 1
            iBarType = 0
            if strBarcodeType == "EAN": iBarType = 1
            if iBarType == 1:
                newLineData[enum.FLBField.CHECK_DIGIT][0] |= 0x80
            else:
                newLineData[enum.FLBField.CHECK_DIGIT][0] &= ~0x80

            if cdPos >= 0:
                newLineData[enum.FLBField.CHECK_DIGIT][0] |= 0x02

            if barItemPos.has_key('F') and barItemPos['F'] >= 0:
                iFLen = barItemLength.get('F', 0)
                if iFLen == 1:
                    iFLen = 0
                elif iFLen == 2:
                    iFLen = 1
                else:
                    iFLen = 2
                newLineData[enum.FLBField.FLAG_TYPE][0] = iFLen
            else:
                newLineData[enum.FLBField.FLAG_TYPE][0] = 2

            if barItemPos.has_key('C') and barItemPos['C'] >= 0:
                iFLen = barItemLength.get('C', 0)
                newLineData[enum.FLBField.ITEM_CODE_DIGIT_NO][0] = iFLen

            iPosP = iPosW = 0
            if barItemPos.has_key('P') and barItemPos['P'] >= 0:
                iPosP = barItemPos['P']
            if barItemPos.has_key('W') and barItemPos['W'] >= 0:
                iPosW = barItemPos['W']

            iLenP = barItemLength.get('P', 0)
            iLenW = barItemLength.get('W', 0)

            data1Len = min(iLenW, iLenP)
            data2Len = max(iLenW, iLenP)
            if iPosP > iPosW:
                data1Type = 3
            else:
                data1Type = 4

            if iPosP < iPosW:
                data2Type = 3
            else:
                data2Type = 4

            newLineData[enum.FLBField.PROGRAM_DATA1][0] = data1Type
            newLineData[enum.FLBField.PROGRAM_DATA2][0] = data2Type
            newLineData[enum.FLBField.PROGRAM_DATA1_DIGIT_NO][0] = data1Len
            newLineData[enum.FLBField.PROGRAM_DATA2_DIGIT_NO][0] = data2Len

            flbmt.add_row(newLineData)

            return False, maxAvailbleNo + 1

    def easySendPlu(self, plu_json_file):
        sm110 = smtws.smtws(self.ip)

        fileList = {}

        plumt = entity.PluMaster()
        tbtmt = entity.TbtMaster()
        flbmt = entity.FlbMaster()
        texmt = entity.TexMaster()

        if not sm110.download_master(tbtmt):
            common.common.log_err("Error On receiving Data From Scale")
            return False

        json_data = common.common.get_json_from_file(plu_json_file)
        for data_line in json_data:
            try:
                iPLUNo = data_line["PLUNo"]
                iWeightingFlag = data_line["WeightingFlag"]
                fUnitPrice = data_line["UnitPrice"]
                iLabelFormat1 = data_line["LabelFormat1"]
                strItemCode = data_line["ItemCode"]
                strBarcodeType = data_line["BarcodeType"]
                strBarcodeFormat = data_line["BarcodeFormat"]
                iMGNo = data_line.get("MGNo", 0)
                iTraceabilityNo = data_line.get("TraceabilityNo", 0)
                strMultibarcode1 = data_line.get("Multibarcode1", "")
                strMultibarcode1Type = data_line.get("Multibarcode1Type", "")
                oMultibarcode2 = data_line.get("Multibarcode2", "")
                strMultibarcode2Type = data_line.get("Multibarcode2Type", "")
                iUsedByDate = data_line.get("UsedByDate", 0)
                iSellByDate = data_line.get("SellByDate", 0)
                iPackedByDate = data_line.get("PackedByDate", 0)
                strSellByTime = data_line.get("SellByTime", 0)
                strPackedByTime = data_line.get("PackedByTime", 0)
                oCommodityName = data_line.get("CommodityName", "")
                oCommodityNameFont = data_line.get("CommodityNameFont", 0)
                oSpecialMessage = data_line.get("SpecialMessage", "")
                oSpecialMessageFont = data_line.get("SpecialMessageFont", "S1")
                oIngredient = data_line.get("Ingredient", "")
                oIngredientFont = data_line.get("IngredientFont", "S1")
            except Exception, e:
                common.common.log_err(traceback.format_exc())
                continue

            # import master.call_list
            new_plu_row = plumt.create_row()

            # 初始化Status
            new_plu_row[enum.PLUField.PLU_STATUS][0] = \
                master.call_list["BIN"]().csv_to_cell("00000000 00000000", 2, plumt.fields_info_dic["PLUStatus1"])
            new_plu_row[enum.PLUField.PLU_STATUS_2][0] = \
                master.call_list["BIN"]().csv_to_cell("00000000 00000000 10000000", 3,
                                                      plumt.fields_info_dic["PLUStatus2"])
            new_plu_row[enum.PLUField.PLU_STATUSB][0] = \
                master.call_list["BIN"]().csv_to_cell(" ".join(["00000000"] * 4), 4,
                                                      plumt.fields_info_dic["PLUStatus1B"])
            new_plu_row[enum.PLUField.PLU_STATUS_2B][0] = \
                master.call_list["BIN"]().csv_to_cell(" ".join(["00000000"] * 8), 8,
                                                      plumt.fields_info_dic["PLUStatus2B"])

            # Commodity
            if oCommodityName:
                commNamesArr = []
                commNamesFontArr = []
                # if type(oCommodityName) is list:
                if isinstance(oCommodityName, list):
                    commNamesArr = oCommodityName
                else:
                    commNamesArr = [oCommodityName]

                if oCommodityNameFont:
                    # if type(oCommodityNameFont) is list:
                    if isinstance(oCommodityNameFont, list):
                        commNamesFontArr = [const.fontMapper.get(fon, 0) for fon in oCommodityNameFont]
                    else:
                        commNamesFontArr = [const.fontMapper.get(oCommodityNameFont, 0)]

                if len(commNamesArr) != len(commNamesFontArr):
                    if isinstance(oCommodityNameFont, (str, unicode)):
                        commNamesFontArr = [const.fontMapper.get(oCommodityNameFont, 0)] * len(commNamesArr)
                    else:
                        commNamesFontArr = [const.fontMapper.get("S1", 0)] * len(commNamesArr)

                combCommLines = [{
                    "font_size": combCommLine[1],
                    "text": combCommLine[0]
                } for combCommLine in zip(commNamesArr, commNamesFontArr)]

                # print combCommLines

                new_plu_row[enum.PLUField.COMMODITY][0] = combCommLines

            # Multi-barcode 1
            if strMultibarcode1:
                iMultiBarcodeType = const.multiBarcodeTypeMapper.get(strMultibarcode1Type, 2)
                iBarcodeType = const.barcodeTypeMapper.get(strMultibarcode1Type, 1)

                new_plu_row[enum.PLUField.MULTI_BARCODE_1][0] = {
                    "fnc1": iBarcodeType,
                    "data": strMultibarcode1,
                    "code": iMultiBarcodeType,
                }

            # Multi-Barcode 2
            if oMultibarcode2:
                iMultiBarcodeType = const.multiBarcodeTypeMapper.get(strMultibarcode2Type, 2)
                iBarcodeType = const.barcodeTypeMapper.get(strMultibarcode2Type, 1)

                multiBarcode2Lines = []
                # if type(oMultibarcode2) is list:
                if isinstance(oMultibarcode2, list):
                    multiBarcode2Lines = oMultibarcode2
                else:
                    multiBarcode2Lines = [oMultibarcode2]

                if iBarcodeType == 5:
                    src_str_comp = '\r\n'.join(["1," + "\"" + mbl + "\"" for mbl in multiBarcode2Lines])
                    # print src_str_comp
                    strCodes = tbtmt.find_records(
                        "SELECT Code FROM tbt WHERE Data = ?", [src_str_comp])
                    if strCodes:
                        iFoundCode = strCodes[0]["Code"][0]
                        new_plu_row[enum.PLUField.MULTI_BARCODE_2][0] = {
                            "fnc1": iBarcodeType,
                            "data": str(iFoundCode),
                            "code": iMultiBarcodeType,
                        }
                    else:
                        iMaxTBTCode = tbtmt.get_max_value_of_key()
                        for indx, mbLine in enumerate(multiBarcode2Lines):
                            new_tbt_row = tbtmt.create_row()
                            new_tbt_row[enum.TBTField.CODE][0] = iMaxTBTCode + 1
                            new_tbt_row[enum.TBTField.DATA][0] = [{
                                "font_size": 1,
                                "text": "\r\n".join(multiBarcode2Lines)
                            }]
                            tbtmt.add_row(new_tbt_row)

                        fileList["tbt"] = tbtmt
                        new_plu_row[enum.PLUField.MULTI_BARCODE_2][0] = {
                            "fnc1": iBarcodeType,
                            "data": str(iMaxTBTCode + 1),
                            "code": iMultiBarcodeType,
                        }

                else:
                    new_plu_row[enum.PLUField.MULTI_BARCODE_1] = {
                        "fnc1": iBarcodeType,
                        "data": oMultibarcode2[0],
                        "code": iMultiBarcodeType,
                    }

            # Special Message
            if oSpecialMessage:
                # if type(oSpecialMessage) is list:
                if isinstance(oSpecialMessage, list):
                    specialMessageLinesArr = oSpecialMessage
                else:
                    specialMessageLinesArr = [oSpecialMessage]

                specialMessageLinesFontArr = []
                # if type(oSpecialMessageFont) is list:
                if isinstance(oSpecialMessageFont, list):
                    specialMessageLinesFontArr = [const.fontMapper.get(font, 0) for font in oSpecialMessageFont]

                if len(specialMessageLinesArr) != len(specialMessageLinesFontArr):
                    # if type(oSpecialMessageFont) in (str, unicode):
                    if isinstance(oSpecialMessageFont, (str, unicode)):
                        specialMessageLinesFontArr = [const.fontMapper.get(oSpecialMessageFont, 0)] * len(
                            specialMessageLinesArr)
                    else:
                        specialMessageLinesFontArr = [const.fontMapper.get("S1", 0)] * len(specialMessageLinesArr)

                combSpecialMessageLines = [{
                    "font_size": combLine[1],
                    "text": combLine[0]
                } for combLine in zip(specialMessageLinesArr, specialMessageLinesFontArr)]

                new_plu_row[enum.PLUField.SPECIAL_MESSAGE][0] = combSpecialMessageLines

            # Ingredient
            if oIngredient:
                # if type(oIngredient) is list:
                if isinstance(oIngredient, list):
                    ingredientLinesArr = oIngredient
                else:
                    ingredientLinesArr = [oIngredient]

                ingredientLinesFontArr = []
                # if type(oIngredientFont) is list:
                if isinstance(oIngredientFont, list):
                    ingredientLinesFontArr = [const.fontMapper.get(font, 0) for font in oIngredientFont]

                if len(ingredientLinesArr) != len(ingredientLinesFontArr):
                    if isinstance(oIngredientFont, (str, unicode)):
                        ingredientLinesFontArr = [const.fontMapper.get(oIngredientFont, 0)] * len(ingredientLinesArr)
                    else:
                        ingredientLinesFontArr = [const.fontMapper.get("S1", 0)] * len(ingredientLinesArr)

                combIngredientLines = [{
                    "font_size": combLine[1],
                    "text": combLine[0]
                } for combLine in zip(ingredientLinesArr, ingredientLinesFontArr)]

                new_plu_row[enum.PLUField.INGREDIENT][0] = combIngredientLines

            # Text
            for i in range(5):
                sTextName = "Text" + str(i + 1)
                sTextFontName = sTextName + "Font"
                oText = data_line.get(sTextName, "")
                oTextFont = data_line.get(sTextFontName, "S1")

                if oText:
                    # if type(oText) is list:
                    if isinstance(oText, list):
                        textLinesArr = oText
                    else:
                        textLinesArr = [oText]

                    textLinesFontArr = []
                    # if type(oTextFont) is list:
                    if isinstance(oTextFont, list):
                        textLinesFontArr = [const.fontMapper.get(font, 0) for font in oTextFont]

                    if len(textLinesArr) != len(textLinesFontArr):
                        if isinstance(oTextFont, (str, unicode)):
                            textLinesFontArr = [const.fontMapper.get(oTextFont, 0)] * len(textLinesArr)
                        else:
                            textLinesFontArr = [const.fontMapper.get("S1", 0)] * len(textLinesArr)

                    combTextLines = [
                        {
                            "font_size": combLine[1],
                            "text": combLine[0]
                        } for combLine in zip(textLinesArr, textLinesFontArr)]

                    src_str_comp = '\r\n'.join(
                        [str(text_line["font_size"]) + "," + "\"" + text_line["text"] + "\"" for text_line in
                         combTextLines])
                    strCodes = texmt.find_records(
                        "SELECT Code FROM tex WHERE [Name] = ?", [src_str_comp])
                    if strCodes:
                        iFoundCode = strCodes[0]["Code"][0]
                        new_plu_row[enum.PLUField.LINKED_TEXT1_NO + i][0] = iFoundCode
                    else:
                        iMaxTexNo = texmt.get_max_value_of_key()
                        for index, line in enumerate(textLinesArr):
                            new_tex_row = texmt.create_row()
                            new_tex_row[enum.TEXField.CODE][0] = iMaxTexNo + 1
                            new_tex_row[enum.TEXField.NAME][0] = [{
                                "font_size": textLinesFontArr[index],
                                "text": "\r\n".join(textLinesArr)
                            }]
                            # print "ADD TEXT:", index, new_tex_row
                            texmt.add_row(new_tex_row)

                        fileList["tex"] = texmt
                        new_plu_row[enum.PLUField.LINKED_TEXT1_NO + i][0] = iMaxTexNo + 1

            # Used by Date
            if iUsedByDate:
                new_plu_row[enum.PLUField.USED_BY_DATE][0] = iUsedByDate

            # Sell by Date
            if iSellByDate:
                new_plu_row[enum.PLUField.SELL_BY_DATE][0] = iSellByDate

            # Packed by Date
            if iPackedByDate:
                new_plu_row[enum.PLUField.PACKED_DATE][0] = iPackedByDate

            # Sell by Time
            if strSellByTime:
                stk = strSellByTime.split(":")
                stk = [int(s) for s in stk]
                hm = reduce(lambda x, y: x * 100 + y, stk)
                new_plu_row[enum.PLUField.SELL_BY_TIME][0] = hm
                new_plu_row[enum.PLUField.PLU_STATUS][0][1]["RTC SELL BY TIME"] = 1

            # Packed By Time
            if strPackedByTime:
                stk = strPackedByTime.split(":")
                stk = [int(s) for s in stk]
                hm = reduce(lambda x, y: x * 100 + y, stk)
                new_plu_row[enum.PLUField.PACKED_TIME][0] = hm
                new_plu_row[enum.PLUField.PLU_STATUS][0][0]["RTC PACKED TIME"] = 1

            # PLUNo
            new_plu_row[enum.PLUField.PLU_NUMBER][0] = iPLUNo
            # Weighting Flag
            new_plu_row[enum.PLUField.PLU_STATUS][0][0]["UNIT"] = iWeightingFlag
            # Unit Price
            new_plu_row[enum.PLUField.UNIT_PRICE][0] = int(fUnitPrice * 100)
            # Label Format 1
            new_plu_row[enum.PLUField.LABEL_1_FORMAT][0] = iLabelFormat1
            # MGNo
            new_plu_row[enum.PLUField.MAIN_GROUP_CODE][0] = iMGNo

            # Traceability
            if iTraceabilityNo:
                new_plu_row[enum.PLUField.TRACEABILITY_LINK][0] = iTraceabilityNo
                new_plu_row[enum.PLUField.TRACEABILITY][0] = 1

            # Ean Data
            if len(strItemCode) == 12:
                new_plu_row[enum.PLUField.F1F2][0] = strItemCode[:2]
                new_plu_row[enum.PLUField.EAN_DATA][0] = {
                    "ean_data": strItemCode[2:],
                    "type": strBarcodeType,
                    "last_byte": 0
                }

            # Barcode Format
            if const.eanMapper.has_key(strBarcodeFormat):
                iBarNo = const.eanMapper[strBarcodeFormat]
            elif const.itfMapper.has_key(strBarcodeFormat):
                iBarNo = const.itfMapper[strBarcodeFormat]
            else:
                iBarNo = -1

            if iBarNo > 0:
                new_plu_row[enum.PLUField.BARCODE_FORMAT][0] = iBarNo
            else:
                found, code = self.createDatForFlexibarcode(flbmt, strBarcodeType, strBarcodeFormat)

                if found:
                    iCode = 33 - 1 + code
                    new_plu_row[enum.PLUField.BARCODE_FORMAT][0] = iCode
                elif code != 0:
                    new_plu_row[enum.PLUField.BARCODE_FORMAT][0] = 33 - 1 + code
                    fileList["flb"] = flbmt

            plumt.add_row(new_plu_row)

        fileList["plu"] = plumt

        for key, value in fileList.items():
            if not sm110.upload_master(value):
                return False
            # print key, "ok"

        common.common.log_info("Downloading Plu To %s Successfully..." % self.ip)
        return True

    def easySendTrace(self, trace_json_file):
        sm110 = smtws.smtws(self.ip)

        fileList = {}

        trgmt = entity.TrgMaster()
        trbmt = entity.TrbMaster()

        if not sm110.download_master(trbmt):
            common.common.log_err("Error On receiving Data From Scale")
            return False

        json_data = common.common.get_json_from_file(trace_json_file)

        for data_line in json_data:
            try:
                iTraceabilityNo = data_line["TraceabilityNo"]
                strReferenceCode = data_line["ReferenceCode"]
                strBarcode = data_line["Barcode"]
                textLines = data_line.get("Text", "")
                textLinesFont = data_line.get("TextFont", "S1")
            except Exception, e:
                common.common.log_err(traceback.format_exc())
                continue

            new_trg_row = trgmt.create_row()
            new_trg_row[enum.TRGField.TRACEABILITY_REFERENCE_TYPE][0] = 1

            # Traceability No
            new_trg_row[enum.TRGField.TRACEABILITY_NO][0] = iTraceabilityNo
            if strReferenceCode:
                new_trg_row[enum.TRGField.TRACEABILITY_REFERENCE_CODE][0] = strReferenceCode

            # Barcode
            if strBarcode:
                new_trb_row = trbmt.create_row()
                new_trb_row[enum.TRBField.BARCODE_DATA][0] = strBarcode

                strCodes = trbmt.find_records("SELECT Code FROM trb WHERE data = ?", [strBarcode])

                if strCodes:
                    iFoundCode = strCodes[0]["Code"][0]
                    new_trg_row[enum.TRGField.TRACEABILITY_BARCODE_NO][0] = iFoundCode
                else:
                    iMaxCode = trbmt.get_max_value_of_key()
                    new_trb_row[enum.TRBField.CODE][0] = iMaxCode + 1
                    trbmt.add_row(new_trb_row)
                    new_trg_row[enum.TRGField.TRACEABILITY_BARCODE_NO][0] = new_trb_row[enum.TRBField.CODE][0]

                    fileList["trb"] = trbmt

            trgmt.add_row(new_trg_row)

        fileList["trg"] = trgmt

        for key, value in fileList.items():
            # print "key:", key
            if not sm110.upload_master(value):
                return False

            # print key, "OK"

        common.common.log_info("Downloading Traceability To %s Successfully..." % self.ip)
        return True

    def process_line(self, curLineNo, cur_row):

        self.dataFilter.set_field_list(cur_row)
        if self.dataFilter.is_filtered(): return True

        gv = {"CurLineNo": str(curLineNo + 1)}
        for clsName, template_infos in self.createMasterList.items():
            master = template_infos.get("Master", None)
            if master is None: continue
            iMaxCode = master.get_max_value_of_key()
            iMaxCode += 1
            iFreeCode = master.get_free_value_of_key()
            strKeyValue = clsName + ".MaxCode"
            gv[strKeyValue] = str(iMaxCode)
            strKeyValue = clsName + ".FreeCode"
            gv[strKeyValue] = str(iFreeCode)

        for clsName, template_infos in self.createMasterList.items():
            # print json.dumps(row, indent=4, separators={':',','})
            newLines = {}
            if not template_infos.has_key("Master"): continue
            master = template_infos["Master"]
            for template_info in template_infos["infos"]:
                iLineNo = int(template_info["line_no"])
                if not newLines.has_key(iLineNo):
                    newLines[iLineNo] = master.create_row()
                sp = common.strparser.StrParser(template_info["source_expression"], cur_row, {}, gv)
                # print "expr:", template_info["source_expression"]
                result = sp.eval(0)
                # print "result:", result
                if newLines[iLineNo].has_key(template_info["field_name"]):
                    newLines[iLineNo][template_info["field_name"]][0] = result

                if iLineNo > 0:
                    newLines[iLineNo][template_info["line_no_field"]][0] = iLineNo

            for newLineKey, newLine in newLines.items():
                template_infos["Master"].import_line(newLine)

    # def easyImportMaster(
    #         self,
    #         csv_file_path,
    #         json_fmt_file_path,
    #         json_scale_group_file="",
    #         json_filter_file=""):
    #
    #     sm110 = smtws.smtws(self.ip)
    #
    #     json_data = common.common.get_json_from_file(json_fmt_file_path)
    #     self.createMasterList = {}
    #
    #     # 分组
    #     strMgNo = ""
    #     if json_scale_group_file:
    #         dGrp = common.scalegroup.DigiGroup()
    #         dGrp.read_from_config_file(json_scale_group_file)
    #         strMgNo = str(dGrp.get_mgno_from_scale(self.ip))
    #
    #     # 过滤
    #     self.dataFilter = common.datafilter.DataFilter()
    #     globalVals = {"ScaleGroupNo": strMgNo}
    #     self.dataFilter.set_glob_vars(globalVals)
    #
    #     for fmt in json_data:
    #         source_expr = fmt["source_expr"]
    #         target_field = fmt["target_field"]
    #         line_no_field = fmt.get("line_no_field", "LineNo")
    #         sp_data = target_field.split(".")
    #         clsName = sp_data[0]
    #         fieldName = sp_data[1]
    #         if len(sp_data) > 2:
    #             lineNo = int(sp_data[2])
    #         else:
    #             lineNo = 0
    #         # lineNo = int(sp_data[2] if len(sp_data) > 2 else '0')
    #
    #         if not self.createMasterList.has_key(clsName):
    #             self.createMasterList[clsName] = {}
    #             self.createMasterList[clsName]["infos"] = []
    #             self.createMasterList[clsName]["Master"] = entity.MasterFactory().createMaster(clsName)
    #
    #         self.createMasterList[clsName]["infos"].append(
    #             {
    #                 "source_expression": source_expr,
    #                 "field_name": fieldName,
    #                 "line_no_field": line_no_field,
    #                 "line_no": lineNo,
    #             }
    #         )
    #
    #     common.csvreader.SmCsvReader().read_line_by_line(
    #         csv_file_path,
    #         self.process_line)
    #
    #     for clsName, template_infos in self.createMasterList.items():
    #         if not sm110.upload_master(template_infos["Master"]):
    #             common.common.log_err("Downloading To Scale Failed...")
    #             return False
    #
    #     common.common.log_info("Downloading To %s Successfully..." % self.ip)
    #     return True
