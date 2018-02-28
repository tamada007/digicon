# -*- mode: python -*-

block_cipher = None


a = Analysis(['SelectScale.py'],
             pathex=[
                'D:\\Projects\\python\\digicon',
                'D:\\Projects\\python\\digicon\\wintool'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('as.png', 'as.png', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='digitool',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='as.ico')
