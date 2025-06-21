"""
Subdomain enumeration worker module.
Handles the background thread for subdomain discovery with concurrent processing.
"""

import requests
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class SubdomainFinderWorker(QThread):
    """Worker thread for subdomain enumeration with concurrent processing."""
    
    update_result = pyqtSignal(str)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    progress_update = pyqtSignal(int, int)  # current, total

    def __init__(self, domain: str, subdomains: List[str], timeout: int = 3, max_workers: int = 20):
        super().__init__()
        self.domain = domain
        self.subdomains = subdomains
        self.timeout = timeout
        self.max_workers = max_workers
        self._stop_flag = False
        self._lock = threading.Lock()
        self._completed_count = 0

    def run(self):
        """Main thread execution method with concurrent processing."""
        try:
            self.enumerate_subdomains_concurrent(self.domain, self.subdomains)
        except Exception as e:
            self.error_occurred.emit(f"Error during enumeration: {str(e)}")
        finally:
            self.finished.emit()

    def enumerate_subdomains_concurrent(self, domain: str, subdomains: List[str]) -> None:
        """Enumerate subdomains using concurrent threads for faster processing."""
        total_subdomains = len(subdomains)
        valid_subdomains = []
        
        self.update_result.emit(f"[*] Starting concurrent enumeration with {self.max_workers} workers...")
        self.update_result.emit(f"[*] Total subdomains to check: {total_subdomains}")
        self.update_result.emit("-" * 50)

        # Use ThreadPoolExecutor for concurrent processing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all subdomain checks
            future_to_subdomain = {
                executor.submit(self.check_single_subdomain, subdomain, domain, idx): (subdomain, idx)
                for idx, subdomain in enumerate(subdomains, start=1)
            }

            # Process completed futures
            for future in as_completed(future_to_subdomain):
                if self._stop_flag:
                    break
                
                subdomain, idx = future_to_subdomain[future]
                
                try:
                    result = future.result()
                    if result:
                        valid_subdomains.append(result)
                        self.update_result.emit(f"{idx}. {result}")
                except Exception as e:
                    self.error_occurred.emit(f"Error checking {subdomain}.{domain}: {str(e)}")
                
                # Update progress
                with self._lock:
                    self._completed_count += 1
                    if self._completed_count % 50 == 0 or self._completed_count == total_subdomains:
                        self.progress_update.emit(self._completed_count, total_subdomains)
                        self.update_result.emit(f"[*] Progress: {self._completed_count}/{total_subdomains} ({self._completed_count/total_subdomains*100:.1f}%)")

        self.update_result.emit("-" * 50)
        self.update_result.emit(f"[*] Found {len(valid_subdomains)} valid subdomains")

    def check_single_subdomain(self, subdomain: str, domain: str, idx: int) -> str:
        """Check a single subdomain and return the full domain if valid."""
        if self._stop_flag:
            return None
            
        full_domain = f"{subdomain}.{domain}"
        if self.is_valid_subdomain(full_domain):
            return full_domain
        return None

    def is_valid_subdomain(self, domain: str) -> bool:
        """Check if a subdomain is valid by making an HTTP request."""
        try:
            # Try both HTTP and HTTPS
            for protocol in ['http', 'https']:
                try:
                    response = requests.get(f"{protocol}://{domain}", 
                                          timeout=self.timeout, 
                                          allow_redirects=False)
                    if response.status_code < 400:  # Accept any non-error status
                        return True
                except requests.RequestException:
                    continue
            return False
        except Exception:
            return False

    @pyqtSlot()
    def stop(self):
        """Stop the enumeration process."""
        self._stop_flag = True 