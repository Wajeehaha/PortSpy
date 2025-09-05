#!/usr/bin/env python3
"""
Test script to demonstrate interactive mode
"""
import subprocess
import sys

def test_interactive_mode():
    """Test the interactive mode of PortSpy"""
    
    # Simulate user input for fully interactive mode
    user_inputs = [
        "google.com",  # target
        "80,443"       # ports
    ]
    
    input_string = "\n".join(user_inputs) + "\n"
    
    try:
        # Run PortSpy in interactive mode with simulated input
        result = subprocess.run(
            [sys.executable, "src/portspy.py", "--timeout", "2"],
            input=input_string,
            text=True,
            capture_output=True,
            cwd="."
        )
        
        print("=== INTERACTIVE MODE TEST ===")
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        print(f"Return code: {result.returncode}")
        
    except Exception as e:
        print(f"Error running test: {e}")

if __name__ == "__main__":
    test_interactive_mode()
