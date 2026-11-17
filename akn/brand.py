"""AKN markalama betigi: RustDesk kaynak kodunu derlemeden once logoyla ve adla gunceller.
Kullanim (depo kok dizininde):  python akn/brand.py "AKNDesk"
"""
import shutil, sys, re, pathlib

APP = sys.argv[1] if len(sys.argv) > 1 else "AKNDesk"
ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "akn" / "assets"

copies = {
    "icon.ico": ["res/icon.ico", "flutter/windows/runner/resources/app_icon.ico"],
    "tray-icon.ico": ["res/tray-icon.ico"],
    "icon.png": ["res/icon.png"],
    "mac-icon.png": ["res/mac-icon.png"],
    "32x32.png": ["res/32x32.png"],
    "64x64.png": ["res/64x64.png"],
    "128x128.png": ["res/128x128.png"],
    "128x128@2x.png": ["res/128x128@2x.png"],
    "flutter-icon.png": ["flutter/assets/icon.png"],
    "logo.png": ["flutter/assets/logo.png"],
}
for src, dsts in copies.items():
    for d in dsts:
        shutil.copyfile(A / src, ROOT / d)
        print("kopyalandi:", d)

def sub(path, pattern, repl):
    p = ROOT / path
    t = p.read_text(encoding="utf-8")
    n, c = re.subn(pattern, repl, t)
    if c == 0:
        sys.exit(f"HATA: {path} icinde degistirilecek satir bulunamadi")
    p.write_text(n, encoding="utf-8")
    print("guncellendi:", path)

sub("libs/hbb_common/src/config.rs",
    r'APP_NAME: RwLock<String> = RwLock::new\("RustDesk"\.to_owned\(\)\)',
    f'APP_NAME: RwLock<String> = RwLock::new("{APP}".to_owned())')
sub("flutter/windows/runner/Runner.rc", r'"FileDescription", "RustDesk Remote Desktop"',
    f'"FileDescription", "{APP} Uzak Masaustu"')
sub("flutter/windows/runner/Runner.rc", r'"ProductName", "RustDesk"', f'"ProductName", "{APP}"')
print("Markalama tamam:", APP)
