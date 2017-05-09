# encoding=gbk

db_name = "sm110.sqlite"

report_list = {
    "Scale Data":
        {
            "SQL": "SELECT scale_ip_addr,scale_number_plu,scale_plu_remain FROM Scd",
            "Tables": "Scd",
            "Fields": [
                "hex2int(substr(lfill(int2hex($(1)),8),0,2)).hex2int(substr(lfill(int2hex($(1)),8),2,2)).hex2int(substr(lfill(int2hex($(1)),8),4,2)).hex2int(substr(lfill(int2hex($(1)),8),6,2))",
                "$(2)", "$(3)"]
        },
    "PLU Total":
        {
            "SQL": "SELECT Plt.PLUNo,plt.TOTAL_DAILY_TOTAL_ACTUAL_PRICE,Plu.Commodity FROM Plt inner join Plu on Plu.Pluno=plt.pluno",
            "Tables": "Plt, Plu",
            "Fields": ["$(1)", "csvindex(2, $(3))", "div($(2), 100)"]
        },
    "PLU Transaction":
        {
            "SQL": "SELECT T_PLU_TRANS_NO, T_PLU_TRANS_PLUNO, T_PLU_TRANS_TP, ITEM_NAME From Ptr",
            "Tables": "Ptr",
            "Fields": ["$(1)", "$(2)", "$(3)", "csvindex(2,$(4))"]
        },
    "Real Time Total Buffer":
        {
            "SQL": "select receiptno,TOTAL_WEIGHT,TOTAL_PRICE_WITH_TAX from rtt",
            "Tables": "Rtt",
            "Fields": ["$(1)", "$(2)", "$(3)"]
        },
    "Real Time Buffer":
        {
            "SQL": "select rtb.RecordNo 记录号,rtb.pluno 商品号,rtb.weight 重量,rtb.actual_price 金额,plu.commodity 品名,plu.specialmessage 特殊信息,plu.ingredient 成份,rtb.traceability_reference_code 追溯信息,rtb.jin_recbuf_weight_for_tw 日期,rtb.jin_recbuf_status_for_tw 时间 from Rtb left join Plu on Plu.Pluno = rtb.pluno",
            "Tables": "Rtb,Plu",
            "Fields": ["$(1)", "$(2)", "$(3)", "$(4)", "csvindex(2,$(5))", "csvindex(2,rtnindex(1,$(6)))",
                       "csvindex(2,rtnindex(1,$(7)))", "$(8)", "$(9)", "$(10)"]
        },

}

# Scale Data
scd_struct = [
    {
        "Name": "scale_data_code",
        "Key": 1,
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "scale_data_size",
        "Type": "HEX",
        "IsSize": 1,
        "Length": 2
    },
    {
        "Name": "scale_dept",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "scale_rct_shop",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "scale_lbl_shop",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "scale_preset_key",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "scale_code",
        "Type": "BCD",
        "Length": 3
    },
    {
        "Name": "scale_i_lbl_format",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "scale_t_lbl_format",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "scale_i_bar_barcode",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "scale_i_bar_r_data",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "scale_i_bar_r_price_data",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "scale_i_bar_flag",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "scale_t_barcode",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "scale_t_bar_l_data",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "scale_t_bar_fix_l_data",
        "Type": "BCD",
        "Length": 5
    },
    {
        "Name": "scale_t_bar_flag",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "scale_t_bar_r_data",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "scale_t_bar_prt_rct",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "scale_prt_bar_f1",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "scale_last_act_date",
        "Type": "BCD",
        "Length": 8
    },
    {
        "Name": "scale_plu_call_low",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "scale_plu_call_upper",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "scale_apc_date",
        "Type": "BCD",
        "Length": 3
    },
    {
        "Name": "scale_ethernet_addr",
        "Type": "HEX",
        "Length": 6
    },
    {
        "Name": "scale_ip_addr",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "scale_thermal_hd_usage_ctr",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "scale_version_num_main",
        "Type": "BYTES",
        "Length": 4
    },
    {
        "Name": "scale_number_plu",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "scale_ram_size",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "scale_preset_group",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "scale_rct_sp_special_message",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "scale_program_update_checksum",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "scale_mainboard_type",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "scale_plu_remain",
        "Type": "BCD",
        "Length": 4
	},
	{
        "Name": "scale_data_update_date",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "scale_data_update_time",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "scale_reserve",
        "Type": "BCD",
        "Length": 84
    }
]

# PLACE
pla_struct = [
    {
        "Name": "Code",
        "Key": 1,
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "RecordSize",
        "Type": "HEX",
        "Length": 2,
        "IsSize": 1
    },
    {
        "Name": "PlaceLabel",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "PlaceStatus",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "PlaceName",
        "Type": "ASCII",
        "Length": 103
	}
]

# MG
mgp_struct = [
    {
        "Name": "Code",
        "Key": 1,
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "RecordSize",
        "Type": "HEX",
        "Length": 2,
        "IsSize": 1
    },
    {
        "Name": "LinkedDeptCode",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "MGName",
        "Type": "BYTES",
        "Length": 16
    },
    {
        "Name": "CodeType",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "TaxRateNo",
        "Type": "BCD",
        "Length": 1
    }
]

# Traceability File
trg_struct = [
    {
        "Name": "Code",
        "Key": 1,
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "RecordSize",
        "IsSize": 1,
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "Born",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "Fatten",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "SlaughterHouse",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "SlaughterCountry",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "CuttingHall",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "CuttingCountry",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "ReferenceDate",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "CountryOfOrigin",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "ReferenceCode",
        "Type": "BYTES",
        "Length": 20
    },
    {
        "Name": "ReferenceType",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "Dummy",
        "Type": "BYTES",
        "Length": 1
    },
    {
        "Name": "TraceLink",
        # "Type": "BYTES",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "GTIN",
        "Type": "BYTES",
        "Length": 14
    },
    {
        "Name": "Kind",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "Category",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "Breed",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "LotNum",
        "Type": "BYTES",
        "Length": 30
    },
    {
        "Name": "ContactRef",
        "Type": "BYTES",
        "Length": 10
    },
    {
        "Name": "EatDate",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "Weight",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "BarcodeNo",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "SupplierCode",
        "Type": "BYTES",
        "Length": 30
    },
    {
        "Name": "SupplierName",
        "Type": "BYTES",
        "Length": 30
    },
    {
        "Name": "SupplierAddr1",
        "Type": "BYTES",
        "Length": 30
    },
    {
        "Name": "SupplierAddr2",
        "Type": "BYTES",
        "Length": 30
    }
]

# Password
pas_struct = [
    {
        "Name": "Code",
        "Key": 1,
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "RecordSize",
        "Type": "HEX",
        "Length": 2,
        "IsSize": 1
    },
    {
        "Name": "XModePwd",
        "Type": "BCD",
        "Length": 3
    },
    {
        "Name": "SModePwd",
        "Type": "BCD",
        "Length": 3
    },
    {
        "Name": "ZModePwd",
        "Type": "BCD",
        "Length": 3
    },
    {
        "Name": "PModePwd",
        "Type": "BCD",
        "Length": 3
    }
]

# Traceability Barcode File
trb_struct = [
    {
        "Name": "Code",
        "Key": 1,
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "RecordSize",
        "Type": "HEX",
        "Length": 2,
        "IsSize": 1
    },
    {
        "Name": "Dummy",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "Data",
        "Type": "BARCODEDATA",
        "Length": 1112
    }
]

# 2D Barcode
tbt_struct = [
    {
        "Name": "Code",
        "Key": 1,
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "RecordSize",
        "Type": "HEX",
        "Length": 2,
        "IsSize": 1
    },
    {
        "Name": "Dummy",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "Data",
        "Type": "ASCII",
        "Length": 10197
    }
]

