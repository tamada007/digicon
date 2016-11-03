#encoding=gbk

import os, sys, re, traceback
#import csv, StringIO

sys.path.append("..")
import libsm120.digiscale, libsm120.entity
import common.common
import libsm120.const

ROOT_PROMPT = "DigiCon"
PROMPT_SYMBOL = ">"


global_data = {"print_formats": []}

class DigiTermItem():
    def __init__(self, parent = None, prompt = ""):
        self.parent = parent
        self.prompt = prompt
        
    def getPrompt(self):
        if self.parent and self.prompt:
            return self.parent.getPrompt() + " " + self.prompt
        else:
            return ROOT_PROMPT
        
    def getClassCommand(self):
        if self.parent and self.prompt:
            return self.parent.getClassCommand() + self.prompt + "."
        else:
            return ""
        
    def getParent(self):
        return self.parent
        
    def getInput(self):
        return raw_input(self.getPrompt() + PROMPT_SYMBOL)
        
   
def test_start():
    
    curTermItem = DigiTermItem()
    quitFlag = False
    while not quitFlag:
        rawInput = ""
        try:
            rawInput = curTermItem.getInput()
            input_text = curTermItem.getClassCommand() + rawInput
        except EOFError:
            break
        
        #Single Command
        if command_list.has_key(input_text):
            result = command_list.get(input_text)({"obj": curTermItem})
            if isinstance(result, dict):
                #quit
                if result.has_key("quit"):
                    quitFlag = result.get("quit")
                #switch to another node
                if result.has_key("switch_to"):
                    curTermItem = result.get("switch_to")
                    
                if result.has_key("global_data") and isinstance(result.get("global_data"), dict):
                    for k, v in result.get("global_data").items():
                        global_data[k] = v

        else:
            found = False
            #Command With argument
            for command2 in command2_list:
                regex = re.compile(command2[0])
                m = regex.match(input_text)
                if m:
                    found = True
                    arg = {"obj": curTermItem, "arg0": m.group(1)}
                    for i, mi in enumerate(m.groups()):
                        arg["arg%d"%i ] = mi
                    result = command2[1](arg)
                    if isinstance(result, dict):
                        if result.has_key("quit"):
                            quitFlag = result.get("quit")


                        #switch to another node
                        if result.has_key("switch_to"):
                            curTermItem = result.get("switch_to")

                    
                        if result.has_key("global_data") and isinstance(result.get("global_data"), dict):
                            for k, v in result.get("global_data").items():
                                global_data[k] = v
                                
            if rawInput and not found:
                print "Command Not Found, Please check Input."
                    
#     print global_data

def cb_help(arg):
    print """Command List:
    help                Help Information
    cls                 Clear Screen
    label               Start Label Programming
    exit                Exit To System Console
    """
    
def cb_help_label(arg):
    print """Command List:
    recv <Scale IP>            receive printing formats from scale to memory
    send <Scale IP>            send printing formats to scale
    save <File Name>           Save printing formats in memory to file
    list                       List All Printing Formats
    load <File Name>           Load printing formats in memory from file
    fields <Format No.>        List All Fields Information of Printing Formats
    edit <Format No.>          Edit One Printing Format
    exit                       Exit To Root
    """        

def cb_help_lbfield_prop(arg):
    print """Command List:
    list                  List current field properties
    set (x|y|w|h|s|c|a)   Set X|Y|Width|Height|Status|CharSize|Angle 
    exit                  Exit to Printing Format 
    """
    

def cb_cls(arg):
    os.system("cls")
    
def cb_exit(arg):
    return { "quit": True }

def cb_enter_label(arg):
    obj_term = arg.get("obj")
    return { 
        "switch_to": DigiTermItem(parent=obj_term, prompt="Label") 
    }

def cb_exit_edit(arg):
    obj_term = arg.get("obj")
    return {
        "switch_to": obj_term.getParent()
    }

