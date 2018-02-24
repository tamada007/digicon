##### encoding:utf-8

db_name = "sm120.sqlite"

report_list = {
    "Scale Data":
        {
            "Tables": "Scd",
            "SQL": "SELECT IP_address,PLU_number,PLU_remain FROM Scd",
            "Fields": ["substr($(1),0,3).substr($(1),3,3).substr($(1),6,3).substr($(1),9,3)", "$(2)", "$(3)"]
        },
    "PLU Total":
        {
            "Tables": "Plu,Plt",
            "SQL": "SELECT plt.*,plu.CommodityName1 FROM plt LEFT JOIN plu ON plt.pluno=plu.pluno"
        },
    "PLU Transaction":
        {
            "Tables": "Ptr",
            "SQL": "SELECT * FROM ptr"
        },
    "Real Time Total Buffer":
        {
            "Tables": "Rtt",
            "SQL": "SELECT * FROM rtt"
        },
    "Real Time Buffer":
        {
            "Tables": "Rtb,Plu",
            "SQL": "SELECT rtb.*,plu.CommodityName1 FROM rtb LEFT JOIN plu on plu.pluno=rtb.pluno"
        },

}

# Spec
spe_struct = {
    "Code": {
        "ColumnIndex": 1,
        "Key": 1,
        "Type": "SMInt"
    },
    "Flag_for_delete": {
        "ColumnIndex": 2,
        "Type": "SMText"
    },
    "Value": {
        "ColumnIndex": 3,
        "Type": "SMText"
    }
}

# Password
pas_struct = {
    "Code": {
        "ColumnIndex": 1,
        "Key": 1,
        "Type": "SMInt"
    },
    "Flag_for_delete": {
        "ColumnIndex": 2,
        "Type": "SMText"
    },
    "XModePwd": {
        "ColumnIndex": 3,
        "Type": "SMInt"
    },
    "SModePwd": {
        "ColumnIndex": 4,
        "Type": "SMInt"
    },
    "ZModePwd": {
        "ColumnIndex": 5,
        "Type": "SMInt"
    },
    "PModePwd": {
        "ColumnIndex": 6,
        "Type": "SMInt"
    },
    "UModePwd": {
        "ColumnIndex": 7,
        "Type": "SMInt"
    },
    "RModePwd": {
        "ColumnIndex": 8,
        "Type": "SMInt"
    },

}

# Scale Data
scd_struct = {
    "Scale_serial_No": {
        "ColumnIndex": 1,
        "Key": 1,
        "Type": "SMInt"
    },
    "Flag_for_delete": {
        "ColumnIndex": 2,
        "Type": "SMText"
    },
    "Boot_version": {
        "ColumnIndex": 3,
        "Type": "SMText"
    },
    "Main_version": {
        "ColumnIndex": 4,
        "Type": "SMText"
    },
    "Const_version": {
        "ColumnIndex": 5,
        "Type": "SMText"
    },
    "Font_version": {
        "ColumnIndex": 6,
        "Type": "SMText"
    },
    "Bmap_version": {
        "ColumnIndex": 7,
        "Type": "SMText"
    },
    "Machine_code": {
        "ColumnIndex": 8,
        "Type": "SMInt"
    },
    "Ethernet_hardware_address": {
        "ColumnIndex": 9,
        "Type": "SMText"
    },
    "IP_address": {
        "ColumnIndex": 10,
        "Type": "SMText"
    },
    "Scale_RAM_size": {
        "ColumnIndex": 11,
        "Type": "SMInt"
    },
    "PLU_number": {
        "ColumnIndex": 12,
        "Type": "SMInt"
    },
    "PLU_remain": {
        "ColumnIndex": 13,
        "Type": "SMInt"
    },
    "PLU_unit_price_after_discount": {
        "ColumnIndex": 14,
        "Type": "SMInt"
    },
    "Scale_RES_Type": {
        "ColumnIndex": 15,
        "Type": "SMInt"
    },
    "Product_No_Thermal_head": {
        "ColumnIndex": 16,
        "Type": "SMText"
    },
    "Revision_No_Thermal_head": {
        "ColumnIndex": 17,
        "Type": "SMText"
    },
    "Lot_No_Thermal_head": {
        "ColumnIndex": 18,
        "Type": "SMText"
    },
    "Serial_No_Thermal_head": {
        "ColumnIndex": 19,
        "Type": "SMText"
    },
    "Head_average_resistance_Thermal_head": {
        "ColumnIndex": 20,
        "Type": "SMText"
    },
    "Thermal_head_usage_Distance": {
        "ColumnIndex": 21,
        "Type": "SMInt"
    },
    "Thermal_head_usage_Cut_count": {
        "ColumnIndex": 22,
        "Type": "SMInt"
    },
    "Main_board_print_Distance": {
        "ColumnIndex": 23,
        "Type": "SMInt"
    },
    "Main_board_print_Cut_count": {
        "ColumnIndex": 24,
        "Type": "SMInt"
    },
    "Scale_type": {
        "ColumnIndex": 25,
        "Type": "SMInt"
    },
    "Minimum_Display": {
        "ColumnIndex": 26,
        "Type": "SMInt"
    },
    "Selection_of_Resolution": {
        "ColumnIndex": 27,
        "Type": "SMInt"
    },
    "Weight_Single_Interval_or_Multi_Interval": {
        "ColumnIndex": 28,
        "Type": "SMInt"
    },
    "Decimal_Point_Position_for_Weight": {
        "ColumnIndex": 29,
        "Type": "SMInt"
    },
    "AD_module_type": {
        "ColumnIndex": 30,
        "Type": "SMInt"
    },
    "COUNTRY_SET": {
        "ColumnIndex": 31,
        "Type": "SMInt"
    },
    "COUNTRY_CODE": {
        "ColumnIndex": 32,
        "Type": "SMInt"
    }
}

# Place
pla_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "LineNo":
        {
            "ColumnIndex": 2,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "DeleteFlag":
        {
            "ColumnIndex": 3,
            "Type": "SMText",
            "MaxLength": 1
        },
    "PlaceFlag":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "PlaceName":
        {
            "ColumnIndex": 5,
            "Type": "SMText",
            "MaxLength": 100
        }

}

