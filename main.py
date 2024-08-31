import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import requests
from typing import List


class SubdomainFinderGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Subdomain Finder")
        self.setGeometry(100, 100, 600, 400)

        # Layout
        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Enter Domain Name:")
        layout.addWidget(self.label)

        # Domain Input
        self.domain_input = QLineEdit()
        layout.addWidget(self.domain_input)

        # Start Button
        self.start_button = QPushButton("Start Enumeration")
        layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_enumeration)

        # Results Display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_enumeration(self):
        domain = self.domain_input.text()
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
