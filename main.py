import sys
import os
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, 
                             QLineEdit, QAction, QVBoxLayout, QWidget, QTabWidget)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QIcon

class BrowserPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.profile = QWebEngineProfile.defaultProfile()
        
        # Otimizações de desempenho e consumo de memória para focar em jogos
        settings = self.profile.settings()
        settings.setAttribute(settings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(settings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(settings.WebAttribute.PluginsEnabled, False)
        settings.setAttribute(settings.WebAttribute.ScreenCaptureEnabled, False)
        
        self.browser = QWebEngineView()
        self.page = QWebEnginePage(self.profile, self.browser)
        self.browser.setPage(self.page)
        
        layout.addWidget(self.browser)

class CPBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Vortex Browser - Leve & Rápido")
        self.setGeometry(100, 100, 1200, 800)
        
        # Ícone da janela e da barra de tarefas
        icon_path = os.path.join(os.path.dirname(__file__), "vaca_dourada.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        # Abas
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_tab_url)
        
        self.setCentralWidget(self.tabs)
        
        # Barra de ferramentas
        navbar = QToolBar()
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
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        
        # Caminho da página inicial (home.html)
        self.home_url = QUrl.fromLocalFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "home.html")))
        
        new_tab_btn = QAction("➕ Nova Aba", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(self.home_url, "Início"))
        navbar.addAction(new_tab_btn)

        # Iniciar com a primeira aba na página inicial
        self.add_new_tab(self.home_url, "Início")

    def add_new_tab(self, qurl, label):
        browser_page = BrowserPage()
        browser_page.browser.setUrl(qurl)
        
        index = self.tabs.addTab(browser_page, label)
        self.tabs.setCurrentIndex(index)
        
        browser_page.browser.urlChanged.connect(lambda q, b=browser_page.browser: self.handle_url_change(q, b))
        browser_page.browser.titleChanged.connect(lambda title, i=index: self.tabs.setTabText(i, title[:15] + "..." if len(title) > 15 else title))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def update_tab_url(self, index):
        if index != -1:
            widget = self.tabs.widget(index)
            current_url = widget.browser.url().toString()
            if "home.html" in current_url:
                self.url_bar.setText("")
            else:
                self.url_bar.setText(current_url)

    def handle_url_change(self, q, browser):
        if self.tabs.currentWidget() and self.tabs.currentWidget().browser == browser:
            url_str = q.toString()
            if "home.html" in url_str:
                self.url_bar.setText("")
            else:
                self.url_bar.setText(url_str)

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
        if w: w.browser.back()

    def current_browser_forward(self):
        w = self.tabs.currentWidget()
        if w: w.browser.forward()

    def current_browser_reload(self):
        w = self.tabs.currentWidget()
        if w: w.browser.reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Vortex Browser")
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    window = CPBrowser()
    window.show()
    sys.exit(app.exec_())
