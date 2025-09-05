from typing import List, Set


def validate_port(port: int) -> bool:
  
    # TCP ports must be between 1 and 65535 (inclusive)
    return 1 <= port <= 65535


def parse_port_range(port_range: str) -> List[int]:
  
    try:
       
        parts = port_range.split("-")
        if len(parts) != 2:
            return []  
        

        start_port = int(parts[0])
        end_port = int(parts[1])
        
       
        if start_port > end_port:
            return []  # Invalid range
        
        
        result = []
        for port in range(start_port, end_port + 1):  # +1 because range() excludes end
            if validate_port(port):  # Only include valid ports
                result.append(port)
        
        return result
        
    except ValueError:
       
        return []


def parse_ports(port_string: str) -> List[int]:
    
    if not port_string or not port_string.strip():
        return [] 
    #combining all ports here
    all_ports = [] 
    
   
    parts = port_string.split(",")
    
   
    for part in parts:
        part = part.strip()  # Remove whitespace
        if not part:
            continue  
        
       
        if "-" in part:
           
            range_ports = parse_port_range(part)
            all_ports.extend(range_ports)  
        else:
            # It's a single port
            try:
                port = int(part)
                if validate_port(port):  # Only adding valid ports
                    all_ports.append(port)
            except ValueError:
               
                continue
    
   
    unique_ports = list(set(all_ports)) 
    unique_ports.sort()  
    
    return unique_ports

