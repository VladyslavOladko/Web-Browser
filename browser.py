from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import os
import sys


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)
        self.setCentralWidget(self.browser)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navigation_tool_bar = QToolBar("Navigation")
        navigation_tool_bar.setIconSize(QSize(16, 16))
        self.addToolBar(navigation_tool_bar)

        # write back button
        back_button = QAction(QIcon(os.path.join("images", "back.png")), "Back", self)
        back_button.setStatusTip("Back to previous page")
        back_button.triggered.connect(self.browser.back)
        navigation_tool_bar.addAction(back_button)

        # write next button
        next_button = QAction(QIcon(os.path.join("images", "next.png")), "Next", self)
        next_button.setStatusTip("Forward to next page")
        next_button.triggered.connect(self.browser.forward)
        navigation_tool_bar.addAction(next_button)

        # write reload button
        reload_button = QAction(QIcon(os.path.join("images", "reload.png")), "Reload", self)
        reload_button.setStatusTip("Reload page")
        reload_button.triggered.connect(self.browser.reload)
        navigation_tool_bar.addAction(reload_button)

        # write home button
        home_button = QAction(QIcon(os.path.join("images", "home.png")), "Home", self)
        home_button.setStatusTip("Back to Home page")
        home_button.triggered.connect(self.navigate_home)
        navigation_tool_bar.addAction(home_button)

        navigation_tool_bar.addSeparator()
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join("images", "non_secure.png")))
        navigation_tool_bar.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navigation_tool_bar.addWidget(self.urlbar)

        stop_button = QAction(QIcon(os.path.join("images", "stop.png")), "Stop", self)
        stop_button.setStatusTip("Stop loading current page")
        stop_button.triggered.connect(self.browser.stop)
        navigation_tool_bar.addAction(stop_button)

        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(QIcon(os.path.join("images", "file.png")), "Open file", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join("images", "file.png")), "Save page to file", self)
        save_file_action.setStatusTip("Open from file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(QIcon(os.path.join("images", "help.png")), "About browser", self)
        about_action.setStatusTip("Find out more about browser")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        self.show()

        self.setWindowIcon(QIcon(os.path.join("images", "browser.png")))

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s - Google" % title)

    def about(self):
        pass

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                        "*.htm *.html",
                                                        "All files (*.*)")
        if filename:
            with open(filename, "r") as f:
                html = f.read()

            self.browser.setHtml(html)
            self.urlbar.SetText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "save page as", "",
                                                        "*.htm *.html",
                                                        "All files (*.*)")
        if filename:
            html = self.browser.page().toHtml()
            with open(filename, "w") as f:
                f.write(html)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    def update_urlbar(self, q):
        if q.scheme() == "https":
            self.httpsicon.setPixmap(QPixmap(os.path.join("images", "")))
        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join("images", "non_secure.png")))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("Browser")
app.setOrganizationName("kotoamatsukami corp")
app.setOrganizationDomain("google.com")

window = MainWindow()
app.exec_()