def cb_send_one_lbformat(arg):
    str_format_code = arg.get("arg0")
    ip = arg.get("arg1")
    try:
        format_code = int(str_format_code)
        if not ip: raise Exception("Empty IP")
    except: return {}


    try:
        print_formats = global_data.get("print_formats")
        print_format = next(
            print_format for print_format in print_formats 
            if isinstance(print_format, dict) and print_format.get("Code") == format_code)
    except StopIteration:
        print "Printing Format Not Found...Failed"
        return {}
    
    prfmt = libsm120.entity.MasterFactory().createMaster("Prf")
    pffmt = libsm120.entity.MasterFactory().createMaster("Pff")

    prf_new_row = prfmt.create_row()
    prf_del_row = prfmt.create_row()
    for key, value in print_format.iteritems():
        if key == "Fields" and isinstance(value, list):
            for field in value:
                pff_new_row = pffmt.create_row()
                if isinstance(field, dict):
                    for key2, value2 in field.iteritems():
                        pff_new_row[key2][0] = value2

                pffmt.add_row(pff_new_row)
                
        elif not isinstance(value, list):
            prf_new_row[key][0] = value

    prf_del_row["DeleteFlag"][0] = 2
    prf_del_row["Code"][0] = print_format.get("Code")
    
    prfmt.add_row(prf_del_row)
    prfmt.add_row(prf_new_row)
    
    try:
        with libsm120.digiscale.DigiSm120(ip) as scale:
            if not scale.send(prfmt) or not scale.send(pffmt):
                raise Exception("Sending To Scale Failed")
            
    except Exception:
        print "Sending Data To Scale... Failed"
    else:
        print "Sending Data To Scale...OK"
    

def cb_send_all_lbformats(arg):
    
#     ip = arg0
    ip = arg.get("arg0")
    if not ip:
        return {}
    
    
    print_formats = global_data.get("print_formats")
    if isinstance(print_formats, list):
        prfmt = libsm120.entity.MasterFactory().createMaster("Prf")
        pffmt = libsm120.entity.MasterFactory().createMaster("Pff")
        
        for print_format in print_formats:
            prf_new_row = prfmt.create_row()
            prf_del_row = prfmt.create_row()
            for key, value in print_format.iteritems():
                if key == "Fields" and isinstance(value, list):
                    for field in value:
                        pff_new_row = pffmt.create_row()
                        if isinstance(field, dict):
                            for key2, value2 in field.iteritems():
                                pff_new_row[key2][0] = value2
                                
                        pffmt.add_row(pff_new_row)
                        
                elif not isinstance(value, list):
                    prf_new_row[key][0] = value

            prf_del_row["DeleteFlag"][0] = 2
            prf_del_row["Code"][0] = print_format.get("Code")

            prfmt.add_row(prf_del_row)
            prfmt.add_row(prf_new_row)
                    
        try:
            with libsm120.digiscale.DigiSm120(ip) as scale:
                if not scale.send(prfmt) or not scale.send(pffmt):
                    raise Exception("Sending To Scale Failed")
                
        except Exception:
            print "Sending Data To Scale... Failed"
        else:
            print "Sending Data To Scale...OK"
            
    return {}

#get label
def cb_recv_all_lbformats(arg):
    
#     ip = arg0
    ip = arg.get("arg0")
    if ip:
#         a_csv_line = csv.reader(StringIO.StringIO(arg0), delimiter=' ').next()
        try:
            with libsm120.digiscale.DigiSm120(ip) as scale:
                prfmt = libsm120.entity.MasterFactory().createMaster("Prf")
                pffmt = libsm120.entity.MasterFactory().createMaster("Pff")
                
                scale.recv(prfmt)
                scale.recv(pffmt)
        except Exception:
            #traceback.print_exc()
            print "Receiving Data From Scale ...Failed"
            return {}

        conn = common.common.open_sqlite_db(libsm120.const.db_name)
        cursor = conn.cursor()
        
        sql = "SELECT * FROM Prf"
        prfData = cursor.execute(sql).fetchall()
        print_formats = []
        for prfDatum in prfData:
            #print prfDatum
            
            print_format = {}
            
            for k in prfDatum.keys():
                print_format[k] = prfDatum[k]
                
            
            sql = "SELECT * FROM Pff WHERE Code = ? ORDER BY FieldCode"
            pffData = cursor.execute(sql, [ prfDatum["Code"] ]).fetchall()
            
            print_format["Fields"] = []
            
            for pffDatum in pffData:
                print_field = {}
                
                for k in pffDatum.keys():
                    print_field[k] = pffDatum[k]
                
