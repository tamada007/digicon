# encoding=gbk
import sys, json, const, traceback
import common.csvreader
import common.common
from common import scale_enc_conv as scale_encoding_converter


# import time

class Master(object):
    # DBConnection = common.common.open_sqlite_db(const.db_name)

    """	
    def __del__(self):
        try:
            if self.conn:
                self.conn.close()
        except:
            pass
    """

    def __init__(self, name, jsonData):
        if isinstance(jsonData, str):
            jsonData = common.common.get_json_from_string(jsonData)
        self.name = name
        self.scale_file_name = name + "0uall.csv"
        self.fields_info = []
        self.fieldKeys = []
        types = {
            "SMInt": "int",
            "SMText": "text",
            "SMFloat": "numeric"}
        type_entity = {
            "SMInt": type(0),
            "SMText": type(""),
            "SMFloat": type(0.0),
        }
        for field_name, dic_field_info in jsonData.items():
            # print finfo
            current_field_info = []
            try:
                current_field_info.append(field_name);
                current_field_info.append(types[dic_field_info["Type"]])
                column_index = dic_field_info["ColumnIndex"]
            # fieldDic[field_name] = column_index
            except Exception, e:
                common.common.log_err(traceback.format_exc())

            if dic_field_info.has_key("Key"):
                self.fieldKeys.append(field_name)
            # current_field_info.append("primary key");

            self.fields_info.append(
                {
                    "index": column_index,
                    "name": field_name,
                    "type": type_entity[dic_field_info["Type"]],
                    "text": " ".join(current_field_info),
                })
        # print "columnindex:%d" %  column_index
        # self.fields_info.append(" ".join(current_field_info))
        self.fields_info = sorted(self.fields_info, key=lambda x: x["index"]);
        # self.conn = common.common.open_sqlite_db(const.db_name)
        # self.conn = Master.DBConnection
        self.conn = common.common.open_sqlite_db(const.db_name)
        # self.conn = open_sqlite_db(":memory:")
        # cursor = self.conn.cursor()
        # print self.fields_info

        field_text = [f["text"] for f in self.fields_info]
        self.conn.execute("DROP TABLE IF EXISTS %s" % self.name)
        self.conn.execute("CREATE TABLE IF NOT EXISTS %s ( %s )" % (
            self.name, ", ".join(field_text)
        )
                          )

    # 		if self.fieldKeys and len(self.fieldKeys) > 0:
    # 			cursor.execute("CREATE INDEX %s ON %s (%s)" % ("indx_" + self.name, self.name, ",".join(self.fieldKeys)))

    def __keyValue(self, f):
        # if type(f) is types.IntType or type(f) is types.FloatType:
        fk, fv = f.items()[0]
        # if type(fv) == int or type(fv) == float:
        # return fv
        # elif type(fv) == str:
        # return "%s%s%s"% (""", fv, """)
        return fv;

    def __keyName(self, f):
        fk, fv = f.items()[0]
        return fk

    def create_row(self):
        dic_list = {}
        # print "fieldsinfo:", self.fields_info
        for i, field_info in enumerate(self.fields_info):
            # print field_info
            # val_list.append(field_info["type"]())
            curNode = [field_info["type"]()]
            dic_list[i + 1] = dic_list[field_info["name"]] = curNode
        # val_list.append( {field_info["name"]: field_info["type"]()} )
        # return val_list
        return dic_list

    def add_row(self, field_dic, is_field_name=True):
        if is_field_name:
            # filteredFieldList = [ {k: v[0]} for k, v in field_dic.items() if type(k) is not int ]
            # filteredFieldList = [{k: v[0]} for k, v in field_dic.items() if not isinstance(k, int)]
            filteredFieldList = [{k: v[0] if isinstance(v, list) else v} for k, v in field_dic.items() if
                                 not isinstance(k, int)]
        else:
            # filteredFieldList = [ {k: v[0]} for k, v in field_dic.items() if type(k) is int ]
            # filteredFieldList = [{k: v[0]} for k, v in field_dic.items() if isinstance(k, int)]
            filteredFieldList = [{k: v[0] if isinstance(v, list) else v} for k, v in field_dic.items() if
                                 isinstance(k, int)]

        # fieldList = [self.__keyValue(f) for f in filteredFieldList]
        # fieldList = [scale_encoding_converter.conv_scale_to_pc(str(self.__keyValue(f))) for f in filteredFieldList]
        field_value_list = []
        for f in filteredFieldList:
            fv = scale_encoding_converter.conv_scale_to_pc(self.__keyValue(f))
            if isinstance(fv, str):
                fv = unicode(fv)
            field_value_list.append(fv)
        field_name = [self.__keyName(f) for f in filteredFieldList]
        # 如果没有字段名时，需要和表声明的长度比较
        if not is_field_name and len(field_value_list) != len(self.fields_info):
            field_value_list = field_value_list[:len(self.fields_info)]
        cursor = self.conn.cursor()
        sql = "INSERT INTO %s %s VALUES( %s )" % (
            self.name,
            "(" + ",".join(field_name) + ")" if is_field_name else "",
            ",".join(["?"] * len(field_value_list)))
        # print sql
        cursor.execute(sql, field_value_list)
        self.conn.commit()

    def add_rows(self, rows_list, with_head=True):
        cursor = self.conn.cursor()
        for row_list in rows_list:
            # print row_list
            # fieldList = [self.__keyValue(f) for f in row_list]
            # field_value_list = [scale_encoding_converter.conv_scale_to_pc(self.__keyValue(f)) for f in row_list]
            field_value_list = []
            for f in row_list:
                fv = scale_encoding_converter.conv_scale_to_pc(self.__keyValue(f))
                if isinstance(fv, str):
                    fv = unicode(fv)
                field_value_list.append(fv)

            field_name = [self.__keyName(f) for f in row_list]
            # 如果没有字段名时，需要和表声明的长度比较
            if not with_head and len(field_value_list) != len(self.fields_info):
                field_value_list = field_value_list[:len(self.fields_info)]
            sql = "INSERT INTO %s %s VALUES( %s )" % (
                self.name,
                "(" + ",".join(field_name) + ")" if with_head else "",
                ",".join(["?"] * len(row_list))
            )
            # print sql
            cursor.execute(sql, field_value_list)
        self.conn.commit()

    def to_csv_mem(self, title=False, encoding=sys.getdefaultencoding()):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM %s %s" % (self.name, "ORDER BY " + ",".join(self.fieldKeys) if self.fieldKeys else "")
        cursor.execute(sql)
        field_names = [f["name"] for f in self.fields_info]
        data_to_return = ""
        if title:
            data_to_return += ",".join(field_names) + "\r\n"
        for row in cursor:
            cells = [unicode(cell).encode(encoding) for cell in row]
            data_to_return += ",".join(cells) + "\r\n"

        return data_to_return

    def to_csv(self, file_path, title=False, encoding=sys.getdefaultencoding()):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM %s %s" % (self.name, "ORDER BY " + ",".join(self.fieldKeys) if self.fieldKeys else "")
        # 		print "begin:", time.time() #testonly
        # 		beg = time.time() #testonly
        cursor.execute(sql)
        # 		print "1 elipsed:", time.time() - beg #testonly

        # 		beg = time.time() #testonly
        with open(file_path, "wb") as fp:
            field_names = [f["name"] for f in self.fields_info]
            if title:
                fp.write(",".join(field_names) + "\r\n")
            for row in cursor:
                # for cell in row: print cell
                # cells = [unicode(cell).encode(encoding) for cell in row]
                # cells = [scale_encoding_converter.conv_pc_to_scale(unicode(cell).encode(encoding)) for cell in row]
                cells = [scale_encoding_converter.conv_pc_to_scale(str(cell)) for cell in row]
                # cells = []
                # indx = 0
                # for cell in row:
                #     print "index:", indx, "cell:", cell
                #     indx += 1
                #     cell_unicode = unicode(cell)
                #     print "cell_unicode:", cell_unicode
                #     cell_encode = cell_unicode.encode(encoding)
                #     print "cell_encode:", cell_encode
                #     cell_scale_data = scale_encoding_converter.conv_pc_to_scale(cell_encode)
                #     print "cell_scale_data:", cell_scale_data
                #     cells.append(cell_scale_data)

                fp.write(",".join(cells) + "\r\n")

                # 		print "2 elipsed:", time.time() - beg #testonly

    def to_json(self, file_path, encoding=sys.getdefaultencoding()):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM %s %s" % (self.name, "ORDER BY " + ",".join(self.fieldKeys) if self.fieldKeys else "")
        cursor.execute(sql)
        # names = map(lambda x: {x[0]: x[1]}, cursor.description)
        names = [(index, desc[0]) for index, desc in enumerate(cursor.description)]
        # print names
        root = []
        for row in cursor:
            node = {}
            for name in names:
                node[name[1]] = unicode(row[name[1]]).encode(encoding)
            root.append(node)

        with open(file_path, "w") as fp:
            fp.write(json.dumps(root, indent=4, ensure_ascii=False))

    def from_json(self, file_path):
        try:
            with open(file_path, "r") as fp:
                json_data = json.load(fp)
            if json_data:
                rs = [[{k: val} for k, val in row.items()] for row in json_data]
                self.add_rows(rs)
            return True
        except Exception, e:
            common.common.log_err(traceback.format_exc())
            return False

    def from_csv_cb(self, row_line, row_data):
        row_dic = {}
        for indx, data in enumerate(row_data):
            row_dic[indx + 1] = [data]
        self.add_row(row_dic, False)

    def from_csv(self, file_path, with_head=False):
        if with_head:
            common.csvreader.SmCsvReader().read_all_lines(
                file_path,
                lambda x: self.add_rows(x, with_head))
        else:
            common.csvreader.SmCsvReader().read_line_by_line(
                file_path,
                self.from_csv_cb,
                head=with_head)

    def get_all_data(self, encoding=sys.getdefaultencoding()):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM %s %s" % (self.name, "ORDER BY " + ",".join(self.fieldKeys) if self.fieldKeys else "")
        cursor.execute(sql)
        names = [(index, desc[0]) for index, desc in enumerate(cursor.description)]
        rows = []
        for row in cursor:
            # cells = [ cell for cell in row ]
            dic1 = {}
            dic2 = {}
            for name in names:
                val = [row[name[0]]]
                dic1[name[1]] = dic2[int(str(name[0] + 1))] = val
            dic3 = dic1.copy()
            dic3.update(dic2)
            rows.append(dic3)
        return rows

    def find_records(self, sql, field_list):
        cursor = self.conn.cursor()
        # print "sql:", sql
        # print "field_list:", field_list
        cursor.execute(sql, field_list)
        names = [(index, desc[0]) for index, desc in enumerate(cursor.description)]
        rows = []
        for row in cursor:
            # yield [ (name[1], row[name[0]]) for name in names ]
            # cells = []
            dic1 = {}
            dic2 = {}
            for name in names:
                val = [row[name[0]]]
                dic1[name[1]] = dic2[str(name[0] + 1)] = val
            # cells.append( {name[1]: val} )
            # cells.append( {str(name[0] + 1): val} )
            dic3 = dic1.copy()
            dic3.update(dic2)
            rows.append(dic3)
        # rows.append(cells)
        return rows

    def get_max_value_of_key(self, strKeyField=""):
        if not self.fieldKeys: return 0
        if not strKeyField:
            strKeyField = self.fieldKeys[0]

        sql = "SELECT IFNULL(MAX(%s), 0) FROM %s" % (strKeyField, self.name)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchone()[0]

    def get_free_value_of_key(self):
        if not self.fieldKeys: return 1
        sql = '''
				SELECT (CASE WHEN EXISTS(SELECT 1 FROM %s WHERE %s=1) THEN MIN(%s+1) ELSE 1 END) 
				FROM %s
				WHERE %s not in(SELECT %s-1 FROM %s)	
			''' % (
            self.name,
            self.fieldKeys[0],
            self.fieldKeys[0],
            self.name,
            self.fieldKeys[0],
            self.fieldKeys[0],
            self.name)

        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchone()[0]
