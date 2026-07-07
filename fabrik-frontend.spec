# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/fabrik_frontend/__main__.py'],
    pathex=[],
    binaries=[('/home/rouaa/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/libtcl9.0.so', '.'), ('/home/rouaa/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/libtcl9tk9.0.so', '.')],
    datas=[],
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
    [],
    exclude_binaries=True,
    name='fabrik-frontend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='fabrik-frontend',
)