# Preset Key
kas_struct = [
    {
        "Name": "Code",
        "Key": 1,
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "RecordSize",
        "Type": "HEX",
        "Length": 2,
        "IsSize": 1
    },
    {
        "Name": "SwitchNo",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "Status",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "CSize",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "Name",
        "Type": "BYTES",
        "Length": 32
    },
    {
        "Name": "ReferToFile",
        "Type": "HEX",
        "Length": 1
    }
]

# Plu
plu_struct = [
    {
        "Name": "PLUNo",
        "Key": 1,
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "RecordSize",
        "Type": "HEX",
        "Length": 2,
        "IsSize": 1
    },
    {
        "Name": "PLUStatus1",
        "Type": "BIN",
        "Length": 2,
        "Detail": [
            {
                "UNIT": 0,
                "UNIT PRICE": 1,
                "SELL BY DATE": 2,
                "USED BY DATE": 3,
                "PACKED DATE": 4,
                "SELL BY TIME": 5,
                "PACKED TIME": 6,
                "RTC PACKED TIME": 7
            },
            {
                "RTC SELL BY TIME": 0,
                "PRICE BASED PER UNIT": 1,
                "NUTRITION PRINT": 3,
                "UNIT PRICE OVERRIDE": 4,
                "SELL BY DATE SOURCE": 5,
                "SECURITY TAG ISSUE CONDITION": 6,
                "APPEND PLU DATA": 7
            }
        ]
    },
    {
        "Name": "PLUStatus2",
        "Type": "BIN",
        "Length": 3,
        "Detail": [
            {
                "LABEL 1 FORMAT": 0,
                "LABEL 2 FORMAT": 1,
                "BARCODE FORMAT": 2,
                "ITEM CODE": 3,
                "MAIN GROUP CODE": 4,
                "COST": 5,
                "PLU TARE": 6,
                "QUANTITY": 7
            },
            {
                "QUANTITY SYMBOL": 0,
                "SPECIAL MESSAGE #": 1,
                "INGREDIENT #": 2,
                "DISCOUNT": 3,
                "NUTRITION": 4,
                "COMMODITY": 5,
                "SPECIAL MESSAGE": 6,
                "INGREDIENT": 7
            },
            {
                "SELL BY DATE": 0,
                "SELL BY TIME": 1,
                "USED BY DATE": 2,
                "PACKED DATE": 3,
                "PACKED TIME": 4,
                "PLACE NUMBER": 5,
                "IMAGE NUMBER": 6,
                "PLU STATUSB & PLU STATUS 2B": 7
            }
        ]
    },
    {
        "Name": "UnitPrice",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "LabelFormat1",
        "Type": "HEX",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 1,
            "Bit": "LABEL 1 FORMAT"
        },
        "Length": 1
    },
    {
        "Name": "LabelFormat2",
        "Type": "HEX",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 1,
            "Bit": "LABEL 2 FORMAT"
        },
        "Length": 1
    },
    {
        "Name": "BarcodeFormat",
        "Type": "HEX",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 1,
            "Bit": "BARCODE FORMAT"
        },
        "Length": 1
    },
    {
        "Name": "F1F2",
        "Type": "F1F2",
        "Length": 1
    },
    {
        "Name": "EANData",
        "Type": "EAN",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 1,
            "Bit": "ITEM CODE"
        },
        "Length": 6
    },
    {
        "Name": "MGCode",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 1,
            "Bit": "MAIN GROUP CODE"
        },
        "Length": 2
    },
    {
        "Name": "SellByDate",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "SELL BY DATE"
        },
        "Printable": {
            "Name": "PLUStatus1",
            "Byte": 1,
            "Bit": "SELL BY DATE"
        },
        "Length": 2
    },
    {
        "Name": "SellByTime",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "SELL BY TIME"
        },
        "Printable": {
            "Name": "PLUStatus1",
            "Byte": 1,
            "Bit": "SELL BY TIME"
        },
        "Length": 2
    },
    {
        "Name": "UsedByDate",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "USED BY DATE"
        },
        "Printable": {
            "Name": "PLUStatus1",
            "Byte": 1,
            "Bit": "USED BY DATE"
        },
        "Length": 2
    },
    {
        "Name": "PackedDate",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "PACKED DATE"
        },
        "Printable": {
            "Name": "PLUStatus1",
            "Byte": 1,
            "Bit": "PACKED DATE"
        },
        "Length": 2
    },
    {
        "Name": "PackedTime",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "PACKED TIME"
        },
        "Printable": {
            "Name": "PLUStatus1",
            "Byte": 1,
            "Bit": "PACKED TIME"
        },
        "Length": 2
    },
    {
        "Name": "Cost",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 1,
            "Bit": "COST"
        },
        "Length": 4
    },
    {
        "Name": "PLUTare",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 1,
            "Bit": "PLU TARE"
        },
        "Length": 2
    },
    {
        "Name": "Quantity",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 1,
            "Bit": "QUANTITY"
        },
        "Length": 2
    },
    {
        "Name": "QuantitySymbolType",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 2,
            "Bit": "QUANTITY SYMBOL"
        },
        "Length": 1
    },
    {
        "Name": "SpecialMessageNo",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 2,
            "Bit": "SPECIAL MESSAGE #"
        },
        "Length": 1
    },
    {
        "Name": "IngredientNo",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 2,
            "Bit": "INGREDIENT #"
        },
        "Length": 1
    },
    {
        "Name": "PlaceNumber",
        "Type": "HEX",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "PLACE NUMBER"
        },
        "Length": 1
    },
    {
        "Name": "Image1",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "IMAGE NUMBER"
        },
        "Length": 1
    },
    {
        "Name": "Image2",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "IMAGE NUMBER"
        },
        "Length": 1
    },
    {
        "Name": "Image3",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "IMAGE NUMBER"
        },
        "Length": 1
    },
    {
        "Name": "Image4",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "IMAGE NUMBER"
        },
        "Length": 1
    },
    {
        "Name": "Image5",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "IMAGE NUMBER"
        },
        "Length": 1
    },
    {
        "Name": "Image6",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "IMAGE NUMBER"
        },
        "Length": 1
    },
    {
        "Name": "Image7",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "IMAGE NUMBER"
        },
        "Length": 1
    },
    {
        "Name": "Image8",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "IMAGE NUMBER"
        },
        "Length": 1
    },
    {
        "Name": "Image9",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "IMAGE NUMBER"
        },
        "Length": 1
    },
    {
        "Name": "Image10",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "IMAGE NUMBER"
        },
        "Length": 1
    },
    {
        "Name": "PLUStatus1B",
        "Type": "BIN",
        "Length": 4,
        "Related": "PLUStatus2B",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "PLU STATUSB & PLU STATUS 2B"
        },
        "Detail": [
            {
                "COUPLED PLU QUANTITY COPY": 0,
                "NEGATIVE PLU (VER XX.14)": 1,
                "PLU PRICE CHANGE": 2,
                "PRINT WEIGHT": 3,
                "PRINT UNIT PRICE": 4,
                "PRINT TOTAL PRICE": 5,
                "PRINT GROSS WT PROPOTIONAL TARE": 6
            },
            {},
            {},
            {
                "PACKED DATE SOURCE": 0
            }
        ]
    },
    {
        "Name": "PLUStatus2B",
        "Type": "BIN",
        "Length": 8,
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 3,
            "Bit": "PLU STATUSB & PLU STATUS 2B"
        },
        "Detail": [
            {
                "2ND PRICE (VER XX.22)": 0,
                "2ND QUANTITY (DP90 ONLY)": 1,
                "PRESET NAME (DP90 ONLY)": 2,
                "BONUS POINT": 3,
                "REFERENCE PLU NUMBER": 4,
                "DISCOUNT DAY OF THE WEEK (VER XX.14)": 5,
                "COUPLED PLU (VER XX.14)": 6,
                "TAX NUMBER": 7
            },
            {
                "2ND QTY SYMBOL TYPE": 0,
                "TRACEABILITY": 1,
                "TRACEABILITY LINK": 2,
                "GROUP CODE": 3,
                "PERCENTAGE TARE": 4,
                "CUSTOMER DISCOUNT": 5,
                "RESTAU DISCOUNT": 6,
                "STAFF DISCOUNT": 7
            },
            {
                "PACKAGING INDICATOR": 0,
                "MULTI BARCODE 1": 1,
                "MULTI BARCODE 2": 2,
                "TOTAL MULTI BARCODE 1": 3,
                "TOTAL MULTI BARCODE 2": 4,
                "STORAGE TEMPERATURE 1st LIMIT": 5,
                "STORAGE TEMPERATURE 2nd LIMIT": 6,
                "PLU SCROLL (U1 only)": 7
            },
            {
                "TEXT # SELECTION": 0,
                "SPECIAL PRICE DISCOUNT": 1,
                "TARE RANGE": 2,
                "MULTI BARCODE1 EXP.": 3,
                "MULTI BARCODE2 EXP.": 4,
                "TTL MULTI BARCODE1 EXP.": 5,
                "TTL MULTI BARCODE2 EXP.": 6
            },
            {
                "LINKED TRAY FILE": 0,
                "EXTEND INGR, SPMG REC# TO 9999": 1,
                "2ND PRINTER (3600 series only)": 2,
                "AI00 SELECTION": 3,
                "GENERIC BARCODE FORMAT": 4,
                "GENERIC BARCODE DATA": 5,
                "AI01 PACKAGING INDICATOR": 6,
                "AI01 SERIAL NUMBER": 7
            },
            {
                "AI02 PACKAGING INDICATOR": 0,
                "AI02 SERIAL NUMBER": 1,
                "TRACE (KOREA ONLY)": 2,
                "EXT TEXT": 3
            },
            {},
            {
                "INDIA BARCODE HEAD (INDIA ONLY)": 0,
                "INDIA EXTEND ITEM CODE (INDIA ONLY)": 1,
                "PRODUCTION DATE": 2,
                "FLEXI NUTRITION #": 3,
                "PRODUCTION TIME": 4
            }
        ]
    },
    {
        "Name": "SecondPrice",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 1,
            "Bit": "2ND PRICE (VER XX.22)"
        },
        "Length": 4
    },
    {
        "Name": "SecondQuantity",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 1,
            "Bit": "2ND QUANTITY (DP90 ONLY)"
        },
        "Length": 2,
        "Disable": 1
    },
    {
        "Name": "CPLUPreset",
        "Type": "ASCII",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 1,
            "Bit": "PRESET NAME (DP90 ONLY)"
        },
        "Length": 33,
        "Disable": 1
    },
    {
        "Name": "BonusPoint",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 1,
            "Bit": "BONUS POINT"
        },
        "Length": 2
    },
    {
        "Name": "RefPLUNo",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 1,
            "Bit": "REFERENCE PLU NUMBER"
        },
        "Length": 4
    },
    {
        "Name": "DiscountDayOfWeek",
        "Type": "BIN",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 1,
            "Bit": "DISCOUNT DAY OF THE WEEK (VER XX.14)"
        },
        "Length": 1
    },
    {
        "Name": "CoupledPLUNo",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 1,
            "Bit": "COUPLED PLU (VER XX.14)"
        },
        "Length": 4
    },
    {
        "Name": "TaxNo",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 1,
            "Bit": "TAX NUMBER"
        },
        "Length": 1
    },
    {
        "Name": "PercentageTare",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 2,
            "Bit": "PERCENTAGE TARE"
        },
        "Length": 2
    },
    {
        "Name": "CustomerDiscount",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 2,
            "Bit": "CUSTOMER DISCOUNT"
        },
        "Length": 4
    },
    {
        "Name": "RestaurantPrice",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 2,
            "Bit": "RESTAU DISCOUNT"
        },
        "Length": 4
    },
    {
        "Name": "StaffDiscount",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 2,
            "Bit": "STAFF DISCOUNT"
        },
        "Length": 4
    },
    {
        "Name": "SecondQuantitySymbolType",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 2,
            "Bit": "2ND QTY SYMBOL TYPE"
        },
        "Length": 1
    },
    {
        "Name": "Traceability",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 2,
            "Bit": "TRACEABILITY"
        },
        "Length": 1
    },
    {
        "Name": "TraceabilityLink",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 2,
            "Bit": "TRACEABILITY LINK"
        },
        "Length": 2
    },
    {
        "Name": "GroupCode",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 2,
            "Bit": "GROUP CODE"
        },
        "Length": 2
    },
    {
        "Name": "StorageTemperature1stLimit",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 3,
            "Bit": "STORAGE TEMPERATURE 1st LIMIT"
        },
        "Length": 2
    },
    {
        "Name": "StorageTemperature2ndLimit",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 3,
            "Bit": "STORAGE TEMPERATURE 2nd LIMIT"
        },
        "Length": 2
    },
    {
        "Name": "PackageIndicator",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 3,
            "Bit": "PACKAGING INDICATOR"
        },
        "Length": 1
    },
    {
        "Name": "MultiBarcode1",
        "Type": "MULTIBARCODE",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 3,
            "Bit": "MULTI BARCODE 1"
        },
        "Length": 51
    },
    {
        "Name": "MultiBarcode1Exp",
        "Type": "MULTIBARCODE",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 4,
            "Bit": "MULTI BARCODE1 EXP."
        },
        "Length": 51
    },
    {
        "Name": "MultiBarcode2",
        "Type": "MULTIBARCODE",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 3,
            "Bit": "MULTI BARCODE 2"
        },
        "Length": 51
    },
    {
        "Name": "MultiBarcode2Exp",
        "Type": "MULTIBARCODE",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 4,
            "Bit": "MULTI BARCODE2 EXP."
        },
        "Length": 51
    },
    {
        "Name": "TotalMultiBarcode1",
        "Type": "MULTIBARCODE",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 3,
            "Bit": "TOTAL MULTI BARCODE 1"
        },
        "Length": 51
    },
    {
        "Name": "TotalMultiBarcode1Exp",
        "Type": "MULTIBARCODE",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 4,
            "Bit": "TTL MULTI BARCODE1 EXP."
        },
        "Length": 51
    },
    {
        "Name": "TotalMultiBarcode2",
        "Type": "MULTIBARCODE",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 3,
            "Bit": "TOTAL MULTI BARCODE 2"
        },
        "Length": 51
    },
    {
        "Name": "TotalMultiBarcode2Exp",
        "Type": "MULTIBARCODE",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 4,
            "Bit": "TTL MULTI BARCODE2 EXP."
        },
        "Length": 51
    },
    {
        "Name": "PLUScroll",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 3,
            "Bit": "PLU SCROLL (U1 only)"
        },
        "Length": 2
    },
    {
        "Name": "LinkedText1No",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 4,
            "Bit": "TEXT # SELECTION"
        },
        "Length": 1
    },
    {
        "Name": "LinkedText2No",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 4,
            "Bit": "TEXT # SELECTION"
        },
        "Length": 1
    },
    {
        "Name": "LinkedText3No",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 4,
            "Bit": "TEXT # SELECTION"
        },
        "Length": 1
    },
    {
        "Name": "LinkedText4No",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 4,
            "Bit": "TEXT # SELECTION"
        },
        "Length": 1
    },
    {
        "Name": "LinkedText5No",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 4,
            "Bit": "TEXT # SELECTION"
        },
        "Length": 1
    },
    {
        "Name": "FirstTare",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 4,
            "Bit": "TARE RANGE"
        },
        "Length": 2
    },
    {
        "Name": "SecondTare",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 4,
            "Bit": "TARE RANGE"
        },
        "Length": 2
    },
    {
        "Name": "LinkedTray1",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 5,
            "Bit": "LINKED TRAY FILE"
        },
        "Length": 1
    },
    {
        "Name": "LinkedTray2",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 5,
            "Bit": "LINKED TRAY FILE"
        },
        "Length": 1
    },
    {
        "Name": "LinkedTray3",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 5,
            "Bit": "LINKED TRAY FILE"
        },
        "Length": 1
    },
    {
        "Name": "ExtendedSpecialMessageNo",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 5,
            "Bit": "EXTEND INGR, SPMG REC# TO 9999"
        },
        "Length": 2
    },
    {
        "Name": "ExtendedIngredientNo",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 5,
            "Bit": "EXTEND INGR, SPMG REC# TO 9999"
        },
        "Length": 2
    },
    {
        "Name": "PLUUccEanPrefix",
        "Type": "BCD",
        "Length": 4,
        "Disable": 1
    },
    {
        "Name": "PLUSerialNo",
        "Type": "BCD",
        "Length": 4,
        "Disable": 1
    },
    {
        "Name": "SecondPrinter",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 5,
            "Bit": "2ND PRINTER (3600 series only)"
        },
        "Length": 1
    },
    {
        "Name": "LabelSizeFor2ndPrinter",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 5,
            "Bit": "2ND PRINTER (3600 series only)"
        },
        "Length": 1
    },
    {
        "Name": "TraceabilityPrint",
        "Type": "BCD",
        "Length": 1,
        "Disable": 1
    },
    {
        "Name": "TraceabilityKorea",
        "Type": "BCD",
        "Length": 1,
        "Disable": 1
    },
    {
        "Name": "Discount",
        "Type": "BYTES",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 2,
            "Bit": "DISCOUNT"
        },
        "Length": 30
    },
    {
        "Name": "Nutrition",
        "Type": "BYTES",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 2,
            "Bit": "NUTRITION"
        },
        "Length": 80
    },
    {
		"Name": "Commodity",
        "Type": "ASCII",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 2,
            "Bit": "COMMODITY"
        },
        "Length": 412
    },
    {
        "Name": "Ingredient",
        "Type": "ASCII",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 2,
            "Bit": "INGREDIENT"
        },
        "Length": 1545
    },
    {
        "Name": "SpecialMessage",
        "Type": "ASCII",
        "Visible": {
            "Name": "PLUStatus2",
            "Byte": 2,
            "Bit": "SPECIAL MESSAGE"
        },
        "Length": 3090
    },
    {
        "Name": "BCC",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "IndiaCode128BarcodeHead",
        "Type": "BYTES",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 8,
            "Bit": "INDIA BARCODE HEAD (INDIA ONLY)"
        },
        "Length": 8
    },
    {
        "Name": "IndiaCode128ExtentItemCode",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 8,
            "Bit": "INDIA EXTEND ITEM CODE (INDIA ONLY)"
        },
        "Length": 4
    },
    {
        "Name": "ProductionDate",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 8,
            "Bit": "PRODUCTION DATE"
        },
        "Length": 4
    },
    {
        "Name": "FlexiNutritionNo",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 8,
            "Bit": "FLEXI NUTRITION #"
        },
        "Length": 4
    },
    {
        "Name": "ProductionTime",
        "Type": "BCD",
        "Visible": {
            "Name": "PLUStatus2B",
            "Byte": 8,
            "Bit": "PRODUCTION TIME"
        },
        "Length": 2
    }
]

