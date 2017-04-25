# encoding=gbk
#

import sys


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

enc_conversion_table = {
    "default": BaseEncConverter("gbk"),
    "Mongolia": MongoliaEncConverter("cp1251")
}

glob_converter = None


def get_conv_table():
    global glob_converter
    if not glob_converter:
        glob_converter = enc_conversion_table.get(sys.getdefaultencoding(), BaseEncConverter("gbk"))
    return glob_converter


def conv_pc_to_scale(data):
    return get_conv_table().pc_to_scale(data)


def conv_scale_to_pc(data):
    return get_conv_table().scale_to_pc(data)
