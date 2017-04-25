# encoding=gbk
# import logging
import logging.handlers
import sqlite3
import json
import sys
import threading

# import const

using_memory_db = True

# 全局内存数据库
#############################
g_memConn = {}
#############################

g_current_thread_data = threading.local()

# csv导入是否有标题行
title_onoff = False


def get_title_onoff():
    return title_onoff


def set_title_onoff(v):
    title_onoff = v


def slurp(file_path):
    with open(file_path) as fp:
        return fp.read()


def close_all_sqlite_db():
    if hasattr(g_current_thread_data, "Database") and isinstance(g_current_thread_data.Database, dict):
        for key in g_current_thread_data.Database:
            # print "key1:", key
            try:
                g_current_thread_data.Database[key].close()
            except:
                pass
        g_current_thread_data.Database.clear()

    for key in g_memConn:
        # print "key2:", key
        try:
            g_memConn[key].close()
        except:
            pass
    g_memConn.clear()


def open_sqlite_db(file_name, use_mem_db=None):
    if not hasattr(g_current_thread_data, "Database"):
        g_current_thread_data.Database = {}

    if g_current_thread_data.Database.has_key(file_name):
        return g_current_thread_data.Database.get(file_name)

    use_memory_db = using_memory_db
    if not use_mem_db is None:
        use_memory_db = use_mem_db

    if not use_memory_db:
        conn = sqlite3.connect(file_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row

        g_current_thread_data.Database[file_name] = conn
        return conn
    else:
        conn = g_current_thread_data.Database[file_name] = open_mem_db(file_name)
        # return open_mem_db(file_name)
        return conn


def open_mem_db(name):
    if not g_memConn.has_key(name):
        g_memConn[name] = sqlite3.connect(":memory:", check_same_thread=False)
        g_memConn[name].row_factory = sqlite3.Row

    return g_memConn[name]


def get_json_from_file(json_file_path, encoding=sys.getdefaultencoding()):
    with open(json_file_path, "r") as fp:
        return json.load(fp, encoding)


def get_json_from_string(text, encoding=sys.getdefaultencoding()):
    return json.loads(text, encoding=encoding)


def dump_json_to_string(obj, encoding=sys.getdefaultencoding(), indent=4):
    return json.dumps(obj, indent=indent, ensure_ascii=False, encoding=encoding)


def save_json_to_file(json_file_path, obj, encoding=sys.getdefaultencoding()):
    with open(json_file_path, "w") as fp:
        fp.write(json.dumps(obj, indent=4, ensure_ascii=False, encoding=encoding))


def clear_all_tables(db_name):
    conn = open_sqlite_db(db_name)
    cursor = conn.cursor()

    for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        sql = "DROP TABLE %s" % row[0]
        cursor.execute(sql)

    conn.commit()


def log2_init():
    import os
    os.remove('digicon.log')


def log_init():
    # logging.basicConfig(level=logging.DEBUG,
    # 				format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    # 				# datefmt='%a, %d %b %Y %H:%M:%S',
    #               datefmt='%Y-%m-%d %H:%M:%S',
    # 				# filename='myapp.log',
    #               filemode='a')

    logger_detail = logging.getLogger('detail')
    logger_result = logging.getLogger('result')

    logger_detail.setLevel(logging.DEBUG)
    logger_result.setLevel(logging.DEBUG)

    # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    # console = logging.StreamHandler()
    # console.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # console.setFormatter(formatter)
    # logging.getLogger('').addHandler(console)

    # formatter = logging.Formatter('%(asctime)s : %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
    formatter = logging.Formatter('%(asctime)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # detail log
    detail_handler = \
        logging.handlers.RotatingFileHandler('digicon_detail.log', mode='a', maxBytes=5 * 1024 * 1024, backupCount=5)
    # detail_handler.setLevel(logging.DEBUG)
    detail_handler.setFormatter(formatter)
    logger_detail.addHandler(detail_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # console_handler.setLevel(logging.DEBUG)
    logger_detail.addHandler(console_handler)

    # result log
    # try:
    #     with open('digicon_result.log', 'w'): pass
    # except:
    #     pass

    # Rthandler = \
    #     logging.handlers.RotatingFileHandler('digicon_result.log', mode='w', maxBytes=5 * 1024 * 1024, backupCount=5)
    # Rthandler.setLevel(logging.DEBUG)

    # file handler
    result_handler = logging.FileHandler("digicon_result.log", mode="w")
    # result_handler.setLevel(logging.DEBUG)
    result_handler.setFormatter(formatter)
    logger_result.addHandler(result_handler)
    # formatter = logging.Formatter('%(asctime)s : %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
    # formatter = logging.Formatter('%(asctime)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    # Rthandler.setFormatter(formatter)


def log2_info(text):
    logging.getLogger('result').info(text)


def log2_err(text):
    logging.getLogger('result').error(text)


def log_info(text):
    logging.getLogger('detail').info(text)


def log_err(text):
    logging.getLogger('detail').error(text)


def int2hex(intVal, length=2):
    return hex(intVal)[2:].upper().rjust(length, '0')


def hex2int(strHex):
    return int(strHex, 16)


def bin2int(strBin):
    return int(strBin, 2)


def bin2hex(strBin):
    return int2hex(bin2int(strBin))
