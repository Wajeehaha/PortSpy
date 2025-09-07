import socket
import time
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from colorama import init, Fore, Back, Style

from service_map import identify_service

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def tcp_scan_port(ip: str, port: int, timeout: float = 2.0) -> Dict[str, any]:
   
    # Record start time for performance measurement
    start_time = time.time()
    
    # Initialize result structure
    result = {
        'port': port,
        'status': 'unknown',
        'service': identify_service(port),
        'response_time': 0.0
    }
    
    try:
       
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
       
        sock.settimeout(timeout)
        
       
        connection_result = sock.connect((ip, port))
        
       
        result['status'] = 'open'
        
    except socket.timeout:
       
        result['status'] = 'filtered'
        
    except ConnectionRefusedError:
       
        result['status'] = 'closed'
        
    except OSError as e:
        # Handle other network errors (host unreachable, etc.)
        if e.errno == 113:  # No route to host
            result['status'] = 'unreachable'
        else:
            result['status'] = 'error'
            
    except Exception as e:
        # Handle any unexpected errors
        result['status'] = 'error'
        
    finally:
        # Always close the socket to free resources
        try:
            sock.close()
        except:
            pass  # Ignore errors during cleanup
    
    # Calculate response time
    result['response_time'] = round(time.time() - start_time, 3)
    
    return result


def tcp_scan_ports(ip: str, ports: List[int], timeout: float = 2.0, 
                   max_threads: int = 100, show_progress: bool = True) -> List[Dict[str, any]]:
    """
    Scan multiple ports concurrently using threading with enhanced visual feedback.
    
    Args:
        ip (str): Target IP address
        ports (List[int]): List of ports to scan
        timeout (float): Connection timeout per port
        max_threads (int): Maximum concurrent threads
        show_progress (bool): Whether to show progress bar
        
    Returns:
        List[Dict]: List of scan results for each port
        
    Learning points:
        - Threading enables concurrent scanning
        - ThreadPoolExecutor manages thread pool
        - tqdm provides beautiful progress bars
        - Concurrent scanning is much faster
    """
    results = []
    open_ports_found = []
    
    print(f"{Fore.CYAN}Scanning {len(ports)} ports on {ip} with {max_threads} threads...{Style.RESET_ALL}")
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit all port scans to the thread pool
        future_to_port = {
            executor.submit(tcp_scan_port, ip, port, timeout): port 
            for port in ports
        }
        
        # Create progress bar if requested
        if show_progress:
            progress_bar = tqdm(
                total=len(ports),
                desc=f"{Fore.YELLOW}Scanning{Style.RESET_ALL}",
                unit="ports",
                ncols=80,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
            )
        
        # Collect results as they complete
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                result = future.result()
                results.append(result)
                
                # Handle open ports with colored output
                if result['status'] == 'open':
                    open_ports_found.append(result)
                    service_name = result['service']
                    response_time = result['response_time']
                    
                    # Print immediate notification for open ports
                    print(f"{Fore.GREEN}[OPEN]{Style.RESET_ALL} Port {Fore.YELLOW}{port}{Style.RESET_ALL}: "
                          f"{Fore.CYAN}{service_name}{Style.RESET_ALL} "
                          f"({response_time:.3f}s)")
                
                # Update progress bar
                if show_progress:
                    progress_bar.update(1)
                    progress_bar.set_postfix({
                        'Open': len(open_ports_found),
                        'Current': port
                    })
                    
            except Exception as exc:
                print(f"{Fore.RED}Port {port} generated an exception: {exc}{Style.RESET_ALL}")
                # Add error result
                results.append({
                    'port': port,
                    'status': 'error',
                    'service': 'ERROR',
                    'response_time': timeout
                })
                if show_progress:
                    progress_bar.update(1)
        
        if show_progress:
            progress_bar.close()
    
    # Sort results by port number for organized output
    results.sort(key=lambda x: x['port'])
    
    # Summary message with colors
    open_count = len([r for r in results if r['status'] == 'open'])
    if open_count > 0:
        print(f"\n{Fore.GREEN}[+] Scan completed! Found {open_count} open ports.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}[+] Scan completed! No open ports found.{Style.RESET_ALL}")
    
    return results


