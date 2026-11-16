#!/bin/bash

echo "========================================="
echo "   Instalando o Vortex Browser...        "
echo "========================================="

cd "$(dirname "${BASH_SOURCE[0]}")"
PROJECT_DIR="$(pwd)"

echo "[1/3] Criando ambiente virtual..."
python3 -m venv "$PROJECT_DIR/venv"

echo "[2/3] Instalando PyQt5..."
"$PROJECT_DIR/venv/bin/pip" install --upgrade pip > /dev/null 2>&1
"$PROJECT_DIR/venv/bin/pip" install PyQt5

ICON_PATH="$PROJECT_DIR/assets/logo.png"
if [ ! -f "$ICON_PATH" ]; then
    ICON_PATH="web-browser"
fi

echo "[3/3] Adicionando o Vortex ao menu de aplicativos..."
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"

cat << EOF > "$DESKTOP_DIR/vortex-browser.desktop"
[Desktop Entry]
Name=Vortex Browser
Comment=Navegador web minimalista e leve
Exec=$PROJECT_DIR/venv/bin/python3 $PROJECT_DIR/main.py
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Network;WebBrowser;
StartupNotify=true
EOF

chmod +x "$DESKTOP_DIR/vortex-browser.desktop"
update-desktop-database "$DESKTOP_DIR" 2>/dev/null

echo "========================================="
echo "  Instalação concluída com sucesso! :)   "
echo "========================================="
