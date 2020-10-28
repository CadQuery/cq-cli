# -*- mode: python ; coding: utf-8 -*-
import sys, site, os
import glob
from path import Path

# Whether we are running in onefile or dir mode
onefile_mode = True
if len(sys.argv) == 3:
    if sys.argv[2] == 'onefile':
        onefile_mode = True
    elif sys.argv[2] == 'dir':
        onefile_mode = False

block_cipher = None
if sys.platform == 'linux':
    occt_dir = Path(sys.prefix) + os.path.sep + 'share' + os.path.sep + 'opencascade'
    ocp_path = (os.path.join(HOMEPATH, 'OCP.cpython-38-x86_64-linux-gnu.so'), '.')
    lib_dir = (os.path.join(Path(sys.prefix), 'lib'), '.')
elif sys.platform == 'darwin':
    occt_dir = Path(sys.prefix) + os.path.sep + 'Library' + os.path.sep + 'share' + os.path.sep + 'opencascade'
    ocp_path = (os.path.join(HOMEPATH, 'OCP.cpython-38-darwin.so'), '.')
    lib_dir = (os.path.join(Path(sys.prefix), 'lib'), '.')
elif sys.platform == 'win32':
    occt_dir = os.path.join(Path(sys.prefix), 'Library', 'share', 'opencascade')
    ocp_path = (os.path.join(HOMEPATH, 'OCP.cp38-win_amd64.pyd'), '.')
    lib_dir = (os.path.join(Path(sys.prefix), 'Lib'), '.')

# Dynamically find all the modules in the cqcodecs directory
hidden_imports = []
file_list = glob.glob('.' + os.path.sep + 'cqcodecs' + os.path.sep + 'cq_codec_*.py')
for file_path in file_list:
    file_name = file_path.split(os.path.sep)[-1]
    module_name = file_name.replace(".py", "")
    hidden_imports.append("cqcodecs." + module_name)
hidden_imports.append('OCP')

a = Analysis(['cq-cli.py'],
             pathex=['.'],
             binaries=[
                 ocp_path
             ],
             datas=[
                 lib_dir,
                 (os.path.join(os.path.dirname(os.path.realpath('__file__')), 'cqcodecs'), 'cqcodecs')
             ],
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

# Select between onefile and dir mode executables
if onefile_mode:
    exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            [],
            name='cq-cli',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            upx_exclude=[],
            runtime_tmpdir=None,
            console=True )
else:
    exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='cq-cli',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )

exclude = ('libGL','libEGL','libbsd')
a.binaries = TOC([x for x in a.binaries if not x[0].startswith(exclude)])

if not onefile_mode:
    coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='cq-cli')
