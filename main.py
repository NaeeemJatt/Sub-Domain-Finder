import requests
from typing import List


# Function to check if a subdomain is valid by its HTTP response status
def is_valid_subdomain(domain: str) -> bool:
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


# Function to enumerate subdomains
def enumerate_subdomains(domain: str, subdomains: List[str]) -> List[str]:
    valid_subdomains = []

    for subdomain in subdomains:
        full_domain = f"{subdomain}.{domain}"
        if is_valid_subdomain(full_domain):
            valid_subdomains.append(full_domain)
            print(f"[+] Valid Subdomain Found: {full_domain}")
        # else:
        #     print(f"[-] Invalid Subdomain: {full_domain}")

    return valid_subdomains


# Function to read subdomains from a file
def read_subdomains_from_file(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r') as file:
            subdomains = file.read().splitlines()
        return subdomains
    except FileNotFoundError:
        print("[-] File not found")
        return []


if __name__ == "__main__":
    domain = input("Enter Domain Name:")
    subdomains_file = "subdomains-10000.txt"  # Change this to the path of your file
    print(f"[*] Enumerating subdomains for: {domain}")

    # Load subdomains from file
    subdomains = read_subdomains_from_file(subdomains_file)

    if subdomains:
        # Enumerate subdomains using the list from the file
        print("\n[*] Checking subdomains from file:")
        valid_subdomains = enumerate_subdomains(domain, subdomains)

        print("\n[*] All valid subdomains found:")
        for subdomain in valid_subdomains:
            print(subdomain)
    else:
        print("[-] No subdomains to check")