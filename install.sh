#!/bin/bash

echo "========================================="
echo "   Configurando o Vortex Browser...      "
echo "========================================="

cd "$(dirname "${BASH_SOURCE[0]}")"
PROJECT_DIR="$(pwd)"


ICON_PATH="$PROJECT_DIR/assets/vaca_dourada.png"
if [ ! -f "$ICON_PATH" ]; then
    ICON_PATH="web-browser"
fi

DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"

cat << EOF > "$DESKTOP_DIR/vortex-browser.desktop"
[Desktop Entry]
Name=Vortex Browser
Comment=Navegador web minimalista e leve
Exec=python3 $PROJECT_DIR/main.py
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Network;WebBrowser;
StartupNotify=true
EOF

chmod +x "$DESKTOP_DIR/vortex-browser.desktop"
update-desktop-database "$DESKTOP_DIR" 2>/dev/null

echo "==================================================="
echo "  Vortex foi instalado no seu menu com sucesso!  :)"
echo "==================================================="