# Date Time
dat_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMText",
            "MaxLength": 1
        },
    "Year":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "Month":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "Day":
        {
            "ColumnIndex": 5,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "Hour":
        {
            "ColumnIndex": 6,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "Minute":
        {
            "ColumnIndex": 7,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "FlagOfChangeValue":
        {
            "ColumnIndex": 8,
            "Type": "SMText",
            "MaxLength": 1
        },
    "ChangeValue":
        {
            "ColumnIndex": 9,
            "Type": "SMInt",
            "MaxLength": 8
        }

}

# Main Group
##################################################
mgp_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMText",
            "MaxLength": 1
        },
    "LinkedDeptCode":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TaxRateNo":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "MGName":
        {
            "ColumnIndex": 5,
            "Type": "SMText",
            "MaxLength": 16
        }
}

mgp_file = 'mgp'
##################################################

# Plu
##################################################
plu_struct = {
    "PLUNo":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMText",
            "MaxLength": 1
        },
    "WeightingFlag":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "PackedDateSourceFlag":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "SellByDateFlag":
        {
            "ColumnIndex": 5,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "UsedByDateFlag":
        {
            "ColumnIndex": 6,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "PackedDateFlag":
        {
            "ColumnIndex": 7,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "SellByTimeFlag":
        {
            "ColumnIndex": 8,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "PackedTimeFlag":
        {
            "ColumnIndex": 9,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "RTCPackedTimeFlag":
        {
            "ColumnIndex": 10,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "RTCSellByTimeFlag":
        {
            "ColumnIndex": 11,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "PriceBasedPerUnitFlag":
        {
            "ColumnIndex": 12,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "NegativePLUFlag":
        {
            "ColumnIndex": 13,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "NutritionPrintFlag":
        {
            "ColumnIndex": 14,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "UnitPriceOverrideFlag":
        {
            "ColumnIndex": 15,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "PLUPriceChangeFlag":
        {
            "ColumnIndex": 16,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "TraceabilityFlag":
        {
            "ColumnIndex": 17,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "PrintGrossWTTareFlag":
        {
            "ColumnIndex": 18,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "UnitPrice":
        {
            "ColumnIndex": 19,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "LabelFormat1":
        {
            "ColumnIndex": 20,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "LabelFormat2":
        {
            "ColumnIndex": 21,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "BarcodeFormat":
        {
            "ColumnIndex": 22,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "BarcodeFlagOfEanData":
        {
            "ColumnIndex": 23,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "ItemCode":
        {
            "ColumnIndex": 24,
            "Type": "SMText",
            "MaxLength": 10
        },
    "ExtendItemCode":
        {
            "ColumnIndex": 25,
            "Type": "SMInt",
            "MaxLength": 0
        },
    "BarcodeTypeOfEanData":
        {
            "ColumnIndex": 26,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "RightSideDataOfEanData":
        {
            "ColumnIndex": 27,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "MGNo":
        {
            "ColumnIndex": 28,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "Cost":
        {
            "ColumnIndex": 29,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "SellByDate":
        {
            "ColumnIndex": 30,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "SellByTime":
        {
            "ColumnIndex": 31,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "UsedByDate":
        {
            "ColumnIndex": 32,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "PackedDate":
        {
            "ColumnIndex": 33,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "PackedTime":
        {
            "ColumnIndex": 34,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "ProductionDate":
        {
            "ColumnIndex": 35,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "PLUTare":
        {
            "ColumnIndex": 36,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "Quantity":
        {
            "ColumnIndex": 37,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "QuantitySymbol":
        {
            "ColumnIndex": 38,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "TaxNo":
        {
            "ColumnIndex": 39,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "PTare":
        {
            "ColumnIndex": 40,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "ImageNo1":
        {
            "ColumnIndex": 41,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "ImageNo2":
        {
            "ColumnIndex": 42,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "ImageNo3":
        {
            "ColumnIndex": 43,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "ImageNo4":
        {
            "ColumnIndex": 44,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "ImageNo5":
        {
            "ColumnIndex": 45,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "ImageNo6":
        {
            "ColumnIndex": 46,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "ImageNo7":
        {
            "ColumnIndex": 47,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "ImageNo8":
        {
            "ColumnIndex": 48,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "ImageNo9":
        {
            "ColumnIndex": 49,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "ImageNo10":
        {
            "ColumnIndex": 50,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "SpecialMessageNo":
        {
            "ColumnIndex": 51,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "IngredientNo":
        {
            "ColumnIndex": 52,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "PlaceNo":
        {
            "ColumnIndex": 53,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "SecondPrice":
        {
            "ColumnIndex": 54,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "CoupledPLUNo":
        {
            "ColumnIndex": 55,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "CustomerDiscount":
        {
            "ColumnIndex": 56,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TraceabilityNo":
        {
            "ColumnIndex": 57,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "LinkedStorageTemperatureNo":
        {
            "ColumnIndex": 58,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo1":
        {
            "ColumnIndex": 59,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo2":
        {
            "ColumnIndex": 60,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo3":
        {
            "ColumnIndex": 61,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo4":
        {
            "ColumnIndex": 62,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo5":
        {
            "ColumnIndex": 63,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo6":
        {
            "ColumnIndex": 64,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo7":
        {
            "ColumnIndex": 65,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo8":
        {
            "ColumnIndex": 66,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo9":
        {
            "ColumnIndex": 67,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo10":
        {
            "ColumnIndex": 68,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo11":
        {
            "ColumnIndex": 69,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo12":
        {
            "ColumnIndex": 70,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo13":
        {
            "ColumnIndex": 71,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo14":
        {
            "ColumnIndex": 72,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo15":
        {
            "ColumnIndex": 73,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TextNo16":
        {
            "ColumnIndex": 74,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "StepDiscountStartDate":
        {
            "ColumnIndex": 75,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "StepDiscountStartTime":
        {
            "ColumnIndex": 76,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "StepDiscountEndDate":
        {
            "ColumnIndex": 77,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "StepDiscountEndTime":
        {
            "ColumnIndex": 78,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "StepDiscountPoint1":
        {
            "ColumnIndex": 79,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "StepDiscountValue1":
        {
            "ColumnIndex": 80,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "StepDiscountPoint2":
        {
            "ColumnIndex": 81,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "StepDiscountValue2":
        {
            "ColumnIndex": 82,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "StepDiscountType":
        {
            "ColumnIndex": 83,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "TypeOfMarkdown":
        {
            "ColumnIndex": 84,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagForSunday":
        {
            "ColumnIndex": 85,
            "Type": "SMText",
            "MaxLength": 1
        },
    "FlagForMonday":
        {
            "ColumnIndex": 86,
            "Type": "SMText",
            "MaxLength": 1
        },
    "FlagForTuesday":
        {
            "ColumnIndex": 87,
            "Type": "SMText",
            "MaxLength": 1
        },
    "FlagForWednesday":
        {
            "ColumnIndex": 88,
            "Type": "SMText",
            "MaxLength": 1
        },
    "FlagForThursday":
        {
            "ColumnIndex": 89,
            "Type": "SMText",
            "MaxLength": 1
        },
    "FlagForFriday":
        {
            "ColumnIndex": 90,
            "Type": "SMText",
            "MaxLength": 1
        },
    "FlagForSaturday":
        {
            "ColumnIndex": 91,
            "Type": "SMText",
            "MaxLength": 1
        },
    "PackagingIndicator":
        {
            "ColumnIndex": 92,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "Multibarcode1No":
        {
            "ColumnIndex": 93,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "Multibarcode2No":
        {
            "ColumnIndex": 94,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TotalMultibarcode1No":
        {
            "ColumnIndex": 95,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TotalMultibarcode2No":
        {
            "ColumnIndex": 96,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "LinkedNutrition":
        {
            "ColumnIndex": 97,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "PluUCCEanPrefix":
        {
            "ColumnIndex": 98,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "PLUSerialNumber":
        {
            "ColumnIndex": 99,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "IndiaCODE128ExtentItemCode":
        {
            "ColumnIndex": 100,
            "Type": "SMInt",
            "MaxLength": 5
        },
    "IndiaCODE128BarcodeHead":
        {
            "ColumnIndex": 101,
            "Type": "SMText",
            "MaxLength": 6
        },
    "CommodityFont1":
        {
            "ColumnIndex": 102,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "CommodityName1":
        {
            "ColumnIndex": 103,
            "Type": "SMText",
            "MaxLength": 100
        },
    "CommodityFont2":
        {
            "ColumnIndex": 104,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "CommodityName2":
        {
            "ColumnIndex": 105,
            "Type": "SMText",
            "MaxLength": 100
        },
    "CommodityFont3":
        {
            "ColumnIndex": 106,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "CommodityName3":
        {
            "ColumnIndex": 107,
            "Type": "SMText",
            "MaxLength": 100
        },
    "CommodityFont4":
        {
            "ColumnIndex": 108,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "CommodityName4":
        {
            "ColumnIndex": 109,
            "Type": "SMText",
            "MaxLength": 100
        },
    "AdvertisementNo":
        {
            "ColumnIndex": 110,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "FlexinutritionNo":
        {
            "ColumnIndex": 111,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "FlagForUnitPriceLimit":
        {
            "ColumnIndex": 112,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "UnitPriceLowerLimit":
        {
            "ColumnIndex": 113,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "UnitPriceUpperLimit":
        {
            "ColumnIndex": 114,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "DiscountPriceImage1":
        {
            "ColumnIndex": 115,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "DiscountPriceImage2":
        {
            "ColumnIndex": 116,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "ProductionTime":
        {
            "ColumnIndex": 117,
            "Type": "SMInt",
            "MaxLength": 4
        }
}

plu_file = 'plu'
##################################################


# Dept
##################################################
dep_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMText",
            "MaxLength": 1
        },
    "DeptName":
        {
            "ColumnIndex": 5,
            "Type": "SMText",
            "MaxLength": 16
        }
}

dep_file = 'dep'
##################################################

# Preset Key
##################################################
kas_struct = {
    "PageNo":
        {
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "KeyNo":
        {
            "ColumnIndex": 2,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "DeleteFlag":
        {
            "ColumnIndex": 3,
            "Type": "SMText",
            "MaxLength": 1
        },
    "SwitchNo":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "Status":
        {
            "ColumnIndex": 5,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "ValueKeyValue":
        {
            "ColumnIndex": 6,
            "Type": "SMInt",
            "MaxLength": 8
        }
}

kas_file = 'kas'
##################################################

# plu total
##################################################
plt_struct = {
    "PLUNo":
        {
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMText",
            "MaxLength": 1
        },
    "Date":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "Time":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "MachineCode":
        {
            "ColumnIndex": 5,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "MGNo":
        {
            "ColumnIndex": 6,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TotalDailyQuantity":
        {
            "ColumnIndex": 7,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyWeight":
        {
            "ColumnIndex": 8,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyActuralPrice":
        {
            "ColumnIndex": 9,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyPlannedPrice":
        {
            "ColumnIndex": 10,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyProfit":
        {
            "ColumnIndex": 11,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermQuantity":
        {
            "ColumnIndex": 12,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermWeight":
        {
            "ColumnIndex": 13,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermActuralPrice":
        {
            "ColumnIndex": 14,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermPlannedPrice":
        {
            "ColumnIndex": 15,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermProfit":
        {
            "ColumnIndex": 16,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalPPKDailyQuantity":
        {
            "ColumnIndex": 17,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalPPKDailyWeight":
        {
            "ColumnIndex": 18,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalPPKDailyActuralPrice":
        {
            "ColumnIndex": 19,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalPPKDailyPlannedPrice":
        {
            "ColumnIndex": 20,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalPPKDailyProfit":
        {
            "ColumnIndex": 21,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalPPKTermQuantity":
        {
            "ColumnIndex": 22,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalPPKTermWeight":
        {
            "ColumnIndex": 23,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalPPKTermActuralPrice":
        {
            "ColumnIndex": 24,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalPPKTermPlannedPrice":
        {
            "ColumnIndex": 25,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalPPKTermProfit":
        {
            "ColumnIndex": 26,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDiscountDailyQuantity":
        {
            "ColumnIndex": 27,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDiscountDailyWeight":
        {
            "ColumnIndex": 28,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDiscountDailyActuralPrice":
        {
            "ColumnIndex": 29,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDiscountDailyPlannedPrice":
        {
            "ColumnIndex": 30,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDiscountDailyProfit":
        {
            "ColumnIndex": 31,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDiscountTermQuantity":
        {
            "ColumnIndex": 32,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDiscountTermWeight":
        {
            "ColumnIndex": 33,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDiscountTermActuralPrice":
        {
            "ColumnIndex": 34,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDiscountTermPlannedPrice":
        {
            "ColumnIndex": 35,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDiscountTermProfit":
        {
            "ColumnIndex": 36,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "LastActDate":
        {
            "ColumnIndex": 37,
            "Type": "SMInt",
            "MaxLength": 6
        }
}

plt_file = 'plt'
##################################################

# Plu Transaction File
##################################################
ptr_struct = {
    "Code":
        {
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 7
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMText",
            "MaxLength": 1
        },
    "Date":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "Time":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "PLUNo":
        {
            "ColumnIndex": 5,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "UnitPrice":
        {
            "ColumnIndex": 6,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "Weight":
        {
            "ColumnIndex": 7,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "Quantity":
        {
            "ColumnIndex": 8,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalPrice":
        {
            "ColumnIndex": 9,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "BeforeUnitPrice":
        {
            "ColumnIndex": 10,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "AfterUnitPrice":
        {
            "ColumnIndex": 11,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "PLUEANdata":
        {
            "ColumnIndex": 12,
            "Type": "SMText",
            "MaxLength": 12
        },
    "PLUCommodityName":
        {
            "ColumnIndex": 13,
            "Type": "SMText",
            "MaxLength": 48
        },
    "BasketNo":
        {
            "ColumnIndex": 14,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "MGNo":
        {
            "ColumnIndex": 15,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "ProcessMode":
        {
            "ColumnIndex": 16,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "TraceabilityReferenceCode":
        {
            "ColumnIndex": 17,
            "Type": "SMText",
            "MaxLength": 20
        },
    "ClerkNo":
        {
            "ColumnIndex": 18,
            "Type": "SMInt",
            "MaxLength": 2
        }
}

ptr_file = 'ptr'
##################################################

# Real Time Buffer File
##################################################
rtb_struct = {
    "Mode":
        {
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "Node":
        {
            "ColumnIndex": 2,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "FlagOfOffLine":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "ReceiptNo":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 7
        },
    "TransactionNo":
        {
            "ColumnIndex": 5,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "DeleteFlag":
        {
            "ColumnIndex": 6,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FileID":
        {
            "ColumnIndex": 7,
            "Type": "SMText",
            "MaxLength": 2
        },
    "IPAddressTail":
        {
            "ColumnIndex": 8,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "TaxRateNo":
        {
            "ColumnIndex": 9,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "PercentDiscountRate":
        {
            "ColumnIndex": 10,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "DiscountAmount":
        {
            "ColumnIndex": 11,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "PLUNo":
        {
            "ColumnIndex": 12,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "WeightQuantity":
        {
            "ColumnIndex": 13,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "Tare":
        {
            "ColumnIndex": 14,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "UnitPriceAfterDiscount":
        {
            "ColumnIndex": 15,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "OriginalUnitPrice":
        {
            "ColumnIndex": 16,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "PriceBeforeSubtotalDiscount":
        {
            "ColumnIndex": 17,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "PLUDiscountType":
        {
            "ColumnIndex": 18,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "FlagOfDiscount":
        {
            "ColumnIndex": 19,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagOfPerDiscount":
        {
            "ColumnIndex": 20,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagOfItem":
        {
            "ColumnIndex": 21,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagOfRefundItem":
        {
            "ColumnIndex": 22,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagOfSubtotal":
        {
            "ColumnIndex": 23,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagOfCorrect":
        {
            "ColumnIndex": 24,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagofVoid":
        {
            "ColumnIndex": 25,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagofUnit":
        {
            "ColumnIndex": 26,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagofPriceBase":
        {
            "ColumnIndex": 27,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "MemberShipNo":
        {
            "ColumnIndex": 28,
            "Type": "SMInt",
            "MaxLength": 8
        },
    "TraceabilityNo":
        {
            "ColumnIndex": 29,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "ReferenceType":
        {
            "ColumnIndex": 30,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "ReferenceDate":
        {
            "ColumnIndex": 31,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "ReferenceCode":
        {
            "ColumnIndex": 32,
            "Type": "SMText",
            "MaxLength": 20
        },
    "LotNumber":
        {
            "ColumnIndex": 33,
            "Type": "SMText",
            "MaxLength": 30
        },
    "TraceLink":
        {
            "ColumnIndex": 34,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "EatDate":
        {
            "ColumnIndex": 35,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "Weight":
        {
            "ColumnIndex": 36,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "BornCountryNo":
        {
            "ColumnIndex": 37,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "FattenCountryNo":
        {
            "ColumnIndex": 38,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "SlaughterHouseNo":
        {
            "ColumnIndex": 39,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "SlaughterCountryNo":
        {
            "ColumnIndex": 40,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "CuttingHallNo":
        {
            "ColumnIndex": 41,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "CuttingCountryNo":
        {
            "ColumnIndex": 42,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "CountryNoOfOrigin":
        {
            "ColumnIndex": 43,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "KindNo":
        {
            "ColumnIndex": 44,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "CategoryNo":
        {
            "ColumnIndex": 45,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "BreedNo":
        {
            "ColumnIndex": 46,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "GTIN":
        {
            "ColumnIndex": 47,
            "Type": "SMText",
            "MaxLength": 14
        },
    "ContactRef":
        {
            "ColumnIndex": 48,
            "Type": "SMText",
            "MaxLength": 10
        },
    "SupplierCode":
        {
            "ColumnIndex": 49,
            "Type": "SMText",
            "MaxLength": 30
        },
    "SupplierName":
        {
            "ColumnIndex": 50,
            "Type": "SMText",
            "MaxLength": 30
        },
    "SupplierAddr1":
        {
            "ColumnIndex": 51,
            "Type": "SMText",
            "MaxLength": 30
        },
    "SupplierAddr2":
        {
            "ColumnIndex": 52,
            "Type": "SMText",
            "MaxLength": 30
        }
}

rtb_file = 'rtb'
##################################################


# Real Time Total
##################################################
rtt_struct = {
    "Mode":
        {
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "Node":
        {
            "ColumnIndex": 2,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "FlagOfOffLine":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "ReceiptNo":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 7
        },
    "DeleteFlag":
        {
            "ColumnIndex": 5,
            "Type": "SMText",
            "MaxLength": 1
        },
    "FileID":
        {
            "ColumnIndex": 6,
            "Type": "SMText",
            "MaxLength": 2
        },
    "Date":
        {
            "ColumnIndex": 7,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "Time":
        {
            "ColumnIndex": 8,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "MachineCode":
        {
            "ColumnIndex": 9,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "ClerkNo":
        {
            "ColumnIndex": 10,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "IPaddressTail":
        {
            "ColumnIndex": 11,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "TransactionNumber":
        {
            "ColumnIndex": 12,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "TotalAmountOfAddOnTax":
        {
            "ColumnIndex": 13,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalAmountOfVATTax":
        {
            "ColumnIndex": 14,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalWeight":
        {
            "ColumnIndex": 15,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalQuantity":
        {
            "ColumnIndex": 16,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalAmount":
        {
            "ColumnIndex": 17,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalFinalAmount":
        {
            "ColumnIndex": 18,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalRoundingAmount":
        {
            "ColumnIndex": 19,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalEUROfinalAmount":
        {
            "ColumnIndex": 20,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalValueOfCash":
        {
            "ColumnIndex": 21,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalValueOfCredit":
        {
            "ColumnIndex": 22,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalChangeAmount":
        {
            "ColumnIndex": 23,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalEUROTender":
        {
            "ColumnIndex": 24,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalChequeAmount":
        {
            "ColumnIndex": 25,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalVoucherAmount":
        {
            "ColumnIndex": 26,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalCardAmount":
        {
            "ColumnIndex": 27,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalPayoutAmount":
        {
            "ColumnIndex": 28,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalAmountWithoutChange":
        {
            "ColumnIndex": 29,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "MemberShipNo":
        {
            "ColumnIndex": 30,
            "Type": "SMInt",
            "MaxLength": 8
        }
}

rtt_file = 'rtt'
##################################################


# Dept Total
##################################################
dpt_struct = {
    "DeptCode":
        {
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "Date":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "Time":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "MachineCode":
        {
            "ColumnIndex": 5,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TotalDailyCustomer":
        {
            "ColumnIndex": 6,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyQuantity":
        {
            "ColumnIndex": 7,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyWeight":
        {
            "ColumnIndex": 8,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyActualPrice":
        {
            "ColumnIndex": 9,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyPlannedPrice":
        {
            "ColumnIndex": 10,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyProfit":
        {
            "ColumnIndex": 11,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalMonthlyCustomer":
        {
            "ColumnIndex": 12,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalMonthlyQuantity":
        {
            "ColumnIndex": 13,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalMonthlyWeight":
        {
            "ColumnIndex": 14,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalMonthlyActualPrice":
        {
            "ColumnIndex": 15,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalMonthlyPlannedPrice":
        {
            "ColumnIndex": 16,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalMonthlyProfit":
        {
            "ColumnIndex": 17,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermCustomer":
        {
            "ColumnIndex": 18,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermQuantity":
        {
            "ColumnIndex": 19,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermWeight":
        {
            "ColumnIndex": 20,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermActualPrice":
        {
            "ColumnIndex": 21,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermPlannedPrice":
        {
            "ColumnIndex": 22,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermProfit":
        {
            "ColumnIndex": 23,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalLastMonthCustomer":
        {
            "ColumnIndex": 24,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalLastMonthQuantity":
        {
            "ColumnIndex": 25,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalLastMonthWeight":
        {
            "ColumnIndex": 26,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalLastMonthActualPrice":
        {
            "ColumnIndex": 27,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalLastMonthPlannedPrice":
        {
            "ColumnIndex": 28,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalLastMonthProfit":
        {
            "ColumnIndex": 29,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "LastActDate":
        {
            "ColumnIndex": 30,
            "Type": "SMInt",
            "MaxLength": 6
        }
}

dpt_file = 'dpt'
##################################################


# MG Total
##################################################
mgt_struct = {
    "MGCode":
        {
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMText",
            "MaxLength": 1
        },
    "Date":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "Time":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "MachineCode":
        {
            "ColumnIndex": 5,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "LinkedDepartmentNo":
        {
            "ColumnIndex": 6,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TotalDailyCustomer":
        {
            "ColumnIndex": 7,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyQuantity":
        {
            "ColumnIndex": 8,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyWeight":
        {
            "ColumnIndex": 9,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyActualPrice":
        {
            "ColumnIndex": 10,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyPlannedPrice":
        {
            "ColumnIndex": 11,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyProfit":
        {
            "ColumnIndex": 12,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyDiscountPrice":
        {
            "ColumnIndex": 13,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyNoOfRefund":
        {
            "ColumnIndex": 14,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyRefundPrice":
        {
            "ColumnIndex": 15,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermCustomer":
        {
            "ColumnIndex": 16,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermQuantity":
        {
            "ColumnIndex": 17,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermWeight":
        {
            "ColumnIndex": 18,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermActualPrice":
        {
            "ColumnIndex": 19,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermPlannedPrice":
        {
            "ColumnIndex": 20,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermProfit":
        {
            "ColumnIndex": 21,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermDiscountPrice":
        {
            "ColumnIndex": 22,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalTermNoOfRefund":
        {
            "ColumnIndex": 23,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "TotalDailyRefundPrice":
        {
            "ColumnIndex": 24,
            "Type": "SMInt",
            "MaxLength": 11
        },
    "LastActDate":
        {
            "ColumnIndex": 25,
            "Type": "SMInt",
            "MaxLength": 6
        }
}

mgt_file = 'mgt'
##################################################

# Traceability Group
##################################################
trg_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMText",
            "MaxLength": 1
        },
    "ReferenceType":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "ReferenceDate":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "ReferenceCode":
        {
            "ColumnIndex": 5,
            "Type": "SMText",
            "MaxLength": 20
        },
    "LotNumber":
        {
            "ColumnIndex": 6,
            "Type": "SMText",
            "MaxLength": 30
        },
    "TraceLink":
        {
            "ColumnIndex": 7,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "EatDate":
        {
            "ColumnIndex": 8,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "Weight":
        {
            "ColumnIndex": 9,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "BornCountryNo":
        {
            "ColumnIndex": 10,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "FattenCountryNo":
        {
            "ColumnIndex": 11,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "SlaughterHouseNo":
        {
            "ColumnIndex": 12,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "SlaughterCountryNo":
        {
            "ColumnIndex": 13,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "CuttingHallNo":
        {
            "ColumnIndex": 14,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "CuttingCountryNo":
        {
            "ColumnIndex": 15,
            "Type": "SMInt",
            "MaxLength": 4
        },
    "CountryNoOfOrigin":
        {
            "ColumnIndex": 16,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "KindNo":
        {
            "ColumnIndex": 17,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "CategoryNo":
        {
            "ColumnIndex": 18,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "BreedNo":
        {
            "ColumnIndex": 19,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "GTIN":
        {
            "ColumnIndex": 20,
            "Type": "SMText",
            "MaxLength": 14
        },
    "ContactRef":
        {
            "ColumnIndex": 21,
            "Type": "SMText",
            "MaxLength": 10
        },
    "SupplierCode":
        {
            "ColumnIndex": 22,
            "Type": "SMText",
            "MaxLength": 30
        },
    "SupplierName":
        {
            "ColumnIndex": 23,
            "Type": "SMText",
            "MaxLength": 30
        },
    "SupplierAddr1":
        {
            "ColumnIndex": 24,
            "Type": "SMText",
            "MaxLength": 30
        },
    "SupplierAddr2":
        {
            "ColumnIndex": 25,
            "Type": "SMText",
            "MaxLength": 30
        },
    "TraceBarcodeNo":
        {
            "ColumnIndex": 26,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "TraceTextNo":
        {
            "ColumnIndex": 27,
            "Type": "SMInt",
            "MaxLength": 6
        }
}

trg_file = 'trg'
##################################################

# Traceability Barcode File
##################################################
trb_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMText",
            "MaxLength": 1
        },
    "Data":
        {
            "ColumnIndex": 3,
            "Type": "SMText",
            "MaxLength": 1111
        }
}

trb_file = 'trb'
##################################################


# Traceability Text File
##################################################
trt_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "LineNo":
        {
            "ColumnIndex": 2,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "DeleteFlag":
        {
            "ColumnIndex": 3,
            "Type": "SMText",
            "MaxLength": 1
        },
    "TraceabilityTextFlag":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "Data":
        {
            "ColumnIndex": 5,
            "Type": "SMText",
            "MaxLength": 100
        }
}

trt_file = 'trt'
##################################################


# Multi Barcode File
##################################################
mub_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMText",
            "MaxLength": 1
        },
    "MultiBarcodeType":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "BarcodeType":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "Data":
        {
            "ColumnIndex": 5,
            "Type": "SMText",
            "MaxLength": 48
        },
    "Link2DBarcodeTextNo":
        {
            "ColumnIndex": 6,
            "Type": "SMInt",
            "MaxLength": 6
        }
}

mub_file = 'mub'
##################################################


# 2D Barcode Text File
##################################################
tbt_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "LineNo":
        {
            "ColumnIndex": 2,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "DeleteFlag":
        {
            "ColumnIndex": 3,
            "Type": "SMText",
            "MaxLength": 1
        },
    "TextFlag":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 0
        },
    "Data":
        {
            "ColumnIndex": 5,
            "Type": "SMText",
            "MaxLength": 100
        }
}

tbt_file = 'tbt'
##################################################


# Print Format File
##################################################
prf_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMText",
            "MaxLength": 1
        },
    "PrintFormatWidth":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "PrintFormatHeight":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "PrintFormatAngle":
        {
            "ColumnIndex": 5,
            "Type": "SMInt",
            "MaxLength": 1
        }
}

prf_file = 'prf'
##################################################

# Print Format Field File
##################################################
pff_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "FieldCode":
        {
            "ColumnIndex": 2,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "YPosition":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "LabelType":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "DeleteFlag":
        {
            "ColumnIndex": 5,
            "Type": "SMText",
            "MaxLength": 1
        },
    "XPosition":
        {
            "ColumnIndex": 6,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "Angle":
        {
            "ColumnIndex": 7,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "PrintStatus":
        {
            "ColumnIndex": 8,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "CharacterSize":
        {
            "ColumnIndex": 9,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "Width":
        {
            "ColumnIndex": 10,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "Height":
        {
            "ColumnIndex": 11,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "Thinkness":
        {
            "ColumnIndex": 12,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "X1Position":
        {
            "ColumnIndex": 13,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "Y1Position":
        {
            "ColumnIndex": 14,
            "Type": "SMInt",
            "MaxLength": 3
        },
    "LinkedFileNo":
        {
            "ColumnIndex": 15,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "LinkedFileSource":
        {
            "ColumnIndex": 16,
            "Type": "SMInt",
            "MaxLength": 0
        },
    "CharacterSizex2x4":
        {
            "ColumnIndex": 17,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "CentType":
        {
            "ColumnIndex": 18,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "AutoSizing":
        {
            "ColumnIndex": 19,
            "Type": "SMInt",
            "MaxLength": 1
        }
}

pff_file = 'pff'
##################################################

# FlexiBarcode File
##################################################
flb_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "DeleteFlag":
        {
            "ColumnIndex": 2,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagType":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "ItemCodeDigitNumber":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "ProgramData1DigitNumber":
        {
            "ColumnIndex": 5,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "ProgramData2DigitNumber":
        {
            "ColumnIndex": 6,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlexibarcodeDigitNumber":
        {
            "ColumnIndex": 7,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagOfMiddleCheckDigit":
        {
            "ColumnIndex": 8,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagOfLastCheckDigit":
        {
            "ColumnIndex": 9,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagOfBarcodeType":
        {
            "ColumnIndex": 10,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "ProgramData1Type":
        {
            "ColumnIndex": 11,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "ProgramData2Type":
        {
            "ColumnIndex": 12,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "ProgramData1Shift":
        {
            "ColumnIndex": 13,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "ProgramData2Shift":
        {
            "ColumnIndex": 14,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagOfIndiaCode128":
        {
            "ColumnIndex": 15,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "FlagOfIndiaCode128LastByte":
        {
            "ColumnIndex": 16,
            "Type": "SMInt",
            "MaxLength": 1
        }
}

flb_file = 'flb'
##################################################



# Special Message
##################################################
spm_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "LineNo":
        {
            "ColumnIndex": 2,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "DeleteFlag":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "Flag":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "Data":
        {
            "ColumnIndex": 5,
            "Type": "SMText",
            "MaxLength": 100
        }
}

spm_file = 'spm'
##################################################

# Ingredient
##################################################
ing_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "LineNo":
        {
            "ColumnIndex": 2,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "DeleteFlag":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "Flag":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "Data":
        {
            "ColumnIndex": 5,
            "Type": "SMText",
            "MaxLength": 100
        }
}

ing_file = 'ing'
##################################################


# Text
##################################################
tex_struct = {
    "Code":
        {
            "Key": 1,
            "ColumnIndex": 1,
            "Type": "SMInt",
            "MaxLength": 6
        },
    "LineNo":
        {
            "ColumnIndex": 2,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "DeleteFlag":
        {
            "ColumnIndex": 3,
            "Type": "SMInt",
            "MaxLength": 1
        },
    "Flag":
        {
            "ColumnIndex": 4,
            "Type": "SMInt",
            "MaxLength": 2
        },
    "Data":
        {
            "ColumnIndex": 5,
            "Type": "SMText",
            "MaxLength": 100
        }
}

tex_file = 'tex'
##################################################

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
    "FRAME 1": 220,
    "FRAME 2": 221,
    "TARE": 24,
    "CLERK": 25,
    "TEXT 1": 260,
    "TEXT 2": 261,
    "TEXT 3": 262,
    "TEXT 4": 263,
    "TEXT 5": 264,
    "TEXT 6": 265,
    "TEXT 7": 266,
    "TEXT 8": 267,
    "TEXT 9": 268,
    "TEXT 10": 269,
    "TEXT 11": 270,
    "TEXT 12": 271,
    "TEXT 13": 272,
    "TEXT 14": 273,
    "TEXT 15": 274,
    "TEXT 16": 275,
    "TEXT 17": 276,
    "TEXT 18": 277,
    "TEXT 19": 278,
    "TEXT 20": 279,
    "PRICE (+ TAX)": 46,
    "TAX RATE": 47,
    "PLACE": 48,
    "IMAGE 1": 490,
    "IMAGE 2": 491,
    "IMAGE 3": 492,
    "IMAGE 4": 493,
    "IMAGE 5": 494,
    "IMAGE 6": 495,
    "IMAGE 7": 496,
    "IMAGE 8": 497,
    "IMAGE 9": 498,
    "IMAGE 10": 499,
    "PRICE BEFORE DISCOUNT": 59,
    "UNIT PRICE BEFORE DISCOUNT": 60,
    "AVERAGE PRICE": 61,
    "AVERAGE WEIGHT": 62,
    "GROSS WEIGHT": 63,
    "EURO UNIT PRICE": 64,
    "EURO TOTAL PRICE": 65,
    "BORN COUNTRY": 66,
    "FATTEN COUNTRY": 67,
    "SLAUGTHER HOUSE": 68,
    "CUTTING HALL": 69,
    "REFER NO": 70,
    "ORIGIN": 71,
    "KIND": 72,
    "CATEGORY": 73,
    "BREED": 74,
    "CONTACT": 75,
    "GTIN": 76,
    "SUPPLIER CODE": 77,
    "SUPPLIER NAME": 78,
    "SUPPLIER ADDRESS 1": 79,
    "SUPPLIER ADDRESS 2": 80,
    "TEMPERATURE": 81,
    "MULTI BARCODE 1": 82,
    "MULTI BARCODE 2": 83,
    "SERIAL NO": 84,
    "TOTAL TITLE": 85,
    "EXCLUDED TAX AMOUNT": 86,
    "INCLUDED TAX AMOUNT": 87,
    "ADVERTISEMENT": 88,
    "DISCOUNT PRICE TAG": 89,
    "DISCOUNT PRICE IMAGE 1": 90,
    "DISCOUNT PRICE IMAGE 2": 91,
    "REWRAP": 92,
    "TRACEABILITY TEXT": 93,
    "PRODUCTION DATE": 94,
    "PRODUCTION TIME": 95,
    "Serving size": 901,
    "Serving container": 902,
    "Selection of 100g / 100ml": 903,
    "Unit weight portion": 904,
    "Number of portions": 905,
    "Energy (kCal)": 906,
    "Energy (kJ)": 907,
    "Energy %": 908,
    "Total fat": 909,
    "Total fat %": 910,
    "Saturate fat": 911,
    "Saturate fat %": 912,
    "Carbohydrate": 913,
    "Carbohydrate %": 914,
    "Sugars": 915,
    "Sugars %": 916,
    "Protein": 917,
    "Protein %": 918,
    "Salt": 919,
    "Salt %": 920,
    "Vitamin A": 921,
    "Vitamin A %": 922,
    "Vitamin D": 923,
    "Vitamin D %": 924,
    "Vitamin E": 925,
    "Vitamin E %": 926,
    "Vitamin K": 927,
    "Vitamin K %": 928,
    "Vitamin C": 929,
    "Vitamin C %": 930,
    "Thiamine": 931,
    "Thiamine %": 932,
    "Riboflavin": 933,
    "Riboflavin %": 934,
    "Niacin": 935,
    "Niacin %": 936,
    "Vitamin B6": 937,
    "Vitamin B6 %": 938,
    "Folic acid": 939,
    "Folic acid %": 940,
    "Vitamin B12": 941,
    "Vitamin B12 %": 942,
    "Biotin": 943,
    "Biotin %": 944,
    "Pantothenic acid": 945,
    "Pantothenic acid %": 946,
    "Potassium": 947,
    "Potassium %": 948,
    "Chloride": 949,
    "Chloride %": 950,
    "Calcium": 951,
    "Calcium %": 952,
    "Phosphorus": 953,
    "Phosphorus %": 954,
    "Magnesium": 955,
    "Magnesium %": 956,
    "Iron": 957,
    "Iron %": 958,
    "Zinc": 959,
    "Zinc %": 960,
    "Copper": 961,
    "Copper %": 962,
    "Manganese": 963,
    "Manganese %": 964,
    "Fluoride": 965,
    "Fluoride %": 966,
    "Selenium": 967,
    "Selenium %": 968,
    "Chromium": 969,
    "Chromium %": 970,
    "Molybdenum": 971,
    "Molybdenum %": 972,
    "Lodine": 973,
    "Lodine %": 974
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
    220: "FRAME 1",
    221: "FRAME 2",
    24: "TARE",
    25: "CLERK",
    260: "TEXT 1",
    261: "TEXT 2",
    262: "TEXT 3",
    263: "TEXT 4",
    264: "TEXT 5",
    265: "TEXT 6",
    266: "TEXT 7",
    267: "TEXT 8",
    268: "TEXT 9",
    269: "TEXT 10",
    270: "TEXT 11",
    271: "TEXT 12",
    272: "TEXT 13",
    273: "TEXT 14",
    274: "TEXT 15",
    275: "TEXT 16",
    276: "TEXT 17",
    277: "TEXT 18",
    278: "TEXT 19",
    279: "TEXT 20",
    46: "PRICE (+ TAX)",
    47: "TAX RATE",
    48: "PLACE",
    490: "IMAGE 1",
    491: "IMAGE 2",
    492: "IMAGE 3",
    493: "IMAGE 4",
    494: "IMAGE 5",
    495: "IMAGE 6",
    496: "IMAGE 7",
    497: "IMAGE 8",
    498: "IMAGE 9",
    499: "IMAGE 10",
    59: "PRICE BEFORE DISCOUNT",
    60: "UNIT PRICE BEFORE DISCOUNT",
    61: "AVERAGE PRICE",
    62: "AVERAGE WEIGHT",
    63: "GROSS WEIGHT",
    64: "EURO UNIT PRICE",
    65: "EURO TOTAL PRICE",
    66: "BORN COUNTRY",
    67: "FATTEN COUNTRY",
    68: "SLAUGTHER HOUSE",
    69: "CUTTING HALL",
    70: "REFER NO",
    71: "ORIGIN",
    72: "KIND",
    73: "CATEGORY",
    74: "BREED",
    75: "CONTACT",
    76: "GTIN",
    77: "SUPPLIER CODE",
    78: "SUPPLIER NAME",
    79: "SUPPLIER ADDRESS 1",
    80: "SUPPLIER ADDRESS 2",
    81: "TEMPERATURE",
    82: "MULTI BARCODE 1",
    83: "MULTI BARCODE 2",
    84: "SERIAL NO",
    85: "TOTAL TITLE",
    86: "EXCLUDED TAX AMOUNT",
    87: "INCLUDED TAX AMOUNT",
    88: "ADVERTISEMENT",
    89: "DISCOUNT PRICE TAG",
    90: "DISCOUNT PRICE IMAGE 1",
    91: "DISCOUNT PRICE IMAGE 2",
    92: "REWRAP",
    93: "TRACEABILITY TEXT",
    94: "PRODUCTION DATE",
    95: "PRODUCTION TIME",
    901: "Serving size",
    902: "Serving container",
    903: "Selection of 100g / 100ml",
    904: "Unit weight portion",
    905: "Number of portions",
    906: "Energy (kCal)",
    907: "Energy (kJ)",
    908: "Energy %",
    909: "Total fat",
    910: "Total fat %",
    911: "Saturate fat",
    912: "Saturate fat %",
    913: "Carbohydrate",
    914: "Carbohydrate %",
    915: "Sugars",
    916: "Sugars %",
    917: "Protein",
    918: "Protein %",
    919: "Salt",
    920: "Salt %",
    921: "Vitamin A",
    922: "Vitamin A %",
    923: "Vitamin D",
    924: "Vitamin D %",
    925: "Vitamin E",
    926: "Vitamin E %",
    927: "Vitamin K",
    928: "Vitamin K %",
    929: "Vitamin C",
    930: "Vitamin C %",
    931: "Thiamine",
    932: "Thiamine %",
    933: "Riboflavin",
    934: "Riboflavin %",
    935: "Niacin",
    936: "Niacin %",
    937: "Vitamin B6",
    938: "Vitamin B6 %",
    939: "Folic acid",
    940: "Folic acid %",
    941: "Vitamin B12",
    942: "Vitamin B12 %",
    943: "Biotin",
    944: "Biotin %",
    945: "Pantothenic acid",
    946: "Pantothenic acid %",
    947: "Potassium",
    948: "Potassium %",
    949: "Chloride",
    950: "Chloride %",
    951: "Calcium",
    952: "Calcium %",
    953: "Phosphorus",
    954: "Phosphorus %",
    955: "Magnesium",
    956: "Magnesium %",
    957: "Iron",
    958: "Iron %",
    959: "Zinc",
    960: "Zinc %",
    961: "Copper",
    962: "Copper %",
    963: "Manganese",
    964: "Manganese %",
    965: "Fluoride",
    966: "Fluoride %",
    967: "Selenium",
    968: "Selenium %",
    969: "Chromium",
    970: "Chromium %",
    971: "Molybdenum",
    972: "Molybdenum %",
    973: "Lodine",
    974: "Lodine %"
}
