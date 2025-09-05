#!/usr/bin/env python3
"""
PortSpy - TCP Port Scanner

A simple, educational TCP port scanner that demonstrates
networking concepts and socket programming in Python.

Enhanced with colorful output and progress bars for better UX.

Author: [Your Name]  
Date: September 6, 2025
"""

import argparse
import time
from typing import List
from colorama import init, Fore, Back, Style

from host_resolver import validate_target
from port_parser import parse_ports
from tcp_scanner import tcp_scan_ports, format_scan_results

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def get_user_input():
    """Get target and ports from user interactively with colorful prompts."""
    print(f"\n{Fore.YELLOW}>> Interactive Mode{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*30}{Style.RESET_ALL}")
    
    # Get target
    while True:
        target = input(f"\n{Fore.GREEN}Enter target hostname or IP address: {Style.RESET_ALL}").strip()
        if target:
            break
        print(f"{Fore.RED}[X] Target cannot be empty. Please try again.{Style.RESET_ALL}")
    
    # Get ports with helpful examples
    print(f"\n{Fore.YELLOW}Port Examples:{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}80,443,22{Style.RESET_ALL}           - Specific ports")
    print(f"  {Fore.CYAN}80-90{Style.RESET_ALL}               - Port range") 
    print(f"  {Fore.CYAN}80,443,8000-8010{Style.RESET_ALL}    - Mixed format")
    print(f"  {Fore.CYAN}common{Style.RESET_ALL}              - Common ports (80,443,22,21,25,53,110,995,993,143)")
    print(f"  {Fore.CYAN}all{Style.RESET_ALL}                 - All ports (1-65535) - Very slow!")
    
    while True:
        ports_input = input(f"\n{Fore.GREEN}Enter ports to scan: {Style.RESET_ALL}").strip()
        if ports_input:
            # Handle special keywords
            if ports_input.lower() == 'common':
                ports_input = '80,443,22,21,25,53,110,995,993,143'
            elif ports_input.lower() == 'all':
                ports_input = '1-65535'
                print(f"{Fore.YELLOW}[!] Scanning all ports will take a very long time!{Style.RESET_ALL}")
                confirm = input(f"{Fore.RED}Are you sure? (y/N): {Style.RESET_ALL}").strip().lower()
                if confirm != 'y':
                    continue
            break
        print(f"{Fore.RED}[X] Ports cannot be empty. Please try again.{Style.RESET_ALL}")
    
    return target, ports_input


def main():
    """Main entry point for the PortSpy application."""
    # Print colorful banner
    print(f"\n{Fore.CYAN}{Back.BLUE}  PortSpy - TCP Port Scanner  {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}")
    
    parser = argparse.ArgumentParser(
        description=f"{Fore.YELLOW}PortSpy - A simple TCP port scanner with colorful output{Style.RESET_ALL}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Fore.GREEN}Examples:{Style.RESET_ALL}
  {Fore.CYAN}%(prog)s{Style.RESET_ALL}                              - Interactive mode
  {Fore.CYAN}%(prog)s google.com{Style.RESET_ALL}                    - Prompt for ports
  {Fore.CYAN}%(prog)s google.com -p 80,443{Style.RESET_ALL}          - Full command line
  {Fore.CYAN}%(prog)s 192.168.1.1 -p 80,443,22{Style.RESET_ALL}     - IP with ports
  {Fore.CYAN}%(prog)s example.com -p 80-85,443,8080{Style.RESET_ALL} - Port ranges
        """
    )
    
    parser.add_argument(
        'target',
        nargs='?',  # Make target optional
        help='Target hostname or IP address to scan (optional - will prompt if not provided)'
    )
    
    parser.add_argument(
        '-p', '--ports',
        help='Ports to scan (optional - will prompt if not provided). '
             'Examples: "80,443", "80-90", "80,443,8000-8010"'
    )
    
    parser.add_argument(
        '-t', '--threads',
        type=int,
        default=50,
        help='Number of threads to use (default: 50)'
    )
    
    parser.add_argument(
        '--timeout',
        type=float,
        default=2.0,
        help='Connection timeout in seconds (default: 2.0)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--no-progress',
        action='store_true',
        help='Disable progress bar'
    )
    
    args = parser.parse_args()
    
    try:
        # Handle interactive input if target or ports not provided
        target = args.target
        ports_input = args.ports
        
        # Interactive mode if no target provided
        if not target:
            target, ports_input = get_user_input()
        # Semi-interactive mode if target provided but no ports
        elif not ports_input:
            print(f"\n{Fore.YELLOW}Port Examples:{Style.RESET_ALL}")
            print(f"  {Fore.CYAN}80,443,22{Style.RESET_ALL}           - Specific ports")
            print(f"  {Fore.CYAN}80-90{Style.RESET_ALL}               - Port range") 
            print(f"  {Fore.CYAN}80,443,8000-8010{Style.RESET_ALL}    - Mixed format")
            print(f"  {Fore.CYAN}common{Style.RESET_ALL}              - Common ports")
            
            while True:
                ports_input = input(f"\n{Fore.GREEN}Enter ports to scan: {Style.RESET_ALL}").strip()
                if ports_input:
                    if ports_input.lower() == 'common':
                        ports_input = '80,443,22,21,25,53,110,995,993,143'
                    break
                print(f"{Fore.RED}❌ Ports cannot be empty. Please try again.{Style.RESET_ALL}")
        else:
            # Use default common ports if not specified
            if not ports_input:
                ports_input = '80,443,22,21,25,53,110,995,993,143'
        
        # Step 1: Validate and resolve target
        print(f"\n{Fore.YELLOW}[>] Resolving target: {Fore.CYAN}{target}{Style.RESET_ALL}")
        target_result = validate_target(target)
        
        # Extract IP from the validation result
        if isinstance(target_result, tuple):
            target_ip = target_result[0]  # IP address
            resolution_msg = target_result[1]  # Message
            print(f"{Fore.GREEN}[+] Target resolved to: {Fore.YELLOW}{target_ip}{Style.RESET_ALL}")
        else:
            target_ip = target_result  # Direct IP address
            print(f"{Fore.GREEN}[+] Target: {Fore.YELLOW}{target_ip}{Style.RESET_ALL}")
        
        # Step 2: Parse port specification
        print(f"\n{Fore.YELLOW}[>] Parsing ports: {Fore.CYAN}{ports_input}{Style.RESET_ALL}")
        ports = parse_ports(ports_input)
        print(f"{Fore.GREEN}[+] Will scan {Fore.YELLOW}{len(ports)}{Style.RESET_ALL} ports")
        
        if args.verbose:
            print(f"{Fore.WHITE}Port list: {sorted(ports)}{Style.RESET_ALL}")
        
        # Step 3: Perform the scan
        print(f"\n{Fore.YELLOW}[>] Starting TCP scan with {Fore.CYAN}{args.threads}{Style.RESET_ALL} threads...")
        print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
        
        start_time = time.time()
        results = tcp_scan_ports(
            ip=target_ip,
            ports=ports,
            max_threads=args.threads,
            timeout=args.timeout,
            show_progress=not args.no_progress
        )
        scan_time = time.time() - start_time
        
        # Step 4: Display results
        print()  # Add some spacing
        report = format_scan_results(
            target=f"{target} ({target_ip})",
            results=results,
            scan_time=scan_time
        )
        print(report)
        
        # Return different exit codes based on results
        open_ports = [r for r in results if r['status'] == 'open']
        return 0 if open_ports else 1
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Scan interrupted by user{Style.RESET_ALL}")
        return 1
        
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        return 1


if __name__ == "__main__":
    exit(main())
