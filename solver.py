from factordb.factordb import FactorDB
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, inverse, GCD
import gmpy2
import binascii
import math
import random
from typing import List, Optional, Tuple, Union
from utils import print_success, print_error, print_info
import logging

logger = logging.getLogger(__name__)

def factorize_with_factordb(n: int) -> List[int]:
    """Factorize n using FactorDB API."""
    try:
        f = FactorDB(n)
        f.connect()
        factors = f.get_factor_list()
        if factors:
            print_success(f"Factors found: {factors}")
            logger.info(f"FactorDB found factors: {factors}")
        else:
            print_error("No factors found in FactorDB")
        return factors
    except Exception as e:
        print_error(f"FactorDB error: {e}")
        logger.error(f"FactorDB error: {e}")
        return []

def integer_square_root(n: int) -> int:
    """Calculate integer square root using Newton's method."""
    if n < 0:
        raise ValueError("Cannot compute square root of negative number")
    if n == 0:
        return 0
    
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def decrypt_rsa(n: int, ct: int, e: int, p: int = 0, q: int = 0, 
               d: int = 0, phi: int = 0) -> Optional[int]:
    """Decrypt RSA ciphertext using available parameters."""
    try:
        if d != 0:
            result = pow(ct, d, n)
            print_success(f"Decrypted using d: {result}")
            return result
        
        if phi != 0:
            d_calc = pow(e, -1, phi)
            result = pow(ct, d_calc, n)
            print_success(f"Decrypted using phi: {result}")
            return result
        
        if p != 0 and q != 0:
            if p == q:
                phi_calc = p * (p - 1)
            else:
                phi_calc = (p - 1) * (q - 1)
            d_calc = pow(e, -1, phi_calc)
            result = pow(ct, d_calc, n)
            print_success(f"Decrypted using p,q: {result}")
            return result
        
        print_error("Insufficient parameters for decryption")
        return None
    except Exception as ex:
        print_error(f"Decryption failed: {ex}")
        logger.error(f"Decryption error: {ex}")
        return None
