# Recommended Project Structure

```
PortSpy/
│
├── portspy.py              # Main entry point
├── src/
│   ├── __init__.py         # Makes src a package
│   ├── scanner.py          # Core scanning functionality
│   ├── port_parser.py      # Port range parsing logic
│   ├── host_resolver.py    # DNS resolution and validation
│   └── service_detector.py # Service identification
├── tests/
│   └── test_scanner.py     # Unit tests (optional but recommended)
├── requirements.txt        # Python dependencies
└── README.md              # Updated documentation
```


