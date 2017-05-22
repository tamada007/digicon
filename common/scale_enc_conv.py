# encoding=gbk
#

import sys
import threading

import platform

def if_this_is_windows():
	return platform.system() == "Windows"

if if_this_is_windows():
	import comtypes
	from comtypes.client import CreateObject

glob_converter = None


class BaseEncConverter(object):
    def __init__(self, enc):
        self.encoding = enc

    def pc_to_scale(self, pc_data):
        # return unicode(pc_data).encode(self.encoding)
        return pc_data

    def scale_to_pc(self, scale_data):
        # return scale_data.decode(self.encoding)
        return scale_data


class MongoliaEncConverter(BaseEncConverter):
    def pc_to_scale(self, pc_data):
        return super(MongoliaEncConverter, self).pc_to_scale(pc_data)

    def scale_to_pc(self, scale_data):
        return super(MongoliaEncConverter, self).scale_to_pc(scale_data)


class SaudiArabicConverter(BaseEncConverter):
    def __init__(self, enc):
        super(SaudiArabicConverter, self).__init__(enc)
        # self.dll = cli.CreateObject("ArbCharacterConvert.ArabicCharConvert")
        # self.dll = CreateObject("ArbCharacterConvert.ArabicCharConvert")
        # print "init's:", threading.currentThread().ident

    @staticmethod
    def get_comdll():
        if if_this_is_windows():
            threading_dll = threading.local()
            if not hasattr(threading_dll, 'ArabicDll'):
                comtypes.CoInitialize()
                threading_dll.ArabicDll = CreateObject("ArbCharacterConvert.ArabicCharConvert")
            return threading_dll.ArabicDll
        else:
            return None
		#return None


    def pc_to_scale(self, pc_data):
        # import comtypes.client as cli
        # from comtypes import client
        # dll = client.CreateObject("ArbCharacterConvert.ArabicCharConvert")
        # print "pctoscale's:", threading.currentThread().ident
        # from comtypes.client import CreateObject
        # comtypes.CoInitialize()
        # dll = CreateObject("ArbCharacterConvert.ArabicCharConvert")
        # result = dll.Uni2ArabSys(pc_data).encode(self.encoding)
        # comtypes.CoUninitialize()
        # return result
        dll = SaudiArabicConverter.get_comdll()
        return dll.Uni2ArabSys(pc_data).encode(self.encoding)

    def scale_to_pc(self, scale_data):
        # import comtypes.client as cli
        # from comtypes import client
        # from comtypes.client import CreateObject
        # dll = client.CreateObject("ArbCharacterConvert.ArabicCharConvert")
        # comtypes.CoInitialize()
        # dll = CreateObject("ArbCharacterConvert.ArabicCharConvert")
        # comtypes.CoUninitialize()
        # return result
        dll = SaudiArabicConverter.get_comdll()
        return dll.ArabSys2Uni(scale_data).encode(self.encoding)


enc_conversion_table = {
    "gbk": lambda: BaseEncConverter("gbk"),
    "cp1251": lambda: MongoliaEncConverter("cp1251"),
    "cp1256": lambda: SaudiArabicConverter("cp1256"),
}


def get_conv_table():
    # global glob_converter
    # if not glob_converter:
    #     glob_converter = enc_conversion_table.get(sys.getdefaultencoding(), BaseEncConverter("gbk"))
    # return glob_converter
    # print "getting!"

    # print "default encoding:", "|" + sys.getdefaultencoding() + "|"
    callback_converter = enc_conversion_table.get(sys.getdefaultencoding())
    # print "c p 2,", callback_converter
    if not callback_converter:
        # print "c p 3"
        return BaseEncConverter("gbk")
    # print "c p 4"
    return callback_converter()


def conv_pc_to_scale(data):
    return get_conv_table().pc_to_scale(data)


def conv_scale_to_pc(data):
    return get_conv_table().scale_to_pc(data)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('cp1256')
    print conv_pc_to_scale('p1')
    print conv_pc_to_scale('p2')
    print conv_pc_to_scale('p3')
    #dll = cli.CreateObject("ArbCharacterConvert.ArabicCharConvert")
    #print dll.Uni2ArabSys('abc')
