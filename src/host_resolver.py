
import socket
import ipaddress
from typing import Optional


def is_valid_ip(ip: str) -> bool:
   
    try:
       
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
       
        return False


def resolve_hostname(hostname: str) -> str:
   
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:  # More specific: DNS resolution error
        return "DNS resolution failed"
    except socket.error:     # General network error
        return "Network error occurred"


def validate_target(target: str) -> tuple[str, str]:
   
    if is_valid_ip(target):
        return (target, "Valid IP address")
    else:
        resolved_ip = resolve_hostname(target)
        if is_valid_ip(resolved_ip):
            return (resolved_ip, "Hostname resolved successfully")
        else:
            return ("", resolved_ip)