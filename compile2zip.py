#encoding=gbk

import zipfile, os
besteamzip=zipfile.PyZipFile("digicon.zip" ,"w", zipfile.ZIP_DEFLATED)
#����һЩ�����õ�.py�ű�
#for filename in ("__main__.py", "Go120.py"): 
for filename in ("__main__.py",): 
    besteamzip.writepy(filename)
for dirname in os.listdir("."):
    initfile=os.path.join(dirname, "__init__.py")
    if os.path.isdir(dirname) and os.path.exists(initfile):
        besteamzip.writepy(dirname)
besteamzip.close()

