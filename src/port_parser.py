"""
Port Parser Module for PortSpy

This module handles parsing different port input formats:
- Single ports: "80" → [80]
- Multiple ports: "22,80,443" → [22, 80, 443]
- Port ranges: "1-1000" → [1, 2, 3, ..., 1000]
- Mixed formats: "80,443,8000-8080" → [80, 443, 8000, 8001, ..., 8080]

Learning objectives:
- String parsing and manipulation
- Range expansion algorithms
- Input validation and sanitization
- List operations and comprehensions
- Error handling for user input
"""

from typing import List, Set


def validate_port(port: int) -> bool:
    """
    Check if a port number is valid (1-65535).
    
    Args:
        port (int): Port number to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Examples:
        >>> validate_port(80)
        True
        >>> validate_port(70000)
        False
        >>> validate_port(0)
        False
        
    Learning points:
        - Valid TCP ports are 1-65535
        - Port 0 is reserved and not usable
        - Ports above 65535 don't exist in TCP/IP
    """
    # TODO: Implement port validation
    # Valid port range is 1-65535
    pass


def parse_port_range(port_range: str) -> List[int]:
    """
    Parse a port range string like "1000-2000" into a list of ports.
    
    Args:
        port_range (str): Range in format "start-end" (e.g., "80-90")
        
    Returns:
        List[int]: List of all ports in the range
        
    Examples:
        >>> parse_port_range("80-83")
        [80, 81, 82, 83]
        >>> parse_port_range("443-443")
        [443]
        
    Learning points:
        - String splitting with "-"
        - Range generation with range()
        - Input validation for malformed ranges
    """
    # TODO: Implement range parsing
    # 1. Split by "-" to get start and end
    # 2. Convert to integers
    # 3. Validate both ports
    # 4. Generate range and return as list
    pass


def parse_ports(port_string: str) -> List[int]:
    """
    Main parser function that handles all port formats.
    
    Args:
        port_string (str): Port specification in various formats
        
    Returns:
        List[int]: Sorted list of unique valid ports
        
    Examples:
        >>> parse_ports("80")
        [80]
        >>> parse_ports("22,80,443")
        [22, 80, 443]
        >>> parse_ports("80-82,443")
        [80, 81, 82, 443]
        >>> parse_ports("80,80,443")
        [80, 443]  # Duplicates removed
        
    Learning points:
        - String splitting and processing
        - Combining different parsing strategies
        - Set operations for removing duplicates
        - Comprehensive input validation
    """
    # TODO: Implement main parsing logic
    # 1. Split input by commas
    # 2. For each part, determine if it's a single port or range
    # 3. Parse accordingly using helper functions
    # 4. Combine results, remove duplicates, sort
    pass


# TODO: You'll implement these functions step by step