def format_scan_results(target: str, results: List[Dict[str, any]], 
                       scan_time: float) -> str:
    """
    Format scan results with colorized output for enhanced readability.
    
    Args:
        target (str): Target hostname or IP
        results (List[Dict]): Scan results from tcp_scan_ports
        scan_time (float): Total scan time in seconds
        
    Returns:
        str: Formatted and colorized results string
        
    Learning points:
        - Professional output formatting with colors
        - User-friendly result presentation
        - Performance metrics display
    """
    # Filter open ports for the summary
    open_ports = [r for r in results if r['status'] == 'open']
    closed_ports = [r for r in results if r['status'] == 'closed']
    filtered_ports = [r for r in results if r['status'] == 'filtered']
    
    # Build the colorized report
    report_lines = []
    
    # Header with colors
    report_lines.append(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    report_lines.append(f"{Fore.CYAN}{Back.BLUE} PortSpy Scan Results {Style.RESET_ALL}")
    report_lines.append(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    report_lines.append(f"{Fore.WHITE}Target: {Fore.YELLOW}{target}{Style.RESET_ALL}")
    report_lines.append(f"{Fore.WHITE}Scanned {Fore.YELLOW}{len(results)}{Style.RESET_ALL} ports in {Fore.GREEN}{scan_time:.2f}{Style.RESET_ALL} seconds")
    report_lines.append("")
    
    if open_ports:
        report_lines.append(f"{Fore.GREEN}Open ports found:{Style.RESET_ALL}")
        report_lines.append(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
        report_lines.append(f"{Fore.WHITE}{'PORT':<8} {'SERVICE':<15} {'STATUS':<10} {'TIME':<8}{Style.RESET_ALL}")
        report_lines.append(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
        
        for result in open_ports:
            port_str = f"{Fore.YELLOW}{result['port']:<8}{Style.RESET_ALL}"
            service_str = f"{Fore.CYAN}{result['service']:<15}{Style.RESET_ALL}"
            status_str = f"{Fore.GREEN}{result['status'].upper():<10}{Style.RESET_ALL}"
            time_str = f"{Fore.WHITE}{result['response_time']:<8.3f}s{Style.RESET_ALL}"
            
            report_lines.append(f"{port_str} {service_str} {status_str} {time_str}")
    else:
        report_lines.append(f"{Fore.YELLOW}No open ports found.{Style.RESET_ALL}")
    
    # Add summary of other port statuses if in verbose mode
    if closed_ports or filtered_ports:
        report_lines.append("")
        if closed_ports:
            report_lines.append(f"{Fore.RED}Closed ports: {len(closed_ports)}{Style.RESET_ALL}")
        if filtered_ports:
            report_lines.append(f"{Fore.YELLOW}Filtered ports: {len(filtered_ports)}{Style.RESET_ALL}")
    
    report_lines.append("")
    report_lines.append(f"{Fore.WHITE}Scan Summary:{Style.RESET_ALL}")
    report_lines.append(f"  {Fore.WHITE}Total ports scanned: {Fore.YELLOW}{len(results)}{Style.RESET_ALL}")
    report_lines.append(f"  {Fore.WHITE}Open ports found: {Fore.GREEN}{len(open_ports)}{Style.RESET_ALL}")
    report_lines.append(f"  {Fore.WHITE}Scan time: {Fore.GREEN}{scan_time:.2f}{Style.RESET_ALL} seconds")
    
    # Calculate and display performance metrics
    if open_ports:
        avg_time = sum(r['response_time'] for r in open_ports) / len(open_ports)
        report_lines.append(f"  {Fore.WHITE}Average response time (open ports): {Fore.GREEN}{avg_time:.3f}s{Style.RESET_ALL}")
        
        # Ports per second metric
        ports_per_sec = len(results) / scan_time if scan_time > 0 else 0
        report_lines.append(f"  {Fore.WHITE}Scan rate: {Fore.GREEN}{ports_per_sec:.1f}{Style.RESET_ALL} ports/sec")
    
    report_lines.append(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    
    return "\n".join(report_lines)



