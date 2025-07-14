#!/data/data/com.termux/files/usr/bin/python3

import re
import sys
import argparse
import os
from pathlib import Path

# ANSI escape codes for colored output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# Try to enable readline for better input handling
try:
    import readline
    # Enable history and arrow key navigation
    readline.parse_and_bind("tab: complete")
    readline.set_history_length(100)
except ImportError:
    pass  # Continue without readline if unavailable

def colorize_matches(text, pattern, color_code=Colors.RED):
    """Apply color to regex matches in text"""
    try:
        compiled = re.compile(pattern)
    except re.error as e:
        return None, f"Regex error: {str(e)}"
    
    last_end = 0
    output = []
    match_count = 0
    
    for match in compiled.finditer(text):
        start, end = match.span()
        
        # Add non-matched part
        output.append(text[last_end:start])
        
        # Add colored match
        output.append(f"{color_code}{text[start:end]}{Colors.RESET}")
        
        last_end = end
        match_count += 1
    
    # Add remaining text
    output.append(text[last_end:])
    
    return ''.join(output), match_count

def get_multiline_input(prompt=""):
    """Get multi-line input with proper handling"""
    print(prompt + " (Press Ctrl+D or Ctrl+Z when finished):")
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass  # Ctrl+D pressed
    
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(
        description='Regex Learning Tool - Test regular expressions with colored matches',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-t', '--text', help='Input text directly')
    parser.add_argument('-f', '--file', help='Path to text file')
    parser.add_argument('-p', '--pattern', help='Regex pattern to test')
    parser.add_argument('-c', '--color', 
                        choices=['red', 'green', 'yellow', 'blue', 'magenta', 'cyan'],
                        default='red',
                        help='Highlight color (default: red)')
    
    args = parser.parse_args()
    
    # Get color code
    color_map = {
        'red': Colors.RED,
        'green': Colors.GREEN,
        'yellow': Colors.YELLOW,
        'blue': Colors.BLUE,
        'magenta': Colors.MAGENTA,
        'cyan': Colors.CYAN
    }
    color_code = color_map[args.color]
    
    # Get input text
    text = ""
    if args.text:
        text = args.text
    elif args.file:
        try:
            file_path = Path(args.file)
            if not file_path.exists():
                print(f"Error: File not found - {args.file}")
                sys.exit(1)
            text = file_path.read_text()
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            sys.exit(1)
    else:
        # Interactive mode with proper multi-line input
        print(f"{Colors.CYAN}Regex Learning Tool (Interactive Mode){Colors.RESET}")
        text = get_multiline_input("Enter text to test against")
        if not text:
            print("No text provided. Exiting.")
            sys.exit(0)
    
    # Pattern handling
    pattern = args.pattern
    print(f"\n{Colors.CYAN}Enter regex patterns to test (Ctrl+C to exit):{Colors.RESET}")
    
    while True:
        try:
            if not pattern:
                pattern = input("\nRegex pattern> ").strip()
                if not pattern:
                    continue
            
            # Test the pattern
            result, match_count = colorize_matches(text, pattern, color_code)
            
            if result is None:
                print(match_count)  # Actually contains error message
            else:
                print("\n" + "-" * 50)
                print(f"Matches found: {Colors.YELLOW}{match_count}{Colors.RESET}")
                print(f"Pattern: {Colors.CYAN}{pattern}{Colors.RESET}")
                print("-" * 50)
                print(result)
                print("-" * 50)
            
            # Reset pattern for next iteration
            pattern = None
            
        except re.error as e:
            print(f"Regex error: {str(e)}")
            pattern = None
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
