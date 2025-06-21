# Subdomain Finder

A Python-based GUI application for discovering subdomains of a given domain. Built with PyQt5, this tool provides an intuitive interface for subdomain enumeration.

## Features

- **Modern GUI**: Clean and responsive user interface built with PyQt5
- **Background Processing**: Non-blocking subdomain enumeration using worker threads
- **Real-time Results**: Live updates as subdomains are discovered
- **Progress Tracking**: Visual feedback on enumeration progress
- **Error Handling**: Robust error handling and user feedback
- **Configurable**: Easy to modify wordlists and settings

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Sub-Domain-Finder
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

1. **Enter Domain**: Type the target domain (e.g., `example.com`)
2. **Start Enumeration**: Click "START ENUMERATION" to begin
3. **Monitor Progress**: Watch real-time results in the display area
4. **Stop if Needed**: Use "STOP ENUMERATION" to halt the process

## Project Structure

```
Sub-Domain-Finder/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── subdomains-10000.txt   # Subdomain wordlist
└── src/                   # Source code directory
    ├── __init__.py        # Package initialization
    ├── gui.py             # Main GUI implementation
    ├── worker.py          # Background worker thread
    └── utils.py           # Utility functions
```

## Dependencies

- **PyQt5**: GUI framework
- **requests**: HTTP library for subdomain validation

## How It Works

1. **Input Validation**: The application validates the domain input
2. **Wordlist Loading**: Reads subdomain candidates from `subdomains-10000.txt`
3. **HTTP Requests**: Makes HTTP requests to each potential subdomain
4. **Response Analysis**: Validates responses to determine if subdomains exist
5. **Real-time Updates**: Displays results as they are discovered

## Customization

### Adding Custom Wordlists

Replace or modify `subdomains-10000.txt` with your own subdomain list. Each subdomain should be on a separate line.

### Modifying Timeout Settings

Edit the `timeout` parameter in `src/worker.py` to adjust HTTP request timeouts.

### Styling Changes

Modify the CSS-like styles in `src/gui.py` to customize the application appearance.

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **File Not Found**: Make sure `subdomains-10000.txt` is in the project root
3. **Network Issues**: Check your internet connection for subdomain validation

### Error Messages

- `"Please enter a domain name"`: Domain field is empty
- `"Please enter a valid domain name"`: Invalid domain format
- `"No subdomains found in the wordlist file"`: Wordlist file is missing or empty

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Author

**Naeem Jatt** - Initial development

---

**Note**: This tool is for educational and authorized testing purposes only. Always ensure you have permission to scan domains before using this tool. 