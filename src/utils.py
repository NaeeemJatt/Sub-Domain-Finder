"""
Utility functions for the subdomain finder application.
"""

import os
from typing import List, Optional


def read_subdomains_from_file(file_path: str) -> List[str]:
    """
    Read subdomain list from a text file.
    
    Args:
        file_path: Path to the subdomains file
        
    Returns:
        List of subdomain strings
    """
    try:
        if not os.path.exists(file_path):
            return []
            
        with open(file_path, 'r', encoding='utf-8') as file:
            subdomains = [line.strip() for line in file if line.strip()]
        return subdomains
    except Exception as e:
        print(f"Error reading subdomains file: {e}")
        return []


def validate_domain(domain: str) -> bool:
    """
    Basic domain validation.
    
    Args:
        domain: Domain string to validate
        
    Returns:
        True if domain is valid, False otherwise
    """
    if not domain:
        return False
    
    # Basic validation - domain should not contain spaces and should have at least one dot
    if ' ' in domain or domain.count('.') < 1:
        return False
    
    # Check for valid characters
    valid_chars = set('abcdefghijklmnopqrstuvwxyz0123456789.-')
    domain_lower = domain.lower()
    
    return all(c in valid_chars for c in domain_lower)


def get_default_subdomains_file() -> str:
    """
    Get the default path to the subdomains file.
    
    Returns:
        Path to the default subdomains file
    """
    # Look for the file in the current directory first
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_path = os.path.join(current_dir, "subdomains-10000.txt")
    
    if os.path.exists(default_path):
        return default_path
    
    # Fallback to the root directory
    return "subdomains-10000.txt" 