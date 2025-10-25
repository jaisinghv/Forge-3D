# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['text_to_3d_gui.py'],
    pathex=[],
    binaries=[('libgeometry.so', '.')],
    datas=[('yolov8n.pt', '.')],
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
    name='TextTo3DGenerator',
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
    name='TextTo3DGenerator',
)
app = BUNDLE(
    coll,
    name='TextTo3DGenerator.app',
    icon=None,
    bundle_identifier=None,
)
