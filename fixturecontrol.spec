# -*- mode: python -*-

block_cipher = None


a = Analysis(['fixturecontrol.py'],
             pathex=['E:\\Python\\day41-治具录入管控查询'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          [],
          exclude_binaries=True,
          name='fixturecontrol',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , version='file_version_info.txt', icon='ball.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='fixturecontrol')
