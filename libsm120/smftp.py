#encoding:gbk
import os
# import codecs
# import re
from ftplib import FTP
import socket
from common import common


class smftp:
	#def __init__(self, hostaddr, username, password, remotedir, port=21):
	def __init__(self, hostaddr, username, password, port=21):
		self.hostaddr = hostaddr
		self.username = username
		self.password = password
		self.port     = port
		self.ftp      = FTP()
		self.file_list = []
		# self.ftp.set_debuglevel(2)
	def __del__(self):
		self.ftp.close()
		# self.ftp.set_debuglevel(0)
		
	def login(self):
		ftp = self.ftp
		connected = False
		try: 
			timeout = 20
			socket.setdefaulttimeout(timeout)
			#ftp.set_pasv(True)
			ftp.set_pasv(False)
			#print u'开始连接到 %s' %(self.hostaddr)
			ftp.connect(self.hostaddr, self.port)
			#print u'成功连接到 %s' %(self.hostaddr)
			#print u'开始登录到 %s' %(self.hostaddr)
			ftp.login(self.username, self.password)
			#print u'成功登录到 %s' %(self.hostaddr)
			#debug_print(ftp.getwelcome())
			connected = True
		except Exception:
			common.log_err( 'Connecting Or Login Failed on %s' % self.hostaddr )

		return connected
			
	#	try:
			#ftp.cwd(self.remotedir)
			#pass
		#except(Exception):
			#common.log_err( '切换目录失败' )

	def is_same_size(self, localfile, remotefile):
		return 0
		pass
#		try:
#			remotefile_size = self.ftp.size(remotefile)
#		except:
#			remotefile_size = -1
#		try:
#			localfile_size = os.path.getsize(localfile)
#		except:
#			localfile_size = -1
#		debug_print('localfile_size:%d  remotefile_size:%d' %(localfile_size, remotefile_size),)
#		if remotefile_size == localfile_size:
#		 	return 1
#		else:
#			return 0
	def download_file(self, localfile, remotefile):
		#if self.is_same_size(localfile, remotefile):
		# 	common.log_info('%s 文件大小相同，无需下载' %localfile)
		# 	return
		#else:
		#	common.log_info('>>>>>>>>>>>>下载文件 %s <<<<<<<<<<<<<<' %localfile)
		#return
		file_handler = open(localfile, 'wb')
		self.ftp.retrbinary(u'RETR %s'%(remotefile), file_handler.write)
		file_handler.close()

	def listFiles(self):
		self.file_list = []
		self.ftp.dir(self.get_file_list)
		remotenames = []
		for entry in self.file_list:
			remotenames.append( entry[1] )
		#remotenames = self.file_list
		return remotenames

	def download_files(self, localdir='./', remotedir='./'):
		try:
			#self.ftp.cwd(remotedir)
			pass
		except:
			#debug_print(u'目录%s不存在，继续...' %remotedir)
			return
		if not os.path.isdir(localdir):
			os.makedirs(localdir)
		common.log_info('切换至目录 %s' %self.ftp.pwd())
		self.file_list = []
		self.ftp.dir(self.get_file_list)
		remotenames = self.file_list
		#print(remotenames)
		#return
		for item in remotenames:
			filetype = item[0]
			filename = item[1]
			local = os.path.join(localdir, filename)
			if filetype == 'd':
				self.download_files(local, filename)
			elif filetype == '-':
				self.download_file(local, filename)
		self.ftp.cwd('..')
		common.log_info('返回上层目录 %s' %self.ftp.pwd())

	def delete_file(self, remotefile):
		self.ftp.delete(remotefile)
		#common.log_info('已删除: %s' %remotefile)

	def upload_file(self, localfile, remotefile):
		if not os.path.isfile(localfile):
			return
		#if self.is_same_size(localfile, remotefile):
		 	#debug_print(u'跳过[相等]: %s' %localfile)
		 	#return
		file_handler = open(localfile, 'rb')
		self.ftp.storbinary('STOR %s' %remotefile, file_handler)
		file_handler.close()
		#common.log_info('已传送: %s' %localfile)
	def upload_files(self, localdir='./', remotedir = './'):
		if not os.path.isdir(localdir):
			return
		localnames = os.listdir(localdir)
		#self.ftp.cwd(remotedir)
		for item in localnames:
			src = os.path.join(localdir, item)
			if os.path.isdir(src):
				try:
					self.ftp.mkd(item)
				except:
					common.log_info('目录已存在 %s' %item)
				self.upload_files(src, item)
			else:
				self.upload_file(src, item)
		self.ftp.cwd('..')

	def get_file_list(self, line):
		ret_arr = []
		#print line
		file_arr = self.get_filename(line)
		if file_arr[1] not in ['.', '..']:
			self.file_list.append(file_arr)
			
	def get_filename(self, line):
		pos = line.rfind(':')
		while(line[pos] != ' '):
			pos += 1
		while(line[pos] == ' '):
			pos += 1
		file_arr = [line[0], line[pos:]]
		return file_arr

def debug_print(s):
	#print s.encode('utf-8')
	#print s.encode(sys.getdefaultencoding())
	pass

