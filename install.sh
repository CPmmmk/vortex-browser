#!/bin/bash

echo "========================================="
echo "   Instalando o Vortex Browser...        "
echo "========================================="

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ICON_PATH="$PROJECT_DIR/assets/logo.png"

if [ ! -f "$ICON_PATH" ]; then
    echo "Aviso: logo.png não encontrado em assets/. O atalho ficará sem ícone."
    ICON_PATH="web-browser"
fi


echo "[1/3] Criando ambiente virtual..."
python3 -m venv "$PROJECT_DIR/venv"

echo "[2/3] Instalando dependências..."
"$PROJECT_DIR/venv/bin/pip" install --upgrade pip > /dev/null 2>&1
"$PROJECT_DIR/venv/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

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