# Label Format
prf_struct = [
    {
        "Name": "Code",
        "Key": 1,
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "RecordSize",
        "Type": "HEX",
        "Length": 2,
        "IsSize": 1
    },
    {
        "Name": "Width",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "Height",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "Status",
        "Type": "BIN",
        "Length": 2,
        "Detail": [
            {},
            {"BIT1": 1, "BIT2": 2}
        ]
    },
    {
        "Name": "PLU_NO",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "PRICE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "UNIT_PRICE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "WEIGHT",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "QUANTITY",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "PACKED_DATE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "PACKED_TIME",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "COMMODITY_NAME",
        "Type": "C1",
        "Length": 14
    },
    {
        "Name": "QUANTITY_SYMBOL",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "SELL_BY_DATE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "SELL_BY_TIME",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "BARCODE",
        "Type": "B1",
        "Length": 12
    },
    {
        "Name": "SHOP_NAME",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "DISCOUNT_VALUE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "USED_BY_DATE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "LOGO",
        "Type": "B2",
        "Length": 12
    },
    {
        "Name": "MG_CODE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "DEPARTMENT_CODE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "SHOP_INTERNAL_SCALE_NO",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "INGREDIENTS",
        "Type": "C3",
        "Length": 26
    },
    {
        "Name": "SPECICAL_MESSAGE",
        "Type": "C4",
        "Length": 18
    },
    {
        "Name": "ITEM_PRICE_AFTER_TAX",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "ITEM_TAX_RATE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "TOTAL_PRICE_BEFORE_TAX",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "FRAME_1",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "FRAME_2",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "FRAME_3",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "FRAME_4",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "FRAME_5",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "FRAME_6",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "FRAME_7",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "FRAME_8",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "FRAME_9",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "FRAME_10",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "TARE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "CLERK_CODE_1",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "IMAGE_1",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "IMAGE_2",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "IMAGE_3",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "IMAGE_4",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "IMAGE_5",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "IMAGE_6",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "IMAGE_7",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "IMAGE_8",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "IMAGE_9",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "IMAGE_10",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "RESERVE_1",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "RESERVE_2",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "RESERVE_3",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "RESERVE_4",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "RESERVE_5",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "RESERVE_6",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "TOTAL_PLU_NO",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "TOTAL_PACKED_DATE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "TOTAL_WEIGHT",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "TOTAL_PACKED_QUANTITY",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "TOTAL_QUANTITY_SYMBOL",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "TOTAL_PRICE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "TOTAL_PACKED_TIME",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "ALL_TOTAL",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "TOTAL_BARCODE",
        "Type": "B1",
        "Length": 12
    },
    {
        "Name": "CLERK_CODE_2",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "TOTAL_FRAME_1",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "TOTAL_FRAME_2",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "TOTAL_FRAME_3",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "TOTAL_FRAME_4",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "TOTAL_FRAME_5",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "TOTAL_FRAME_6",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "TOTAL_FRAME_7",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "TOTAL_FRAME_8",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "TOTAL_FRAME_9",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "TOTAL_FRAME_10",
        "Type": "B3",
        "Length": 12
    },
    {
        "Name": "TEXT_1",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_2",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_3",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_4",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_5",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_6",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_7",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_8",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_9",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_10",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_11",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_12",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_13",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_14",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_15",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_16",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_17",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_18",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_19",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TEXT_20",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TOTAL_ADD_ON_TAX_AMT",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "TOTAL_VAT_TAX_AMT",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "PLACE",
        "Type": "C2",
        "Length": 12
    },
    {
        "Name": "TOTAL_IMAGE_1",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "TOTAL_IMAGE_2",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "TOTAL_IMAGE_3",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "TOTAL_IMAGE_4",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "TOTAL_IMAGE_5",
        "Type": "B4",
        "Length": 12
    },
    {
        "Name": "AVERAGE_PRICE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "AVERAGE_WEIGHT",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "BONUS",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "TOTAL_USED_BY_DATE",
        "Type": "N1",
        "Length": 8
    },
    {
        "Name": "SECOND_QUANTITY",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "DATE_CODE",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "CLERK_NAME",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "DEPT_NAME",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "DUPLICATE_TTL_PRICES",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "DUPLICATE_UNIT_PRICES",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "PERCENTAGE_TARE",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
			"Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "SECOND_QTY_SYMBOL",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "BORN",
        "Type": "N1",
        "Visible": {
			"Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "FATTEN",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "SLAUGHTER",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "CUT",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "REFERENCE",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "ORIGIN",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
			"Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "GROUP_CODE",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "TOTAL_BORN",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "TOTAL_FATTEN",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "TOTAL_SLAUGHTER",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "TOTAL_CUT",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "TOTAL_REFERENCE",
		"Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "TOTAL_ORIGIN",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "MULTI_BARCODE_1",
        "Type": "B5",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 12
    },
    {
        "Name": "MULTI_BARCODE_2",
        "Type": "B5",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 12
    },
    {
        "Name": "TTL_MULTI_BARCODE_1",
        "Type": "B5",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 12
    },
    {
        "Name": "TTL_MULTI_BARCODE_2",
        "Type": "B5",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 12
    },
    {
        "Name": "STORAGE_TEMPERATURE",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "SERIAL_NUMBER",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "TOTAL_SERIAL_NUMBER",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "GROSS_WEIGHT",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "LABEL_ITEM_CODE",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "REWRAP",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 8
    },
    {
        "Name": "RESERVED1",
        "Type": "BYTES",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT1"
        },
        "Length": 18
    },
    {
        "Name": "TRACEABILITY_KIND",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT2"
        },
        "Length": 8
    },
    {
        "Name": "TRACEABILITY_CATEGORY",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT2"
        },
        "Length": 8
	},
	{
        "Name": "TRACEABILITY_BREED",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT2"
        },
        "Length": 8
    },
    {
        "Name": "TRACEABILITY_CONTACT",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT2"
        },
        "Length": 8
    },
    {
        "Name": "TRACEABILITY_GTIN",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT2"
        },
        "Length": 8
    },
    {
        "Name": "SUPPLIER_CODE",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT2"
        },
        "Length": 8
    },
    {
        "Name": "SUPPLIER_NAME",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT2"
        },
        "Length": 8
    },
    {
        "Name": "SUPPLIER_ADDRESS_1",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT2"
        },
        "Length": 8
    },
    {
        "Name": "SUPPLIER_ADDRESS_2",
        "Type": "N1",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT2"
        },
        "Length": 8
    },
    {
        "Name": "RESERVED2",
        "Type": "BYTES",
        "Visible": {
            "Name": "Status",
            "Byte": 2,
            "Bit": "BIT2"
        },
        "Length": 192
    }
]

