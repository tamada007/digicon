import time, traceback

from common import common
from smftp import smftp
# import master
import os

import socket

class DigiSm120(object):
    def __init__(self, ip, port=21, usr='admin', pwd='admin'):
        self.ip = ip
        self.port = port
        self.usr = usr
        self.pwd = pwd
        self.ftp = smftp(self.ip, self.usr, self.pwd)
        self.connected = False

    # 		self.connect()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        try:
            # self.ftp.close()
            del self.ftp
        except:
            pass

        self.connected = False

    def check_connection(self):
        try:
            socket.setdefaulttimeout(10)
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.ip, 21))
            conn.close()
            return True
        except socket.error, e:
            return False

    def connect(self):
        self.connected = self.ftp.login()

    def send_by_name(self, name, data):
        try:
            local_file = self.ip + "_" + name
            local_file = os.path.join(common.get_current_directory(), local_file)
            remote_file = name
            with open(local_file, "wb") as fp:
                fp.write(data)
            # ftp = smftp(self.ip, self.usr, self.pwd)
            # try:
            # ftp.login()
            self.ftp.upload_file(local_file, remote_file)
            # time.sleep(0.3)
            return True
        # except Exception as e:
        # print e
        except Exception, e:
            common.log_err(traceback.format_exc())
            return False

    def dele_by_name(self, name):
        try:
            remote_file = name
            self.ftp.delete_file(remote_file)
            return True
        except Exception, e:
            common.log_err(traceback.format_exc())
            return False

    def get_scale_file_name_entire(self, master):
        return self.ip + "_" + master.scale_file_name

    def create_csv(self, master):
        try:
            # local_file = self.ip + "_" + master.scale_file_name
            local_file = self.get_scale_file_name_entire(master)
            local_file = os.path.join(common.get_current_directory(), local_file)
            master.to_csv(local_file)
            return local_file

        except Exception, e:
            common.log_err(traceback.format_exc())
            return ""

    def send_file(self, master, created_file):
        try:
            remote_file = master.scale_file_name
            self.ftp.upload_file(created_file, remote_file)
            return True

        except Exception, e:
            common.log_err(traceback.format_exc())
            return False

    # def send_file(self, master, in_file_name):
    #     try:
    #         remote_file = master.scale_file_name
    #         local_file = in_file_name
    #         self.ftp.upload_file(local_file, remote_file)
    #         return True
    #     except Exception, e:
    #         common.log_err(traceback.format_exc())
    #         return False

    def send(self, master):
        try:
            # local_file = self.ip + "_" + master.scale_file_name
            local_file = self.get_scale_file_name_entire(master)
            remote_file = master.scale_file_name
            master.to_csv(local_file)
            # ftp = smftp(self.ip, self.usr, self.pwd)
            # try:
            # ftp.login()
            self.ftp.upload_file(local_file, remote_file)
            # time.sleep(0.3)
            return True
        # except Exception as e:
        # print e
        except Exception, e:
            common.log_err(traceback.format_exc())
            return False

    def recv(self, master):
        try:
            # local_file = self.ip + "_" + master.scale_file_name
            local_file = self.get_scale_file_name_entire(master)
            remote_file = master.scale_file_name
            # ftp = smftp(self.ip, self.usr, self.pwd)
            # ftp.login()
            self.ftp.download_file(local_file, remote_file)
            # time.sleep(0.1)
            master.from_csv(local_file, with_head=False)
            return True
        except Exception, e:
            common.log_err(traceback.format_exc())
            return False

    def recv_file(self, master):
        try:
            # local_file = self.ip + "_" + master.scale_file_name
            local_file = self.get_scale_file_name_entire(master)
            remote_file = master.scale_file_name
            self.ftp.download_file(local_file, remote_file)
            return local_file
        except Exception, e:
            common.log_err(traceback.format_exc())
            return ""

    def dele(self, master):
        try:
            # ftp = smftp(self.ip, self.usr, self.pwd)
            # ftp.login()
            self.ftp.delete_file(master.scale_file_name)
            # time.sleep(0.3)
            return True
        except Exception, e:
            common.log_err(traceback.format_exc())
            return False
