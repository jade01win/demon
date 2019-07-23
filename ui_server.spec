# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['ui_server.py'],
             pathex=['C:\\Users\\leon\\Desktop\\python\\demon-master'],
             binaries=[],
             datas=[('./icon.png', 'icon.png'), ('./logo.png', 'logo.png')],
             hiddenimports=['tkinter', 'tkinter.ttk', 'ttkthemes'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ui_server',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='icon.ico')