#Modular equation Order 2 ax^2 + bx + c = 0 mod n
def Modulare_Equation_Order2(a, b, c, n):
    # Fonction pour calculer le pgcd étendu
    def extended_gcd(aa, bb):
        last_remainder, remainder = abs(aa), abs(bb)
        x, last_x, y, last_y = 0, 1, 1, 0
        while remainder:
            last_remainder, (quotient, remainder) = remainder, divmod(last_remainder, remainder)
            x, last_x = last_x - quotient * x, x
            y, last_y = last_y - quotient * y, y
        return last_remainder, last_x * (-1 if aa < 0 else 1), last_y * (-1 if bb < 0 else 1)

    # Normaliser les coefficients
    a %= n
    b %= n
    c %= n

    # Calculer le discriminant
    delta = (b * b - 4 * a * c) % n

    # Vérifier si le discriminant est un résidu quadratique mod n
    def is_quadratic_residue(d, n):
        return pow(d, (n - 1) // 2, n) == 1

    if not is_quadratic_residue(delta, n):
        return []  # Pas de solution si delta n'est pas un résidu quadratique

    # Trouver une racine carrée de delta mod n
    def modular_sqrt(a, p):
        if pow(a, (p - 1) // 2, p) != 1:
            return None
        if p % 4 == 3:
            return pow(a, (p + 1) // 4, p)
        s, e = p - 1, 0
        while s % 2 == 0:
            s //= 2
            e += 1
        n = 2
        while pow(n, (p - 1) // 2, p) == 1:
            n += 1
        x = pow(a, (s + 1) // 2, p)
        b = pow(a, s, p)
        g = pow(n, s, p)
        r = e
        while True:
            t = b
            m = 0
            for m in range(r):
                if t == 1:
                    break
                t = pow(t, 2, p)
            if m == 0:
                return x
            gs = pow(g, 2 ** (r - m - 1), p)
            g = (gs * gs) % p
            x = (x * gs) % p
            b = (b * g) % p
            r = m

    sqrt_delta = modular_sqrt(delta, n)
    if sqrt_delta is None:
        return []

    # Résoudre les équations quadratiques résultantes
    x1 = (-b + sqrt_delta) * pow(2 * a, -1, n) % n
    x2 = (-b - sqrt_delta) * pow(2 * a, -1, n) % n

    return sorted({x1, x2})


def pollard_rho_factorization(n: int) -> Optional[int]:
    """Pollard's rho algorithm for factorization."""
    if n % 2 == 0:
        return 2
    
    x = random.randint(2, n - 2)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    
    while d == 1:
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = math.gcd(abs(x - y), n)
        
        if d == n:
            return None
    
    return d if d != n else None


def fermat_factorization(n: int) -> Optional[Tuple[int, int]]:
    """Fermat's factorization method."""
    if n % 2 == 0:
        return (2, n // 2)
    
    a = int(math.ceil(math.sqrt(n)))
    b2 = a * a - n
    
    while not gmpy2.is_square(b2):
        a += 1
        b2 = a * a - n
        if a > n // 2:
            return None
    
    b = int(math.sqrt(b2))
    p, q = a - b, a + b
    
    if p * q == n and p > 1 and q > 1:
        return (p, q)
    return None


def wiener_attack(n: int, e: int) -> Optional[int]:
    """Wiener's attack for small private exponents."""
    def continued_fraction(n, d):
        if d == 0:
            return
        while d:
            a = n // d
            yield a
            n, d = d, n - a * d

    def convergents(cf):
        h0, h1 = 0, 1
        k0, k1 = 1, 0
        for a in cf:
            h = a * h1 + h0
            k = a * k1 + k0
            yield h, k
            h0, h1 = h1, h
            k0, k1 = k1, k

    for h, k in convergents(continued_fraction(e, n)):
        if k == 0:
            continue
        
        phi_n = (e * k - 1) // h
        if phi_n <= 0:
            continue
            
        s = n - phi_n + 1
        discriminant = s * s - 4 * n
        
        if discriminant < 0:
            continue
            
        sqrt_discriminant = int(math.sqrt(discriminant))
        if sqrt_discriminant * sqrt_discriminant != discriminant:
            continue
            
        p = (s + sqrt_discriminant) // 2
        q = (s - sqrt_discriminant) // 2
        
        if p * q == n and p != 1 and q != 1:
            d = inverse(e, phi_n)
            return d
    
    return None


def common_modulus_attack(n: int, c1: int, c2: int, e1: int, e2: int) -> Optional[int]:
    """Common modulus attack when gcd(e1, e2) = 1."""
    try:
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, s, t = extended_gcd(e1, e2)
        if gcd != 1:
            return None
        
        if s < 0:
            c1 = inverse(c1, n)
            s = -s
        if t < 0:
            c2 = inverse(c2, n)
            t = -t
        
        m = pow(c1, s, n) * pow(c2, t, n) % n
        return m
    except Exception as e:
        print_error(f"Common modulus attack failed: {e}")
        return None


def low_public_exponent_attack(ct: int, e: int, n: int) -> Optional[int]:
    """Attack for low public exponents (typically e=3)."""
    if e == 3:
        return cube_root_attack(ct, n)
    
    k = 0
    while True:
        m_candidate = gmpy2.iroot(ct + k * n, e)[0]
        if pow(m_candidate, e) == ct + k * n:
            return int(m_candidate)
        k += 1
        if k > 1000:
            break
    
    return None


def trial_division(n: int, limit: int = 10000) -> List[int]:
    """Simple trial division for small factors."""
    factors = []
    d = 2
    
    while d * d <= n and d <= limit:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    
    if n > 1:
        factors.append(n)
    
    return factors


def cube_root_attack(ct: int, n: int = None) -> Optional[bytes]:
    """Attempt cube root attack for small e=3 cases."""
    try:
        with gmpy2.local_context(gmpy2.context(), precision=300) as ctx:
            if n is None:
                cube_root = gmpy2.cbrt(ct)
            else:
                k = 0
                while True:
                    test_val = ct + k * n
                    cube_root = gmpy2.cbrt(test_val)
                    if pow(int(cube_root), 3) == test_val:
                        break
                    k += 1
                    if k > 1000:
                        print_error("Cube root attack failed after 1000 iterations")
                        return None
            
            result = int(cube_root)
            try:
                hex_val = hex(result)[2:]
                if len(hex_val) % 2:
                    hex_val = '0' + hex_val
                return binascii.unhexlify(hex_val)
            except:
                return str(result).encode()
    except Exception as e:
        print_error(f"Cube root attack failed: {e}")
        return None
    

def generate_ssh_key(n: int, e: int, d: int, p: int, q: int, output_path: str) -> bool:
    """Generate SSH private key from RSA parameters."""
    try:
        if not all([n, e, d, p, q]):
            print_error("All RSA parameters (n, e, d, p, q) are required")
            return False
        
        key = RSA.construct((n, e, d, p, q))
        private_key_pem = key.export_key(format='PEM')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(private_key_pem.decode())
        
        print_success(f"SSH private key saved to {output_path}")
        print_info("Don't forget to set proper permissions: chmod 600 <keyfile>")
        logger.info(f"SSH key generated and saved to {output_path}")
        return True
    except Exception as e:
        print_error(f"SSH key generation failed: {e}")
        logger.error(f"SSH key generation error: {e}")
        return False
    