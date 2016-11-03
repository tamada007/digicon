
from distutils.core import setup
#import glob
import py2exe

setup(
	console=["__main__.py", "base"],
# 	packages=["base"],
	#options={ "py2exe":{"bundle_files": 1} }
)