# Text
tex_struct = [
    {
        "Name": "Code",
        "Key": 1,
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "RecordSize",
        "Type": "HEX",
        "Length": 2,
        "IsSize": 1
    },
    {
        "Name": "Label",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "Name",
        "Type": "ASCII",
        "Length": 206
    }
]

# Flexi-barcode
flb_struct = [
    {
        "Name": "Code",
        "Key": 1,
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "RecordSize",
        "Type": "HEX",
        "Length": 2,
        "IsSize": 1
    },
    {
        "Name": "FlagType",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "ItemCodeDigitNum",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "ProgramData1DigitNum",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "ProgramData2DigitNum",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "FlexibarcodeDigitNum",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "CheckDigit",
        "Type": "BIN",
        "Length": 1,
        "Detail": [
            {
                "Mid CD": 0,
                "Last CD": 1,
                "code128": 2,
                "last byte": 5,
                "barcode type": 7
            }
        ]
    },
    {
        "Name": "ProgramData1",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "ProgramData2",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "ProgramData1Shift",
        "Type": "BCD",
        "Length": 1
    },
    {
        "Name": "ProgramData2Shift",
        "Type": "BCD",
        "Length": 1
    }
]

# PLU Transaction Report
ptr_struct = [
    {
        "Name": "T_PLU_TRANS_NO",
        "Type": "BCD",
        "Key": 1,
        "Length": 4
    },
    {
        "Name": "T_PLU_TRANS_SIZE",
        "Type": "HEX",
        "IsSize": 1,
        "Length": 2
    },
    {
        "Name": "T_PLU_TRANS_PLUNO",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "T_PLU_TRANS_UP",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "T_PLU_TRANS_WT",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "T_PLU_TRANS_QTY",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "T_PLU_TRANS_TP",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "T_PLU_TRANS_DATE",
        "Type": "BCD",
        "Length": 3
    },
    {
        "Name": "T_PLU_TRANS_TIME",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "Traceability_Code",
        "Type": "BCD",
        "Length": 5
    },
    {
        "Name": "T_PLU_TRANS_RESERVE",
        "Type": "BYTES",
        "Length": 5
    },
    {
        "Name": "SCALE_NO",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "BEFORE_PRICE",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "AFTER_PRICE",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "ITEM_CODE",
        "Type": "BCD",
        "Length": 7
    },
    {
        "Name": "ITEM_NAME",
        "Type": "ASCII",
        "Length": 50
    }
]

