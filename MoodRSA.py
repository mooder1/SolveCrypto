#!/usr/bin/env python3
"""
RSA Solver Interface - Enhanced version with multiple attack methods
"""

import logging
from typing import Optional, Dict, Any
from pathlib import Path
from Crypto.Util.number import long_to_bytes

from config import SOLVE_COMMANDS, OUTPUT_DIR
from utils import (
    clear_screen, animated_loading, print_success, print_error,
    print_info, print_warning, display_help, save_result
)
import solver

logger = logging.getLogger(__name__)


class MoodRSA:
    """Advanced RSA solver with multiple attack methods."""
    
    def __init__(self, n: int = 0, ct: int = 0, e: int = 0, p: int = 0, 
                 q: int = 0, phi: int = 0, d: int = 0):
        self.rsa_params = {
            'n': n, 'ct': ct, 'e': e, 'p': p, 
            'q': q, 'phi': phi, 'd': d
        }
        self.running = True
        
    def run(self) -> None:
        """Main solver loop."""
        animated_loading("Starting RSA Solver", 1.0)
        clear_screen()
        
        print_info("RSA Solver Mode - Type 'help' for available attacks")
        
        while self.running:
            try:
                cmd = input("\n{мσσɔεя1💀} ==> ").strip().lower()
                if not cmd:
                    continue
                    
                self._process_command(cmd)
                
            except KeyboardInterrupt:
                print_info("\nUse 'exit' to return to main menu.")
            except EOFError:
                break
    
    def _process_command(self, cmd: str) -> None:
        """Process solver commands."""
        for cmd_type, aliases in SOLVE_COMMANDS.items():
            if cmd in aliases:
                method_name = f"_attack_{cmd_type}"
                if hasattr(self, method_name):
                    getattr(self, method_name)()
                else:
                    print_error(f"Attack method {cmd_type} not implemented yet")
                return
        
        print_error(f"Unknown command: {cmd}. Type 'help' for available attacks.")
    
    def _attack_factor(self) -> None:
        """Factor the modulus n using various methods."""
        n = self.rsa_params['n']
        if not n:
            print_error("Modulus n is not set")
            return
        
        print_info("Trying factorization methods...")
        
        # Try FactorDB first
        factors = solver.factorize_with_factordb(n)
        if len(factors) == 2:
            self.rsa_params['p'] = factors[0]
            self.rsa_params['q'] = factors[1]
            self._calculate_phi_and_d()
            return
        elif len(factors) > 2:
            print_info("Multiple factors found, calculating phi...")
            phi = 1
            for factor in factors:
                phi *= (factor - 1)
            self.rsa_params['phi'] = phi
            self._calculate_d()
            return
        
        # Try trial division
        print_info("Trying trial division...")
        factors = solver.trial_division(n)
        if len(factors) == 2:
            self.rsa_params['p'] = factors[0]
            self.rsa_params['q'] = factors[1]
            self._calculate_phi_and_d()
            return
        
        # Try Pollard's rho
        print_info("Trying Pollard's rho...")
        factor = solver.pollard_rho_factorization(n)
        if factor and factor != n:
            self.rsa_params['p'] = factor
            self.rsa_params['q'] = n // factor
            self._calculate_phi_and_d()
            return
        
        # Try Fermat factorization
        print_info("Trying Fermat factorization...")
        result = solver.fermat_factorization(n)
        if result:
            self.rsa_params['p'], self.rsa_params['q'] = result
            self._calculate_phi_and_d()
            return
        
        print_error("All factorization methods failed")
    
    def _attack_square(self) -> None:
        """Square root attack for special cases."""
        n = self.rsa_params['n']
        if not n:
            print_error("Modulus n is not set")
            return
        
        try:
            p = solver.integer_square_root(n)
            if p * p == n:
                print_success(f"Perfect square found: {p}")
                self.rsa_params['p'] = p
                self.rsa_params['q'] = p
                self._decrypt_and_display()
            else:
                print_error("n is not a perfect square")
        except Exception as e:
            print_error(f"Square root attack failed: {e}")
    
    def _attack_wiener(self) -> None:
        """Wiener's attack for small private exponents."""
        n, e = self.rsa_params['n'], self.rsa_params['e']
        if not n or not e:
            print_error("Both n and e must be set")
            return
        
        print_info("Attempting Wiener's attack...")
        d = solver.wiener_attack(n, e)
        if d:
            self.rsa_params['d'] = d
            print_success(f"Private exponent found: {d}")
            self._decrypt_and_display()
        else:
            print_error("Wiener's attack failed")
    
    def _attack_common_modulus(self) -> None:
        """Common modulus attack."""
        print_info("Common modulus attack requires two ciphertexts with same n but different e values")
        try:
            n = self.rsa_params['n']
            c1 = self.rsa_params['ct']
            e1 = self.rsa_params['e']
            
            if not all([n, c1, e1]):
                print_error("n, ct, and e must be set")
                return
                
            c2 = int(input("Enter second ciphertext: "))
            e2 = int(input("Enter second exponent: "))
            
            result = solver.common_modulus_attack(n, c1, c2, e1, e2)
            if result:
                self._display_result(result)
            else:
                print_error("Common modulus attack failed")
        except ValueError:
            print_error("Invalid input for common modulus attack")
    
    def _attack_pollard_rho(self) -> None:
        """Pollard's rho factorization."""
        n = self.rsa_params['n']
        if not n:
            print_error("Modulus n is not set")
            return
        
        print_info("Running Pollard's rho factorization...")
        factor = solver.pollard_rho_factorization(n)
        if factor and factor != n:
            self.rsa_params['p'] = factor
            self.rsa_params['q'] = n // factor
            print_success(f"Factors found: {factor} and {n // factor}")
            self._calculate_phi_and_d()
        else:
            print_error("Pollard's rho failed")
    
    def _attack_fermat(self) -> None:
        """Fermat factorization for close primes."""
        n = self.rsa_params['n']
        if not n:
            print_error("Modulus n is not set")
            return
        
        print_info("Running Fermat factorization...")
        result = solver.fermat_factorization(n)
        if result:
            p, q = result
            self.rsa_params['p'] = p
            self.rsa_params['q'] = q
            print_success(f"Factors found: {p} and {q}")
            self._calculate_phi_and_d()
        else:
            print_error("Fermat factorization failed")
    
    def _attack_modulare(self) -> None:
        """Modular arithmetic operations."""
        print_info("Modular Operations:")
        print_info("1. Linear equations")
        print_info("2. Quadratic equations")
        print_info("3. Cube root attack (e=3)")
        
        try:
            choice = int(input("Choose operation [1-3]: "))
            
            if choice == 1:
                print_info("Linear modular equations not implemented yet")
            elif choice == 2:
                print_info("Enter coefficients for ax² + bx + c ≡ 0 (mod n)")
                a = int(input("a: "))
                b = int(input("b: "))
                c = int(input("c: "))
                n = self.rsa_params['n']
                if not n:
                    n = int(input("n: "))
                
                solutions = solver.Modulare_Equation_Order2(a, b, c, n)
                if solutions:
                    print_success(f"Solutions: {solutions}")
                else:
                    print_error("No solutions found")
            elif choice == 3:
                ct = self.rsa_params['ct']
                n = self.rsa_params.get('n')
                if not ct:
                    print_error("Ciphertext ct is not set")
                    return
                
                result = solver.cube_root_attack(ct, n)
                if result:
                    print_success(f"Cube root result: {result}")
                    try:
                        text = result.decode('utf-8', errors='ignore')
                        print_info(f"Decoded text: {text}")
                    except:
                        print_info(f"Raw bytes: {result}")
                else:
                    print_error("Cube root attack failed")
        except ValueError:
            print_error("Invalid input")
    
    def _attack_pwn(self) -> None:
        """Decrypt using available parameters."""
        result = solver.decrypt_rsa(**self.rsa_params)
        if result is not None:
            self._display_result(result)
        else:
            print_error("Decryption failed - insufficient parameters")
    
    def _attack_ssh(self) -> None:
        """Generate SSH private key."""
        params = self.rsa_params
        required = ['n', 'e', 'd', 'p', 'q']
        
        if not all(params[key] for key in required):
            missing = [key for key in required if not params[key]]
            print_error(f"Missing required parameters: {', '.join(missing)}")
            return
        
        output_path = OUTPUT_DIR / "id_rsa"
        success = solver.generate_ssh_key(
            params['n'], params['e'], params['d'], 
            params['p'], params['q'], str(output_path)
        )
        
        if success:
            print_info(f"SSH key saved to {output_path}")
    
    def _attack_options(self) -> None:
        """Display current RSA parameters."""
        from utils import format_rsa_options
        from rich.console import Console
        
        console = Console()
        table = format_rsa_options(**self.rsa_params)
        console.print(table)
    
    def _attack_help(self) -> None:
        """Display help information."""
        display_help(SOLVE_COMMANDS, "RSA Attack Methods")
    
    def _attack_exit(self) -> None:
        """Exit solver mode."""
        self.running = False
        print_info("Returning to main menu...")
    
    def _calculate_phi_and_d(self) -> None:
        """Calculate phi and d from p and q."""
        p, q, e = self.rsa_params['p'], self.rsa_params['q'], self.rsa_params['e']
        
        if p and q:
            if p == q:
                phi = p * (p - 1)
            else:
                phi = (p - 1) * (q - 1)
            self.rsa_params['phi'] = phi
            print_success(f"Calculated φ(n) = {phi}")
            
            if e:
                try:
                    d = pow(e, -1, phi)
                    self.rsa_params['d'] = d
                    print_success(f"Calculated private exponent d = {d}")
                except ValueError:
                    print_error("Cannot calculate d - e and φ(n) are not coprime")
    
    def _calculate_d(self) -> None:
        """Calculate d from e and phi."""
        e, phi = self.rsa_params['e'], self.rsa_params['phi']
        
        if e and phi:
            try:
                d = pow(e, -1, phi)
                self.rsa_params['d'] = d
                print_success(f"Calculated private exponent d = {d}")
            except ValueError:
                print_error("Cannot calculate d - e and φ(n) are not coprime")
    
    def _decrypt_and_display(self) -> None:
        """Decrypt and display result."""
        result = solver.decrypt_rsa(**self.rsa_params)
        if result is not None:
            self._display_result(result)
    
    def _display_result(self, result: int) -> None:
        """Display decryption result in multiple formats."""
        animated_loading("Decrypting", 1.0)
        
        print_success(f"Decrypted integer: {result}")
        
        try:
            text_bytes = long_to_bytes(result)
            text = text_bytes.decode('utf-8', errors='ignore')
            print_success(f"Decrypted text: {text}")
            
            # Save result to file
            save_result(f"Integer: {result}\nText: {text}\nBytes: {text_bytes.hex()}", 
                       "decryption_result.txt", OUTPUT_DIR)
            
        except Exception as e:
            print_warning(f"Could not decode as text: {e}")
            print_info(f"Raw result: {result}")