#                 if print_field.has_key("Code"):    
#                     del print_field["Code"]
                    
                    
                print_format["Fields"].append( print_field )
                
            print_formats.append( print_format )


#         file_name = ip + "_printformat.json"
#         common.common.save_json_to_file(file_name, print_formats)
        


#         names = [(index, desc[0]) for index, desc in enumerate(cursor.description)]
#         field_names = [ data[1] for data in names ]
#         print field_names
        
        
    print "Get Printing Format From Scale to Memory ... OK"

    return { "global_data": { "print_formats": print_formats } }

def cb_save_all_lbformats(arg):
    file_name = arg.get("arg0")
    if file_name and global_data.has_key("print_formats"):
        common.common.save_json_to_file(file_name, global_data.get("print_formats"))
        
        print "Saving Printing Format To %s ...OK" % file_name

def cb_load_lbformat_from_file(arg):
    file_name = arg.get("arg0")
    try:
        if file_name:
            print_formats = common.common.get_json_from_file(file_name)
            
            if not check_available_print_formats(print_formats):
                raise Exception("Incorrect Printing Format")
            
            global_data["print_formats"] = print_formats 
    except:
        print "Loading Printing Format Failed"
    else:
        print "Loading Printing Format From %s ... OK" % file_name
        

def check_available_print_formats(print_formats):
    if not isinstance(print_formats, list): return False
    
    for print_format in print_formats:
        if not isinstance(print_format, dict): return False
        
        if not print_format.has_key("Code"): return False
        
        if not print_format.has_key("Fields") or not isinstance(print_format.get("Fields"), list):
            return False
        
        for field in print_format.get("Fields"):
            if not isinstance(field, dict): return False
            
            if not field.has_key("FieldCode"): return False


    return True


def cb_list_all_lbformats(arg):
    print_formats = global_data.get("print_formats")
    if print_formats:
        for print_format in print_formats:
            if isinstance(print_format, dict):
                print "Code: %2d    Width: %2d    Height: %2d    Angle: %2d" % (
                        print_format.get("Code"),
                        print_format.get("PrintFormatWidth"),
                        print_format.get("PrintFormatHeight"),
                        print_format.get("PrintFormatAngle"),
                )
                
        
def cb_edit_one_lbformat(arg):
    str_format_code = arg.get("arg0")
    try: format_code = int(str_format_code)
    except: return {}
    
    obj_term = arg.get("obj")
    
    print_formats = global_data.get("print_formats")
    for print_format in print_formats:
        if isinstance(print_format, dict):
            if format_code == print_format.get("Code"):
                return { 
                    "switch_to": DigiTermItem(parent=obj_term, prompt="FmtNo." + str_format_code) 
                }

    print "Printing Format No. Not Found."


def cb_set_one_lbformat_prop(arg):
    str_format_code = arg.get("arg0")
    str_format_property = arg.get("arg1")
    try:
        format_code = int(str_format_code)
    except: return {}
    
    mapString = {
        "width" :  "PrintFormatWidth",
        "height" : "PrintFormatHeight",
        "angle" :  "PrintFormatAngle"
    }

    print_formats = global_data.get("print_formats")
    
    try:
        print_format = next(
            print_format for print_format in print_formats 
            if isinstance(print_format, dict) and print_format.get("Code") == format_code)
    except StopIteration:
        print "Printing Format Not Found...Failed"
        return {}
    
    str_property = mapString.get(str_format_property)
    if str_property:
        print "%s: %s" % (str_format_property, str(print_format.get(str_property)))
        try:
            print_format[str_property] = input("Input New %s (Empty To Keep):" % str_format_property)
        except:
            pass
    else:
        print "Format Property Not Found... Failed"
    
    

