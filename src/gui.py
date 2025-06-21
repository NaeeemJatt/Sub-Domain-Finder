"""
Main GUI module for the Subdomain Finder application.
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, 
    QTextEdit, QVBoxLayout, QWidget, QMessageBox, QProgressBar, QHBoxLayout, QSpinBox
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont

from .worker import SubdomainFinderWorker
from .utils import read_subdomains_from_file, validate_domain, get_default_subdomains_file


class SubdomainFinderGUI(QMainWindow):
    """Main GUI window for the Subdomain Finder application."""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.subdomains_file = get_default_subdomains_file()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Sub-Domain Finder - Fast Edition")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("background-color: #2C3E50;")

        # Create central widget and layout
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Add UI components
        self._create_title_section(layout)
        self._create_input_section(layout)
        self._create_settings_section(layout)
        self._create_button_section(layout)
        self._create_progress_section(layout)
        self._create_result_section(layout)

        # Initial button state
        self.stop_button.setEnabled(False)

    def _create_title_section(self, layout):
        """Create the title section of the UI."""
        title = QLabel("Sub-Domain-Finder")
        title.setFont(QFont("Georgia", 30, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        subtitle = QLabel("Fast Concurrent Edition")
        subtitle.setFont(QFont("Georgia", 16))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #3498db;")
        layout.addWidget(subtitle)

        author = QLabel("by Naeem Jatt")
        author.setFont(QFont("Georgia", 20))
        author.setAlignment(Qt.AlignCenter)
        author.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(author)

    def _create_input_section(self, layout):
        """Create the input section of the UI."""
        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("Enter Domain Name (e.g., example.com)")
        self.domain_input.setStyleSheet("""
            padding: 15px; 
            font-size: 18px; 
            color: white; 
            background-color: #34495E; 
            border: 1px solid white;
            border-radius: 10px;
        """)
        layout.addWidget(self.domain_input)

    def _create_settings_section(self, layout):
        settings_layout = QHBoxLayout()
        
        # Thread count setting
        thread_label = QLabel("Threads:")
        thread_label.setStyleSheet("color: white; font-size: 14px;")
        settings_layout.addWidget(thread_label)
        
        self.thread_spinbox = QSpinBox()
        self.thread_spinbox.setRange(5, 100)
        self.thread_spinbox.setValue(20)
        self.thread_spinbox.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            color: white;
            background-color: #34495E;
            border: 1px solid white;
            border-radius: 5px;
        """)
        settings_layout.addWidget(self.thread_spinbox)
        
        # Timeout setting
        timeout_label = QLabel("Timeout (s):")
        timeout_label.setStyleSheet("color: white; font-size: 14px;")
        settings_layout.addWidget(timeout_label)
        
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setRange(1, 10)
        self.timeout_spinbox.setValue(3)
        self.timeout_spinbox.setStyleSheet("""
            padding: 8px;
            font-size: 14px;
            color: white;
            background-color: #34495E;
            border: 1px solid white;
            border-radius: 5px;
        """)
        settings_layout.addWidget(self.timeout_spinbox)
        
        settings_layout.addStretch()
        layout.addLayout(settings_layout)

    def _create_button_section(self, layout):
        """Create the button section of the UI."""
        # Start Button
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

        # Stop Button
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

    def _create_progress_section(self, layout):
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #34495E;
                border-radius: 10px;
                text-align: center;
                font-size: 14px;
                color: white;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #27ae60, stop:1 #2ecc71);
                border-radius: 8px;
            }
        """)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

    def _create_result_section(self, layout):
        """Create the result display section of the UI."""
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("padding: 15px; font-size: 16px; background-color: white;")
        self.result_display.setFixedHeight(250)
        layout.addWidget(self.result_display)

    def start_enumeration(self):
        """Start the subdomain enumeration process."""
        # Button animation
        self._animate_button(self.start_button)

        # Validate input
        domain = self.domain_input.text().strip()
        if not domain:
            self._show_warning("Please enter a domain name.")
            return

        if not validate_domain(domain):
            self._show_warning("Please enter a valid domain name (e.g., example.com)")
            return

        # Read subdomains file
        subdomains = read_subdomains_from_file(self.subdomains_file)
        if not subdomains:
            self.result_display.append("[-] No subdomains found in the wordlist file.")
            self.result_display.append(f"[-] Expected file: {self.subdomains_file}")
            return

        # Get settings
        max_workers = self.thread_spinbox.value()
        timeout = self.timeout_spinbox.value()

        # Clear previous results
        self.result_display.clear()
        self.result_display.append(f"[*] Starting FAST enumeration for: {domain}")
        self.result_display.append(f"[*] Using {max_workers} concurrent threads")
        self.result_display.append(f"[*] Timeout: {timeout} seconds")
        self.result_display.append(f"[*] Using wordlist: {self.subdomains_file}")
        self.result_display.append(f"[*] Total subdomains to check: {len(subdomains)}")
        self.result_display.append("-" * 50)

        # Setup progress bar
        self.progress_bar.setMaximum(len(subdomains))
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        # Update button states
        self.stop_button.setEnabled(True)
        self.start_button.setEnabled(False)

        # Start worker thread with new settings
        self.worker = SubdomainFinderWorker(domain, subdomains, timeout, max_workers)
        self.worker.update_result.connect(self.update_result_display)
        self.worker.progress_update.connect(self.update_progress)
        self.worker.finished.connect(self.on_enumeration_finished)
        self.worker.error_occurred.connect(self.on_error_occurred)
        self.worker.start()

    def update_result_display(self, message: str):
        """Update the result display with a new message."""
        self.result_display.append(message)
        # Auto-scroll to bottom
        self.result_display.verticalScrollBar().setValue(
            self.result_display.verticalScrollBar().maximum()
        )

    def update_progress(self, current: int, total: int):
        self.progress_bar.setValue(current)
        percentage = (current / total) * 100
        self.progress_bar.setFormat(f"Progress: {current}/{total} ({percentage:.1f}%)")

    def on_enumeration_finished(self):
        """Handle enumeration completion."""
        self.result_display.append("-" * 50)
        self.result_display.append("[*] Enumeration completed!")
        self.progress_bar.setVisible(False)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def on_error_occurred(self, error_message: str):
        """Handle errors during enumeration."""
        self.result_display.append(f"[!] Error: {error_message}")

    def stop_enumeration(self):
        """Stop the enumeration process."""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.result_display.append("[*] Stopping enumeration...")
            QMessageBox.information(self, "Enumeration Stopped", 
                                  "Enumeration has been stopped successfully.")

    def _animate_button(self, button):
        """Animate button press."""
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(200)
        animation.setStartValue(button.geometry())
        animation.setEndValue(button.geometry().adjusted(0, 0, 0, 5))
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.start()

    def _show_warning(self, message: str):
        """Show a warning message box."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setStyleSheet("QLabel{color: white;} QMessageBox{background-color: #2C3E50;}")
        msg_box.exec_()


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    window = SubdomainFinderGUI()
    window.show()
    sys.exit(app.exec_()) 