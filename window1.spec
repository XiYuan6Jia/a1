# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['window1.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/image/b2.png', 'assets/image'),
        ('assets/image/b1.png', 'assets/image'),
        ('assets/image/Idle_lth.gif', 'assets/image'),
        ('assets/image/Idle_lth-export.gif', 'assets/image'),
        ('assets/audio/Toby Fox - sans_.wav', 'assets/audio')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='window1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