def cb_set_one_lbfield_prop(arg):
#     obj_term = arg.get("obj")
    str_format_code = arg.get("arg0")
    str_field_code = arg.get("arg1")
    str_field_property = arg.get("arg2")
    

    try:
        format_code = int(str_format_code)
        field_code  = int(str_field_code)
    except: return {}
    
    
    mapString = {
        "x" : "XPosition",
        "y" : "YPosition",
        "w" : "Width",
        "h" : "Height",
        "s" : "PrintStatus",
        "a" : "Angle",
        "c" : "CharacterSize",
    }
    
    
    print_formats = global_data.get("print_formats")
    
    try:
        print_format = next(
            print_format for print_format in print_formats 
            if isinstance(print_format, dict) and print_format.get("Code") == format_code)
    except StopIteration:
        print "Printing Format Not Found...Failed"
        return {}
    
    
    fields = print_format.get("Fields")
    if isinstance(fields, list):
        try:
            field = next(field for field in fields if isinstance(field, dict) and field.get("FieldCode") == field_code)
        except StopIteration:
            print "Field Not Found...Failed"
        else:
            str_property = mapString.get(str_field_property)
            if str_property:
                print "%s: %s" % (str_field_property, str(field.get(str_property)))
                try:
                    field[str_property] = input("Input New %s (Empty To Keep):" % str_field_property)
                except:
                    print "Invalid Input...Failed"
            else:
                print "Field Property Not Found... Failed"
    
    
def cb_new_one_lbformat(arg):
    obj_term = arg.get("obj")
    try:
        format_code = int(arg.get("arg0"))
    except: return {}
    
    print_formats = global_data.get("print_formats")
    try:
        print_format = next(
            print_format for print_format in print_formats 
            if isinstance(print_format, dict) and print_format.get("Code") == format_code)
    except StopIteration:
        print_formats.append({
            "Code": format_code,
            "PrintFormatWidth": 56,
            "PrintFormatHeight": 40,
            "PrintFormatAngle": 0,
            "Fields": []
        })
        return { 
            "switch_to": DigiTermItem(parent=obj_term, prompt="FmtNo.%d" % format_code) 
        }
        
    else:
        print "Printing Format already exists... Failed"
    

def cb_del_one_lbformat(arg):
    try:
        format_code = int(arg.get("arg0"))
    except: return {}

    try:
        print_formats = global_data.get("print_formats")
        print_format = next(
            print_format for print_format in print_formats 
            if isinstance(print_format, dict) and print_format.get("Code") == format_code)
        
        print_formats.remove(print_format)
    except StopIteration:
        print "Printing Format Not Found...Failed"
        return {}
    
    except ValueError:
        print "Deleting Failed"
    
    else:
        print "Deleteing...OK"
    
    
def cb_del_one_field(arg):
    try:
        str_field_code = arg.get("arg1")
        format_code = int(arg.get("arg0"))
        field_code  = int(str_field_code)
    except: return {}

    print_formats = global_data.get("print_formats")
    
    try:
        print_format = next(
            print_format for print_format in print_formats 
            if isinstance(print_format, dict) and print_format.get("Code") == format_code)
    except StopIteration:
        print "Printing Format Not Found...Failed"
        return {}
    
    fields = print_format.get("Fields")
    if isinstance(fields, list):
        found = False
        for field in fields:
            if isinstance(field, dict):
                if field.get("FieldCode") == field_code:
                    fields.remove(field)
                    print "Deleting Field...OK"
                    found = True
                    break
#                     field_name = libsm120.const.printFormatIndexList.get(field_code)
                    #found
#                     return {
#                         "switch_to": DigiTermItem(parent=obj_term, prompt="FieldNo.%d (%s)" % (field_code, field_name))
#                     }
        if not found:
            print "Field Not Found...Failed"
    

