#!/usr/bin/env python3
"""
SolveCrypto v2.0 - Advanced RSA Challenge Solver
Created by Mooder1

Main entry point for the RSA cryptography challenge solver.
"""

import sys
import logging
from typing import Dict, Any, Optional
import click
from pathlib import Path

from config import (
    DEFAULT_RSA_VALUES, MAIN_COMMANDS, OUTPUT_DIR, LOG_FILE
)
from utils import (
    setup_logging, display_banner, validate_integer_input,
    format_rsa_options, display_help, print_success, print_error,
    print_info, clear_screen, animated_loading
)
from MoodRSA import MoodRSA


class SolveCryptoMain:
    """Main application class for SolveCrypto."""
    
    def __init__(self, debug: bool = False):
        self.rsa_params = DEFAULT_RSA_VALUES.copy()
        self.logger = setup_logging(LOG_FILE, logging.DEBUG if debug else logging.INFO)
        self.running = True
        
    def run(self) -> None:
        """Main application loop."""
        try:
            clear_screen()
            display_banner()
            animated_loading("Initializing SolveCrypto", 1.5)
            clear_screen()
            
            print_info("Welcome to SolveCrypto v2.0! Type 'help' for commands.")
            
            while self.running:
                try:
                    cmd = input("\n{Mooder1🤠} ==> ").strip()
                    if not cmd:
                        continue
                        
                    self._process_command(cmd)
                except KeyboardInterrupt:
                    print_info("\nUse 'exit' to quit properly.")
                except EOFError:
                    break
                    
        except Exception as e:
            print_error(f"Application error: {e}")
            self.logger.error(f"Application error: {e}")
        finally:
            print_info("Thanks for using SolveCrypto! 🔐")
    
    def _process_command(self, cmd: str) -> None:
        """Process user commands."""
        parts = cmd.split()
        if not parts:
            return
            
        command = parts[0].lower()
        
        for cmd_type, aliases in MAIN_COMMANDS.items():
            if command in aliases:
                if cmd_type == 'set' and len(parts) >= 3:
                    self._set_parameter(parts[1].lower(), parts[2])
                elif cmd_type == 'start':
                    self._start_solver()
                elif cmd_type == 'options':
                    self._show_options()
                elif cmd_type == 'help':
                    display_help(MAIN_COMMANDS, "Main Commands")
                elif cmd_type == 'exit':
                    self.running = False
                return
        
        print_error(f"Unknown command: {command}. Type 'help' for available commands.")
    
    def _set_parameter(self, key: str, value: str) -> None:
        """Set RSA parameter with validation."""
        valid_params = {'n', 'ct', 'e', 'p', 'q', 'phi', 'd'}
        
        if key not in valid_params:
            print_error(f"Invalid parameter: {key}. Valid: {', '.join(valid_params)}")
            return
        
        validated_value = validate_integer_input(value, key)
        if validated_value is None:
            return
        
        self.rsa_params[key] = validated_value
        print_success(f"Set {key} = {validated_value}")
        self.logger.info(f"Parameter set: {key} = {validated_value}")
    
    def _start_solver(self) -> None:
        """Start the RSA solver interface."""
        try:
            solver = MoodRSA(**self.rsa_params)
            solver.run()
        except Exception as e:
            print_error(f"Solver error: {e}")
            self.logger.error(f"Solver error: {e}")
    
    def _show_options(self) -> None:
        """Display current RSA parameters."""
        from rich.console import Console
        console = Console()
        table = format_rsa_options(**self.rsa_params)
        console.print(table)


@click.command()
@click.option('--debug', is_flag=True, help='Enable debug logging')
@click.option('--version', is_flag=True, help='Show version information')
def main(debug: bool, version: bool) -> None:
    """SolveCrypto v2.0 - Advanced RSA Challenge Solver."""
    if version:
        print("SolveCrypto v2.0.0")
        print("Advanced RSA Challenge Solver")
        print("Created by Mooder1")
        return
    
    app = SolveCryptoMain(debug=debug)
    app.run()


if __name__ == "__main__":
    main()