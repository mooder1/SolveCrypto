# SolveCrypto v2.0

Advanced RSA cryptography challenge solver with multiple attack methods and modern Python implementation.

## 🚀 Features

### RSA Attack Methods
- **Factorization Attacks**
  - FactorDB integration for known factors
  - Trial division for small factors  
  - Pollard's rho algorithm
  - Fermat factorization for close primes
  
- **Specialized Attacks**
  - Wiener's attack for small private exponents
  - Common modulus attack
  - Low public exponent attacks (e.g., e=3)
  - Square root attacks for special cases

- **Mathematical Tools**
  - Modular arithmetic operations
  - Quadratic equation solving
  - Cube root attacks
  - Extended GCD algorithms

- **Key Generation**
  - SSH private key generation from RSA parameters
  - PEM format output with proper permissions warnings

### Modern Features
- **Rich CLI Interface**: Colorful terminal output with tables and progress bars
- **Robust Error Handling**: Comprehensive input validation and error messages
- **Logging System**: Detailed logging for debugging and audit trails
- **Type Hints**: Full type annotation for better code maintainability
- **Modular Architecture**: Clean separation of concerns and extensible design

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup
```bash
# Clone or download the project
cd SolveCrypto

# Install dependencies
pip install -r requirements.txt

# Optional: Install in development mode
pip install -e .
```

### Dependencies
- `factordb-python` - Integer factorization via FactorDB
- `pycryptodome` - RSA operations and cryptographic functions
- `gmpy2` - High-precision arithmetic
- `click` - Command-line interface framework
- `rich` - Rich text and beautiful formatting
- `colorama` - Cross-platform colored terminal output
- `sympy` - Symbolic mathematics

## 🎯 Usage

### Basic Usage
```bash
# Start the interactive application
python3 main.py

# Show version information
python3 main.py --version

# Enable debug logging
python3 main.py --debug
```

### Interactive Commands

#### Main Level Commands
- `set <param> <value>` - Set RSA parameters (n, ct, e, p, q, phi, d)
- `options` - Display current RSA parameters
- `start` - Enter RSA solving mode
- `help` - Show available commands
- `exit` - Exit the application

#### Solver Level Commands
- `factor` - Factor the modulus using multiple methods
- `square` - Try square root attack for special cases
- `wiener` - Wiener's attack for small private exponents
- `common` - Common modulus attack (requires two ciphertexts)
- `pollard` - Pollard's rho factorization
- `fermat` - Fermat factorization for close primes
- `modulare` - Modular arithmetic operations
- `pwn` - Decrypt using available parameters
- `ssh` - Generate SSH private key from RSA parameters
- `options` - Display current parameters
- `help` - Show attack methods
- `exit` - Return to main menu

### Example Session
```bash
$ python3 main.py

{Mooder1🤠} ==> set n 3233
✓ Set n = 3233

{Mooder1🤠} ==> set e 17
✓ Set e = 17

{Mooder1🤠} ==> set ct 2790
✓ Set ct = 2790

{Mooder1🤠} ==> start

{мσσɔεя1💀} ==> factor
ℹ Trying factorization methods...
✓ Factors found: [61, 53]
✓ Calculated φ(n) = 3120
✓ Calculated private exponent d = 2753

{мσσɔεя1💀} ==> pwn
✓ Decrypted integer: 310939249775
✓ Decrypted text: Hello!
✓ Result saved to Output/decryption_result.txt
```

## 🔧 Configuration

### Custom Configuration
Edit `config.py` to customize:
- Default RSA parameter values
- Command aliases and mappings
- Output directory location
- Animation and UI settings
- Logging configuration

### Environment Variables
- `SOLVECRYPTO_LOG_LEVEL` - Set logging level (DEBUG, INFO, WARNING, ERROR)
- `SOLVECRYPTO_OUTPUT_DIR` - Custom output directory path

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Run all tests
python3 test_solver.py

# Run with verbose output
python3 -m pytest test_solver.py -v

# Run specific test class
python3 -m unittest test_solver.TestSolverFunctions -v
```

## 📁 Project Structure

```
SolveCrypto/
├── main.py              # Main application entry point
├── solver.py            # Core RSA solving algorithms
├── MoodRSA.py          # Interactive solver interface
├── config.py           # Configuration constants
├── utils.py            # Utility functions and helpers
├── settings.py         # Legacy settings (deprecated)
├── test_solver.py      # Comprehensive test suite
├── requirements.txt    # Python dependencies
├── setup.py           # Package setup configuration
├── CLAUDE.md          # Claude Code guidance
├── README.md          # This file
└── Output/            # Generated keys and results
    ├── id_rsa         # Generated SSH keys
    └── *.txt          # Decryption results
```

## 🔒 Security Considerations

- **Key Storage**: Generated SSH keys are saved with warnings about proper permissions
- **Input Validation**: All user inputs are validated and sanitized
- **Safe Operations**: Mathematical operations use safe bounds checking
- **No Hardcoded Secrets**: No sensitive information stored in code

## 🚨 Attack Method Details

### Factorization Methods
1. **FactorDB Lookup** - Query online database for known factors
2. **Trial Division** - Systematic division by small primes
3. **Pollard's Rho** - Probabilistic factorization algorithm
4. **Fermat's Method** - Difference of squares for close primes

### Specialized Attacks
1. **Wiener's Attack** - Exploits small private exponents using continued fractions
2. **Common Modulus** - Attacks multiple ciphertexts with same modulus
3. **Low Public Exponent** - Exploits small public exponents (e=3, e=5)
4. **Square Root Attack** - For perfect square moduli

### When to Use Each Attack
- **Small n (< 10^10)**: Start with trial division
- **Close primes**: Use Fermat factorization
- **Small e (3, 17, 65537)**: Try low exponent attacks
- **Multiple ciphertexts**: Consider common modulus attack
- **Large e**: Attempt Wiener's attack

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -e .[dev]

# Run tests before committing
python3 test_solver.py

# Check code style
python3 -m flake8 *.py

# Type checking
python3 -m mypy *.py
```

### Adding New Attack Methods
1. Add the algorithm to `solver.py`
2. Create corresponding method in `MoodRSA.py` following the `_attack_*` pattern
3. Add command aliases to `config.py`
4. Write tests in `test_solver.py`
5. Update documentation

## 📄 License

This project is open source. See the LICENSE file for details.

## 🙏 Acknowledgments

- **FactorDB** - Online integer factorization database
- **PyCryptodome** - Comprehensive cryptography library
- **GMPY2** - High-performance mathematical operations
- **Rich** - Beautiful terminal formatting

## 📞 Support

- **Issues**: Report bugs and feature requests via GitHub issues
- **Documentation**: See `CLAUDE.md` for development guidance
- **Testing**: Run test suite for validation

---

**SolveCrypto v2.0** - Making RSA challenge solving accessible and efficient! 🔐