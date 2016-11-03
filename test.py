import sys

reload(sys)
sys.setdefaultencoding('gbk')

from common.converter import ScalesConverter

ScalesConverter().easyImportMaster('192.168.68.125:sm110', 'plu_import.csv', 'plu_template.json')
