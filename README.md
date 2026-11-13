# Vortex Browser

A fast, ultra-lightweight, and easily customizable web browser built with Python and PyQt5. Designed to run smoothly on low-end hardware without eating up your RAM.

Um navegador web rápido, ultraleve e fácil de modificar, feito em Python e PyQt5. Criado para rodar liso em hardware modesto sem devorar sua memória RAM.

<img width="1910" height="1013" alt="fotoDoVortex" src="https://github.com/user-attachments/assets/7d4a981e-36e7-45ba-b60e-4449b892e661" />


---

### Why Vortex? / Por que o Vortex?

Modern browsers consume gigabytes of RAM just to keep a few tabs open. Vortex was built around three core principles:
* **Lightweight:** Minimal background footprint, ideal for older laptops, tiling window managers, and web games (`.io`).
* **Simple & Distraction-Free:** Clean dark interface with built-in ad-blocking and zero bloatware.
* **Hackable / Modifiable:** Written in clean Python — easy to read, tweak, and customize to fit your own workflow.

Navegadores modernos consomem gigabytes de RAM só para manter algumas abas abertas. O Vortex foi criado com três ideias principais:
* **Leveza:** Consumo mínimo em segundo plano, ideal para notebooks mais fracos, window managers leves e jogos web (`.io`).
* **Simples e sem distrações:** Interface escura limpa, bloqueio de anúncios integrado e zero recursos inúteis.
* **Modificável:** Feito em Python direto ao ponto — fácil de ler, alterar e adaptar do seu jeito.

---

### Memory Comparison / Comparação de Consumo (RAM)

Tested on Linux under the same conditions (idle / 1 tab open):
*(Testado no Linux nas mesmas condições)*



<img width="1917" height="202" alt="Captura de tela_2026-11-13_03-03-04" src="https://github.com/user-attachments/assets/43f44870-11bb-416b-9c0f-f68936b04f52" />
<img width="1917" height="289" alt="Captura de tela_2026-11-13_03-00-56" src="https://github.com/user-attachments/assets/1df140e9-44ec-4979-b50c-b4279ac77f36" />


<img width="1915" height="448" alt="Captura de tela_2026-11-13_02-56-51" src="https://github.com/user-attachments/assets/ffe96272-3915-4e2c-80f8-23fed8a68cd6" />


| Browser / Navegador | RAM Usage (Idle) (Start page) | RAM Usage with 1 tab (splop.io) |
| :--- | :---: | :---: |
| **Vortex Browser** | ~340,7 MB | ~378,4 MB |
| **Falkon** | ~525,4 MB | ~1,087 GB |
| **Chromium** | ~1,323 GB | ~1,425 GB |
---

### Installation (Linux) / Instalação

No need to run scripts manually every time. Run the installer once to add Vortex to your system's application menu:
*(Não precisa rodar pelo terminal toda vez. Execute o instalador uma vez para adicionar o Vortex ao menu de aplicativos do sistema:)*

```bash
git clone [https://github.com/CPmmmk/vortex-browser.git](https://github.com/CPmmmk/vortex-browser.git)
cd vortex-browser.git
pip install -r requirements.txt
chmod +x install.sh && ./install.sh
