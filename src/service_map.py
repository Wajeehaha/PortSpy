
import socket
from port_parser import validate_port


def identify_service(port: int) -> str:
   
    try:
        # Validate port first
        if not validate_port(port):
            return "UNKNOWN"
            
        # Query system's service database
        service_name = socket.getservbyport(port, "tcp")
        return service_name.upper()  
        
    except OSError:
        # Service not found in system database
        return "UNKNOWN"