# PLU Total
plt_struct = [
    {
        "Name": "PLUNo",
        "Type": "BCD",
        "Key": 1,
        "Length": 4
    },
    {
        "Name": "PLU_TOTAL_RECORD_SIZE",
        "Type": "HEX",
        "IsSize": 1,
        "Length": 2
    },
    {
        "Name": "EAN_CODE",
        "Type": "BCD",
        "Length": 7
    },
    {
        "Name": "DUMMY",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "MAIN_GROUP_CODE",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "TOTAL_DAILY_TOTAL_ACTUAL_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_DAILY_TOTAL_PLANNED_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_DAILY_TOTAL_PCS",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_DAILY_TOTAL_WEIGHT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_DAILY_TOTAL_PROFIT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_TERM_TOTAL_ACTUAL_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_TERM_TOTAL_PLANNED_PRICE",
		"Type": "HEX",
		"Length": 4
    },
    {
        "Name": "TOTAL_TERM_TOTAL_PCS",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_TERM_TOTAL_WEIGHT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_TERM_TOTAL_PROFIT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_PREPACK_DAILY_TOTAL_ACTUAL_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_PREPACK_DAILY_TOTAL_PLANNED_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_PREPACK_DAILY_TOTAL_PCS",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_PREPACK_DAILY_TOTAL_WEIGHT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_PREPACK_DAILY_TOTAL_PROFIT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_PREPACK_TERM_TOTAL_ACTUAL_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_PREPACK_TERM_TOTAL_PLANNED_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_PREPACK_TERM_TOTAL_PCS",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_PREPACK_TERM_TOTAL_WEIGHT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_PREPACK_TERM_TOTAL_PROFIT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_DISCOUNT_TOTAL_ACTUAL_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_DISCOUNT_TOTAL_PLANNED_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_DISCOUNT_TOTAL_PCS",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_DISCOUNT_TOTAL_WEIGHT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_DISCOUNT_TOTAL_PROFIT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "LAST_ACT_DATE",
        "Type": "BCD",
        "Length": 3
    },
    {
        "Name": "DUMMY2",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "TOTAL_TERM_DISCOUNT_TOTAL_ACTUAL_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_TERM_DISCOUNT_TOTAL_PLANNED_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_TERM_DISCOUNT_TOTAL_PCS",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_TERM_DISCOUNT_TOTAL_WEIGHT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_TERM_DISCOUNT_TOTAL_PROFIT",
        "Type": "HEX",
        "Length": 4
    }
]

