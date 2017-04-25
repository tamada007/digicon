# encoding=gbk

from entity import *
import common.common
import common.csvreader
import common.datafilter
import common.scalegroup
import common.strparser
import const
import digiscale
import entity
import enum
import master
import os
import sys
import json
import traceback

csJsonPrfFile = "prf.json"
csJsonPffFile = "pff.json"


class Easy:
    def __init__(self, ip, port=21, usr="admin", pwd="admin"):
        self.ip = ip
        self.port = port
        self.usr = usr
        self.pwd = pwd

    def createJsonForFlexiBarcode(
            self,
            flexiBarcodeJsonFile,
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

        flbmt = FlbMaster()
        if flbmt.from_json(flexiBarcodeJsonFile):
            flb_rows = flbmt.get_all_data()
            for flb_row in flb_rows:
                iCode = flb_row[enum.FLBField.FLB_Code][0]
                if iCode > maxAvailbleNo: maxAvailbleNo = iCode
                iBarType = flb_row[enum.FLBField.FLB_FlagOfBarcodeType][0]
                if iBarType:
                    if strBarcodeType == "ITF": continue
                elif strBarcodeType == "EAN":
                    continue

                osBarcode = ""
                osBarcodeArr = []
                iFlagType = flb_row[enum.FLBField.FLB_FlagType][0]
                if iFlagType == 1:
                    osBarcode += "FF"
                    osBarcodeArr.append("FF")
                elif iFlagType == 0:
                    osBarcode += "F"
                    osBarcodeArr.append("F")

                osBarcode += " "
                iItemCodeDigitNum = flb_row[enum.FLBField.FLB_ItemCodeDigitNumber][0]
                osBarcode += "C" * iItemCodeDigitNum
                osBarcodeArr.append("C" * iItemCodeDigitNum)
                osBarcode += " "
                iProgramData1DigitNum = flb_row[enum.FLBField.FLB_ProgramData1DigitNumber][0]
                iProgramData2DigitNum = flb_row[enum.FLBField.FLB_ProgramData2DigitNumber][0]

                iProgramData1Type = flb_row[enum.FLBField.FLB_ProgramData1Type][0]
                if iProgramData1DigitNum > 0:
                    if iProgramData1Type == 3:
                        osBarcode += "W" * iProgramData1DigitNum
                        osBarcodeArr.append("W" * iProgramData1DigitNum)
                    elif iProgramData1Type == 4:
                        osBarcode += "P" * iProgramData1DigitNum
                        osBarcodeArr.append("P" * iProgramData1DigitNum)
                osBarcode += " "

                iMiddleCheckDigit = flb_row[enum.FLBField.FLB_FlagOfMiddleCheckDigit][0]
                if iMiddleCheckDigit:
                    osBarcode += "CD"
                    osBarcodeArr.append("CD")
                    osBarcode += " "

                iProgramData2Type = flb_row[enum.FLBField.FLB_ProgramData2Type][0]
                if iProgramData2Type > 0:
                    if iProgramData2Type == 3:
                        osBarcode += "W" * iProgramData2DigitNum
                        osBarcodeArr.append("W" * iProgramData2DigitNum)
                    elif iProgramData2Type == 4:
                        osBarcode += "P" * iProgramData2DigitNum
                        osBarcodeArr.append("P" * iProgramData2DigitNum)

                osBarcode += " "

                iLastCheckDigit = flb_row[enum.FLBField.FLB_FlagOfLastCheckDigit][0]
                if iLastCheckDigit:
                    osBarcode += "CD"
                    osBarcodeArr.append("CD")
                    osBarcode += " "

                osBarcode = " ".join(osBarcodeArr)

                if osBarcode == strBarcodeFormat:
                    return True, iCode, ""

            newLineData = flbmt.create_row()
            if maxAvailbleNo + 1 > 9: maxAvailbleNo = 0
            newLineData[enum.FLBField.FLB_Code][0] = maxAvailbleNo + 1
            iBarType = 0
            if strBarcodeType == "EAN": iBarType = 1
            newLineData[enum.FLBField.FLB_FlagOfBarcodeType][0] = iBarType

            if cdPos >= 0:
                newLineData[enum.FLBField.FLB_FlagOfLastCheckDigit][0] = 1

            if barItemPos.has_key('F') and barItemPos['F'] >= 0:
                iFLen = barItemLength.get('F', 0)
                if iFLen == 1:
                    iFLen = 0
                elif iFLen == 2:
                    iFLen = 1
                else:
                    iFLen = 2
                newLineData[enum.FLBField.FLB_FlagType][0] = iFLen
            else:
                newLineData[enum.FLBField.FLB_FlagType][0] = 2

            if barItemPos.has_key('C') and barItemPos['C'] >= 0:
                iFLen = barItemLength.get('C', 0)
                newLineData[enum.FLBField.FLB_ItemCodeDigitNumber][0] = iFLen

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

            newLineData[enum.FLBField.FLB_ProgramData1Type][0] = data1Type
            newLineData[enum.FLBField.FLB_ProgramData2Type][0] = data2Type
            newLineData[enum.FLBField.FLB_ProgramData1DigitNumber][0] = data1Len
            newLineData[enum.FLBField.FLB_ProgramData2DigitNumber][0] = data2Len

            flbmt.add_row(newLineData)

            out_file_name = self.ip + "_" + str(maxAvailbleNo + 1) + "_" + "flb0uall.json"
            flbmt.to_json(out_file_name)
            return False, maxAvailbleNo + 1, out_file_name

    def easySendPlu(self, plu_json_file):
        flexiBarcodeJsonFile = self.ip + "_flexibarcode.json"
        multiBarcodeJsonFile = self.ip + "_multibarcode.json"
        specialMessageJsonFile = self.ip + "_spm.json"
        ingredientJsonFile = self.ip + "_ing.json"
        t2dBarcodeJsonFile = self.ip + "_t2dbarcode.json"
        txtJsonFile = self.ip + "_text.json"

        plumt = entity.PluMaster()
        flbmt = entity.FlbMaster()
        mubmt = entity.MubMaster()
        tbtmt = entity.TbtMaster()
        spmmt = entity.SpmMaster()
        ingmt = entity.IngMaster()
        texmt = entity.TexMaster()

        sm120 = digiscale.DigiSm120(self.ip, self.port, self.usr, self.pwd)
        sm120.connect()

        fileList = {}

        # '''
        if not reduce(lambda x, y: x and y, [
            sm120.recv(flbmt),
            sm120.recv(mubmt),
            sm120.recv(tbtmt),
            sm120.recv(texmt),
            sm120.recv(spmmt),
            sm120.recv(ingmt)
        ]):
            common.common.log_err("Error On Receiving Data From Scale")
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

            new_plu_row = plumt.create_row()
            maxCommLine = 0
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
                        commNamesFontArr = oCommodityNameFont
                    else:
                        commNamesFontArr = [oCommodityNameFont]

                if len(commNamesArr) != len(commNamesFontArr):
                    # if type(oCommodityNameFont) in (str, unicode):
                    if isinstance(oCommodityNameFont, (str, unicode)):
                        commNamesFontArr = [const.fontMapper.get(oCommodityNameFont, 0)] * len(commNamesArr)
                    else:
                        commNamesFontArr = [const.fontMapper.get("S1", 0)] * len(commNamesArr)

                lenCommNames = len(commNamesArr)
                if lenCommNames > 0:
                    new_plu_row[enum.PLUField.PLU_1st_line_of_Comm_name_data][0] = commNamesArr[0]
                if lenCommNames > 1:
                    new_plu_row[enum.PLUField.PLU_2nd_line_of_Comm_name_data][0] = commNamesArr[1]
                if lenCommNames > 2:
                    new_plu_row[enum.PLUField.PLU_3rd_line_of_Comm_name_data][0] = commNamesArr[2]
                if lenCommNames > 3:
                    new_plu_row[enum.PLUField.PLU_4th_line_of_Comm_name_data][0] = commNamesArr[3]

                lenCommNamesFont = len(commNamesFontArr)
                if lenCommNamesFont > 0:
                    new_plu_row[enum.PLUField.PLU_Font_for_Comm_name_of_1st_line][0] = commNamesFontArr[0]
                if lenCommNamesFont > 1:
                    new_plu_row[enum.PLUField.PLU_Font_for_Comm_name_of_2nd_line][0] = commNamesFontArr[1]
                if lenCommNamesFont > 2:
                    new_plu_row[enum.PLUField.PLU_Font_for_Comm_name_of_3rd_line][0] = commNamesFontArr[2]
                if lenCommNamesFont > 3:
                    new_plu_row[enum.PLUField.PLU_Font_for_Comm_name_of_4th_line][0] = commNamesFontArr[3]

            # Multi-barcode 1
            if strMultibarcode1:
                new_mub_row = mubmt.create_row()
                iMultiBarcodeType = const.multiBarcodeTypeMapper.get(strMultibarcode1Type, 2)
                iBarcodeType = const.barcodeTypeMapper.get(strMultibarcode1Type, 1)

                iMaxMubCode = mubmt.get_max_value_of_key("Code")
                new_mub_row[enum.MUBField.MUB_MultiBarcodeType][0] = iMultiBarcodeType
                new_mub_row[enum.MUBField.MUB_BarcodeType][0] = iBarcodeType
                new_mub_row[enum.MUBField.MUB_Data][0] = strMultibarcode1

                find_rows = mubmt.find_records(
                    "SELECT * FROM mub WHERE BarcodeType=? AND MultiBarcodeType=? AND Data=?",
                    [iBarcodeType, iMultiBarcodeType, strMultibarcode1])
                iFoundCode = 0
                if find_rows:
                    iFoundCode = find_rows[0]["Code"][0]
                    new_plu_row[enum.PLUField.PLU_Multibarcode_1_No][0] = iFoundCode
                # print "iFoundCode:", iFoundCode
                else:
                    new_mub_row[enum.MUBField.MUB_Code][0] = iMaxMubCode + 1
                    mubmt.add_row(new_mub_row)
                    out_file_name = self.ip + "_mub0uall.json"
                    mubmt.to_json(out_file_name)
                    fileList["mub"] = out_file_name
                    new_plu_row[enum.PLUField.PLU_Multibarcode_1_No][0] = new_mub_row[enum.MUBField.MUB_Code][0]

            # Multi-Barcode 2
            if oMultibarcode2:
                iMultiBarcodeType = const.multiBarcodeTypeMapper.get(strMultibarcode2Type, 2)
                iBarcodeType = const.barcodeTypeMapper.get(strMultibarcode2Type, 1)
                new_mub_row = mubmt.create_row()
                new_mub_row[enum.MUBField.MUB_MultiBarcodeType][0] = iMultiBarcodeType
                new_mub_row[enum.MUBField.MUB_BarcodeType][0] = iBarcodeType
                multiBarcode2Lines = []
                # if type(oMultibarcode2) is list:
                if isinstance(oMultibarcode2, list):
                    multiBarcode2Lines = oMultibarcode2
                else:
                    multiBarcode2Lines = [oMultibarcode2]

                if iBarcodeType == 5:
                    src_str_comp = ','.join(multiBarcode2Lines)
                    strCodes = tbtmt.find_records(
                        "SELECT Code FROM tbt GROUP BY Code HAVING GROUP_CONCAT(Data) = ?", [src_str_comp])
                    if strCodes:
                        iFoundCode = strCodes[0]["Code"][0]
                        new_mub_row[enum.MUBField.MUB_Link2DBarcodeTextNo][0] = iFoundCode
                    else:
                        iMaxTBTCode = tbtmt.get_max_value_of_key()
                        for indx, mbLine in enumerate(multiBarcode2Lines):
                            new_tbt_row = tbtmt.create_row()
                            new_tbt_row[enum.TBTField.TBT_Code][0] = iMaxTBTCode + 1
                            new_tbt_row[enum.TBTField.TBT_LineNo][0] = indx + 1
                            new_tbt_row[enum.TBTField.TBT_2DData][0] = mbLine
                            tbtmt.add_row(new_tbt_row)

                        out_file_name = self.ip + "_" + "tbt0uall.json"
                        tbtmt.to_json(out_file_name)
                        fileList["tbt"] = out_file_name
                        new_mub_row[enum.MUBField.MUB_Link2DBarcodeTextNo][0] = iMaxTBTCode + 1
                else:
                    new_mub_row[enum.MUBField.MUB_Data][0] = ','.join(multiBarcode2Lines)

                iMaxMubCode = mubmt.get_max_value_of_key()
                sql_params = [
                    iBarcodeType,
                    iMultiBarcodeType,
                    new_mub_row[enum.MUBField.MUB_Link2DBarcodeTextNo][0]
                ]
                # Not compare with for Data QR
                sql = "SELECT * FROM mub WHERE BarcodeType=? AND MultiBarcodeType=? AND Link2DBarcodeTextNo=?"
                iFoundCode = 0
                if iBarcodeType != 5:
                    sql += " AND Data=?"
                    sql_params.append(new_mub_row[enum.MUBField.MUB_Data][0])

                strCodes = mubmt.find_records(sql, sql_params)
                if strCodes:
                    iFoundCode = strCodes[0]["Code"][0]
                    new_plu_row[enum.PLUField.PLU_Multibarcode_2_No][0] = iFoundCode
                else:
                    new_mub_row[enum.MUBField.MUB_Code][0] = iMaxMubCode + 1
                    mubmt.add_row(new_mub_row)
                    out_file_name = self.ip + "_" + "mub0uall.json"
                    mubmt.to_json(out_file_name)
                    fileList["mub"] = out_file_name
                    new_plu_row[enum.PLUField.PLU_Multibarcode_2_No][0] = new_mub_row[enum.MUBField.MUB_Code][0]

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

                src_str_comp = ','.join(specialMessageLinesArr)
                strCodes = spmmt.find_records(
                    "SELECT Code FROM spm GROUP BY Code HAVING GROUP_CONCAT(Data) = ?", [src_str_comp])
                if strCodes:
                    iFoundCode = strCodes[0]["Code"][0]
                    new_plu_row[enum.PLUField.PLU_Special_message_No][0] = iFoundCode
                else:
                    iMaxSPMNo = spmmt.get_max_value_of_key()
                    for index, line in enumerate(specialMessageLinesArr):
                        new_spm_row = spmmt.create_row()
                        new_spm_row[enum.SPMField.SPM_Code][0] = iMaxSPMNo + 1
                        new_spm_row[enum.SPMField.SPM_LineNo][0] = index + 1
                        new_spm_row[enum.SPMField.SPM_Data][0] = line
                        if len(specialMessageLinesArr) == len(specialMessageLinesFontArr):
                            new_spm_row[enum.SPMField.SPM_Flag][0] = specialMessageLinesFontArr[index]

                        spmmt.add_row(new_spm_row)

                    out_file_name = self.ip + "_" + "spm0uall.json"
                    spmmt.to_json(out_file_name)
                    fileList["spm"] = out_file_name
                    new_plu_row[enum.PLUField.PLU_Special_message_No][0] = iMaxSPMNo + 1

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
                    # if type(oIngredientFont) in (str, unicode):
                    if isinstance(oIngredientFont, (str, unicode)):
                        ingredientLinesFontArr = [const.fontMapper.get(oIngredientFont, 0)] * len(ingredientLinesArr)
                    else:
                        ingredientLinesFontArr = [const.fontMapper.get("S1", 0)] * len(ingredientLinesArr)

                src_str_comp = ','.join(ingredientLinesArr)
                strCodes = ingmt.find_records(
                    "SELECT Code FROM ing GROUP BY Code HAVING GROUP_CONCAT(Data) = ?", [src_str_comp])
                if strCodes:
                    iFoundCode = strCodes[0]["Code"][0]
                    new_plu_row[enum.PLUField.PLU_Ingredient_No][0] = iFoundCode
                else:
                    iMaxIngNo = ingmt.get_max_value_of_key()
                    for index, line in enumerate(ingredientLinesArr):
                        new_ing_row = ingmt.create_row()
                        new_ing_row[enum.INGField.ING_Code][0] = iMaxIngNo + 1
                        new_ing_row[enum.INGField.ING_LineNo][0] = index + 1
                        new_ing_row[enum.INGField.ING_Data][0] = line
                        if len(ingredientLinesArr) == len(ingredientLinesFontArr):
                            new_ing_row[enum.INGField.ING_Flag][0] = ingredientLinesFontArr[index]

                        ingmt.add_row(new_ing_row)

                    out_file_name = self.ip + "_" + "ing0uall.json"
                    spmmt.to_json(out_file_name)
                    fileList["ing"] = out_file_name
                    new_plu_row[enum.PLUField.PLU_Ingredient_No][0] = iMaxIngNo + 1

            # Text
            for i in range(16):
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
                        # if type(oTextFont) in (str, unicode):
                        if isinstance(oTextFont, (str, unicode)):
                            textLinesFontArr = [const.fontMapper.get(oTextFont, 0)] * len(textLinesArr)
                        else:
                            textLinesFontArr = [const.fontMapper.get("S1", 0)] * len(textLinesArr)

                    src_str_comp = ','.join(textLinesArr)
                    strCodes = texmt.find_records(
                        "SELECT Code FROM tex GROUP BY Code HAVING GROUP_CONCAT(Data) = ?", [src_str_comp])
                    if strCodes:
                        iFoundCode = strCodes[0]["Code"][0]
                        new_plu_row[enum.PLUField.PLU_Text_1_No + i][0] = iFoundCode
                    else:
                        iMaxTexNo = texmt.get_max_value_of_key()
                        for index, line in enumerate(textLinesArr):
                            new_tex_row = texmt.create_row()
                            new_tex_row[enum.TEXField.TEX_Code][0] = iMaxTexNo + 1
                            new_tex_row[enum.TEXField.TEX_LineNo][0] = index + 1
                            new_tex_row[enum.TEXField.TEX_Data][0] = line
                            if len(textLinesArr) == len(textLinesFontArr):
                                new_tex_row[enum.TEXField.TEX_Flag][0] = textLinesFontArr[index]

                            texmt.add_row(new_tex_row)

                        out_file_name = self.ip + "_" + "tex0uall.json"
                        texmt.to_json(out_file_name)
                        fileList["tex"] = out_file_name
                        new_plu_row[enum.PLUField.PLU_Text_1_No + i][0] = iMaxTexNo + 1

            # Used by Date
            if iUsedByDate:
                new_plu_row[enum.PLUField.PLU_Used_by_date][0] = iUsedByDate
                new_plu_row[enum.PLUField.PLU_Flag_for_used_by_date][0] = 1

            # Sell by Date
            if iSellByDate:
                new_plu_row[enum.PLUField.PLU_Sell_by_date][0] = iSellByDate
                new_plu_row[enum.PLUField.PLU_Flag_for_sell_by_date][0] = 1

            # Packed by Date
            if iPackedByDate:
                new_plu_row[enum.PLUField.PLU_Packed_date][0] = iPackedByDate
                new_plu_row[enum.PLUField.PLU_Flag_for_packed_date][0] = 1

            # Sell by Time
            if strSellByTime:
                stk = strSellByTime.split(":")
                stk = [int(s) for s in stk]
                hm = reduce(lambda x, y: x * 100 + y, stk)
                new_plu_row[enum.PLUField.PLU_Flag_for_sell_by_time][0] = 1
                new_plu_row[enum.PLUField.PLU_Flag_for_RTC_sell_by_time][0] = 1
                new_plu_row[enum.PLUField.PLU_Sell_by_time][0] = hm

            # Packed By Time
            if strPackedByTime:
                stk = strPackedByTime.split(":")
                stk = [int(s) for s in stk]
                hm = reduce(lambda x, y: x * 100 + y, stk)
                new_plu_row[enum.PLUField.PLU_Flag_for_packed_time][0] = 1
                new_plu_row[enum.PLUField.PLU_Flag_for_RTC_packed_time][0] = 1
                new_plu_row[enum.PLUField.PLU_Packed_time][0] = hm

            # PLUNo
            new_plu_row[enum.PLUField.PLU_PLU_code][0] = iPLUNo
            # Weighting Flag
            new_plu_row[enum.PLUField.PLU_Flag_for_weighed_Non_weighed_item][0] = iWeightingFlag
            # Unit Price
            new_plu_row[enum.PLUField.PLU_Unit_Price][0] = int(fUnitPrice * 100)
            # Label Format 1
            new_plu_row[enum.PLUField.PLU_Label_1_format][0] = iLabelFormat1
            # MGNo
            new_plu_row[enum.PLUField.PLU_MG_No][0] = iMGNo
            # Traceability
            if iTraceabilityNo:
                new_plu_row[enum.PLUField.PLU_Traceability_No][0] = iTraceabilityNo
                new_plu_row[enum.PLUField.PLU_Flag_for_traceability][0] = 1

            # Ean Data
            if len(strItemCode) == 12:
                new_plu_row[enum.PLUField.PLU_Barcode_flag_of_EAN_data][0] = strItemCode[:2]
                new_plu_row[enum.PLUField.PLU_Item_code_of_EAN_data][0] = strItemCode[2:]

            if strBarcodeType == "EAN":
                bt = 0
            else:
                bt = 9
            new_plu_row[enum.PLUField.PLU_Barcode_type_of_EAN_data][0] = bt

            # Barcode Format
            if const.eanMapper.has_key(strBarcodeFormat):
                iBarNo = const.eanMapper[strBarcodeFormat]
            elif const.itfMapper.has_key(strBarcodeFormat):
                iBarNo = const.itfMapper[strBarcodeFormat]
            else:
                iBarNo = -1

            if iBarNo > 0:
                new_plu_row[enum.PLUField.PLU_Barcode_format][0] = iBarNo
            else:
                found, code, out_file = self.createJsonForFlexiBarcode(
                    flexiBarcodeJsonFile, strBarcodeType, strBarcodeFormat)

                if found:
                    iCode = 33 - 1 + code
                    new_plu_row[enum.PLUField.PLU_Barcode_format][0] = iCode
                elif code != 0:
                    new_plu_row[enum.PLUField.PLU_Barcode_format][0] = 33 - 1 + code
                    fileList["flb"] = out_file

            pluToDelete = plumt.create_row()
            pluToDelete[enum.PLUField.PLU_PLU_code][0] = iPLUNo
            pluToDelete[enum.PLUField.PLU_Flag_for_delete][0] = 1
            plumt.add_row(pluToDelete)

            plumt.add_row(new_plu_row)

        out_file_name = self.ip + "_" + "plu0uall.json"
        plumt.to_json(out_file_name)
        fileList["plu"] = out_file_name

        if fileList.has_key("flb"):
            sm120.send(flbmt)
        # print "sending flb ok"

        if fileList.has_key("mub"):
            sm120.send(mubmt)
        # print "sending mub ok"

        if fileList.has_key("tbt"):
            sm120.send(tbtmt)
        # print "sending tbt ok"

        if fileList.has_key("spm"):
            sm120.send(spmmt)
        # print "sending spm ok"

        if fileList.has_key("tex"):
            sm120.send(texmt)
        # print "sending tex ok"

        if fileList.has_key("ing"):
            sm120.send(ingmt)
        # print "sending ing ok"

        if fileList.has_key("plu"):
            sm120.send(plumt)
        # print "sending plu ok"

        common.common.log_info("Downloading Plu To %s Successfully..." % self.ip)
        return True

    def easySendTrace(self, trace_json_file):
        traceBarcodeJsonFile = self.ip + "_tracebarcode.json"
        traceTextJsonFile = self.ip + "_tracetext.json"

        trgmt = entity.TrgMaster()
        trbmt = entity.TrbMaster()
        trtmt = entity.TrtMaster()

        sm120 = digiscale.DigiSm120(self.ip, self.port, self.usr, self.pwd)
        sm120.connect()

        fileList = {}

        if not reduce(lambda x, y: x and y, [
            sm120.recv(trbmt),
            sm120.recv(trtmt)
        ]):
            common.common.log_err("Error On Receiving Data From Scale!")
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
            new_trg_row[enum.TRGField.TRG_ReferenceType][0] = 1

            # Traceability No
            new_trg_row[enum.TRGField.TRG_Code][0] = iTraceabilityNo
            if strReferenceCode:
                new_trg_row[enum.TRGField.TRG_ReferenceCode][0] = strReferenceCode

            # Barcode
            if strBarcode:

                strCodes = trbmt.find_records("SELECT Code FROM trb WHERE data = ?", [strBarcode])

                if strCodes:
                    iFoundCode = strCodes[0]["Code"][0]
                    new_trg_row[enum.TRGField.TRG_TraceBarcodeNo][0] = iFoundCode
                else:
                    new_trb_row = trbmt.create_row()
                    iMaxCode = trbmt.get_max_value_of_key()
                    new_trb_row[enum.TRBField.TRB_Data][0] = strBarcode
                    new_trb_row[enum.TRBField.TRB_Code][0] = iMaxCode + 1
                    trbmt.add_row(new_trb_row)
                    new_trg_row[enum.TRGField.TRG_TraceBarcodeNo][0] = new_trb_row[enum.TRBField.TRB_Code][0]

                    out_file_name = self.ip + "_" + "trb0uall.json"
                    trbmt.to_json(out_file_name)
                    fileList["trb"] = out_file_name

            # Text
            if textLines:
                traceTextLines = []
                traceTextLinesFont = []
                # if type(textLines) is list:
                if isinstance(textLines, list):
                    traceTextLines = textLines
                elif isinstance(textLines, (str, unicode)):
                    # elif type(textLines) in (str, unicode):
                    traceTextLines = [textLines]

                if textLinesFont:
                    traceTextLinesFont = [const.fontMapper.get(font, 0) for font in textLinesFont]

                if len(traceTextLines) != len(traceTextLinesFont):
                    # if type(traceTextLinesFont) in (str, unicode):
                    if isinstance(traceTextLinesFont, (str, unicode)):
                        traceTextLinesFont = [const.fontMapper.get(traceTextLinesFont, 0)] * len(traceTextLines)
                    else:
                        traceTextLinesFont = [const.fontMapper.get("S1", 0)] * len(traceTextLines)

                src_str_comp = ','.join(traceTextLines)
                strCodes = trtmt.find_records(
                    "SELECT Code FROM trt GROUP BY Code HAVING GROUP_CONCAT(Data) = ?",
                    [src_str_comp])
                if strCodes:
                    iFoundCode = strCodes[0]["Code"][0]
                    new_trg_row[enum.TRGField.TRG_TraceTextNo][0] = iFoundCode
                else:
                    iMaxTRTNo = trtmt.get_max_value_of_key()
                    for index, line in enumerate(traceTextLines):
                        new_trt_row = trtmt.create_row()
                        new_trt_row[enum.TRTField.TRT_Code][0] = iMaxTRTNo + 1
                        new_trt_row[enum.TRTField.TRT_LineNo][0] = index + 1
                        new_trt_row[enum.TRTField.TRT_Data][0] = line
                        if len(traceTextLines) == len(traceTextLinesFont):
                            new_trt_row[enum.TRTField.TRT_Flag][0] = traceTextLinesFont[index]

                        trtmt.add_row(new_trt_row)
                    new_trg_row[enum.TRGField.TRG_TraceTextNo][0] = new_trt_row[enum.TRTField.TRT_Code][0]

                    out_file_name = self.ip + "_" + "trt0uall.json"
                    trtmt.to_json(out_file_name)
                    fileList["trt"] = out_file_name

            trgToDelete = trgmt.create_row()
            trgToDelete[enum.TRGField.TRG_Code][0] = iTraceabilityNo
            trgToDelete[enum.TRGField.TRG_DeleteFlag][0] = 1
            trgmt.add_row(trgToDelete)

            trgmt.add_row(new_trg_row)

        out_file_name = self.ip + "_" + "trg0uall.json"
        trgmt.to_json(out_file_name)
        fileList["trg"] = out_file_name

        if fileList.has_key("trb"):
            sm120.send(trbmt)
        # print "sending trb ok"

        if fileList.has_key("trt"):
            sm120.send(trtmt)
        # print "sending trt ok"

        if fileList.has_key("trg"):
            sm120.send(trgmt)
        # print "sending trg ok"

        common.common.log_info("Downloading Traceability To %s Successfully..." % self.ip)
        return True

    def easyRecvPrintFormat(self, json_file_path):
        prfmt = entity.PrfMaster()
        pffmt = entity.PffMaster()

        sm120 = digiscale.DigiSm120(self.ip, self.port, self.usr, self.pwd)
        sm120.connect()
        if not sm120.connected: return False

        if sm120.recv(prfmt) and sm120.recv(pffmt):
            prf_all_data = prfmt.get_all_data()
            pff_all_data = pffmt.get_all_data()
            prfJsonArray = []

            for prf_cur_row in prf_all_data:
                prf_code = prf_cur_row[enum.PRFField.PRF_Code][0]
                prfJsonNode = {}
                prfJsonNode["Code"] = prf_code
                prfJsonNode["Width"] = prf_cur_row[enum.PRFField.PRF_Width][0]
                prfJsonNode["Height"] = prf_cur_row[enum.PRFField.PRF_Height][0]
                prfJsonNode["Angle"] = prf_cur_row[enum.PRFField.PRF_Angle][0]

                pffJsonArray = []
                for pff_cur_row in pff_all_data:
                    pff_code = pff_cur_row[enum.PFFField.PFF_Code][0]
                    if pff_code != prf_code: continue

                    pffJsonNode = {}

                    strFieldName = const.printFormatIndexList.get(pff_cur_row[enum.PFFField.PFF_FieldCode][0], "")
                    pffJsonNode["Field"] = strFieldName
                    pffJsonNode["YPosition"] = pff_cur_row[enum.PFFField.PFF_YPosition][0]
                    pffJsonNode["LabelType"] = pff_cur_row[enum.PFFField.PFF_LabelType][0]
                    pffJsonNode["XPosition"] = pff_cur_row[enum.PFFField.PFF_XPosition][0]
                    pffJsonNode["Angle"] = pff_cur_row[enum.PFFField.PFF_Angle][0]
                    pffJsonNode["PrintStatus"] = pff_cur_row[enum.PFFField.PFF_PrintStatus][0]
                    pffJsonNode["CharacterSize"] = pff_cur_row[enum.PFFField.PFF_CharSize][0]
                    pffJsonNode["Width"] = pff_cur_row[enum.PFFField.PFF_Width][0]
                    pffJsonNode["Height"] = pff_cur_row[enum.PFFField.PFF_Height][0]
                    pffJsonNode["Thickness"] = pff_cur_row[enum.PFFField.PFF_Thickness][0]
                    pffJsonNode["X1Position"] = pff_cur_row[enum.PFFField.PFF_X1Position][0]
                    pffJsonNode["Y1Position"] = pff_cur_row[enum.PFFField.PFF_Y1Position][0]
                    pffJsonNode["LinkedFileNo"] = pff_cur_row[enum.PFFField.PFF_LinkedFileNo][0]
                    pffJsonNode["CharacterSizex2x4"] = pff_cur_row[enum.PFFField.PFF_CharSizex2x4][0]
                    pffJsonNode["CentType"] = pff_cur_row[enum.PFFField.PFF_CentType][0]
                    pffJsonNode["AutoSizing"] = pff_cur_row[enum.PFFField.PFF_AutoSizing][0]

                    pffJsonArray.append(pffJsonNode)

                prfJsonNode["Fields"] = pffJsonArray
                prfJsonArray.append(prfJsonNode)

            common.common.save_json_to_file(json_file_path, prfJsonArray)
            common.common.log_info("%s Created" % json_file_path)

    def easySendPrintFormat(self, fmt_json_file_path):
        prfJsonFilePath = self.ip + "_" + csJsonPrfFile
        pffJsonFilePath = self.ip + "_" + csJsonPffFile
        json_data = common.common.get_json_from_file(fmt_json_file_path)
        prfmt = entity.PrfMaster()
        pffmt = entity.PffMaster()
        for prf in json_data:
            strCode = prf.get("Code", "0")
            strWidth = prf.get("Width", "0")
            strHeight = prf.get("Height", "0")
            strAngle = prf.get("Angle", "0")

            # Delete Old Data
            ##################################################
            prf_new_row = prfmt.create_row()
            prf_new_row[enum.PRFField.PRF_Code][0] = strCode
            prf_new_row[enum.PRFField.PRF_DeleteFlag][0] = "2"
            prfmt.add_row(prf_new_row)
            ##################################################

            # New Data
            ##################################################
            prf_new_row = prfmt.create_row()
            prf_new_row[enum.PRFField.PRF_Code][0] = strCode
            prf_new_row[enum.PRFField.PRF_Width][0] = strWidth
            prf_new_row[enum.PRFField.PRF_Height][0] = strHeight
            prf_new_row[enum.PRFField.PRF_Angle][0] = strAngle
            prfmt.add_row(prf_new_row)
            ##################################################

            for fieldNode in prf.get("Fields", []):
                pff_new_row = pffmt.create_row()
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
                pff_new_row[enum.PFFField.PFF_Code][0] = strCode
                pff_new_row[enum.PFFField.PFF_FieldCode][0] = str(
                    const.printFormatIndexListStringList.get(strField, -1))
                pff_new_row[enum.PFFField.PFF_YPosition][0] = iYPosition
                pff_new_row[enum.PFFField.PFF_LabelType][0] = iLabelType
                pff_new_row[enum.PFFField.PFF_XPosition][0] = iXPosition
                pff_new_row[enum.PFFField.PFF_Angle][0] = iAngle
                pff_new_row[enum.PFFField.PFF_PrintStatus][0] = iPrintStatus
                pff_new_row[enum.PFFField.PFF_CharSize][0] = iCharacterSize
                pff_new_row[enum.PFFField.PFF_Width][0] = iWidth
                pff_new_row[enum.PFFField.PFF_Height][0] = iHeight
                pff_new_row[enum.PFFField.PFF_Thickness][0] = iThickness
                pff_new_row[enum.PFFField.PFF_X1Position][0] = iX1Position
                pff_new_row[enum.PFFField.PFF_Y1Position][0] = iY1Position
                pff_new_row[enum.PFFField.PFF_LinkedFileNo][0] = iLinkedFileNo
                pff_new_row[enum.PFFField.PFF_LinkedFileSource][0] = iLinkedFileSouce
                pff_new_row[enum.PFFField.PFF_CharSizex2x4][0] = iCharacterSizex2x4
                pff_new_row[enum.PFFField.PFF_CentType][0] = iCentType
                pff_new_row[enum.PFFField.PFF_AutoSizing][0] = iAutoSizing
                pffmt.add_row(pff_new_row)

        sm120 = digiscale.DigiSm120(self.ip, self.port, self.usr, self.pwd)
        sm120.connect()
        if not sm120.connected: return False
        if not sm120.send(prfmt) or not sm120.send(pffmt):
            common.common.log_err("Failed To Send Label Format")
            return False

        common.common.log_info("Sending Label Format To %s Successfully" % self.ip)
        return True

    def exportCSV(
            self,
            export_template_file="",
            export_template_info="",
            export_csv_file="",
            title=False,
            encoding=sys.getdefaultencoding(),
            append=True):

        if export_template_file:
            json_data = common.common.get_json_from_file(export_template_file)
        elif export_template_info:
            if isinstance(export_template_info, str):
                json_data = common.common.get_json_from_string(export_template_info)
            else:
                json_data = export_template_info

        sql = json_data.get("SQL", "")
        tableNames = json_data.get("Tables", "")
        targetFields = json_data.get("Fields", [])

        table_list = tableNames.split(",")

        sm120 = digiscale.DigiSm120(self.ip, self.port, self.usr, self.pwd)
        sm120.connect()
        if not sm120.connected: return False

        master_list = map(lambda x: entity.MasterFactory().createMaster(x.strip()), table_list)

        for m in master_list:
            if not sm120.recv(m):
                common.common.log_info("Retrieving %s From %s Failed" % (m.name, self.ip))
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
                    # fp.write(",".join(field_names) + "\n");
                    fp.write(",".join(field_names).decode('utf8').encode(encoding) + "\r\n")

            for row in cursor:
                cells = [unicode(cell).encode(encoding) for cell in row]
                if targetFields:
                    target_cells = []
                    for target_field in targetFields:
                        strpar = common.strparser.StrParser(target_field, cells)
                        target_cells.append(strpar.eval(0))
                    fp.write(",".join(target_cells) + "\r\n")
                else:
                    fp.write(",".join(cells) + "\n")

        common.common.log_info("Exporting From %s To %s Successfully..." % (self.ip, export_csv_file))
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
                template_infos["Master"].add_row(newLine)

    def easyDeleteFile(self, mas_name):
        master_list = mas_name.split(',')
        sm120 = digiscale.DigiSm120(self.ip, self.port, self.usr, self.pwd)
        sm120.connect()
        if not sm120.connected: return False
        for master_name in master_list:
            master = entity.MasterFactory().createMaster(master_name)
            if not sm120.dele(master): return False
        return True

    def easyImportMaster(
            self,
            csv_file_path,
            json_fmt_file_path,
            json_scale_group_file="",
            json_filter_file=""):
        # print common.common.slurp(csv_file_path)
        json_data = common.common.get_json_from_file(json_fmt_file_path)
        self.createMasterList = {}

        strMgNo = ""
        if json_scale_group_file:
            dGrp = common.scalegroup.DigiGroup()
            dGrp.read_from_config_file(json_scale_group_file)
            strMgNo = str(dGrp.get_mgno_from_scale(self.ip))

        self.dataFilter = common.datafilter.DataFilter()
        globalVals = {"ScaleGroupNo": strMgNo}
        self.dataFilter.set_glob_vars(globalVals)

        if json_filter_file:
            json_data2 = common.common.get_json_from_file(json_filter_file)
            # if type(json_data2) is list:
            if isinstance(json_data2, list):
                self.dataFilter.set_expressions([dat for dat in json_data2])

        for fmt in json_data:
            source_expr = fmt["source_expr"]
            target_field = fmt["target_field"]
            line_no_field = fmt.get("line_no_field", "LineNo")
            sp_data = target_field.split(".")
            clsName = sp_data[0]
            fieldName = sp_data[1]
            if len(sp_data) > 2:
                lineNo = int(sp_data[2])
            else:
                lineNo = 0
            # lineNo = int(sp_data[2] if len(sp_data) > 2 else '0')

            if not self.createMasterList.has_key(clsName):
                self.createMasterList[clsName] = {}
                self.createMasterList[clsName]["infos"] = []
                self.createMasterList[clsName]["Master"] = entity.MasterFactory().createMaster(clsName)

            self.createMasterList[clsName]["infos"].append(
                {
                    "source_expression": source_expr,
                    "field_name": fieldName,
                    "line_no_field": line_no_field,
                    "line_no": lineNo,
                }
            )

        common.csvreader.SmCsvReader().read_line_by_line(
            csv_file_path,
            self.process_line)

        sm120 = digiscale.DigiSm120(self.ip, self.port, self.usr, self.pwd)
        sm120.connect()
        if not sm120.connected: return False
        for clsName, template_infos in self.createMasterList.items():
            if not sm120.send(template_infos["Master"]):
                common.common.log_err("Downloading To Scale Failed...")
                return False

        common.common.log_info("Downloading To %s Successfully..." % self.ip)
        return True

    # if __name__ == "__main__":
    # Easy("S0501").easyImportMaster("mgp_import.csv", "im.it")
    # Easy("S0501"). easySendPrintFormat("fmt.json")
    # Easy("S0501").easySendPlu("easyplu.json")
    # Easy("S0501").easySendTrace("easytrace.json")
    # plumd = common.common.MasterFactory().createMaster('Plu')
    # entity.PrfMaster().to_json("aaaa.json")
    # entity.PrfMaster().from_json("aaaa.json")
