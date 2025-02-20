# -*- mode: python ; coding: utf-8 -*-

# client.spec
# PyInstaller-Spezifikationsdatei für das Bundling von "client.py"

# Falls du Verschlüsselung der Bytecode-Dateien möchtest, kannst du PyInstaller
# mit einem AES-Schlüssel versehen. Ansonsten lass block_cipher einfach auf None.
block_cipher = None

added_files = [
    ('assets/LoginBackground/*.png', 'assets/LoginBackground'),
    ('assets/Kampf_Background/*.png', 'assets/Kampf_Background'),
    ('assets/titel_Hauptmenu/*.png', 'assets/titel_Hauptmenu'),
    ('assets/buttons/*.png', 'assets/buttons'),
    ('music/*.mp3', 'music'),
    ('LoginScreen.py', '.'),
    ('buttons.py', '.'),
    ('utils.py', '.'),
    ('registration_screen.py', '.'),
    ('animated_background.py', '.'),
    ('gladiator_types.py', '.'),
    ('config.py', '.')
]

a = Analysis(
    ['client.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'LoginScreen',
        'buttons',
        'utils',
        'registration_screen',
        'animated_background',
        'gladiator_types',
        'config',
        'pygame',
        'dotenv',
        'json',
        'socket',
        'sys',
        'os',
        'time'
    ],
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
    name='Gladiator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Temporär auf True für bessere Fehlermeldungen
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='client'                 # Name des finalen Ausgabeverzeichnisses
)