# Real Time Buffer
rtb_struct = [
    {
        "Name": "RecordNo",
        "Type": "BCD",
        "Key": 1,
        "Length": 4
    },
    {
        "Name": "RECEIPT_BUFFER_SIZE",
        "Type": "HEX",
        "IsSize": 1,
        "Length": 2
    },
    {
        "Name": "ITEM_STATUS",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PLUNo",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "MGNo",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "QUANTITY",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "WEIGHT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "UNIT_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "UNIT_PRICE_AFTER_DISCOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "UP_DISCOUNT_AMOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "NOMINAL_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "ACTUAL_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PRICE_AFTER_DISCOUNT_AND_TAX",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PRICE_AFTER_SUB_TOTAL_DISC",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PRICE_AFTER_UP_OVERRIDE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_PRICE_DISCOUNT_AMOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "ITEM_PRICE_AFTER_TOTAL_ROUNDING",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TAX_RATE_NUMBER",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "DUMMY1",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "TAX_RATE",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TAX_VALUE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TAX_VALUE_AFTER_SUB_TOTAL_DISC",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "SPECIAL_PRICE_NUMBER",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "DUMMY2",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "SCALE_NUMBER",
        "Type": "HEX",
        "Length": 3
    },
    {
        "Name": "DUMMY3",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "VALUE_OF_POINT_1",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PRICE_OF_POINT_1",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "VALUE_OF_POINT_2",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PRICE_OF_POINT_2",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TARE_VALUE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "STEP_POINT_DISC_STATUS",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "MARKDOWN_STATUS",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "JIN_RECBUF_WEIGHT_FOR_TW",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "JIN_RECBUF_STATUS_FOR_TW",
        "Type": "BCD",
        "Length": 2
    },
    {
        "Name": "PUBLICITY_FREE_WEIGHT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PUBLICITY_BONUS_POINT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PUBLICITY_FREE_QUANTITY",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TRACEABILITY_BORN_COUNTRY",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TRACEABILITY_FATTEN_COUNTRY",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TRACEABILITY_SLAUGHTER_HOUSE",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TRACEABILITY_SLAUGHTER_COUNTRY",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TRACEABILITY_CUTTING_HALL",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TRACEABILITY_CUTTING_COUNTRY",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TRACEABILITY_REFERENCE_DATE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TRACEABILITY_ORIGIN_COUNTRY",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TRACEABILITY_REFERENCE_CODE",
        "Type": "BYTES",
        "Length": 20
    },
    {
        "Name": "TRACEABILITY_REFERENCE_TYPE",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "TRACEABILITY_REFERENCE_SET",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "BEFORE_PRICE_KOREA",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "ITEM_CODE_KOREA",
        "Type": "HEX",
        "Length": 7
    },
    {
        "Name": "IP_ADDRESS_KOREA",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "ITEM_NAME_KOREA",
        "Type": "BYTES",
        "Length": 50
    },
    {
        "Name": "PAYMENT_TTL_NUM",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "DUMMY4",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "PAYMENT_NUM_1",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QTY_1",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_1",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_1",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE1",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUM_2",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QTY_2",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_2",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_2",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE2",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUM_3",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QTY_3",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_3",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_3",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE3",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TRACEABILITY_GTIN",
        "Type": "BYTES",
        "Length": 14
    },
    {
        "Name": "TRACEABILITY_KIND",
        "Type": "BYTES",
        "Length": 2
    },
    {
        "Name": "TRACEABILITY_CATEGORY",
        "Type": "BYTES",
        "Length": 2
    },
    {
        "Name": "TRACEABILITY_BREED",
        "Type": "BYTES",
        "Length": 2
    },
    {
        "Name": "TRACEABILITY_LOT_NUM",
        "Type": "BYTES",
        "Length": 30
    },
    {
        "Name": "TRACEABILITY_CONTACT_REF",
        "Type": "BYTES",
        "Length": 10
    },
    {
        "Name": "TRACEABILITY_EAT_DATE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TRACEABILITY_WEIGHT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TRACEABILITY_ID",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PRICE_BEFORE_DISCOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "ITEM_CODE",
        "Type": "BCD",
        "Length": 7
    },
    {
        "Name": "IP_ADDRESS_TAIL",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "ITEM_NAME",
        "Type": "BYTES",
        "Length": 50
    },
    {
        "Name": "PLU_SELL_BY_DATE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PLU_EAN",
        "Type": "BCD",
        "Length": 7
    },
    {
        "Name": "SCALE_PORT_NO",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "CLERK_CODE",
        "Type": "HEX",
        "Length": 4
    }
]

# Real Time Total Buffer
rtt_struct = [
    {
        "Name": "ReceiptNo",
        "Type": "BCD",
        "Key": 1,
        "Length": 4
    },
    {
        "Name": "TOTAL_RECEIPT_RECORD_SIZE",
        "Type": "HEX",
        "IsSize": 1,
        "Length": 2
    },
    {
        "Name": "TOTAL_NOMINAL_TRANSACTION",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "RECEIPT_BUFFER_STATUS_1",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "TOTAL_RECEIPT_NUMBER",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_ACTUAL_TRANSACTION",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "TOTAL_REFUND_TRANSACTION",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "NEW_PLU_TRANSACTION",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "TOTAL_CLERK_NAME",
        "Type": "BYTES",
        "Length": 17
    },
    {
        "Name": "ADDSUBTRACT_STATUS",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "DUMMY1",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "TOTAL_WEIGHT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_QUANTITY",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "SUBTOTAL_GROSS_AMOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_NOMINAL_PRICE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "SUBTOTAL_NET_AMOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TEMP_SUBTOTAL_NET_AMOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_PRICE_WITH_TAX",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TEMP_TOTAL_PRICE_WITH_TAX",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMOUNT_OF_ADDON_TAX",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMOUNT_OF_VAT_TAX",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TEMP_TOTAL_AMOUNT_OF_ADDON_TAX",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TEMP_TOTAL_AMOUNT_OF_VAT_TAX",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "SUBTOTAL_DISCOUNT_AMOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "SUBTOTAL_DISCOUNT_PERCENTAGE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "SUBTOTAL_ITEM_DISC_AMOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "SUBTOTAL_ITEM_DISC_REMAINER",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMOUNT_OF_REBATE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_CASH_RECEIVED",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_No_OF_CASH_PAYMENT",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_VALUE_OF_CHEQUES",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_No_OF_CHEQUES",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_VALUE_OF_VOUCHER",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_No_OF_VOUCHER",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "FLOAT_CUSTOMER_NUMBER",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "FLOAT_CUSTOMER_TABLE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_VAULE_OF_CREDIT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_No_OF_CREDIT",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_REAL_TIME_DATE",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "TOTAL_REAL_TIME_TIME",
        "Type": "BCD",
        "Length": 4
    },
    {
        "Name": "TOTAL_REAL_TIME_CLERK",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_REAL_TIME_RCT_No",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_REAL_TIME_SCALE_No",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_TENDER_AMOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_CHANGE_AMOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_DISC_AMOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_NET_AMOUNT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_NO_OF_CUSTOMER",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_BARCODE",
        "Type": "HEX",
        "Length": 8
    },
    {
        "Name": "TOTAL_EFT_CHANGE",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_EFT_CHANGE_NO",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_BONUS_POINT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMT_WITH_GST",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMT_WO_GST",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_ROUNDING_AMT",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_PAYMENT_NUMBER",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "DUMMY2",
        "Type": "HEX",
        "Length": 1
    },
    {
        "Name": "PAYMENT_NUMBER_1",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QUANTITY_1",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_LOCAL_1",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_1",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE1",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUMBER_2",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QUANTITY_2",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_LOCAL_2",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_2",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE2",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUMBER_3",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QUANTITY_3",
		"Type": "HEX",
		"Length": 4
	},
	{
        "Name": "PAYMENT_AMOUNT_LOCAL_3",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_3",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE3",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUMBER_4",
        "Type": "HEX",
        "Length": 2
    },
	{
		"Name": "PAYMENT_QUANTITY_4",
		"Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_LOCAL_4",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_4",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE4",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUMBER_5",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QUANTITY_5",
        "Type": "HEX",
        "Length": 4
    },
    {
		"Name": "PAYMENT_AMOUNT_LOCAL_5",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "PAYMENT_AMOUNT_EURO_5",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "RESERVE5",
		"Type": "HEX",
		"Length": 2
	},
	{
		"Name": "PAYMENT_NUMBER_6",
		"Type": "HEX",
		"Length": 2
	},
	{
		"Name": "PAYMENT_QUANTITY_6",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "PAYMENT_AMOUNT_LOCAL_6",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "PAYMENT_AMOUNT_EURO_6",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "RESERVE6",
		"Type": "HEX",
		"Length": 2
	},
	{
		"Name": "PAYMENT_NUMBER_7",
		"Type": "HEX",
		"Length": 2
	},
	{
		"Name": "PAYMENT_QUANTITY_7",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "PAYMENT_AMOUNT_LOCAL_7",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "PAYMENT_AMOUNT_EURO_7",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "RESERVE7",
		"Type": "HEX",
		"Length": 2
	},
	{
		"Name": "PAYMENT_NUMBER_8",
		"Type": "HEX",
		"Length": 2
	},
	{
		"Name": "PAYMENT_QUANTITY_8",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "PAYMENT_AMOUNT_LOCAL_8",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "PAYMENT_AMOUNT_EURO_8",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "RESERVE8",
		"Type": "HEX",
		"Length": 2
	},
	{
		"Name": "PAYMENT_NUMBER_9",
		"Type": "HEX",
		"Length": 2
	},
	{
		"Name": "PAYMENT_QUANTITY_9",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "PAYMENT_AMOUNT_LOCAL_9",
		"Type": "HEX",
		"Length": 4
	},
	{
		"Name": "PAYMENT_AMOUNT_EURO_9",
		"Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE9",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUMBER_10",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QUANTITY_10",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_LOCAL_10",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_10",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE10",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUMBER_11",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QUANTITY_11",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_LOCAL_11",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_11",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE11",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUMBER_12",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QUANTITY_12",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_LOCAL_12",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_12",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE12",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUMBER_13",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QUANTITY_13",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_LOCAL_13",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_13",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE13",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUMBER_14",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QUANTITY_14",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_LOCAL_14",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_14",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE14",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUMBER_15",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QUANTITY_15",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_LOCAL_15",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_15",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE15",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_NUMBER_16",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "PAYMENT_QUANTITY_16",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_LOCAL_16",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "PAYMENT_AMOUNT_EURO_16",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "RESERVE16",
        "Type": "HEX",
        "Length": 2
    },
    {
        "Name": "TOTAL_RECEIPT_TAX_AMT1",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_RECEIPT_TAX_AMT2",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_RECEIPT_TAX_AMT3",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_RECEIPT_TAX_AMT4",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_RECEIPT_TAX_AMT5",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_RECEIPT_TAX_AMT6",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_RECEIPT_TAX_AMT7",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_RECEIPT_TAX_AMT8",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_RECEIPT_TAX_AMT9",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_RECEIPT_TAX_AMT10",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMT_EXCLUDE_TAX1",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMT_EXCLUDE_TAX2",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMT_EXCLUDE_TAX3",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMT_EXCLUDE_TAX4",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMT_EXCLUDE_TAX5",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMT_EXCLUDE_TAX6",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMT_EXCLUDE_TAX7",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMT_EXCLUDE_TAX8",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMT_EXCLUDE_TAX9",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "TOTAL_AMT_EXCLUDE_TAX10",
        "Type": "HEX",
        "Length": 4
    },
    {
        "Name": "CREDIT_RECORD_No",
        "Type": "HEX",
        "Length": 4
    }
]

