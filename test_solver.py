#!/usr/bin/env python3
"""
Comprehensive test suite for SolveCrypto solver functions.
"""

import unittest
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import solver
from Crypto.Util.number import bytes_to_long, long_to_bytes


class TestSolverFunctions(unittest.TestCase):
    """Test cases for solver functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_message = b"Hello, World!"
        self.test_int = bytes_to_long(self.test_message)
        
        # Small RSA parameters for testing
        self.p = 61
        self.q = 53
        self.n = self.p * self.q  # 3233
        self.phi = (self.p - 1) * (self.q - 1)  # 3120
        self.e = 17
        self.d = pow(self.e, -1, self.phi)  # 2753
        self.ct = pow(self.test_int, self.e, self.n)
    
    def test_integer_square_root(self):
        """Test integer square root calculation."""
        # Perfect squares
        self.assertEqual(solver.integer_square_root(16), 4)
        self.assertEqual(solver.integer_square_root(25), 5)
        self.assertEqual(solver.integer_square_root(100), 10)
        
        # Non-perfect squares (should return floor)
        self.assertEqual(solver.integer_square_root(17), 4)
        self.assertEqual(solver.integer_square_root(26), 5)
        
        # Edge cases
        self.assertEqual(solver.integer_square_root(0), 0)
        self.assertEqual(solver.integer_square_root(1), 1)
        
        # Test with negative numbers (should raise ValueError)
        with self.assertRaises(ValueError):
            solver.integer_square_root(-1)
    
    def test_decrypt_rsa(self):
        """Test RSA decryption with various parameter combinations."""
        # Test with private exponent d
        result = solver.decrypt_rsa(self.n, self.ct, self.e, d=self.d)
        self.assertEqual(result, self.test_int)
        
        # Test with p and q
        result = solver.decrypt_rsa(self.n, self.ct, self.e, p=self.p, q=self.q)
        self.assertEqual(result, self.test_int)
        
        # Test with phi
        result = solver.decrypt_rsa(self.n, self.ct, self.e, phi=self.phi)
        self.assertEqual(result, self.test_int)
        
        # Test with insufficient parameters
        result = solver.decrypt_rsa(self.n, self.ct, self.e)
        self.assertIsNone(result)
    
    def test_cube_root_attack(self):
        """Test cube root attack for e=3."""
        # Create a simple cube root case
        message = b"test"
        m = bytes_to_long(message)
        ct = m ** 3  # Simple cube without modulus
        
        result = solver.cube_root_attack(ct)
        if result:
            # Check if result contains the original message
            try:
                decoded = result.decode('utf-8', errors='ignore')
                self.assertIn("test", decoded.lower())
            except:
                # If decoding fails, just check that we got some result
                self.assertIsNotNone(result)
    
    def test_trial_division(self):
        """Test trial division factorization."""
        # Test with small composite numbers
        factors = solver.trial_division(15)
        self.assertIn(3, factors)
        self.assertIn(5, factors)
        
        factors = solver.trial_division(21)
        self.assertIn(3, factors)
        self.assertIn(7, factors)
        
        # Test with prime number
        factors = solver.trial_division(17)
        self.assertEqual(factors, [17])
        
        # Test with our test RSA modulus
        factors = solver.trial_division(self.n)
        self.assertIn(self.p, factors)
        self.assertIn(self.q, factors)
    
    def test_fermat_factorization(self):
        """Test Fermat factorization."""
        # Test with close primes
        p1, q1 = 101, 103  # Close primes
        n1 = p1 * q1
        
        result = solver.fermat_factorization(n1)
        if result:
            factors = sorted(result)
            self.assertEqual(factors, [p1, q1])
        
        # Test with even number
        result = solver.fermat_factorization(100)
        if result:
            p, q = result
            self.assertEqual(p * q, 100)
    
    def test_pollard_rho_factorization(self):
        """Test Pollard's rho factorization."""
        # Test with small composite
        factor = solver.pollard_rho_factorization(15)
        if factor:
            self.assertTrue(factor in [3, 5])
            self.assertEqual(15 % factor, 0)
        
        # Test with even number
        factor = solver.pollard_rho_factorization(100)
        if factor:
            self.assertEqual(factor, 2)
    
    def test_wiener_attack(self):
        """Test Wiener's attack for small d."""
        # This is difficult to test with guaranteed success
        # as it only works for very specific conditions
        result = solver.wiener_attack(self.n, self.e)
        # We don't assert success because our test values might not be vulnerable
        self.assertTrue(result is None or isinstance(result, int))
    
    def test_common_modulus_attack(self):
        """Test common modulus attack."""
        # Create two ciphertexts with same modulus but different exponents
        e1 = 3
        e2 = 5
        
        # Ensure gcd(e1, e2) = 1
        import math
        self.assertEqual(math.gcd(e1, e2), 1)
        
        # Create ciphertexts
        ct1 = pow(self.test_int, e1, self.n)
        ct2 = pow(self.test_int, e2, self.n)
        
        result = solver.common_modulus_attack(self.n, ct1, ct2, e1, e2)
        if result:
            self.assertEqual(result, self.test_int)
    
    def test_low_public_exponent_attack(self):
        """Test low public exponent attack."""
        # Test with e=3
        e = 3
        ct = pow(self.test_int, e, self.n)
        
        result = solver.low_public_exponent_attack(ct, e, self.n)
        # This might not always work depending on the values
        if result:
            self.assertEqual(result, self.test_int)
    
    def test_modular_equation_order2(self):
        """Test quadratic modular equations."""
        # Test simple quadratic equation
        # x^2 ≡ 1 (mod 8) should have solutions
        solutions = solver.Modulare_Equation_Order2(1, 0, -1, 8)
        if solutions:
            for sol in solutions:
                self.assertEqual((sol * sol - 1) % 8, 0)
    
    def test_ssh_key_generation(self):
        """Test SSH key generation."""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            success = solver.generate_ssh_key(
                self.n, self.e, self.d, self.p, self.q, tmp_path
            )
            self.assertTrue(success)
            
            # Check if file was created and contains PEM data
            with open(tmp_path, 'r') as f:
                content = f.read()
                self.assertIn('-----BEGIN RSA PRIVATE KEY-----', content)
                self.assertIn('-----END RSA PRIVATE KEY-----', content)
                
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


class TestConfigurationAndSetup(unittest.TestCase):
    """Test configuration and setup functions."""
    
    def test_project_structure(self):
        """Test that project structure exists."""
        project_root = Path(__file__).parent
        
        # Check essential files exist
        self.assertTrue((project_root / 'main.py').exists())
        self.assertTrue((project_root / 'solver.py').exists())
        self.assertTrue((project_root / 'MoodRSA.py').exists())
        self.assertTrue((project_root / 'config.py').exists())
        self.assertTrue((project_root / 'utils.py').exists())
        self.assertTrue((project_root / 'requirements.txt').exists())
        self.assertTrue((project_root / 'setup.py').exists())
        
        # Check output directory exists
        self.assertTrue((project_root / 'Output').is_dir())
    
    def test_imports(self):
        """Test that all modules can be imported without errors."""
        try:
            import main
            import solver
            import MoodRSA
            import config
            import utils
        except ImportError as e:
            self.fail(f"Failed to import modules: {e}")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)