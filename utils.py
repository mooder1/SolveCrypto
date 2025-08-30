import os
import time
import logging
from typing import Union, Optional
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
import colorama
from colorama import Fore, Style

colorama.init()
console = Console()

def setup_logging(log_file: Path, level: int = logging.INFO) -> logging.Logger:
    """Setup logging configuration."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def animated_loading(text: str = "Loading", duration: float = 2.0):
    """Display animated loading with progress bar."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description=text, total=None)
        time.sleep(duration)

def display_banner():
    """Display application banner."""
    banner = """
╔═══════════════════════════════════════════╗
║          SolveCrypto v2.0                 ║
║     Advanced RSA Challenge Solver         ║
║                                           ║
║         Created by Mooder1 🤠             ║
╚═══════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold blue"))

def validate_integer_input(value: str, param_name: str) -> Optional[int]:
    """Validate integer input with proper error handling."""
    try:
        if not value or value == '0':
            return 0
        return int(value)
    except ValueError:
        console.print(f"[red]Error: {param_name} must be a valid integer[/red]")
        return None

def format_rsa_options(n: int = 0, ct: int = 0, e: int = 0, p: int = 0, 
                      q: int = 0, phi: int = 0, d: int = 0) -> str:
    """Format RSA options display."""
    table = Table(title="Current RSA Parameters", show_header=True)
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="yellow")
    
    table.add_row("n (modulus)", str(n) if n else "Not set")
    table.add_row("ct (ciphertext)", str(ct) if ct else "Not set")
    table.add_row("e (exponent)", str(e) if e else "Not set")
    table.add_row("p (prime 1)", str(p) if p else "Not set")
    table.add_row("q (prime 2)", str(q) if q else "Not set")
    table.add_row("φ(n) (phi)", str(phi) if phi else "Not set")
    table.add_row("d (private exp)", str(d) if d else "Not set")
    
    return table

def display_help(commands: dict, title: str = "Available Commands"):
    """Display help information."""
    table = Table(title=title, show_header=True)
    table.add_column("Command", style="cyan")
    table.add_column("Aliases", style="yellow")
    table.add_column("Description", style="green")
    
    descriptions = {
        'set': 'Set RSA parameters (e.g., set n 12345)',
        'options': 'Display current RSA parameters',
        'start': 'Enter solving mode',
        'factor': 'Factor the modulus n',
        'square': 'Try square root attack',
        'modulare': 'Modular arithmetic operations',
        'pwn': 'Decrypt the ciphertext',
        'ssh': 'Generate SSH private key',
        'wiener': 'Wiener attack for small d',
        'common_modulus': 'Common modulus attack',
        'pollard_rho': 'Pollard rho factorization',
        'fermat': 'Fermat factorization',
        'help': 'Show this help message',
        'exit': 'Exit the program'
    }
    
    for cmd, aliases in commands.items():
        desc = descriptions.get(cmd, "No description available")
        table.add_row(cmd, ", ".join(aliases), desc)
    
    console.print(table)

def print_success(message: str):
    """Print success message."""
    console.print(f"[green]✓ {message}[/green]")

def print_error(message: str):
    """Print error message."""
    console.print(f"[red]✗ {message}[/red]")

def print_info(message: str):
    """Print info message."""
    console.print(f"[blue]ℹ {message}[/blue]")

def print_warning(message: str):
    """Print warning message."""
    console.print(f"[yellow]⚠ {message}[/yellow]")

def save_result(content: str, filename: str, output_dir: Path):
    """Save result to file with error handling."""
    try:
        output_path = output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print_success(f"Result saved to {output_path}")
        return True
    except Exception as e:
        print_error(f"Failed to save result: {e}")
        return False