multiBarcodeTypeMapper = {
    "EAN128A": 0,
    "EAN128B": 1,
    "EAN128C": 2,
    "CODE128": 2,
    "QR": 3
}

barcodeTypeMapper = {
    "EAN128A": 1,
    "EAN128B": 1,
    "EAN128C": 1,
    "CODE128": 3,
    "QR": 5
}

eanMapper = {
    "FF CCCCC 0 XXXX CD": 3,
    "FF CCCCCC XXXX CD": 4,
    "FF CCCCC XXXXX CD": 5,
    "F CCCCCC XXXXX CD": 6,
    "F CCCCC XXXXXX CD": 7,
    "FF CCCCCCCCCC CD": 8,
    "FF CCCC XXXXXX CD": 9,
    "FF CCCCC CD": 10,
    "F CC XXXX CD": 11,
    "FF CCC XXXXXXX CD": 17,
    "FF CC XXXXXXXX CD": 18,
    "CCC WWWW PPPPP CD": 19,
    "CCCCCCC XXXXXX": 20,
    "FF CCCCC PCD XXXX CD": 21,
    "FF RRRRR XXXXX CD": 22,
    "F CCCCC XXXXXX CD": 23,
    "FFF CCCC PPPPP CD": 24,
    "FF CCCCC WWWWW CD": 25,
    "F CCCCC WWWWW 0 CD": 26,
    "FF CCCCCC WWWW CD": 27,
    "CCCCCCC XXXXXX": 28,
    "FF CCC XXXXXXX CD": 29,
    "F CCCCCCC WWWW CD": 30,
    "FF CC NNN PPPPP CD": 31,
    "FF C NNNN PPPPP CD": 32
}

itfMapper = {
    "FF CCCCC XXXX WWWW CD": 1,
    "F CCCCCC XXXX WWWW CD": 2,
    "FF CCCCC XXXXX WWWWW CD": 5,
    "F CCCCCC XXXXX WWWWW CD": 6,
    "0F CCCCC XXXXXX WWWWWW CD": 7,
    "FF CCCCC CD": 10,
    "F CC XXXX WWWW CD": 11,
    "NON   BARCODE": 12,
    "FX CCCCC XXXX WWWW CD": 13,
    "0FX CCCCCC XXXX WWWW CD": 14,
    "0F CCCCC XXXXX WWWWW CD": 16,
    "FF CCC XXXXXXX WWWWWWW CD": 17,
    "0CCC WWWW PPPPP CD": 19,
    "CCCCCCC XXXXXXX": 20,
    "FF CCCCC XXXX WWWW CD": 21,
    "FF RRRRR XXXXX WWWWW CD": 22,
    "F CCCCC XXXXXX WWWWW CD": 23,
    "FFF CCCC PPPPP WWWWW CD": 24,
    "FF CCCCC WWWWW PPPPP CD": 25,
    "F CCCCC WWWWW PPPPPP CD": 26,
    "FF CCCCCC WWWWW XXXX CD": 27,
    "CCCCCCC XXXXXXX WWWWWW": 28,
    "FF CCC XXXXXXX WWWWW CD": 29,
    "F CCCCCCC WWWW PPPPP CD": 30,
    "FF CC NNN PPPPP WWWWW CD": 31,
    "FF C NNNN PPPPP WWWWW CD": 32
}

fontMapper = {
    "S1": 0,
    "S2": 1,
    "S3": 2,
    "S4": 3,
    "S5": 4,
    "M1": 5,
    "M2": 6,
    "M3": 7,
    "M4": 8,
    "M5": 9,
    "X1": 80,
    "X2": 81,
    "X3": 82,
    "X4": 83,
    "X5": 84,
    "B1": 10,
    "B2": 11,
    "B3": 26,
    "B4": 27,
    "B5": 28,
    "B6": 29,
    "J1": 16,
    "J2": 17,
    "J3": 18,
    "J4": 19,
    "G1": 22,
    "G2": 23,
    "G3": 20,
    "G4": 21,
    "G5": 24,
    "G6": 25,
    "T1": 30,
    "T2": 31,
    "T3": 32,
    "TX": 96,
    "K1": 33,
    "K2": 34,
    "K3": 35,
    "K4": 36,
    "K5": 37,
    "K6": 38
}

