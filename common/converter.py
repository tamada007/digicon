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

from threading import Thread

FLEXIBARCODE_converter = {
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

TRACE_converter = {
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

PRESETKEY_converter = {
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

PLU_converter = {
	"sm110": [
		{"source": "$(PLUNo)",                         "target": "Plu.PLUNo"},
		{"source": "$(UnitPrice)",                     "target": "Plu.UnitPrice"},
		{
			"source": "0000000isnull($(WeightingFlag),0) 000isnull($(PriceOverride),0)0000",
			"target": "Plu.PLUStatus1"
		},
		{"source": "isnull($(BarcodeFlag),00)",        "target": "Plu.F1F2"},
		{
			"source": "isnull($(ItemCode),0000000000),isnull($(BarcodeType),EAN),isnull($(BarcodeX),0)",
			"target": "Plu.EANData"
		},
		{
			"condition": "isnotempty($(PlaCode))",
			"statements": [
				{
					"source": "$(PlaCode)",
					"target": "Plu.PlaceNumber"
				},
				{
					"condition": "isnotempty($(PlaceName))",
					"statements": [
						{ "source": "$(PlaCode)",      "target": "Pla.Code",	},
						{ "source": 'isnull($(PlaceFont),21),"csvformat($(PlaceName))"',    "target": "Pla.PlaceName" }
					]
				}
			]
		},
		{
			#"sourceold": "twsascii(\"$(Commodity1Font),$(Commodity2Font),$(Commodity3Font),$(Commodity4Font)\",\"csvformat($(Commodity1)),csvformat($(Commodity2)),csvformat($(Commodity3)),csvformat($(Commodity4))\")",
			"source": 'twsascii("$(Commodity1Font),$(Commodity2Font),$(Commodity3Font),$(Commodity4Font)","""csvformat4($(Commodity1))"",""csvformat4($(Commodity2))"",""csvformat4($(Commodity3))"",""csvformat4($(Commodity4))""")',
			"target": "Plu.Commodity"
		},
		{"source": "isnull($(BarcodeFormat),0)",       "target": "Plu.BarcodeFormat"},
		{"source": "isnull($(LabelFormat1),17)",       "target": "Plu.LabelFormat1"},
		{"source": "$(UsedByDate)",                    "target": "Plu.UsedByDate"},
		{"source": "$(SellByDate)",                    "target": "Plu.SellByDate"},
		{"source": "$(PackedByDate)",                  "target": "Plu.PackedDate"},
		{"source": "$(SellByTime)",                    "target": "Plu.SellByTime"},
		{"source": "$(PackedByTime)",                  "target": "Plu.PackedTime"},
		{"source": "$(MGNo)",                          "target": "Plu.MGCode"},
		{
			#"sourceold": "twsascii(\"$(SpecialMessage1Font),$(SpecialMessage2Font),$(SpecialMessage3Font),$(SpecialMessage4Font),$(SpecialMessage5Font),$(SpecialMessage6Font),$(SpecialMessage7Font),$(SpecialMessage8Font),$(SpecialMessage9Font),$(SpecialMessage10Font)\",\"csvformat($(SpecialMessage1)),csvformat($(SpecialMessage2)),csvformat($(SpecialMessage3)),csvformat($(SpecialMessage4)),csvformat($(SpecialMessage5)),csvformat($(SpecialMessage6)),csvformat($(SpecialMessage7)),csvformat($(SpecialMessage8)),csvformat($(SpecialMessage9)),csvformat($(SpecialMessage10))\")",
			"source": 'twsascii("$(SpecialMessage1Font),$(SpecialMessage2Font),$(SpecialMessage3Font),$(SpecialMessage4Font),$(SpecialMessage5Font),$(SpecialMessage6Font),$(SpecialMessage7Font),$(SpecialMessage8Font),$(SpecialMessage9Font),$(SpecialMessage10Font)","""csvformat4($(SpecialMessage1))"",""csvformat4($(SpecialMessage2))"",""csvformat4($(SpecialMessage3))"",""csvformat4($(SpecialMessage4))"",""csvformat4($(SpecialMessage5))"",""csvformat4($(SpecialMessage6))"",""csvformat4($(SpecialMessage7))"",""csvformat4($(SpecialMessage8))"",""csvformat4($(SpecialMessage9))"",""csvformat4($(SpecialMessage10))""")',
			"target": "Plu.SpecialMessage"
		},
		{
			#"sourceold": "twsascii(\"$(Ingredient1Font),$(Ingredient2Font),$(Ingredient3Font),$(Ingredient4Font),$(Ingredient5Font),$(Ingredient6Font),$(Ingredient7Font),$(Ingredient8Font),$(Ingredient9Font),$(Ingredient10Font)\",\"csvformat($(Ingredient1)),csvformat($(Ingredient2)),csvformat($(Ingredient3)),csvformat($(Ingredient4)),csvformat($(Ingredient5)),csvformat($(Ingredient6)),csvformat($(Ingredient7)),csvformat($(Ingredient8)),csvformat($(Ingredient9)),csvformat($(Ingredient10))\")",			
			"source": 'twsascii("$(Ingredient1Font),$(Ingredient2Font),$(Ingredient3Font),$(Ingredient4Font),$(Ingredient5Font),$(Ingredient6Font),$(Ingredient7Font),$(Ingredient8Font),$(Ingredient9Font),$(Ingredient10Font)","""csvformat4($(Ingredient1))"",""csvformat4($(Ingredient2))"",""csvformat4($(Ingredient3))"",""csvformat4($(Ingredient4))"",""csvformat4($(Ingredient5))"",""csvformat4($(Ingredient6))"",""csvformat4($(Ingredient7))"",""csvformat4($(Ingredient8))"",""csvformat4($(Ingredient9))"",""csvformat4($(Ingredient10))""")',			
			"target": "Plu.Ingredient"
		},
		{
			"condition": "isnotempty($(Multibarcode1))",
			"source": "1,$(Multibarcode1),2",
			"target": "Plu.MultiBarcode1"
		},
		{
			"condition": "isnotempty($(Multibarcode2))",
			"statements": [
				{
					"condition": "isnotempty($(NoLinkTo2DBarcodeText))",
					"source": "5,$(Multibarcode2),2",
					"target": "Plu.MultiBarcode2"
				},
				{
					"condition": "isempty($(NoLinkTo2DBarcodeText))",
					"source": "5,isnull($(MubCode2),$(CurLineNo)),3", 
					"target": "Plu.MultiBarcode2"
				},
				{
					"condition": "isempty($(NoLinkTo2DBarcodeText))",
					"source": "isnull($(MubCode2),$(CurLineNo))",
					"target": "Tbt.Code"
				},
				{
					"comment": "isnotnull(\"csvindex(1,$(Multibarcode2))\",\"21,\"\"csvindex(1,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(2,$(Multibarcode2))\",\"\n21,\"\"csvindex(2,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(3,$(Multibarcode2))\",\"\n21,\"\"csvindex(3,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(4,$(Multibarcode2))\",\"\n21,\"\"csvindex(4,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(5,$(Multibarcode2))\",\"\n21,\"\"csvindex(5,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(6,$(Multibarcode2))\",\"\n21,\"\"csvindex(6,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(7,$(Multibarcode2))\",\"\n21,\"\"csvindex(7,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(8,$(Multibarcode2))\",\"\n21,\"\"csvindex(8,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(9,$(Multibarcode2))\",\"\n21,\"\"csvindex(9,$(Multibarcode2))\"\"\")isnotnull(\"csvindex(10,$(Multibarcode2))\",\"\n21,\"\"csvindex(10,$(Multibarcode2))\"\"\")",
					"condition": "isempty($(NoLinkTo2DBarcodeText))", 
					"source": 'twsascii("21,21,21,21,21,21,21,21,21,21","csvindex(1,csvformat($(Multibarcode2))),csvindex(2,csvformat($(Multibarcode2))),csvindex(3,csvformat($(Multibarcode2))),csvindex(4,csvformat($(Multibarcode2))),csvindex(5,csvformat($(Multibarcode2))),csvindex(6,csvformat($(Multibarcode2))),csvindex(7,csvformat($(Multibarcode2))),csvindex(8,csvformat($(Multibarcode2))),csvindex(9,csvformat($(Multibarcode2))),csvindex(10,csvformat($(Multibarcode2)))")',
					"target": "Tbt.Data"
				}
			]
		},

		{
			"condition": "isnotempty($(Text1))",
			"statements": [
				{"source": "isnull($(TexCode1),$(CurLineNo))",               "target": "Plu.LinkedText1No"},
				{"source": "isnull($(TexCode1),$(CurLineNo))",               "target": "Tex.Code.1"},
				{"source": 'isnull($(Text1Font),0),"$(Text1)"',              "target": "Tex.Name.1"}
			]
		},
		{
			"condition": "isnotempty($(Text2))",
			"statements": [
				{"source": "isnull($(TexCode2),$(CurLineNo))",               "target": "Plu.LinkedText2No"},
				{"source": "isnull($(TexCode2),$(CurLineNo))",               "target": "Tex.Code.2"},
				{"source": 'isnull($(Text2Font),0),"$(Text2)"',              "target": "Tex.Name.2"}
			]
		},
		{
			"condition": "isnotempty($(Text3))",
			"statements": [
				{"source": "isnull($(TexCode3),$(CurLineNo))",               "target": "Plu.LinkedText3No"},
				{"source": "isnull($(TexCode3),$(CurLineNo))",               "target": "Tex.Code.3"},
				{"source": 'isnull($(Text3Font),0),"$(Text3)"',              "target": "Tex.Name.3"}
			]
		},
		{
			"condition": "isnotempty($(Text4))",
			"statements": [
				{"source": "isnull($(TexCode4),$(CurLineNo))",               "target": "Plu.LinkedText4No"},
				{"source": "isnull($(TexCode4),$(CurLineNo))",               "target": "Tex.Code.4"},
				{"source": 'isnull($(Text4Font),0),"$(Text4)"',              "target": "Tex.Name.4"}
			]
		},
		{
			"condition": "isnotempty($(Text5))",
			"statements": [
				{"source": "isnull($(TexCode5),$(CurLineNo))",               "target": "Plu.LinkedText5No"},
				{"source": "isnull($(TexCode5),$(CurLineNo))",               "target": "Tex.Code.5"},
				{"source": 'isnull($(Text5Font),0),"$(Text5)"',              "target": "Tex.Name.5"}
			]
		},
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
		{
			"condition": "isnotempty($(TraceabilityFlag))",
			"source": "$(TraceabilityFlag)",
			"target": "Plu.Traceability"
		},
		{
			"condition": "isnotempty($(TraceabilityNo))",
			"source": "$(TraceabilityNo)",
			"target": "Plu.TraceabilityLink"
		}
	],
	"sm120": [
		{"source": "$(PLUNo)",          "target": "Plu.PLUNo"},
		{"source": "$(UnitPrice)",      "target": "Plu.UnitPrice"},
		{
			"source": "isnull($(WeightingFlag),0)",
			"target": "Plu.WeightingFlag"
		},
		{
			"source": "isnull($(BarcodeFlag),0)",
			"target": "Plu.BarcodeFlagOfEanData"
		},
		{
			"source": "isnull($(PriceOverride),0)",
			"target": "Plu.UnitPriceOverrideFlag"
		},
		{
			"source": "isnull($(ItemCode),0000000000",
			"target": "Plu.ItemCode"
		},
			
		{
			"condition": "isnotempty($(PlaCode))",
			"statements": [
				{ "source": "$(PlaCode)",					"target": "Plu.PlaceNo" 	},
				{
					"condition": "isnotempty($(PlaceName))",
					"statements": [
						{"source": "$(PlaCode)",        "target": "Pla.Code.-1"},
						{"source": "1",                 "target": "Pla.LineNo.-1"},
						{"source": "2",                 "target": "Pla.DeleteFlag.-1"},
						{"source": "0",                 "target": "Pla.PlaceFlag.-1"},
						
						{"source": "$(PlaCode)",        "target": "Pla.Code.1",	},
						{"source": "1",                 "target": "Pla.LineNo.1"},
						{"source": 'isnull($(PlaceFont),21)',    "target": "Pla.PlaceFlag.1" },
						{"source": '$(PlaceName)',      "target": "Pla.PlaceName.1" }
					]
				}
			]
		},
			
		{
			"condition": "isnotempty($(Commodity1))",
			"statements": [
				{"source": '"csvformat($(Commodity1))"',   "target": "Plu.CommodityName1"},
				{"source": "isnull($(Commodity1Font),0)",  "target": "Plu.CommodityFont1"}
			]
		},
		{
			"condition": "isnotempty($(Commodity2))",
			"statements": [
				{"source": '"csvformat($(Commodity2))"',   "target": "Plu.CommodityName2"},
				{"source": "isnull($(Commodity2Font),0)",  "target": "Plu.CommodityFont2"}
			]
		},
		{
			"condition": "isnotempty($(Commodity3))",
			"statements": [
				{"source": '"csvformat($(Commodity3))"',   "target": "Plu.CommodityName3"},
				{"source": "isnull($(Commodity3Font),0)",  "target": "Plu.CommodityFont3"}
			]
		},
		{
			"condition": "isnotempty($(Commodity4))",
			"statements": [
				{"source": '"csvformat($(Commodity4))"',   "target": "Plu.CommodityName4"},
				{"source": "isnull($(Commodity4Font),0)",  "target": "Plu.CommodityFont4"}
			]
		},
		{
			"source": "isnull($(BarcodeFormat),0)",
			"target": "Plu.BarcodeFormat"
		},
		{
			"source": "isnull($(LabelFormat1),0)",
			"target": "Plu.LabelFormat1"
		},
		{
			"condition": "isnotempty($(UsedByDate))",
			"statements": [
				{ "source": "1",             "target": "Plu.UsedByDateFlag" },
				{ "source": "$(UsedByDate)", "target": "Plu.UsedByDate" }
			]
		},
		{
			"condition": "isnotempty($(SellByDate))",
			"statements": [
				{ "source": "1",             "target": "Plu.SellByDateFlag" },
				{ "source": "$(SellByDate)", "target": "Plu.SellByDate" }
			]
		},
		{
			"condition": "isnotempty($(PackedByDate))",
			"statements": [
				{ "source": "1",               "target": "Plu.PackedDateFlag" },
				{ "source": "$(PackedByDate)", "target": "Plu.PackedDate" }
			]
		},

		{
			"condition": "isnotempty($(PackedByTime))",
			"statements": [
				{ "source": "1",               "target": "Plu.PackedTimeFlag" },
				{ "source": "$(PackedByTime)", "target": "Plu.PackedTime" }
			]
		},
		{
			"condition": "isnotempty($(SellByTime))",
			"statements": [
				{ "source": "1",               "target": "Plu.SellByTimeFlag" },
				{ "source": "$(SellByTime)",   "target": "Plu.SellByTime" }
			]
		},
		
		{"source": "$(MGNo)",           "target": "Plu.MGNo"},
		{
			"source": "iif(equals($(BarcodeType),EAN),0,9",
			"target": "Plu.BarcodeTypeOfEanData"
		},
		{"source": "isnull($(SpmCode),$(CurLineNo))",        "target": "Plu.SpecialMessageNo"},
		{"source": "isnull($(IngCode),$(CurLineNo))",        "target": "Plu.IngredientNo"},
		{
			"condition": "isnotempty($(TraceabilityFlag))",
			"source": "$(TraceabilityFlag)",
			"target": "Plu.TraceabilityFlag"
		},
		{
			"condition": "isnotempty($(TraceabilityNo))",
			"source": "$(TraceabilityNo)",
			"target": "Plu.TraceabilityNo"
		},
		{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.-1"},
		{"source": "1",                                 "target": "Spm.LineNo.-1"},
		{"source": "2",                                 "target": "Spm.DeleteFlag.-1"},
		{
			"condition": "isnotempty($(SpecialMessage1))",
			"statements": [
				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.1"},
				{"source": "1",                                 "target": "Spm.LineNo.1"},
				{"source": '"csvformat($(SpecialMessage1))"',   "target": "Spm.Data.1"},
				{"source": "isnull($(SpecialMessage1Font),0)",  "target": "Spm.Flag.1"}
			]
		},
		{
			"condition": "isnotempty($(SpecialMessage2))",
			"statements": [
				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.2"},
				{"source": "2",                                 "target": "Spm.LineNo.2"},
				{"source": '"csvformat($(SpecialMessage2))"',   "target": "Spm.Data.2"},
				{"source": "isnull($(SpecialMessage2Font),0)",  "target": "Spm.Flag.2"}
			]
		},
		{
			"condition": "isnotempty($(SpecialMessage3))",
			"statements": [
				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.3"},
				{"source": "3",                                 "target": "Spm.LineNo.3"},
				{"source": '"csvformat($(SpecialMessage3))"',   "target": "Spm.Data.3"},
				{"source": "isnull($(SpecialMessage3Font),0)",  "target": "Spm.Flag.3"}
			]
		},
		{
			"condition": "isnotempty($(SpecialMessage4))",
			"statements": [
				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.4"},
				{"source": "4",                                 "target": "Spm.LineNo.4"},
				{"source": '"csvformat($(SpecialMessage4))"',   "target": "Spm.Data.4"},
				{"source": "isnull($(SpecialMessage4Font),0)",  "target": "Spm.Flag.4"}
			]
		},
		{
			"condition": "isnotempty($(SpecialMessage5))",
			"statements": [
				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.5"},
				{"source": "5",                                 "target": "Spm.LineNo.5"},
				{"source": '"csvformat($(SpecialMessage5))"',   "target": "Spm.Data.5"},
				{"source": "isnull($(SpecialMessage5Font),0)",  "target": "Spm.Flag.5"}
			]
		},
		{
			"condition": "isnotempty($(SpecialMessage6))",
			"statements": [
				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.6"},
				{"source": "6",                                 "target": "Spm.LineNo.6"},
				{"source": '"csvformat($(SpecialMessage6))"',   "target": "Spm.Data.6"},
				{"source": "isnull($(SpecialMessage6Font),0)",  "target": "Spm.Flag.6"}
			]
		},
		{
			"condition": "isnotempty($(SpecialMessage7))",
			"statements": [
				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.7"},
				{"source": "7",                                 "target": "Spm.LineNo.7"},
				{"source": '"csvformat($(SpecialMessage7))"',   "target": "Spm.Data.7"},
				{"source": "isnull($(SpecialMessage7Font),0)",  "target": "Spm.Flag.7"}
			]
		},
		{
			"condition": "isnotempty($(SpecialMessage8))",
			"statements": [
				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.8"},
				{"source": "8",                                 "target": "Spm.LineNo.8"},
				{"source": '"csvformat($(SpecialMessage8))"',   "target": "Spm.Data.8"},
				{"source": "isnull($(SpecialMessage8Font),0)",  "target": "Spm.Flag.8"}
			]
		},
		{
			"condition": "isnotempty($(SpecialMessage9))",
			"statements": [
				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.9"},
				{"source": "9",                                 "target": "Spm.LineNo.9"},
				{"source": '"csvformat($(SpecialMessage9))"',   "target": "Spm.Data.9"},
				{"source": "isnull($(SpecialMessage9Font),0)",  "target": "Spm.Flag.9"}
			]
		},
		{
			"condition": "isnotempty($(SpecialMessage10))",
			"statements": [
				{"source": "isnull($(SpmCode),$(CurLineNo))",   "target": "Spm.Code.10"},
				{"source": "10",                                "target": "Spm.LineNo.10"},
				{"source": '"csvformat($(SpecialMessage10))"',  "target": "Spm.Data.10"},
				{"source": "isnull($(SpecialMessage10Font),0)", "target": "Spm.Flag.10"}
			]
		},
		{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.-1"},
		{"source": "1",                                 "target": "Ing.LineNo.-1"},
		{"source": "2",                                 "target": "Ing.DeleteFlag.-1"},
		{
			"condition": "isnotempty($(Ingredient1))",
			"statements": [
				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.1"},
				{"source": "1",                                 "target": "Ing.LineNo.1"},
				{"source": '"csvformat($(Ingredient1))"',       "target": "Ing.Data.1"},
				{"source": "isnull($(Ingredient1Font),0)",      "target": "Ing.Flag.1"}
			]
		},
		{
			"condition": "isnotempty($(Ingredient2))",
			"statements": [
				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.2"},
				{"source": "2",                                 "target": "Ing.LineNo.2"},
				{"source": '"csvformat($(Ingredient2))"',       "target": "Ing.Data.2"},
				{"source": "isnull($(Ingredient2Font),0)",      "target": "Ing.Flag.2"}
			]
		},
		{
			"condition": "isnotempty($(Ingredient3))",
			"statements": [
				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.3"},
				{"source": "3",                                 "target": "Ing.LineNo.3"},
				{"source": '"csvformat($(Ingredient3))"',       "target": "Ing.Data.3"},
				{"source": "isnull($(Ingredient3Font),0)",      "target": "Ing.Flag.3"}
			]
		},
		{
			"condition": "isnotempty($(Ingredient4))",
			"statements": [
				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.4"},
				{"source": "4",                                 "target": "Ing.LineNo.4"},
				{"source": '"csvformat($(Ingredient4))"',       "target": "Ing.Data.4"},
				{"source": "isnull($(Ingredient4Font),0)",      "target": "Ing.Flag.4"}
			]
		},
		{
			"condition": "isnotempty($(Ingredient5))",
			"statements": [
				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.5"},
				{"source": "5",                                 "target": "Ing.LineNo.5"},
				{"source": '"csvformat($(Ingredient5))"',       "target": "Ing.Data.5"},
				{"source": "isnull($(Ingredient5Font),0)",      "target": "Ing.Flag.5"}
			]
		},
		{
			"condition": "isnotempty($(Ingredient6))",
			"statements": [
				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.6"},
				{"source": "6",                                 "target": "Ing.LineNo.6"},
				{"source": '"csvformat($(Ingredient6))"',       "target": "Ing.Data.6"},
				{"source": "isnull($(Ingredient6Font),0)",      "target": "Ing.Flag.6"}
			]
		},
		{
			"condition": "isnotempty($(Ingredient7))",
			"statements": [
				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.7"},
				{"source": "7",                                 "target": "Ing.LineNo.7"},
				{"source": '"csvformat($(Ingredient7))"',       "target": "Ing.Data.7"},
				{"source": "isnull($(Ingredient7Font),0)",      "target": "Ing.Flag.7"}
			]
		},
		{
			"condition": "isnotempty($(Ingredient8))",
			"statements": [
				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.8"},
				{"source": "8",                                 "target": "Ing.LineNo.8"},
				{"source": '"csvformat($(Ingredient8))"',       "target": "Ing.Data.8"},
				{"source": "isnull($(Ingredient8Font),0)",      "target": "Ing.Flag.8"}
			]
		},
		{
			"condition": "isnotempty($(Ingredient9))",
			"statements": [
				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.9"},
				{"source": "9",                                 "target": "Ing.LineNo.9"},
				{"source": '"csvformat($(Ingredient9))"',       "target": "Ing.Data.9"},
				{"source": "isnull($(Ingredient9Font),0)",      "target": "Ing.Flag.9"}
			]
		},
		{
			"condition": "isnotempty($(Ingredient10))",
			"statements": [
				{"source": "isnull($(IngCode),$(CurLineNo))",   "target": "Ing.Code.10"},
				{"source": "10",                                "target": "Ing.LineNo.10"},
				{"source": '"csvformat($(Ingredient10))"',      "target": "Ing.Data.10"},
				{"source": "isnull($(Ingredient10Font),0)",     "target": "Ing.Flag.10"}
			]
		},

		{
			"condition": "isnotempty($(Text1))",
			"statements": [
				{"source": "isnull($(TexCode1),$(CurLineNo))",  "target": "Tex.Code.-1"},
				{"source": "1",                                 "target": "Tex.LineNo.-1"},
				{"source": "2",                                 "target": "Tex.DeleteFlag.-1"},
				{"source": "isnull($(TexCode1),$(CurLineNo))",  "target": "Plu.TextNo1"},
				{"source": "isnull($(TexCode1),$(CurLineNo))",  "target": "Tex.Code.1"},
				{"source": "1",                                 "target": "Tex.LineNo.1"},
				{"source": '"csvformat($(Text1))"',             "target": "Tex.Data.1"},
				{"source": "isnull($(Text1Font),0)",            "target": "Tex.Flag.1"}
			]
		},
		{
			"condition": "isnotempty($(Text2))",
			"statements": [
				{"source": "isnull($(TexCode2),$(CurLineNo))",  "target": "Tex.Code.-2"},
				{"source": "1",                                 "target": "Tex.LineNo.-2"},
				{"source": "2",                                 "target": "Tex.DeleteFlag.-2"},
				{"source": "isnull($(TexCode2),$(CurLineNo))",  "target": "Plu.TextNo2"},
				{"source": "isnull($(TexCode2),$(CurLineNo))",  "target": "Tex.Code.2"},
				{"source": "1",                                 "target": "Tex.LineNo.2"},
				{"source": '"csvformat($(Text2))"',             "target": "Tex.Data.2"},
				{"source": "isnull($(Text2Font),0)",            "target": "Tex.Flag.2"}
			]
		},
		{
			"condition": "isnotempty($(Text3))",
			"statements": [
				{"source": "isnull($(TexCode3),$(CurLineNo))",  "target": "Tex.Code.-3"},
				{"source": "1",                                 "target": "Tex.LineNo.-3"},
				{"source": "2",                                 "target": "Tex.DeleteFlag.-3"},
				{"source": "isnull($(TexCode3),$(CurLineNo))",  "target": "Plu.TextNo3"},
				{"source": "isnull($(TexCode3),$(CurLineNo))",  "target": "Tex.Code.3"},
				{"source": "1",                                 "target": "Tex.LineNo.3"},
				{"source": '"csvformat($(Text3))"',             "target": "Tex.Data.3"},
				{"source": "isnull($(Text3Font),0)",            "target": "Tex.Flag.3"}
			]
		},
		{
			"condition": "isnotempty($(Text4))",
			"statements": [
				{"source": "isnull($(TexCode4),$(CurLineNo))",  "target": "Tex.Code.-4"},
				{"source": "1",                                 "target": "Tex.LineNo.-4"},
				{"source": "2",                                 "target": "Tex.DeleteFlag.-4"},
				{"source": "isnull($(TexCode4),$(CurLineNo))",  "target": "Plu.TextNo4"},
				{"source": "isnull($(TexCode4),$(CurLineNo))",  "target": "Tex.Code.4"},
				{"source": "1",                                 "target": "Tex.LineNo.4"},
				{"source": '"csvformat($(Text4))"',             "target": "Tex.Data.4"},
				{"source": "isnull($(Text4Font),0)",            "target": "Tex.Flag.4"}
			]
		},
		{
			"condition": "isnotempty($(Text5))",
			"statements": [
				{"source": "isnull($(TexCode5),$(CurLineNo))",  "target": "Tex.Code.-5"},
				{"source": "1",                                 "target": "Tex.LineNo.-5"},
				{"source": "2",                                 "target": "Tex.DeleteFlag.-5"},
				{"source": "isnull($(TexCode5),$(CurLineNo))",  "target": "Plu.TextNo5"},
				{"source": "isnull($(TexCode5),$(CurLineNo))",  "target": "Tex.Code.5"},
				{"source": "1",                                 "target": "Tex.LineNo.5"},
				{"source": '"csvformat($(Text5))"',             "target": "Tex.Data.5"},
				{"source": "isnull($(Text5Font),0)",            "target": "Tex.Flag.5"}
			]
		},
		{
			"condition": "isnotempty($(Text6))",
			"statements": [
				{"source": "isnull($(TexCode6),$(CurLineNo))",  "target": "Tex.Code.-6"},
				{"source": "1",                                 "target": "Tex.LineNo.-6"},
				{"source": "2",                                 "target": "Tex.DeleteFlag.-6"},
				{"source": "isnull($(TexCode6),$(CurLineNo))",  "target": "Plu.TextNo6"},
				{"source": "isnull($(TexCode6),$(CurLineNo))",  "target": "Tex.Code.6"},
				{"source": "1",                                 "target": "Tex.LineNo.6"},
				{"source": '"csvformat($(Text6))"',             "target": "Tex.Data.6"},
				{"source": "isnull($(Text6Font),0)",            "target": "Tex.Flag.6"}
			]
		},
		{
			"condition": "isnotempty($(Text7))",
			"statements": [
				{"source": "isnull($(TexCode7),$(CurLineNo))",  "target": "Tex.Code.-7"},
				{"source": "1",                                 "target": "Tex.LineNo.-7"},
				{"source": "2",                                 "target": "Tex.DeleteFlag.-7"},
				{"source": "isnull($(TexCode7),$(CurLineNo))",  "target": "Plu.TextNo7"},
				{"source": "isnull($(TexCode7),$(CurLineNo))",  "target": "Tex.Code.7"},
				{"source": "1",                                 "target": "Tex.LineNo.7"},
				{"source": '"csvformat($(Text7))"',             "target": "Tex.Data.7"},
				{"source": "isnull($(Text7Font),0)",            "target": "Tex.Flag.7"}
			]
		},
		{
			"condition": "isnotempty($(Text8))",
			"statements": [
				{"source": "isnull($(TexCode8),$(CurLineNo))",  "target": "Tex.Code.-8"},
				{"source": "1",                                 "target": "Tex.LineNo.-8"},
				{"source": "2",                                 "target": "Tex.DeleteFlag.-8"},
				{"source": "isnull($(TexCode8),$(CurLineNo))",  "target": "Plu.TextNo8"},
				{"source": "isnull($(TexCode8),$(CurLineNo))",  "target": "Tex.Code.8"},
				{"source": "1",                                 "target": "Tex.LineNo.8"},
				{"source": '"csvformat($(Text8))"',             "target": "Tex.Data.8"},
				{"source": "isnull($(Text8Font),0)",            "target": "Tex.Flag.8"}
			]
		},
		{
			"condition": "isnotempty($(Text9))",
			"statements": [
				{"source": "isnull($(TexCode9),$(CurLineNo))",  "target": "Tex.Code.-9"},
				{"source": "1",                                 "target": "Tex.LineNo.-9"},
				{"source": "2",                                 "target": "Tex.DeleteFlag.-9"},
				{"source": "isnull($(TexCode9),$(CurLineNo))",  "target": "Plu.TextNo9"},
				{"source": "isnull($(TexCode9),$(CurLineNo))",  "target": "Tex.Code.9"},
				{"source": "1",                                 "target": "Tex.LineNo.9"},
				{"source": '"csvformat($(Text9))"',             "target": "Tex.Data.9"},
				{"source": "isnull($(Text9Font),0)",            "target": "Tex.Flag.9"}
			]
		},
		{
			"condition": "isnotempty($(Text10))",
			"statements": [
				{"source": "isnull($(TexCode10),$(CurLineNo))", "target": "Tex.Code.-10"},
				{"source": "1",                                 "target": "Tex.LineNo.-10"},
				{"source": "2",                                 "target": "Tex.DeleteFlag.-10"},
				{"source": "isnull($(TexCode10),$(CurLineNo))", "target": "Plu.TextNo10"},
				{"source": "isnull($(TexCode10),$(CurLineNo))", "target": "Tex.Code.10"},
				{"source": "1",                                 "target": "Tex.LineNo.10"},
				{"source": '"csvformat($(Text10))"',            "target": "Tex.Data.10"},
				{"source": "isnull($(Text10Font),0)",           "target": "Tex.Flag.10"}
			]
		},

		{
			"condition": "isnotempty($(Multibarcode1))",
			"statements": [
				{"source": "isnull($(MubCode1),$(CurLineNo))", "target": "Plu.Multibarcode1No"},
				{"source": "isnull($(MubCode1),$(CurLineNo))", "target": "Mub.Code.1"},
				{"source": "2",                                "target": "Mub.MultiBarcodeType.1"},
				{"source": "1",                                "target": "Mub.BarcodeType.1"},
				{"source": "$(Multibarcode1)",                 "target": "Mub.Data.1"}
			]
		},

		{
			"condition": "isnotempty($(Multibarcode2))",
			"statements": [
				{"source": "isnull($(TbtCode),$(CurLineNo))",   "target": "Tbt.Code.-1"},
				{"source": "1",                                 "target": "Tbt.LineNo.-1"},
				{"source": "2",                                 "target": "Tbt.DeleteFlag.-1"},

				{"source": "isnull($(MubCode2),$(CurLineNo))", "target": "Plu.Multibarcode2No"},
				{"source": "isnull($(MubCode2),$(CurLineNo))", "target": "Mub.Code.2"},
				{"source1": "3",                               "target1": "Mub.MultiBarcodeType.2"},
				{
					"source": "iif(isempty($(NoLinkTo2DBarcodeText)),3,2)",
					"target": "Mub.MultiBarcodeType.2"
				},
				{"source": "5",                                "target": "Mub.BarcodeType.2"},
				{
					"condition": "isempty($(NoLinkTo2DBarcodeText))",
					"source": "isnull($(TbtCode),$(CurLineNo))",
					"target": "Mub.Link2DBarcodeTextNo.2"
				},
				{
					"condition": "isnotempty($(NoLinkTo2DBarcodeText))",
					"source": "$(Multibarcode2)",
					"target": "Mub.Data.2"
				},
				{
					"condition1": "great(csvcount($(Multibarcode2)), 0)",
					"condition": "and(isempty($(NoLinkTo2DBarcodeText)),great(csvcount($(Multibarcode2)),0))",
					"statements": [
						{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.1"},
						{"source": "1",                                "target": "Tbt.LineNo.1"},
						{"source": '"csvindex(1,$(Multibarcode2))"',   "target": "Tbt.Data.1"},
						{
							"condition": "great(csvcount($(Multibarcode2)), 1)",
							"statements": [
								{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.2"},
								{"source": "2",                                "target": "Tbt.LineNo.2"},
								{"source": '"csvindex(2,$(Multibarcode2))"',   "target": "Tbt.Data.2"},
								{
									"condition": "great(csvcount($(Multibarcode2)), 2)",
									"statements": [
										{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.3"},
										{"source": "3",                                "target": "Tbt.LineNo.3"},
										{"source": '"csvindex(3,$(Multibarcode2))"',   "target": "Tbt.Data.3"},
										{
											"condition": "great(csvcount($(Multibarcode2)), 3)",
											"statements": [
												{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.4"},
												{"source": "4",                                "target": "Tbt.LineNo.4"},
												{"source": '"csvindex(4,$(Multibarcode2))"',   "target": "Tbt.Data.4"},
												{
													"condition": "great(csvcount($(Multibarcode2)), 4)",
													"statements": [
														{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.5"},
														{"source": "5",                                "target": "Tbt.LineNo.5"},
														{"source": '"csvindex(5,$(Multibarcode2))"',   "target": "Tbt.Data.5"},
														{
															"condition": "great(csvcount($(Multibarcode2)), 5)",
															"statements": [
																{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.6"},
																{"source": "6",                                "target": "Tbt.LineNo.6"},
																{"source": '"csvindex(6,$(Multibarcode2))"',   "target": "Tbt.Data.6"},
																{
																	"condition": "great(csvcount($(Multibarcode2)), 6)",
																	"statements": [
																		{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.7"},
																		{"source": "7",                                "target": "Tbt.LineNo.7"},
																		{"source": '"csvindex(7,$(Multibarcode2))"',   "target": "Tbt.Data.7"},
																		{
																			"condition": "great(csvcount($(Multibarcode2)), 7)",
																			"statements": [
																				{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.8"},
																				{"source": "8",                                "target": "Tbt.LineNo.8"},
																				{"source": '"csvindex(8,$(Multibarcode2))"',   "target": "Tbt.Data.8"},
																				{
																					"condition": "great(csvcount($(Multibarcode2)), 8)",
																					"statements": [
																						{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.9"},
																						{"source": "9",                                "target": "Tbt.LineNo.9"},
																						{"source": '"csvindex(9,$(Multibarcode2))"',   "target": "Tbt.Data.9"},
																						{
																							"condition": "great(csvcount($(Multibarcode2)), 9)",
																							"statements": [
																								{"source": "isnull($(TbtCode),$(CurLineNo))",  "target": "Tbt.Code.10"},
																								{"source": "10",                               "target": "Tbt.LineNo.10"},
																								{"source": '"csvindex(10,$(Multibarcode2))"',  "target": "Tbt.Data.10"}
																							]
																						}
																					]
																				}
																			]
																		}
																	]
																}
															]
														}
													]
												}
											]
										}
									]
								}
							]
						}
					]
				}
			]
		}

	]
}

class ScalesConverter():
	def __init__(self, conv=PLU_converter):
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
				
		self.createMasterList["Converter"] = {}
		self.createMasterList["Converter"]["infos"] = []
		for fmt in json_data:
			source_expr  = fmt["source_expr"]
			target_field = fmt["target_field"]
			sp_data = target_field.split(".")
			fieldName = sp_data[0]
			if len(sp_data) > 1:
				lineNo = int(sp_data[1])
			else:
				lineNo = 0

			self.createMasterList["Converter"]["infos"].append(
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

		self.dataFilter.set_field_list(cur_row)
		if self.dataFilter.is_filtered(): return True

		gv = {"CurLineNo": str(curLineNo + 1)}

		template_infos = self.createMasterList["Converter"]
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
		#value_list_sm110 = {}
		#value_list_sm120 = {}
		value_list={
			"sm110": {},
			"sm120": {}
		}

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
				
			if not self.createMasterList[scale_type].has_key(tgt_table):
				self.createMasterList[scale_type][tgt_table] = {}
				self.createMasterList[scale_type][tgt_table]["infos"] = []
				self.createMasterList[scale_type][tgt_table]["Master"] = self.masterFactory[scale_type].createMaster(tgt_table)
		
			if not value_list[scale_type].has_key(tgt_table):
				value_list[scale_type][tgt_table] = {}

			if not value_list[scale_type][tgt_table].has_key(tgt_lineno):
				value_list[scale_type][tgt_table][tgt_lineno] = self.createMasterList[scale_type][tgt_table]["Master"].create_row()

			value_list[scale_type][tgt_table][tgt_lineno][tgt_field][0] = result
			
		def parse_recur(curNode, scale_type):
			src       = curNode.get("source", None)
			dst       = curNode.get("target", None)
			cond      = curNode.get("condition", None)
			statments = curNode.get("statements", None)
			if cond and "TRUE" != self.strParser.eval(
					0,
					expr=cond, 
					fieldByIndex=[], 
					fieldByName=dic_data, 
					globalName=gv,
					resetPos=True):
				return

			if src and dst:
				append_line(src,dst, scale_type)
			if isinstance(statments, list):
				for statement in statments:
					parse_recur(statement, scale_type)

#  		beg = time.time(); #testonly

		#统一格式分派给具体秤
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



