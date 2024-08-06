# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('threshold.py', '.'), ('main_page.py', '.'), ('second_page.py', '.'), ('small_bottle_threshold.csv', '.'), ('bottle_threshold.csv', '.'), ('can_threshold.csv', '.'), ('can_threshold.csv', '.'), ('runs/detect/train16/weights/best.pt', 'runs/detect/train16/weights'), ('.venv/Lib/site-packages/ultralytics/cfg/default.yaml', 'ultralytics/cfg')],
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
    name='main',
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
)