printFormatIndexListStringList = {
    "PLU NO": 1,
    "PRICE (-TAX)": 2,
    "UNIT PRICE": 3,
    "WEIGHT": 4,
    "QUANTITY": 5,
    "PACKED DATE": 6,
    "PACKED TIME": 7,
    "COMMODITY": 8,
    "QUANTITY UNIT": 9,
    "SELL DATE": 10,
    "SELL TIME": 11,
    "BARCODE": 12,
    "SHOP NAME": 13,
    "DISCOUNT VALUE": 14,
    "USED DATE": 15,
    "LOGO": 16,
    "MAIN GROUP CODE": 17,
    "DEPARTMENT CODE": 18,
    "SCALE NUMBER": 19,
    "INGREDIENT": 20,
    "SPECIAL MESSAGE": 21,
    "TAX RATE": 23,
    "PRICE (+ TAX)": 24,
    "FRAME 1": 25,
    "FRAME 2": 26,
    "TARE": 35,
    "CLERK": 36,
    "IMAGE 1": 37,
    "IMAGE 2": 38,
    "IMAGE 3": 39,
    "IMAGE 4": 40,
    "IMAGE 5": 41,
    "IMAGE 6": 42,
    "IMAGE 7": 43,
    "IMAGE 8": 44,
    "IMAGE 9": 45,
    "IMAGE 10": 46,
    "TEXT 1": 73,
    "TEXT 2": 74,
    "TEXT 3": 75,
    "TEXT 4": 76,
    "TEXT 5": 77,
    "TEXT 6": 78,
    "TEXT 7": 79,
    "TEXT 8": 80,
    "TEXT 9": 81,
    "TEXT 10": 82,
    "TEXT 11": 83,
    "TEXT 12": 84,
    "TEXT 13": 85,
    "TEXT 14": 86,
    "TEXT 15": 87,
    "TEXT 16": 88,
    "TEXT 17": 89,
    "TEXT 18": 90,
    "TEXT 19": 91,
    "TEXT 20": 92,
    "PLACE": 95,
    "AVERAGE PRICE": 101,
    "AVERAGE WEIGHT": 102,
    "BORN COUNTRY": 113,
    "FATTEN COUNTRY": 114,
    "SLAUGTHER HOUSE": 115,
    "CUTTING HALL": 116,
    "REFER NO": 117,
    "ORIGIN": 118,
    "MULTI BARCODE 1": 126,
    "MULTI BARCODE 2": 127,
    "TEMPERATURE": 130,
    "SERIAL NO": 131,
    "GROSS WEIGHT": 133,
    "REWRAP": 135,
    "KIND": 137,
    "CATEGORY": 138,
    "BREED": 139,
    "CONTACT": 140,
    "GTIN": 141,
    "SUPPLIER CODE": 142,
    "SUPPLIER NAME": 143,
    "SUPPLIER ADDRESS 1": 144,
    "SUPPLIER ADDRESS 2": 145,
}

printFormatIndexList = {
    1: "PLU NO",
    2: "PRICE (-TAX)",
    3: "UNIT PRICE",
    4: "WEIGHT",
    5: "QUANTITY",
    6: "PACKED DATE",
    7: "PACKED TIME",
    8: "COMMODITY",
    9: "QUANTITY UNIT",
    10: "SELL DATE",
    11: "SELL TIME",
    12: "BARCODE",
    13: "SHOP NAME",
    14: "DISCOUNT VALUE",
    15: "USED DATE",
    16: "LOGO",
    17: "MAIN GROUP CODE",
    18: "DEPARTMENT CODE",
    19: "SCALE NUMBER",
    20: "INGREDIENT",
    21: "SPECIAL MESSAGE",
    23: "TAX RATE",
    24: "PRICE (+ TAX)",
    25: "FRAME 1",
    26: "FRAME 2",
    35: "TARE",
    36: "CLERK",
    37: "IMAGE 1",
    38: "IMAGE 2",
    39: "IMAGE 3",
    40: "IMAGE 4",
    41: "IMAGE 5",
    42: "IMAGE 6",
    43: "IMAGE 7",
    44: "IMAGE 8",
    45: "IMAGE 9",
    46: "IMAGE 10",
    # 59 : "PRICE BEFORE DISCOUNT",
    # 60 : "UNIT PRICE BEFORE DISCOUNT",
    73: "TEXT 1",
    74: "TEXT 2",
    75: "TEXT 3",
    76: "TEXT 4",
    77: "TEXT 5",
    78: "TEXT 6",
    79: "TEXT 7",
    80: "TEXT 8",
    81: "TEXT 9",
    82: "TEXT 10",
    83: "TEXT 11",
    84: "TEXT 12",
    85: "TEXT 13",
    86: "TEXT 14",
    87: "TEXT 15",
    88: "TEXT 16",
    89: "TEXT 17",
    90: "TEXT 18",
    91: "TEXT 19",
    92: "TEXT 20",
    95: "PLACE",
    # 64 : "EURO UNIT PRICE",
    # 65 : "EURO TOTAL PRICE",
    101: "AVERAGE PRICE",
    102: "AVERAGE WEIGHT",
    113: "BORN COUNTRY",
    114: "FATTEN COUNTRY",
    115: "SLAUGTHER HOUSE",
    116: "CUTTING HALL",
    117: "REFER NO",
    118: "ORIGIN",
    126: "MULTI BARCODE 1",
    127: "MULTI BARCODE 2",
    130: "TEMPERATURE",
    131: "SERIAL NO",
    133: "GROSS WEIGHT",
    135: "REWRAP",
    137: "KIND",
    138: "CATEGORY",
    139: "BREED",
    140: "CONTACT",
    141: "GTIN",
    142: "SUPPLIER CODE",
    143: "SUPPLIER NAME",
    144: "SUPPLIER ADDRESS 1",
    145: "SUPPLIER ADDRESS 2",
    # 85 : "TOTAL TITLE",
    # 86 : "EXCLUDED TAX AMOUNT",
    # 87 : "INCLUDED TAX AMOUNT",
    # 88 : "ADVERTISEMENT",
    # 89 : "DISCOUNT PRICE TAG",
    # 90 : "DISCOUNT PRICE IMAGE 1",
    # 91 : "DISCOUNT PRICE IMAGE 2",
    # 93 : "TRACEABILITY TEXT",
    # 94 : "PRODUCTION DATE",
    # 95 : "PRODUCTION TIME",
    # 901 : "Serving size",
    # 902 : "Serving container",
    # 903 : "Selection of 100g / 100ml",
    # 904 : "Unit weight portion",
    # 905 : "Number of portions",
    # 906 : "Energy (kCal)",
    # 907 : "Energy (kJ)",
    # 908 : "Energy %",
    # 909 : "Total fat",
    # 910 : "Total fat %",
    # 911 : "Saturate fat",
    # 912 : "Saturate fat %",
    # 913 : "Carbohydrate",
    # 914 : "Carbohydrate %",
    # 915 : "Sugars",
    # 916 : "Sugars %",
    # 917 : "Protein",
    # 918 : "Protein %",
    # 919 : "Salt",
    # 920 : "Salt %",
    # 921 : "Vitamin A",
    # 922 : "Vitamin A %",
    # 923 : "Vitamin D",
    # 924 : "Vitamin D %",
    # 925 : "Vitamin E",
    # 926 : "Vitamin E %",
    # 927 : "Vitamin K",
    # 928 : "Vitamin K %",
    # 929 : "Vitamin C",
    # 930 : "Vitamin C %",
    # 931 : "Thiamine",
    # 932 : "Thiamine %",
    # 933 : "Riboflavin",
    # 934 : "Riboflavin %",
    # 935 : "Niacin",
    # 936 : "Niacin %",
    # 937 : "Vitamin B6",
    # 938 : "Vitamin B6 %",
    # 939 : "Folic acid",
    # 940 : "Folic acid %",
    # 941 : "Vitamin B12",
    # 942 : "Vitamin B12 %",
    # 943 : "Biotin",
    # 944 : "Biotin %",
    # 945 : "Pantothenic acid",
    # 946 : "Pantothenic acid %",
    # 947 : "Potassium",
    # 948 : "Potassium %",
    # 949 : "Chloride",
    # 950 : "Chloride %",
    # 951 : "Calcium",
    # 952 : "Calcium %",
    # 953 : "Phosphorus",
    # 954 : "Phosphorus %",
    # 955 : "Magnesium",
    # 956 : "Magnesium %",
    # 957 : "Iron",
    # 958 : "Iron %",
    # 959 : "Zinc",
    # 960 : "Zinc %",
    # 961 : "Copper",
    # 962 : "Copper %",
    # 963 : "Manganese",
    # 964 : "Manganese %",
    # 965 : "Fluoride",
    # 966 : "Fluoride %",
    # 967 : "Selenium",
    # 968 : "Selenium %",
    # 969 : "Chromium",
    # 970 : "Chromium %",
    # 971 : "Molybdenum",
    # 972 : "Molybdenum %",
    # 973 : "Lodine",
    # 974 : "Lodine %"
}
