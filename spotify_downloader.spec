# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_gui.pyw'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('lib', 'lib'),
        ('interface', 'interface'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'yt_dlp',
        'requests',
        'colorama',
        'urllib3',
        'interface.gui',
        'interface.ui',
        'lib.spotify_lib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['gradio'],  # Exclude gradio as it's not needed for GUI
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
    name='SpotifyDownloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
