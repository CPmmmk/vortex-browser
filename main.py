import os
import sys

# 1. Flags de desempenho (GPU) e Dark Mode forçado no motor do navegador
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--ignore-gpu-blocklist"
    "--blink-settings=forceDarkModeEnabled=true"
)

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QLineEdit,
    QAction,
    QVBoxLayout,
    QWidget,
    QTabWidget,
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView,
    QWebEngineProfile,
    QWebEnginePage,
)
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtGui import QIcon

# Estilo "Pretão Universo" (#000000) para toda a interface do navegador
DARK_UNIVERSE_STYLE = """
QMainWindow, QWidget {
    background-color: #000000;
    color: #e0e0e0;
}
QToolBar {
    background-color: #000000;
    border-bottom: 1px solid #141414;
    spacing: 6px;
    padding: 4px;
}
QToolButton {
    background-color: #0a0a0a;
    color: #ffffff;
    border: 1px solid #1a1a1a;
    border-radius: 4px;
    padding: 4px 8px;
}
QToolButton:hover {
    background-color: #1a1a1a;
}
QLineEdit {
    background-color: #080808;
    color: #ffffff;
    border: 1px solid #1f1f1f;
    border-radius: 6px;
    padding: 5px 10px;
    selection-background-color: #333333;
}
QLineEdit:focus {
    border: 1px solid #444444;
}
QTabWidget::pane {
    border: none;
    background-color: #000000;
}
QTabBar::tab {
    background-color: #050505;
    color: #777777;
    border: 1px solid #121212;
    border-bottom: none;
    padding: 6px 14px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
QTabBar::tab:selected {
    background-color: #121212;
    color: #ffffff;
    border-top: 2px solid #555555;
}
QTabBar::tab:hover:!selected {
    background-color: #0c0c0c;
    color: #bbbbbb;
}
"""


class AdBlocker(QWebEngineUrlRequestInterceptor):

  def interceptRequest(self, info):
    url = info.requestUrl().toString().lower()
    bloqueados = [
        "doubleclick.net",
        "googlesyndication.com",
        "googleadservices.com",
        "adnxs.com",
        "adinplay.com",
        "pubmatic.com",
        "rubiconproject.com",
        "criteo.com",
        "taboola.com",
        "outbrain.com",
        "google-analytics.com",
        "ads.",
        "/ads/",
        "adserver",
    ]
    if any(b in url for b in bloqueados):
      info.block(True)


class BrowserPage(QWidget):

  def __init__(self, profile, parent=None):
    super().__init__(parent)
    layout = QVBoxLayout(self)
    layout.setContentsMargins(0, 0, 0, 0)

    self.browser = QWebEngineView()
    # Define o fundo inicial como preto absoluto para não dar clarão branco ao abrir aba
    self.browser.page().setBackgroundColor(Qt.black)

    self.page = QWebEnginePage(profile, self.browser)
    self.page.setBackgroundColor(Qt.black)
    self.browser.setPage(self.page)

    layout.addWidget(self.browser)