def cb_new_one_field(arg):
    obj_term = arg.get("obj")
    try:
        format_code = int(arg.get("arg0"))
    except: return {}

    print_formats = global_data.get("print_formats")
    
    try:
        print_format = next(
            print_format for print_format in print_formats 
            if isinstance(print_format, dict) and print_format.get("Code") == format_code)
    except StopIteration:
        print "Printing Format Not Found...Failed"
        return {}
    
    
    fields = print_format.get("Fields")
    for key, value in libsm120.const.printFormatIndexList.iteritems():
        print "%d: %s" % (key, value)
    
    try:
        field_code = input("Input No.:")
        name = libsm120.const.printFormatIndexList.get(field_code)
        if name:
            pass
    except:
        print "Invalid Value...Failed"
        return {}

    if isinstance(fields, list):
        try:
            next(field for field in fields if isinstance(field, dict) and field.get("FieldCode") == field_code)
        except StopIteration:
            fields.append({
                "Code": format_code, 
                "XPosition": 0, 
                "YPosition": 0, 
                "Width": 0, 
                "Height": 0, 
                "Angle": 0, 
                "X1Position": 0, 
                "Y1Position": 0, 
                "PrintStatus": 7, 
                "CharacterSizex2x4": 0, 
                "LinkedFileSource": 0, 
                "LinkedFileNo": 0, 
                "DeleteFlag": "", 
                "LabelType": 0, 
                "CentType": 0, 
                "AutoSizing": 0, 
                "Thinkness": 0, 
                "FieldCode": field_code, 
                "CharacterSize": 0,
            })

            field_name = libsm120.const.printFormatIndexList.get(field_code)
            return {
                "switch_to": DigiTermItem(parent=obj_term, prompt="FieldNo.%d (%s)" % (field_code, field_name))
            }
            
        else:
            print "Field exists...Failed"
            

def cb_edit_one_field(arg):
    obj_term = arg.get("obj")
    str_field_code = arg.get("arg1")
    try:
        format_code = int(arg.get("arg0"))
        field_code  = int(str_field_code)
    except: return {}
    
    print_formats = global_data.get("print_formats")
    
    try:
        print_format = next(
            print_format for print_format in print_formats 
            if isinstance(print_format, dict) and print_format.get("Code") == format_code)
    except StopIteration:
        print "Printing Format Not Found...Failed"
        return {}
    
    fields = print_format.get("Fields")
    if isinstance(fields, list):
        for field in fields:
            if isinstance(field, dict):
                if field.get("FieldCode") == field_code:
                    field_name = libsm120.const.printFormatIndexList.get(field_code)
                    #found
                    return {
                        "switch_to": DigiTermItem(parent=obj_term, prompt="FieldNo.%d (%s)" % (field_code, field_name))
                    }

def cb_list_lbfield_prop(arg):
    str_field_code = arg.get("arg1")
    try:
        format_code = int(arg.get("arg0"))
        field_code  = int(str_field_code)
    except: return {}
    
    print_formats = global_data.get("print_formats")
    if format_code and isinstance(print_formats, list):
        for print_format in print_formats:
            if isinstance(print_format, dict):
                if print_format.get("Code") == format_code:
                    
                    fields = print_format.get("Fields")
                    if isinstance(fields, list):
                        for field in fields:
                            if isinstance(field, dict):
                                if field.get("FieldCode") == field_code:
                                    
                                    field_name = libsm120.const.printFormatIndexList.get(field_code)
                                    #found
                                    
                                    print "%4s %-20s %3s %3s %3s %3s %3s %3s %3s" % ("Id", "Name", "X", "Y", "W", "H", "S", "A", "C")
                                    
                                    x = field.get("XPosition")
                                    y = field.get("YPosition")
                                    w = field.get("Width")
                                    h = field.get("Height")
                                    s = field.get("PrintStatus")
                                    a = field.get("Angle")
                                    c = field.get("CharacterSize")
                
                                    print "%4d %-20s %3d %3d %3d %3d %3d %3d %3d" % (field_code, field_name[:20], x, y, w, h, s, a, c)
                                    
                                    break
                                    
                    break
    return {}
    
    
        
