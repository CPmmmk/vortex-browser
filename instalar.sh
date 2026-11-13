#!/bin/bash

# Pega o caminho exato da pasta atual onde o script está rodando
DIR_ATUAL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARQUIVO_MAIN="$DIR_ATUAL/main.py"
ARQUIVO_ICONE="$DIR_ATUAL/vaca_dourada.png"
DESTINO_DESKTOP="$HOME/.local/share/applications/vortex-browser.desktop"

# Garante que a pasta de aplicativos locais existe
mkdir -p "$HOME/.local/share/applications"

# Cria o atalho oficial do sistema
cat << EOF > "$DESTINO_DESKTOP"
[Desktop Entry]
Version=1.0
Type=Application
Name=Vortex Browser
Comment=Navegador leve e otimizado para jogos
Exec=python3 "$ARQUIVO_MAIN"
Icon=$ARQUIVO_ICONE
Terminal=false
Categories=Network;WebBrowser;
StartupWMClass=Vortex Browser
EOF

# Dá permissão de execução
chmod +x "$DESTINO_DESKTOP"
chmod +x "$ARQUIVO_MAIN"

# Atualiza o banco de dados do menu do Mint
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null

echo " Vortex Browser instalado no menu do sistema com sucesso!"
