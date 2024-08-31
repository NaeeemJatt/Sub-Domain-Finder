import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget, \
    QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont
import requests
from typing import List


class SubdomainFinderGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sub-Domain-Finder")
        self.setGeometry(100, 100, 800, 600)

        # Set background color to a dark color
        self.setStyleSheet("background-color: #2C3E50;")

        # Layout
        layout = QVBoxLayout()

        # Title Label
        title = QLabel("Sub-Domain-Finder")
        title.setFont(QFont("Arial", 30, QFont.Bold))  # Font size
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        # Author Label
        author = QLabel("by Naeem Jatt")
        author.setFont(QFont("Arial", 14))
        author.setAlignment(Qt.AlignCenter)
        author.setStyleSheet("color: #ECF0F1;")  # Slightly different color for author name
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

        # Start Button with Animation
        self.start_button = QPushButton("Start Enumeration")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF; 
                color: white; 
                padding: 15px; 
                font-size: 18px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:pressed {
                background-color: #4682B4;
            }
        """)
        self.start_button.setFixedWidth(300)
        self.start_button.clicked.connect(self.start_enumeration)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        # Drop shadow effect for the button
        shadow_effect = QGraphicsDropShadowEffect(self.start_button)
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(0, 0, 0, 160))
        shadow_effect.setOffset(0, 0)
        self.start_button.setGraphicsEffect(shadow_effect)

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
            QMessageBox.warning(self, "Input Error", "Please enter a domain name.",)
            return

        # Subdomain enumeration logic
        subdomains_file = "subdomains-10000.txt"

        self.result_display.clear()
        self.result_display.append(f"[*] Enumerating subdomains for: {domain}")

        subdomains = self.read_subdomains_from_file(subdomains_file)

        if subdomains:
            self.result_display.append("\n[*] Checking subdomains from file:")
            valid_subdomains = self.enumerate_subdomains(domain, subdomains)

            self.result_display.append("\n[*] All valid subdomains found:")
            for subdomain in valid_subdomains:
                self.result_display.append(subdomain)
        else:
            self.result_display.append("[-] No subdomains to check")

    def is_valid_subdomain(self, domain: str) -> bool:
        try:
            response = requests.get(f"http://{domain}", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def enumerate_subdomains(self, domain: str, subdomains: List[str]) -> List[str]:
        valid_subdomains = []

        for subdomain in subdomains:
            full_domain = f"{subdomain}.{domain}"
            if self.is_valid_subdomain(full_domain):
                valid_subdomains.append(full_domain)
                self.result_display.append(f"[+] Valid Subdomain Found: {full_domain}")

        return valid_subdomains

    def read_subdomains_from_file(self, file_path: str) -> List[str]:
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
