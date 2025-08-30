import os
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "Output"
OUTPUT_DIR.mkdir(exist_ok=True)

DEFAULT_RSA_VALUES = {
    'n': 0,
    'ct': 0,
    'e': 0,
    'p': 0,
    'q': 0,
    'phi': 0,
    'd': 0
}

ANIMATIONS = [
    "[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]",
    "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]",
    "[■■■■■■■■■□]", "[■■■■■■■■■■]"
]

MAIN_COMMANDS = {
    'options': ['ops', 'options', 'option'],
    'start': ['mood', 'start', 'breakall'],
    'set': ['set'],
    'help': ['help', '?'],
    'exit': ['exit', 'quit', 'q']
}

SOLVE_COMMANDS = {
    'options': ['ops', 'options', 'option'],
    'factor': ['factorize', 'fact', 'factors'],
    'square': ['racine', 'square', 'sqrt', 'sqr'],
    'modulare': ['mod', 'modulare', 'modular'],
    'pwn': ['reveal', 'decrypt', 'solve'],
    'ssh': ['pemKey', 'ssh', 'pem'],
    'wiener': ['wiener', 'wien'],
    'common_modulus': ['common', 'cm'],
    'pollard_rho': ['pollard', 'rho'],
    'fermat': ['fermat', 'fm'],
    'help': ['help', '?'],
    'exit': ['exit', 'quit', 'back']
}

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = PROJECT_ROOT / "solvecrypto.log"