def cb_list_lbformat_all_fields(arg):
    try: format_code = int(arg.get("arg0"))
    except: return {}
    print_formats = global_data.get("print_formats")
    if format_code and isinstance(print_formats, list):
        for print_format in print_formats:
            if isinstance(print_format, dict):
                if print_format.get("Code") == format_code:
                    
                    #found
                    print_format_width  = print_format.get("PrintFormatWidth")
                    print_format_height = print_format.get("PrintFormatHeight")
                    print_format_angle  = print_format.get("PrintFormatAngle")
                    
                    print "Code:     %d" % format_code
                    print "Width:    %d" % print_format_width
                    print "Height:   %d" % print_format_height
                    print "Angle:    %d" % print_format_angle
                    
                    print "%4s %-20s %3s %3s %3s %3s %3s %3s %3s" % ("Id", "Name", "X", "Y", "W", "H", "S", "A", "C")
                    
                    fields = print_format.get("Fields")
                    if isinstance(fields, list):
                        for field in fields:
                            field_code = field.get("FieldCode")
                            if not field_code: continue
                            field_name = libsm120.const.printFormatIndexList.get(field_code)
                            x = field.get("XPosition")
                            y = field.get("YPosition")
                            w = field.get("Width")
                            h = field.get("Height")
                            s = field.get("PrintStatus")
                            a = field.get("Angle")
                            c = field.get("CharacterSize")
                            

                            print "%4d %-20s %3d %3d %3d %3d %3d %3d %3d" % (field_code, field_name[:20], x, y, w, h, s, a, c)
                    
                    
                    break
        

command_list = {
    "exit":  cb_exit,
    "cls":   cb_cls,

    "quit":  cb_exit,
    "help":  cb_help,
    "label": cb_enter_label,
    
    "Label.cls":  cb_cls,
    "Label.exit": cb_exit_edit,
    "Label.quit": cb_exit_edit,
    "Label.list": cb_list_all_lbformats,
    "Label.help": cb_help_label,
}

command2_list = [
    ("Label\.recv (.+)" ,                                   cb_recv_all_lbformats),
    ("Label\.send (.+)" ,                                   cb_send_all_lbformats),
    ("Label\.save (.+)" ,                                   cb_save_all_lbformats),
    ("Label\.load (.+)" ,                                   cb_load_lbformat_from_file),
    ("Label\.list (.+)" ,                                   cb_list_all_lbformats),
    ("Label\.fields (.+)" ,                                 cb_list_lbformat_all_fields),
    ("Label\.edit (.+)" ,                                   cb_edit_one_lbformat),
    ("Label\.new (\d+)" ,                                   cb_new_one_lbformat),
    ("Label\.del (\d+)" ,                                   cb_del_one_lbformat),
    ("Label\.FmtNo\.(\d+)\.cls" ,                           cb_cls),
    ("Label\.FmtNo\.(\d+)\.set (.+)" ,                      cb_set_one_lbformat_prop),
    ("Label\.FmtNo\.(\d+)\.send (.+)" ,                     cb_send_one_lbformat),
    ("Label\.FmtNo\.(\d+)\.exit" ,                          cb_exit_edit),
    ("Label\.FmtNo\.(\d+)\.fields" ,                        cb_list_lbformat_all_fields),
    ("Label\.FmtNo\.(\d+)\.list" ,                          cb_list_lbformat_all_fields),
    ("Label\.FmtNo\.(\d+)\.edit (\d+)" ,                    cb_edit_one_field),
    ("Label\.FmtNo\.(\d+)\.new" ,                           cb_new_one_field),
    ("Label\.FmtNo\.(\d+)\.del (\d+)" ,                     cb_del_one_field),
    ("Label\.FmtNo\.(\d+)\.FieldNo\.(\d+).+\.cls" ,         cb_cls),
    ("Label\.FmtNo\.(\d+)\.FieldNo\.(\d+).+\.set (.+)" ,    cb_set_one_lbfield_prop),
    ("Label\.FmtNo\.(\d+)\.FieldNo\.(\d+).+\.exit" ,        cb_exit_edit),
    ("Label\.FmtNo\.(\d+)\.FieldNo\.(\d+).+\.list" ,        cb_list_lbfield_prop),
    ("Label\.FmtNo\.(\d+)\.FieldNo\.(\d+).+\.help" ,        cb_help_lbfield_prop),
]


if __name__ == '__main__':
    test_start()
#     cb_recv_all_lbformats(None, "192.168.68.184")
    