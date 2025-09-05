# PortSpy 🔍

**A Professional TCP Port Scanner Built with Python**

PortSpy is an educational and practical TCP port scanner that demonstrates networking concepts, socket programming, and concurrent programming techniques. Built as a learning project, it combines professional-grade features with clean, readable code.

## ✨ Features

### Core Functionality
- **TCP Connect Scanning**: Fast and reliable port scanning using TCP connections
- **Multi-threaded Architecture**: Concurrent scanning for dramatically improved performance
- **Smart Host Resolution**: Supports both IP addresses and hostnames with DNS resolution
- **Service Identification**: Dynamic service detection using system service databases
- **Flexible Port Specification**: Support for individual ports, ranges, and mixed formats

### User Experience
- **Interactive Mode**: Prompts for target and ports if not provided via command line
- **Colorful Output**: Enhanced readability with colorama-powered colored terminal output
- **Progress Tracking**: Real-time progress bars using tqdm during scanning operations
- **Professional Reporting**: Detailed scan results with performance metrics and statistics
- **Cross-platform Support**: Works on Windows, macOS, and Linux

### Advanced Features
- **Configurable Threading**: Adjustable thread pool size for optimal performance
- **Timeout Control**: Customizable connection timeouts for different network conditions
- **Comprehensive Error Handling**: Robust error handling for network issues and edge cases
- **Verbose Mode**: Detailed logging for debugging and learning purposes

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Wajeehaha/PortSpy.git
   cd PortSpy
   ```

2. **Set up virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Basic Usage

**Simple scan:**
```bash
python src/portspy.py google.com
```

**Custom ports:**
```bash
python src/portspy.py 192.168.1.1 -p 22,80,443,8080
```

**Port ranges:**
```bash
python src/portspy.py scanme.nmap.org -p 1-100,443,8000-8010
```

**Interactive mode:**
```bash
python src/portspy.py
# Will prompt for target and ports
```

## 📋 Command Line Options

```
PortSpy - A simple TCP port scanner with colorful output

positional arguments:
  target                Target hostname or IP address to scan

optional arguments:
  -h, --help            Show help message and exit
  -p PORTS, --ports PORTS
                        Ports to scan (default: common ports)
                        Examples: "80,443", "80-90", "80,443,8000-8010"
  -t THREADS, --threads THREADS
                        Number of threads to use (default: 50)
  --timeout TIMEOUT     Connection timeout in seconds (default: 2.0)
  -v, --verbose         Enable verbose output
  --no-progress         Disable progress bar
```

## 💡 Usage Examples

### Basic Scanning
```bash
# Scan common ports on Google
python src/portspy.py google.com

# Scan specific ports on local network
python src/portspy.py 192.168.1.1 -p 22,80,443,3389

# Quick scan with shorter timeout
python src/portspy.py example.com --timeout 1
```

### Advanced Scanning
```bash
# High-performance scan with more threads
python src/portspy.py target.com -p 1-1000 -t 100

# Verbose output for debugging
python src/portspy.py localhost -p 80-85 -v

# Quiet mode without progress bar
python src/portspy.py target.com --no-progress
```

### Interactive Mode
```bash
# Run without arguments for interactive prompts
python src/portspy.py

# Example interaction:
# Target (hostname or IP): scanme.nmap.org
# Ports (80,443 or 1-100 or 'common'): 20-30,80,443
```

## 🏗️ Architecture

PortSpy follows a modular architecture with clean separation of concerns:

### Core Modules

- **`portspy.py`**: Main application entry point and CLI interface
- **`host_resolver.py`**: DNS resolution and IP address validation
- **`port_parser.py`**: Port specification parsing and validation
- **`service_map.py`**: Service identification using system databases
- **`tcp_scanner.py`**: Core TCP scanning functionality with threading

### Key Components

```
PortSpy/
├── src/
│   ├── portspy.py          # Main CLI application
│   ├── host_resolver.py    # Target resolution logic
│   ├── port_parser.py      # Port parsing utilities
│   ├── service_map.py      # Service identification
│   ├── tcp_scanner.py      # Core scanning engine
│   └── __init__.py
├── tests/                  # Unit tests (future)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Technical Details

### Scanning Process
1. **Target Resolution**: Validates and resolves hostnames to IP addresses
2. **Port Parsing**: Converts port specifications into scannable port lists
3. **Concurrent Scanning**: Uses ThreadPoolExecutor for parallel port scanning
4. **Service Detection**: Identifies services using `socket.getservbyport()`
5. **Result Formatting**: Generates professional reports with statistics

### Performance Characteristics
- **Threading**: Configurable thread pool (default: 50 threads)
- **Timeouts**: Per-connection timeout control (default: 2 seconds)  
- **Efficiency**: Typical scan rates of 100-500 ports/second
- **Memory**: Low memory footprint with efficient resource management

### Network Protocols
- **TCP Connect Scan**: Full TCP three-way handshake
- **Port States**: Open, Closed, Filtered, Error detection
- **Service Detection**: System service database integration

## 🎓 Educational Value

PortSpy is designed as a learning tool that demonstrates:

### Networking Concepts
- TCP/IP protocol fundamentals
- Socket programming with Python
- DNS resolution and hostname handling
- Port scanning methodologies
- Network service identification

### Programming Techniques
- Concurrent programming with ThreadPoolExecutor
- Error handling and exception management
- Modular design and separation of concerns
- Command-line interface development
- Professional code documentation

### Best Practices
- Type hints for better code clarity
- Comprehensive docstrings and examples
- Clean architecture with testable components
- Cross-platform compatibility considerations

## 🛡️ Ethical Usage

PortSpy is intended for:
- **Educational purposes** and learning networking concepts
- **Security testing** of your own systems and networks
- **Network administration** and troubleshooting
- **Authorized penetration testing** with proper permissions

### Important Notes
- Always obtain explicit permission before scanning networks you don't own
- Respect rate limits and avoid overloading target systems
- Use responsibly and in accordance with applicable laws and regulations
- Some networks may consider port scanning as hostile activity

## 🤝 Contributing

Contributions are welcome! Here are ways you can help:

1. **Report Issues**: Found a bug or have a feature request? Open an issue!
2. **Code Contributions**: Submit pull requests with improvements or new features
3. **Documentation**: Help improve documentation and examples
4. **Testing**: Add unit tests or test on different platforms

### Development Setup
```bash
git clone https://github.com/Wajeehaha/PortSpy.git
cd PortSpy
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built as an educational project to demonstrate networking and Python concepts
- Inspired by professional network scanning tools like Nmap
- Uses Python's built-in `socket` library for core functionality
- Enhanced with `colorama` and `tqdm` for better user experience

## 📚 Learning Resources

If you're using PortSpy to learn networking, check out these resources:
- [TCP/IP Protocol Fundamentals](https://en.wikipedia.org/wiki/Internet_protocol_suite)
- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [Network Port Scanning Techniques](https://nmap.org/book/man-port-scanning-techniques.html)
- [Concurrent Programming in Python](https://docs.python.org/3/library/concurrent.futures.html)

---

**Happy Scanning!** 🚀

*Remember: With great power comes great responsibility. Use PortSpy ethically and responsibly.*
