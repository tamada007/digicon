# encoding=gbk
import re
import socket
import traceback

from common import common


class ReqData:
    Read_File = 1
    Read_Record = 2
    Write_File = 3
    Del_Record = 4
    Del_File = 5

    def create_request_data(self, method, file_no, record_no):
        return {
            ReqData.Read_File: "F7%02x%08d" % (file_no, record_no),
            ReqData.Write_File: "F1%02x" % file_no,
            ReqData.Read_Record: "F0%02x%08d" % (file_no, record_no),
            ReqData.Del_File: "F2%02x" % file_no,
            ReqData.Del_Record: "F3%02x%08d" % (file_no, record_no),
        }.get(method, "")


class TwsException(Exception):
    pass


class smtws:
    def __init__(self, hostname):
        #  		socket.setdefaulttimeout(5)
        socket.setdefaulttimeout(15)
        self.hostaddr = socket.gethostbyname(hostname)
        self.hostname = hostname
        self.port = self.get_port()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def get_port(self):
        p = re.compile(r"(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})")
        m = p.match(self.hostaddr)
        if m:
            return 2000 + int(m.group(4))
        raise TwsException("Port Error")

    def check_connection(self):
        try:
            socket.setdefaulttimeout(10)
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.hostaddr, self.port))
            conn.close()
            return True
        except socket.error, e:
            return False

    def delete_file(self, file_no):
        request_data = ReqData().create_request_data(ReqData.Del_File, file_no, 0).decode("hex")
        try:
            socket.setdefaulttimeout(10)
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.hostaddr, self.port))
            conn.send(request_data)
            ack_data = conn.recv(1)
            if not ack_data: raise TwsException("No Ack")
            ack = ord(ack_data[0])
            if ack == 0xE1: raise TwsException("Write Error")
            if ack == 0xE2: raise TwsException("No Data")
            if ack != 0x06: raise TwsException("Unknown Error")
        except socket.error, e:
            # print e
            common.log_err(self.hostname + ' - ' + str(e))
            return False
        except TwsException, e:
            # print e
            common.log_err(self.hostname + ' - ' + str(e))
            return False
        else:
            return True

    def delete_records(self, file_no, records_no):
        try:
            socket.setdefaulttimeout(10)
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.hostaddr, self.port))
            for record_no in records_no:
                # print record_no
                request_data = ReqData().create_request_data(ReqData.Del_Record, file_no, record_no).decode("hex")
                conn.send(request_data)
                ack_data = conn.recv(1)
                if not ack_data: raise TwsException("No Ack")
                ack = ord(ack_data[0])
                try:
                    if ack == 0xE1: raise TwsException("Write Error")
                    if ack == 0xE2: raise TwsException("No Data")
                    if ack != 0x06: raise TwsException("Unknown Error")
                except TwsException, e:
                    # print e
                    # traceback.print_exc()
                    common.log_err(self.hostname + ' - ' + str(e))
        except socket.error, e:
            # traceback.print_exc()
            common.log_err(self.hostname + ' - ' + str(e))
            return False
        # except TwsException, e:
        # print e
        # return False
        else:
            return True

    def download_file(self, file_no):
        file_name = "%s.%02x.dat" % (self.hostname, file_no)
        try:
            socket.setdefaulttimeout(10)
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.hostaddr, self.port))
            record_no = 0
            with open(file_name, "w") as fp:
                while True:
                    request_data = ReqData().create_request_data(ReqData.Read_File, file_no, record_no)
                    request_data = request_data.decode("hex")
                    conn.send(request_data)
                    received_data = conn.recv(1460)
                    received_length = len(received_data)
                    if received_length == 1:
                        ack = ord(received_data[0])
                        if ack == 0xE0:
                            raise TwsException("Error on Reading")
                        if ack == 0xE2:
                            break

                    else:
                        received_data = received_data.encode("hex").upper()
                        # 计算长度
                        real_size = int(received_data[8:12], 16)
                        while real_size > received_length:
                            if received_length % 1460 == 0:
                                conn.send('\x06')

                            received_data_plus = conn.recv(1460)
                            if not received_data_plus: break
                            received_data_plus_length = len(received_data_plus)
                            received_data_plus = received_data_plus.encode("hex").upper()
                            received_length += received_data_plus_length
                            received_data += received_data_plus
                        #
                        try:
                            record_no = int(received_data[:8])
                        except Exception, e:
                            record_no = int(received_data[:8], 16)
                        fp.write(received_data + "\r\n")

        except TwsException, e:
            # print e
            common.log_err(self.hostname + ' - ' + str(e))
            return ""
        except socket.error, e:
            common.log_err(self.hostname + ' - ' + str(e))
            # print e
            return ""
        else:
            return file_name

    def upload_file(self, file_no, file_name):
        request_data = ReqData().create_request_data(ReqData.Write_File, file_no, 0)
        # tmpline = ""
        try:
            socket.setdefaulttimeout(10)
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.hostaddr, self.port))
            with open(file_name, "r") as fp:
                for line in fp:
                    data_send = request_data + line.rstrip()
                    data_send = data_send.decode("hex")
                    conn.send(data_send)
                    ack_data = conn.recv(1)
                    if not ack_data:
                        raise TwsException("No Ack")
                    ack = ord(ack_data[0])
                    if ack == 0xE1: raise TwsException("Write Error")
                    if ack == 0xE3: raise TwsException("No Free Space")
                    if ack == 0xE2: raise TwsException("No Data")
                    if ack != 0x06: raise TwsException("Unknown Error")

        except socket.error, e:
            common.log_err(self.hostname + ' - ' + str(e))
            # print "socket error"
            # 			traceback.print_exc()
            # print tmpline
            # print e

            return False
        except TwsException, e:
            # print e
            common.log_err(self.hostname + ' - ' + str(e))
            return False
        except Exception, e:
            # print e
            common.log_err(self.hostname + ' - ' + str(e))
            return False
        else:
            return True

    def upload_master(self, master):
        file_path = "%s.%s.dat" % (self.hostname, hex(master.file_no)[2:])
        master.to_dat(file_path)
        return self.upload_file(master.file_no, file_path)

    def download_master(self, master):
        # 		file_path = "%s.%s.dat" % (self.hostname, hex(master.file_no)[2:])
        file_path = self.download_file(master.file_no)
        if file_path:
            return master.add_rows(file_path)
        return False

    def delete_master(self, master):
        # all_keys = master.get_all_keys()
        # return self.delete_records(master.file_no, all_keys)
        return self.delete_file(master.file_no)