class CPBrowser(QMainWindow):

  def __init__(self):
    super().__init__()
    self.setWindowTitle("Vortex Browser - Black Edition")
    self.setGeometry(100, 100, 1200, 800)
    self.setStyleSheet(DARK_UNIVERSE_STYLE)

    icon_path = os.path.join(os.path.dirname(__file__), "vaca_dourada.png")
    if os.path.exists(icon_path):
      self.setWindowIcon(QIcon(icon_path))

    # Configuração global do perfil e AdBlocker
    self.profile = QWebEngineProfile.defaultProfile()
    self.interceptor = AdBlocker()
    self.profile.setUrlRequestInterceptor(self.interceptor)

    settings = self.profile.settings()
    settings.setAttribute(settings.WebAttribute.JavascriptEnabled, True)
    settings.setAttribute(settings.WebAttribute.LocalStorageEnabled, True)
    settings.setAttribute(settings.WebAttribute.PluginsEnabled, False)
    settings.setAttribute(settings.WebAttribute.ScreenCaptureEnabled, False)
    settings.setAttribute(
        settings.WebAttribute.Accelerated2dCanvasEnabled, True
    )
    settings.setAttribute(settings.WebAttribute.WebGLEnabled, True)

    # Abas
    self.tabs = QTabWidget()
    self.tabs.setTabsClosable(True)
    self.tabs.tabCloseRequested.connect(self.close_tab)
    self.tabs.currentChanged.connect(self.on_tab_changed)
    self.setCentralWidget(self.tabs)

    # Barra de ferramentas
    navbar = QToolBar()
    navbar.setMovable(False)
    self.addToolBar(navbar)

    back_btn = QAction("◀", self)
    back_btn.triggered.connect(self.current_browser_back)
    navbar.addAction(back_btn)

    forward_btn = QAction("▶", self)
    forward_btn.triggered.connect(self.current_browser_forward)
    navbar.addAction(forward_btn)

    reload_btn = QAction("🔄", self)
    reload_btn.triggered.connect(self.current_browser_reload)
    navbar.addAction(reload_btn)

    self.url_bar = QLineEdit()
    self.url_bar.setPlaceholderText("Pesquisar ou digitar endereço...")
    self.url_bar.returnPressed.connect(self.navigate_to_url)
    navbar.addWidget(self.url_bar)

    self.home_url = QUrl.fromLocalFile(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "home.html"))
    )

    new_tab_btn = QAction("➕ Nova Aba", self)
    new_tab_btn.triggered.connect(
        lambda: self.add_new_tab(self.home_url, "Início")
    )
    navbar.addAction(new_tab_btn)

    self.add_new_tab(self.home_url, "Início")

  def add_new_tab(self, qurl, label):
    browser_page = BrowserPage(self.profile)
    browser_page.browser.setUrl(qurl)

    index = self.tabs.addTab(browser_page, label)
    self.tabs.setCurrentIndex(index)

    browser_page.browser.urlChanged.connect(
        lambda q, b=browser_page.browser: self.handle_url_change(q, b)
    )
    browser_page.browser.titleChanged.connect(
        lambda title, b=browser_page.browser: self.update_tab_title(title, b)
    )

  def update_tab_title(self, title, browser):
    for i in range(self.tabs.count()):
      if self.tabs.widget(i).browser == browser:
        self.tabs.setTabText(i, title[:15] + "..." if len(title) > 15 else title)
        break

  def close_tab(self, index):
    if self.tabs.count() > 1:
      widget = self.tabs.widget(index)
      self.tabs.removeTab(index)
      widget.deleteLater()  # Libera a RAM da aba fechada imediatamente
    else:
      self.close()

  def on_tab_changed(self, index):
    if index == -1:
      return

    # Atualiza barra de URL
    active_widget = self.tabs.widget(index)
    current_url = active_widget.browser.url().toString()
    self.url_bar.setText("" if "home.html" in current_url else current_url)

    # Pausa renderização das abas inativas para economizar CPU sem matar o site
    for i in range(self.tabs.count()):
      widget = self.tabs.widget(i)
      if widget:
        widget.browser.page().setVisible(i == index)

  def handle_url_change(self, q, browser):
    if (
        self.tabs.currentWidget()
        and self.tabs.currentWidget().browser == browser
    ):
      url_str = q.toString()
      self.url_bar.setText("" if "home.html" in url_str else url_str)

  def navigate_to_url(self):
    url = self.url_bar.text().strip()
    if not url:
      return
    if not url.startswith("http://") and not url.startswith("https://"):
      if "." in url and " " not in url:
        url = "https://" + url
      else:
        url = f"https://www.google.com/search?q={url}"

    current_widget = self.tabs.currentWidget()
    if current_widget:
      current_widget.browser.setUrl(QUrl(url))

  def current_browser_back(self):
    w = self.tabs.currentWidget()
    if w:
      w.browser.back()

  def current_browser_forward(self):
    w = self.tabs.currentWidget()
    if w:
      w.browser.forward()

  def current_browser_reload(self):
    w = self.tabs.currentWidget()
    if w:
      w.browser.reload()


if __name__ == "__main__":
  app = QApplication(sys.argv)
  QApplication.setApplicationName("Vortex Browser")
  app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

  window = CPBrowser()
  window.show()
  sys.exit(app.exec_())
