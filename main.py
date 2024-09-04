import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget, \
    QMessageBox
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QFont, QIcon


class SubdomainFinderWorker(QThread):
    update_result = pyqtSignal(str)
    finished = pyqtSignal()
    stop_requested = pyqtSignal()

    def __init__(self, domain: str, subdomains):
        super().__init__()
        self.domain = domain
        self.subdomains = subdomains
        self._stop_flag = False

    def run(self):
        self.enumerate_subdomains(self.domain, self.subdomains)
        self.finished.emit()

    def enumerate_subdomains(self, domain: str, subdomains) -> None:
        valid_subdomains = []
        for idx, subdomain in enumerate(subdomains, start=1):
            if self._stop_flag:
                break
            full_domain = f"{subdomain}.{domain}"
            if self.is_valid_subdomain(full_domain):
                valid_subdomains.append(full_domain)
                self.update_result.emit(f"{idx}. {full_domain}")

    def is_valid_subdomain(self, domain: str) -> bool:
        try:
            response = requests.get(f"http://{domain}", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    @pyqtSlot()
    def stop(self):
        self._stop_flag = True


class SubdomainFinderGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sub-Domain Finder")
        self.setGeometry(100, 100, 800, 600)

        # Set background color to a dark color
        self.setStyleSheet("background-color: #2C3E50;")

        # Layout
        layout = QVBoxLayout()

        # Title Label
        title = QLabel("Sub-Domain-Finder")
        title.setFont(QFont("Georgia", 30, QFont.Bold))  # Changed font style to Georgia
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        # Author Label
        author = QLabel("by Naeem Jatt")
        author.setFont(QFont("Georgia", 14))  # Changed font style to Georgia
        author.setAlignment(Qt.AlignCenter)
        author.setStyleSheet("color: #ECF0F1; margin-top: -15px;")  # Move closer to title
        layout.addWidget(author)

        # Domain Input
        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("Enter Domain Name")
        self.domain_input.setStyleSheet("""
            padding: 15px; 
            font-size: 18px; 
            color: white; 
            background-color: #34495E; 
            border: 1px solid white;
            border-radius: 10px;
        """)
        layout.addWidget(self.domain_input)

        # Start Button with New Design
        self.start_button = QPushButton("START ENUMERATION")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #3a7bd5, stop:1 #00d2ff); 
                color: white; 
                padding: 12px 18px;
                font-size: 18px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #3a7bd5, stop:1 #00d2ff);
            }
            QPushButton:pressed {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #3a7bd5, stop:1 #00d2ff);
                border: 2px solid #2980B9;  
            }
        """)
        self.start_button.setFixedWidth(250)
        self.start_button.clicked.connect(self.start_enumeration)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        # Stop Button with New Design
        self.stop_button = QPushButton("STOP ENUMERATION")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #ff6e7f, stop:1 #bfe9ff); 
                color: white; 
                padding: 12px 18px;
                font-size: 18px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #ff6e7f, stop:1 #bfe9ff);
            }
            QPushButton:pressed {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #ff6e7f, stop:1 #bfe9ff);
                border: 2px solid #A93226;  
            }
        """)
        self.stop_button.setFixedWidth(250)
        self.stop_button.clicked.connect(self.stop_enumeration)
        layout.addWidget(self.stop_button, alignment=Qt.AlignCenter)

        # Result Display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("padding: 15px; font-size: 16px; background-color: white;")
        layout.addWidget(self.result_display)
        self.result_display.setFixedHeight(200)  # Decreased height of result box

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Disable the stop button initially
        self.stop_button.setEnabled(False)

    def start_enumeration(self):
        # Button animation
        animation = QPropertyAnimation(self.start_button, b"geometry")
        animation.setDuration(200)
        animation.setStartValue(self.start_button.geometry())
        animation.setEndValue(self.start_button.geometry().adjusted(0, 0, 0, 5))
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.start()

        # Check if domain input is empty
        domain = self.domain_input.text()
        if not domain:
            # Show warning with white text
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Please enter a domain name.")
            msg_box.setStyleSheet("QLabel{color: white;} QMessageBox{background-color: #2C3E50;}")
            msg_box.exec_()
            return

        # Subdomain enumeration logic
        subdomains_file = "subdomains-10000.txt"

        self.result_display.clear()

        subdomains = self.read_subdomains_from_file(subdomains_file)

        if subdomains:
            # Enable stop button and disable start button
            self.stop_button.setEnabled(True)
            self.start_button.setEnabled(False)
            # Start the worker thread for enumeration
            self.worker = SubdomainFinderWorker(domain, subdomains)
            self.worker.update_result.connect(self.update_result_display)
            self.worker.finished.connect(self.on_enumeration_finished)
            self.worker.start()
        else:
            self.result_display.append("[-] No subdomains to check")

    def update_result_display(self, message: str):
        self.result_display.append(message)

    def on_enumeration_finished(self):
        self.result_display.append("[*] Enumeration completed.")
        # Re-enable the start button and disable the stop button
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def stop_enumeration(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.stop()
            self.worker.finished.connect(self.on_enumeration_finished)
            QMessageBox.information(self, "Enumeration Stopped", "Enumeration has been stopped successfully.")

    def read_subdomains_from_file(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                subdomains = file.read().splitlines()
            return subdomains
        except FileNotFoundError:
            self.result_display.append("[-] File not found")
            return []


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubdomainFinderGUI()
    window.show()
    sys.exit(app.exec_())
