import sys
import os
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTabWidget, QShortcut
)
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserTab(QWidget):
    def __init__(self, parent_browser):
        super().__init__()
        self.parent_browser = parent_browser
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.view = QWebEngineView()
        self.layout.addWidget(self.view)
        
        self.zoom_factor = 1.0

    def zoom_in(self):
        self.zoom_factor = min(3.0, self.zoom_factor + 0.1)
        self.view.setZoomFactor(self.zoom_factor)

    def zoom_out(self):
        self.zoom_factor = max(0.3, self.zoom_factor - 0.1)
        self.view.setZoomFactor(self.zoom_factor)

    def reset_zoom(self):
        self.zoom_factor = 1.0
        self.view.setZoomFactor(self.zoom_factor)


class VortexBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vortex Browser")
        self.setGeometry(100, 100, 1100, 700)
        
        if os.path.exists("assets/vaca_dourada.png"):
            self.setWindowIcon(QIcon("assets/vaca_dourada.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(4, 4, 4, 4)

        self.top_bar_layout = QHBoxLayout()
        self.top_bar_layout.setSpacing(6)

        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.reload_btn = QPushButton("↻")
        self.url_bar = QLineEdit()
        self.new_tab_btn = QPushButton("+")
        
        for btn in (self.back_btn, self.forward_btn, self.reload_btn):
            btn.setFixedWidth(35)
            btn.setFixedHeight(30)

        self.new_tab_btn.setFixedWidth(35)
        self.new_tab_btn.setFixedHeight(30)
        self.new_tab_btn.setToolTip("Abrir nova aba")
        self.new_tab_btn.clicked.connect(lambda: self.add_new_tab())

        self.url_bar.setFixedHeight(30)

        self.top_bar_layout.addWidget(self.back_btn)
        self.top_bar_layout.addWidget(self.forward_btn)
        self.top_bar_layout.addWidget(self.reload_btn)
        self.top_bar_layout.addWidget(self.url_bar)
        self.top_bar_layout.addWidget(self.new_tab_btn) 

        self.layout.addLayout(self.top_bar_layout)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setDocumentMode(True)
        
        tab_bar = self.tabs.tabBar()
        tab_bar.setElideMode(Qt.TextElideMode.ElideRight)  
        tab_bar.setUsesScrollButtons(True)                 
        tab_bar.setExpanding(False)                       
        tab_bar.setMovable(True)                

        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)

        self.layout.addWidget(self.tabs)

        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.back_btn.clicked.connect(lambda: self.current_view().back())
        self.forward_btn.clicked.connect(lambda: self.current_view().forward())
        self.reload_btn.clicked.connect(lambda: self.current_view().reload())

        QShortcut(QKeySequence("Ctrl+="), self, lambda: self.current_tab_widget().zoom_in())
        QShortcut(QKeySequence("Ctrl+-"), self, lambda: self.current_tab_widget().zoom_out())
        QShortcut(QKeySequence("Ctrl+0"), self, lambda: self.current_tab_widget().reset_zoom())
        QShortcut(QKeySequence("F5"), self, lambda: self.current_view().reload())
        QShortcut(QKeySequence("Ctrl+R"), self, lambda: self.current_view().reload())
        QShortcut(QKeySequence("Ctrl+T"), self, lambda: self.add_new_tab())
        QShortcut(QKeySequence("Ctrl+W"), self, lambda: self.close_tab(self.tabs.currentIndex()))

        home_path = os.path.abspath("home.html")
        if not os.path.exists(home_path):
            with open(home_path, "w", encoding="utf-8") as f:
                f.write("<html><body style='background:#111;color:#fff;font-family:sans-serif;text-align:center;padding-top:20vh;'><h1>Vortex Browser</h1><p>Minimalista e Leve</p></body></html>")
        
        self.add_new_tab(f"file:///{home_path}", "Nova Aba")

    def current_view(self):
        current_widget = self.tabs.currentWidget()
        if current_widget:
            return current_widget.view
        return None

    def current_tab_widget(self):
        return self.tabs.currentWidget()

    def add_new_tab(self, url=None, label="Nova Aba"):
        browser_tab = BrowserTab(self)
        
        if not url:
            home_path = os.path.abspath("home.html")
            url = f"file:///{home_path}"

        browser_tab.view.load(QUrl(url))
        
        index = self.tabs.addTab(browser_tab, label)
        self.tabs.setCurrentIndex(index)

        browser_tab.view.urlChanged.connect(lambda q, vt=browser_tab: self.update_url(q, vt))
        browser_tab.view.titleChanged.connect(lambda title, vt=browser_tab: self.update_title(title, vt))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            widget.deleteLater()
            self.tabs.removeTab(index)
        else:
            home_path = os.path.abspath("home.html")
            self.current_view().load(QUrl(f"file:///{home_path}"))

    def tab_changed(self, index):
        view = self.current_view()
        if view:
            self.url_bar.setText(view.url().toString())

    def update_url(self, q, browser_tab):
        if self.tabs.currentWidget() == browser_tab:
            url_str = q.toString()
            
            if "home.html" in url_str:
                self.url_bar.clear()
            else:
                self.url_bar.setText(url_str)

    def update_title(self, title, browser_tab):
        index = self.tabs.indexOf(browser_tab)
        if index != -1:
            clean_title = title if len(title) < 18 else title[:15] + "..."
            self.tabs.setTabText(index, clean_title)

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        view = self.current_view()
        if not view:
            return

        if text.startswith("http://") or text.startswith("https://") or text.startswith("file:///"):
            view.load(QUrl(text))
        elif "." in text and " " not in text:
            view.load(QUrl("https://" + text))
        else:
            query = text.replace(" ", "+")
            view.load(QUrl(f"https://duckduckgo.com/?q={query}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyleSheet("""
        QMainWindow { background-color: #121212; }
        QLineEdit { 
            background-color: #1e1e1e; 
            color: #ffffff; 
            border: 1px solid #2c2c2c; 
            border-radius: 6px; 
            padding: 4px 10px; 
            font-size: 13px;
        }
        QLineEdit:focus { 
            border: 1px solid #0066cc; 
            background-color: #181818;
        }
        QPushButton { 
            background-color: #1e1e1e; 
            color: #ffffff; 
            border: 1px solid #2c2c2c; 
            border-radius: 6px; 
            font-weight: bold; 
        }
        QPushButton:hover { background-color: #282828; }
        QPushButton:pressed { background-color: #111111; }
        QTabWidget::pane { 
            border: 1px solid #222222; 
            background: #121212; 
            border-radius: 4px;
        }
        QTabBar::tab { 
            background: #1a1a1a; 
            color: #888; 
            padding: 6px 14px; 
            border-top-left-radius: 6px; 
            border-top-right-radius: 6px; 
            margin-right: 2px; 
            border: 1px solid #222;
            border-bottom: none;
        }
        QTabBar::tab:selected { 
            background: #242424; 
            color: #fff; 
            border-bottom: 2px solid #0066cc; 
        }
    """)

    browser = VortexBrowser()
    browser.show()
    sys.exit(app.exec_())
