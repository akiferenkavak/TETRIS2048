# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Tetris_2048.py'],
    pathex=[],
    binaries=[],
    datas=[('images', 'images'), ('lib', 'lib'), ('menu_images', 'menu_images'), ('sounds', 'sounds'), ('win_lose_images', 'win_lose_images')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Tetris_2048',
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
    icon=['icon\\tetris2048.ico'],
)
