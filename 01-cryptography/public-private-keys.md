# Public-Private Keys 🔐

## Introduction

Imagine you have a magical mailbox with two special keys: one key (public) that anyone can use to put mail IN the box, but only you have the other key (private) that can take mail OUT. This is the essence of public-private key cryptography - the revolutionary system that makes secure blockchain transactions possible without ever sharing secrets.

This cryptographic innovation, also known as asymmetric cryptography, solved one of the greatest challenges in secure communication: how can two parties who have never met exchange information securely over an insecure network? The answer transformed not just blockchain, but the entire internet.

## The Fundamental Problem: Key Distribution 🗝️

### Traditional Cryptography Challenge

Before public-key cryptography, all encryption was **symmetric**:

```
Traditional Symmetric Encryption:
Alice and Bob need the SAME secret key

Step 1: Alice and Bob must somehow share a secret key
Step 2: Alice encrypts message with secret key
Step 3: Alice sends encrypted message to Bob
Step 4: Bob decrypts message with the same secret key

PROBLEM: How do Alice and Bob share the secret key securely?
```

**The Chicken-and-Egg Problem:**
- Need secure communication to share the secret key
- But need the secret key to have secure communication!

### The Revolutionary Solution: Asymmetric Keys

Public-key cryptography elegantly solves this with **two different keys**:

```
Asymmetric Encryption:
Each person has a KEY PAIR (public + private)

Alice's Keys:        Bob's Keys:
- Public Key A       - Public Key B
- Private Key A      - Private Key B

Alice can encrypt TO Bob using Bob's PUBLIC key
Only Bob can decrypt using his PRIVATE key
```

## How Public-Private Key Cryptography Works 🔧

### Key Generation

The magic starts with **mathematical relationships** between the two keys:

```python
# Conceptual example (simplified)
import random

def generate_keypair():
    """
    Simplified key generation (NOT secure - educational only!)
    Real implementation uses complex mathematical functions
    """
    # In reality, this involves:
    # - Large prime numbers (RSA)
    # - Elliptic curve mathematics (ECDSA)
    # - Complex modular arithmetic
    
    private_key = random.randint(1, 1000000)  # Secret number
    public_key = (private_key * 17) % 1000003  # Mathematical relationship
    
    return private_key, public_key

# Generate keypair
private, public = generate_keypair()
print(f"Private Key: {private} (KEEP SECRET!)")
print(f"Public Key:  {public} (SHARE FREELY!)")
```

### The Mathematical Magic

The security relies on **mathematical one-way functions**:

```
Easy Direction:    Private Key → Public Key (fast computation)
Hard Direction:    Public Key → Private Key (practically impossible)

Examples:
- RSA: Based on factoring large prime numbers
- ECDSA: Based on elliptic curve discrete logarithm problem  
- Ed25519: Based on twisted Edwards curves
```

### Core Properties

1. **Related but Different**: Keys are mathematically related but distinct
2. **Computationally Infeasible**: Can't derive private from public key
3. **Bidirectional Operations**: Either key can be used for encryption/decryption
4. **Signature Capability**: Private key can create signatures only public key can verify

## Real Cryptographic Systems 🛡️

### RSA (Rivest-Shamir-Adleman)

**How RSA Works:**

```python
# RSA Key Generation (simplified educational version)
def simple_rsa_keygen():
    """
    Educational RSA - DO NOT USE FOR REAL SECURITY!
    Real RSA uses 2048+ bit numbers
    """
    # Step 1: Choose two prime numbers
    p = 61  # In reality, this would be hundreds of digits long
    q = 53
    
    # Step 2: Calculate n = p * q
    n = p * q  # 61 * 53 = 3233
    
    # Step 3: Calculate φ(n) = (p-1)(q-1)  
    phi = (p - 1) * (q - 1)  # 60 * 52 = 3120
    
    # Step 4: Choose e (public exponent)
    e = 17  # Common choice, coprime with φ(n)
    
    # Step 5: Calculate d (private exponent)
    # d is the modular inverse of e mod φ(n)
    d = pow(e, -1, phi)  # d = 2753
    
    # Public key: (n, e)
    # Private key: (n, d) 
    return (n, e), (n, d)

# Generate RSA keypair
public_key, private_key = simple_rsa_keygen()
print(f"RSA Public Key:  n={public_key[0]}, e={public_key[1]}")
print(f"RSA Private Key: n={private_key[0]}, d={private_key[1]}")

# RSA Encryption/Decryption
def rsa_encrypt(message_int, public_key):
    n, e = public_key
    return pow(message_int, e, n)

def rsa_decrypt(ciphertext, private_key):
    n, d = private_key
    return pow(ciphertext, d, n)

# Example
message = 42  # In reality, we'd convert text to numbers
encrypted = rsa_encrypt(message, public_key)
decrypted = rsa_decrypt(encrypted, private_key)

print(f"\nRSA Example:")
print(f"Original:  {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
```

**RSA Security:**
- Security based on difficulty of factoring large numbers
- Current recommendation: 2048-bit keys minimum
- 4096-bit keys for high-security applications

### Elliptic Curve Cryptography (ECC)

**Used by:** Bitcoin, Ethereum, most modern blockchains

```python
# Conceptual ECC explanation
def explain_elliptic_curves():
    """
    Elliptic curves: y² = x³ + ax + b
    
    Bitcoin uses secp256k1 curve: y² = x³ + 7
    """
    
    # Key properties of elliptic curves:
    properties = {
        'Point Addition': 'Adding two points gives another point on curve',
        'Scalar Multiplication': 'Multiplying point by number (private key)',
        'One-Way Function': 'Easy: k*G = P, Hard: Given P and G, find k',
        'Discrete Log Problem': 'Foundation of ECC security'
    }
    
    print("Elliptic Curve Cryptography (Bitcoin's secp256k1):")
    for prop, desc in properties.items():
        print(f"  {prop}: {desc}")
    
    # Bitcoin's approach
    print(f"\nBitcoin Key Generation:")
    print(f"1. Private Key: Random 256-bit number (k)")
    print(f"2. Public Key:  k * G (where G is generator point)")
    print(f"3. Address:     hash(Public Key)")

explain_elliptic_curves()
```

**ECC Advantages:**
- Smaller key sizes for same security level
- Faster computation than RSA
- Lower memory and bandwidth requirements
- Perfect for mobile and blockchain applications

**Security Comparison:**
```
Security Level | RSA Key Size | ECC Key Size | Ratio
80-bit        | 1024 bits    | 160 bits     | 6.4:1
112-bit       | 2048 bits    | 224 bits     | 9.1:1  
128-bit       | 3072 bits    | 256 bits     | 12:1
256-bit       | 15360 bits   | 512 bits     | 30:1
```

### Ed25519 (EdDSA)

**Used by:** Solana, Monero, some newer cryptocurrencies

```python
# Ed25519 properties
def ed25519_overview():
    """
    Ed25519: Modern elliptic curve signature scheme
    """
    advantages = {
        'Security': 'Designed to avoid security pitfalls',
        'Performance': 'Very fast signature generation/verification', 
        'Deterministic': 'Same input always gives same signature',
        'Small Keys': '32-byte public keys, 64-byte signatures',
        'Side-Channel Resistance': 'Resistant to timing attacks'
    }
    
    print("Ed25519 (EdDSA) Advantages:")
    for feature, description in advantages.items():
        print(f"  {feature}: {description}")

ed25519_overview()
```

## Blockchain Applications 🔗

### Bitcoin Address Generation

```python
import hashlib

def bitcoin_address_generation():
    """
    How Bitcoin creates addresses from public keys
    """
    # Step 1: Start with a private key (256-bit number)
    private_key = "18e14a7b6a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321725"
    print(f"1. Private Key: {private_key}")
    
    # Step 2: Generate public key (in reality, this uses elliptic curve math)
    # For demonstration, we'll simulate the process
    public_key_x = "50863ad64a87ae8a2fe83c1af1a8403cb53f53e486d8511dad8a04887e5b2352"
    public_key_y = "2cd470243453a299fa9e77237716103abc11a1df38855ed6f2ee187e9c582ba6"
    
    # Compressed public key (33 bytes)
    if int(public_key_y, 16) % 2 == 0:
        compressed_pubkey = "02" + public_key_x
    else:
        compressed_pubkey = "03" + public_key_x
    
    print(f"2. Compressed Public Key: {compressed_pubkey}")
    
    # Step 3: SHA-256 hash of public key
    pubkey_bytes = bytes.fromhex(compressed_pubkey)
    sha256_hash = hashlib.sha256(pubkey_bytes).digest()
    print(f"3. SHA-256 Hash: {sha256_hash.hex()}")
    print(f"3. SHA-256 Hash: {sha256_hash.hex()}")
    
    # Step 4: RIPEMD-160 hash
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_hash)
    pubkey_hash = ripemd160.digest()
    print(f"4. RIPEMD-160 Hash: {pubkey_hash.hex()}")
    
    # Step 5: Add version byte (0x00 for main network)
    versioned_payload = b'\x00' + pubkey_hash
    print(f"5. With Version Byte: {versioned_payload.hex()}")
    
    # Step 6: Double SHA-256 for checksum
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
    print(f"6. Checksum: {checksum.hex()}")
    
    # Step 7: Concatenate and encode in Base58
    address_bytes = versioned_payload + checksum
    print(f"7. Address Bytes: {address_bytes.hex()}")
    
    # Base58 encoding (simplified representation)
    print(f"8. Bitcoin Address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa (example)")
    print(f"   (Real implementation requires Base58 encoding)")

bitcoin_address_generation()
```

### Ethereum Address Generation

```python
def ethereum_address_generation():
    """
    Ethereum uses a simpler address generation process
    """
    # Step 1: Private key (same as Bitcoin)
    private_key = "18e14a7b6a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321725"
    print(f"1. Private Key: {private_key}")
    
    # Step 2: Generate public key (64 bytes, uncompressed)
    # Elliptic curve multiplication: public_key = private_key * G
    public_key_x = "50863ad64a87ae8a2fe83c1af1a8403cb53f53e486d8511dad8a04887e5b2352"
    public_key_y = "2cd470243453a299fa9e77237716103abc11a1df38855ed6f2ee187e9c582ba6"
    public_key = public_key_x + public_key_y
    print(f"2. Public Key (uncompressed): {public_key}")
    
    # Step 3: Keccak-256 hash (not SHA-256!)
    from Crypto.Hash import keccak
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(bytes.fromhex(public_key))
    hash_result = keccak_hash.hexdigest()
    print(f"3. Keccak-256 Hash: {hash_result}")
    
    # Step 4: Take last 20 bytes as address
    ethereum_address = "0x" + hash_result[-40:]  # Last 40 hex chars = 20 bytes
    print(f"4. Ethereum Address: {ethereum_address}")

ethereum_address_generation()
```

### Wallet Key Management

```python
class SimpleWallet:
    """
    Simplified blockchain wallet for educational purposes
    """
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.address = None
    
    def generate_keys(self):
        """Generate new keypair"""
        # In reality, this would use cryptographically secure random numbers
        import secrets
        
        # Generate 256-bit private key
        self.private_key = secrets.randbits(256)
        
        # Generate public key (simplified - real implementation uses ECC)
        self.public_key = pow(self.private_key, 65537, 2**256 - 189)
        
        # Generate address (simplified hash)
        addr_data = f"{self.public_key}".encode()
        self.address = hashlib.sha256(addr_data).hexdigest()[:40]
        
        print(f"Generated new wallet:")
        print(f"Private Key: {hex(self.private_key)}")
        print(f"Public Key:  {hex(self.public_key)}")
        print(f"Address:     0x{self.address}")
    
    def sign_transaction(self, transaction_data):
        """Create digital signature (simplified)"""
        if not self.private_key:
            raise ValueError("No private key available")
        
        # Hash the transaction
        tx_hash = hashlib.sha256(transaction_data.encode()).digest()
        
        # Sign with private key (simplified - real implementation uses ECDSA)
        signature = pow(int.from_bytes(tx_hash, 'big'), self.private_key, 2**256 - 189)
        
        return hex(signature)
    
    def export_private_key(self):
        """Export private key (WARNING: Keep secure!)"""
        if not self.private_key:
            return None
        return hex(self.private_key)
    
    def import_private_key(self, private_key_hex):
        """Import existing private key"""
        self.private_key = int(private_key_hex, 16)
        # Regenerate public key and address
        self.public_key = pow(self.private_key, 65537, 2**256 - 189)
        addr_data = f"{self.public_key}".encode()
        self.address = hashlib.sha256(addr_data).hexdigest()[:40]
        
        print(f"Imported wallet:")
        print(f"Address: 0x{self.address}")

# Example wallet usage
wallet = SimpleWallet()
wallet.generate_keys()

# Sign a transaction
transaction = "Send 10 ETH from Alice to Bob"
signature = wallet.sign_transaction(transaction)
print(f"\nTransaction: {transaction}")
print(f"Signature: {signature[:32]}...")
```

## Key Security and Management 🔒

### Private Key Security Best Practices

```python
def demonstrate_key_security():
    """
    Show the importance of private key security
    """
    scenarios = {
        'Lost Private Key': {
            'consequence': 'Funds permanently inaccessible',
            'real_example': '$140M in Bitcoin lost on hard drives',
            'prevention': 'Multiple secure backups, hardware wallets'
        },
        'Stolen Private Key': {
            'consequence': 'Complete loss of funds, identity theft',
            'real_example': 'Exchange hacks, phishing attacks', 
            'prevention': 'Hardware wallets, never share keys'
        },
        'Weak Random Generation': {
            'consequence': 'Keys predictable, funds stolen',
            'real_example': 'Bad random number generators compromised',
            'prevention': 'Use cryptographically secure random sources'
        },
        'Side-Channel Attacks': {
            'consequence': 'Key extraction through power/timing analysis',
            'real_example': 'Hardware wallet vulnerabilities',
            'prevention': 'Constant-time algorithms, shielded devices'
        }
    }
    
    print("Private Key Security Threats:")
    print("=" * 50)
    
    for threat, details in scenarios.items():
        print(f"\n{threat}:")
        print(f"  Consequence: {details['consequence']}")
        print(f"  Real Example: {details['real_example']}")
        print(f"  Prevention: {details['prevention']}")

demonstrate_key_security()
```

### Hardware vs Software Wallets

```python
def wallet_security_comparison():
    """
    Compare different wallet security approaches
    """
    wallet_types = {
        'Paper Wallet': {
            'security': 'High (offline)',
            'convenience': 'Very Low',
            'cost': 'Free',
            'vulnerability': 'Physical damage, loss, theft'
        },
        'Software Wallet (Hot)': {
            'security': 'Medium (online)',
            'convenience': 'High',
            'cost': 'Free',
            'vulnerability': 'Malware, keyloggers, network attacks'
        },
        'Hardware Wallet (Cold)': {
            'security': 'Very High (offline)',
            'convenience': 'Medium', 
            'cost': '$50-200',
            'vulnerability': 'Physical attacks, supply chain'
        },
        'Multi-Signature Wallet': {
            'security': 'Highest (distributed)',
            'convenience': 'Low',
            'cost': 'Transaction fees',
            'vulnerability': 'Coordination complexity'
        }
    }
    
    print("Wallet Security Comparison:")
    print("Type".ljust(20) + " | Security | Convenience | Cost | Main Vulnerability")
    print("-" * 80)
    
    for wallet_type, props in wallet_types.items():
        print(f"{wallet_type:20} | {props['security']:8} | {props['convenience']:11} | "
              f"{props['cost']:8} | {props['vulnerability']}")

wallet_security_comparison()
```

### Key Derivation and HD Wallets

```python
class HDWallet:
    """
    Hierarchical Deterministic (HD) Wallet implementation
    Generates multiple keys from single seed
    """
    def __init__(self, seed_phrase):
        self.seed = self.phrase_to_seed(seed_phrase)
        self.master_private_key = self.generate_master_key()
        self.accounts = {}
    
    def phrase_to_seed(self, phrase):
        """Convert mnemonic phrase to seed (simplified)"""
        # Real implementation uses PBKDF2 with 2048 iterations
        seed = hashlib.sha512(phrase.encode()).digest()
        return seed
    
    def generate_master_key(self):
        """Generate master private key from seed"""
        # Simplified - real implementation uses HMAC-SHA512
        master_key = int.from_bytes(self.seed[:32], 'big')
        return master_key
    
    def derive_child_key(self, parent_key, index):
        """Derive child key from parent (simplified)"""
        # Real HD wallet derivation is more complex
        child_data = f"{parent_key}{index}".encode()
        child_hash = hashlib.sha256(child_data).digest()
        child_key = int.from_bytes(child_hash, 'big')
        return child_key
    
    def generate_account(self, account_index):
        """Generate new account with multiple addresses"""
        account_key = self.derive_child_key(self.master_private_key, account_index)
        addresses = []
        
        # Generate 5 addresses for this account
        for addr_index in range(5):
            address_key = self.derive_child_key(account_key, addr_index)
            # Convert to address (simplified)
            addr_data = f"{address_key}".encode()
            address = hashlib.sha256(addr_data).hexdigest()[:40]
            addresses.append(f"0x{address}")
        
        self.accounts[account_index] = {
            'account_key': hex(account_key),
            'addresses': addresses
        }
        
        return addresses
    
    def get_backup_phrase(self):
        """Get mnemonic backup phrase"""
        # In reality, this would be generated during wallet creation
        words = ["abandon", "ability", "able", "about", "above", "absent", 
                "absorb", "abstract", "absurd", "abuse", "access", "accident"]
        return " ".join(words)

# Example HD Wallet usage
seed_phrase = "abandon ability able about above absent absorb abstract absurd abuse access accident"
hd_wallet = HDWallet(seed_phrase)

print("HD Wallet Example:")
print(f"Seed Phrase: {seed_phrase}")
print(f"Backup Phrase: {hd_wallet.get_backup_phrase()}")

# Generate first account
account_0_addresses = hd_wallet.generate_account(0)
print(f"\nAccount 0 Addresses:")
for i, addr in enumerate(account_0_addresses):
    print(f"  Address {i}: {addr}")
```

## Multi-Signature Systems 🔐

### How Multi-Sig Works

```python
class MultiSigWallet:
    """
    Multi-signature wallet requiring multiple keys to authorize transactions
    """
    def __init__(self, required_signatures, total_signers):
        self.required_sigs = required_signatures
        self.total_signers = total_signers
        self.signers = {}
        self.pending_transactions = {}
        
    def add_signer(self, name, public_key):
        """Add authorized signer"""
        self.signers[name] = public_key
        print(f"Added signer: {name}")
    
    def create_transaction(self, tx_id, transaction_data):
        """Create new transaction requiring signatures"""
        self.pending_transactions[tx_id] = {
            'data': transaction_data,
            'signatures': {},
            'approved': False
        }
        print(f"Created transaction {tx_id}: {transaction_data}")
    
    def sign_transaction(self, tx_id, signer_name, signature):
        """Signer approves transaction"""
        if tx_id not in self.pending_transactions:
            return False, "Transaction not found"
        
        if signer_name not in self.signers:
            return False, "Unauthorized signer"
        
        tx = self.pending_transactions[tx_id]
        tx['signatures'][signer_name] = signature
        
        # Check if we have enough signatures
        sig_count = len(tx['signatures'])
        if sig_count >= self.required_sigs:
            tx['approved'] = True
            return True, f"Transaction approved! ({sig_count}/{self.required_sigs})"
        else:
            return True, f"Signature recorded ({sig_count}/{self.required_sigs})"
    
    def execute_transaction(self, tx_id):
        """Execute approved transaction"""
        if tx_id not in self.pending_transactions:
            return False, "Transaction not found"
        
        tx = self.pending_transactions[tx_id]
        if not tx['approved']:
            sig_count = len(tx['signatures'])
            return False, f"Need {self.required_sigs - sig_count} more signatures"
        
        # Execute transaction (simplified)
        print(f"Executing: {tx['data']}")
        del self.pending_transactions[tx_id]
        return True, "Transaction executed successfully"

# Example: 2-of-3 multi-sig wallet
multisig = MultiSigWallet(required_signatures=2, total_signers=3)

# Add signers
multisig.add_signer("Alice", "pubkey_alice_123...")
multisig.add_signer("Bob", "pubkey_bob_456...")  
multisig.add_signer("Carol", "pubkey_carol_789...")

# Create transaction
multisig.create_transaction("tx_001", "Send 100 ETH to 0x1234...")

# Signers approve (need 2 out of 3)
success, msg = multisig.sign_transaction("tx_001", "Alice", "signature_alice")
print(msg)

success, msg = multisig.sign_transaction("tx_001", "Bob", "signature_bob")
print(msg)

# Execute approved transaction
success, msg = multisig.execute_transaction("tx_001")
print(msg)
```

### Multi-Sig Use Cases

```python
def multisig_use_cases():
    """
    Real-world applications of multi-signature wallets
    """
    use_cases = {
        'Corporate Treasury (3-of-5)': {
            'scenario': 'Company needs multiple executives to approve large expenditures',
            'signers': 'CEO, CFO, CTO, Board Member 1, Board Member 2',
            'threshold': '3 signatures required',
            'benefit': 'Prevents single person from draining funds'
        },
        'Joint Account (2-of-2)': {
            'scenario': 'Married couple sharing cryptocurrency holdings',
            'signers': 'Spouse A, Spouse B', 
            'threshold': 'Both signatures required',
            'benefit': 'Both parties must agree to transactions'
        },
        'Escrow Service (2-of-3)': {
            'scenario': 'Buyer and seller with neutral arbitrator',
            'signers': 'Buyer, Seller, Arbitrator',
            'threshold': '2 signatures required',
            'benefit': 'Dispute resolution without central authority'
        },
        'DAO Governance (7-of-12)': {
            'scenario': 'Decentralized organization managing treasury',
            'signers': '12 elected council members',
            'threshold': '7 signatures required (majority)',
            'benefit': 'Democratic control of organizational funds'
        }
    }
    
    print("Multi-Signature Wallet Use Cases:")
    print("=" * 50)
    
    for use_case, details in use_cases.items():
        print(f"\n{use_case}:")
        for key, value in details.items():
            print(f"  {key.capitalize()}: {value}")

multisig_use_cases()
```

## Key Exchange and Agreement 🤝

### Diffie-Hellman Key Exchange

```python
def diffie_hellman_demo():
    """
    Demonstrate how two parties can agree on a shared secret
    without directly sharing it
    """
    print("Diffie-Hellman Key Exchange Demo")
    print("=" * 40)
    
    # Public parameters (known to everyone)
    p = 23  # Prime number (in reality, this is hundreds of digits)
    g = 5   # Generator (primitive root modulo p)
    
    print(f"Public Parameters:")
    print(f"  p (prime): {p}")
    print(f"  g (generator): {g}")
    
    # Alice's keys
    alice_private = 6  # Alice's secret
    alice_public = pow(g, alice_private, p)  # g^a mod p
    
    # Bob's keys  
    bob_private = 15   # Bob's secret
    bob_public = pow(g, bob_private, p)      # g^b mod p
    
    print(f"\nAlice:")
    print(f"  Private key: {alice_private} (secret)")
    print(f"  Public key:  {alice_public} (shared)")
    
    print(f"\nBob:")
    print(f"  Private key: {bob_private} (secret)")
    print(f"  Public key:  {bob_public} (shared)")
    
    # Both compute shared secret
    alice_shared = pow(bob_public, alice_private, p)    # (g^b)^a mod p
    bob_shared = pow(alice_public, bob_private, p)      # (g^a)^b mod p
    
    print(f"\nShared Secret Calculation:")
    print(f"  Alice computes: {bob_public}^{alice_private} mod {p} = {alice_shared}")
    print(f"  Bob computes:   {alice_public}^{bob_private} mod {p} = {bob_shared}")
    print(f"  Secrets match:  {alice_shared == bob_shared}")
    
    # The magic: (g^a)^b = (g^b)^a = g^(ab) mod p
    print(f"\nMathematical proof: g^(a*b) mod p = g^({alice_private}*{bob_private}) mod {p} = {pow(g, alice_private * bob_private, p)}")

diffie_hellman_demo()
```

### Elliptic Curve Diffie-Hellman (ECDH)

```python
def ecdh_explanation():
    """
    Explain ECDH used in modern blockchain systems
    """
    print("Elliptic Curve Diffie-Hellman (ECDH)")
    print("=" * 40)
    
    explanation = {
        'Classical DH': 'Uses modular exponentiation: g^x mod p',
        'ECDH': 'Uses elliptic curve point multiplication: x * G',
        'Advantage': 'Smaller keys for same security level',
        'Bitcoin Usage': 'BIP32 key derivation, Lightning Network',
        'Ethereum Usage': 'Node communication, wallet protocols'
    }
    
    for concept, description in explanation.items():
        print(f"{concept:15}: {description}")
    
    print(f"\nECDH Process:")
    print(f"1. Alice: private_a * G = public_A (point on curve)")
    print(f"2. Bob:   private_b * G = public_B (point on curve)")
    print(f"3. Alice: private_a * public_B = shared_secret")
    print(f"4. Bob:   private_b * public_A = shared_secret")
    print(f"5. Both get same point due to: private_a * (private_b * G) = private_b * (private_a * G)")

ecdh_explanation()
```

## Performance and Security Analysis ⚡

### Key Size vs Security Comparison

```python
def security_level_comparison():
    """
    Compare different cryptographic systems' security levels
    """
    import matplotlib.pyplot as plt
    
    # Security levels and corresponding key sizes
    security_data = {
        'RSA': {
            80: 1024,
            112: 2048, 
            128: 3072,
            192: 7680,
            256: 15360
        },
        'ECC': {
            80: 160,
            112: 224,
            128: 256, 
            192: 384,
            256: 512
        },
        'AES (Symmetric)': {
            80: 80,
            112: 112,
            128: 128,
            192: 192, 
            256: 256
        }
    }
    
    print("Security Level vs Key Size Comparison")
    print("=" * 50)
    print("Security | RSA (bits) | ECC (bits) | AES (bits) | ECC Advantage")
    print("-" * 65)
    
    for security_level in [80, 112, 128, 192, 256]:
        rsa_size = security_data['RSA'][security_level]
        ecc_size = security_data['ECC'][security_level]
        aes_size = security_data['AES'][security_level]
        ratio = rsa_size / ecc_size
        
        print(f"{security_level:8} | {rsa_size:10} | {ecc_size:10} | {aes_size:10} | {ratio:.1f}x smaller")

security_level_comparison()
```

### Performance Benchmarking

```python
import time
import secrets

def benchmark_key_operations():
    """
    Benchmark key generation and operations
    """
    iterations = 1000
    
    # Simulate RSA key generation (simplified)
    def simulate_rsa_keygen():
        # Real RSA is much more complex
        p = secrets.randbits(1024)
        q = secrets.randbits(1024) 
        return p * q
    
    # Simulate ECC key generation
    def simulate_ecc_keygen():
        # Real ECC uses elliptic curve math
        return secrets.randbits(256)
    
    # Benchmark key generation
    print("Key Generation Performance:")
    print("=" * 30)
    
    # RSA benchmark
    start = time.time()
    for _ in range(iterations // 10):  # Fewer iterations as RSA is slower
        simulate_rsa_keygen()
    rsa_time = time.time() - start
    
    # ECC benchmark  
    start = time.time()
    for _ in range(iterations):
        simulate_ecc_keygen()
    ecc_time = time.time() - start
    
    print(f"RSA (2048-bit):  {rsa_time:.4f}s for {iterations//10} keys")
    print(f"ECC (256-bit):   {ecc_time:.4f}s for {iterations} keys")
    print(f"ECC is ~{(rsa_time * 10) / ecc_time:.1f}x faster")
    
    # Memory usage comparison
    print(f"\nMemory Usage:")
    print(f"RSA Public Key:  256 bytes (2048 bits)")
    print(f"RSA Private Key: 1024+ bytes")
    print(f"ECC Public Key:  33 bytes (compressed)")
    print(f"ECC Private Key: 32 bytes")

benchmark_key_operations()
```

## Common Vulnerabilities and Attacks 🛡️

### Weak Random Number Generation

```python
def demonstrate_weak_rng():
    """
    Show dangers of weak random number generation
    """
    import random
    
    print("Weak Random Number Generation Dangers")
    print("=" * 45)
    
    # BAD: Using predictable random
    print("❌ INSECURE: Using Python's random module")
    random.seed(12345)  # Predictable seed
    weak_keys = [random.getrandbits(256) for _ in range(5)]
    
    # Attacker with same seed can predict keys
    random.seed(12345)  # Same seed  
    predicted_keys = [random.getrandbits(256) for _ in range(5)]
    
    print(f"Original keys match predicted: {weak_keys == predicted_keys}")
    
    # GOOD: Using cryptographically secure random
    print(f"\n✅ SECURE: Using secrets module")
    secure_keys = [secrets.randbits(256) for _ in range(5)]
    more_secure_keys = [secrets.randbits(256) for _ in range(5)]
    
    print(f"Secure keys are different: {secure_keys != more_secure_keys}")
    
    # Real-world consequences
    print(f"\nReal-world Examples:")
    print(f"• 2010: Android Bitcoin wallet bug - weak random")
    print(f"• 2013: Blockchain.info incident - predictable keys") 
    print(f"• 2018: Ethereum address collisions - poor entropy")

demonstrate_weak_rng()
```

### Side-Channel Attacks

```python
def timing_attack_demo():
    """
    Demonstrate timing attack vulnerability
    """
    import time
    
    def vulnerable_key_check(input_key, real_key):
        """
        VULNERABLE: Stops comparing at first difference
        """
        for i in range(min(len(input_key), len(real_key))):
            if input_key[i] != real_key[i]:
                return False
        return len(input_key) == len(real_key)
    
    def secure_key_check(input_key, real_key):
        """
        SECURE: Always checks full key length
        """
        if len(input_key) != len(real_key):
            return False
        
        result = True
        for i in range(len(real_key)):
            if input_key[i] != real_key[i]:
                result = False
        return result
    
    real_key = "supersecretkey123456"
    
    # Time vulnerable function
    wrong_key_short = "a"
    wrong_key_partial = "supersecret"  # Partially correct
    
    start = time.time()
    for _ in range(100000):
        vulnerable_key_check(wrong_key_short, real_key)
    time_short = time.time() - start
    
    start = time.time() 
    for _ in range(100000):
        vulnerable_key_check(wrong_key_partial, real_key)
    time_partial = time.time() - start
    
    print("Timing Attack Demonstration:")
    print(f"Short wrong key time:    {time_short:.6f}s")
    print(f"Partial match time:      {time_partial:.6f}s")
    print(f"Timing difference:       {abs(time_partial - time_short):.6f}s")
    print(f"Attacker can detect partial matches!")

timing_attack_demo()
```

## Advanced Applications 🚀

### Threshold Cryptography

```python
def threshold_cryptography_demo():
    """
    Demonstrate threshold signatures (t-of-n)
    """
    print("Threshold Cryptography (Shamir's Secret Sharing)")
    print("=" * 50)
    
    def shamir_share_secret(secret, threshold, num_shares):
        """
        Split secret into shares where any 'threshold' can reconstruct
        """
        import random
        
        # Simplified version for demonstration
        shares = []
        coefficients = [secret] + [random.randint(1, 1000) for _ in range(threshold - 1)]
        
        for i in range(1, num_shares + 1):
            # Evaluate polynomial at point i
            y = sum(coeff * (i ** power) for power, coeff in enumerate(coefficients)) % 1009
            shares.append((i, y))
        
        return shares
    
    def reconstruct_secret(shares, threshold):
        """
        Reconstruct secret from threshold number of shares
        """
        if len(shares) < threshold:
            return None
        
        # Lagrange interpolation (simplified)
        # In reality, this is more complex modular arithmetic
        secret = 0
        for i, (xi, yi) in enumerate(shares[:threshold]):
            term = yi
            for j, (xj, _) in enumerate(shares[:threshold]):
                if i != j:
                    term = (term * (0 - xj)) // (xi - xj)
            secret += term
        
        return abs(secret) % 1009
    
    # Example: 3-of-5 threshold scheme
    secret = 42  # Private key or seed
    threshold = 3
    num_shares = 5
    
    print(f"Original secret: {secret}")
    print(f"Threshold: {threshold} of {num_shares} shares needed")
    
    # Create shares
    shares = shamir_share_secret(secret, threshold, num_shares)
    print(f"\nGenerated shares:")
    for i, (x, y) in enumerate(shares):
        print(f"  Share {i+1}: ({x}, {y})")
    
    # Reconstruct with minimum threshold
    subset = shares[:threshold]
    reconstructed = reconstruct_secret(subset, threshold)
    print(f"\nReconstructed with {threshold} shares: {reconstructed}")
    print(f"Successful reconstruction: {reconstructed == secret}")

threshold_cryptography_demo()
```

### Ring Signatures (Privacy)

```python
def ring_signature_explanation():
    """
    Explain ring signatures used in privacy coins
    """
    print("Ring Signatures for Privacy")
    print("=" * 30)
    
    concept = {
        'Purpose': 'Hide the real signer among a group',
        'Process': 'Signer creates signature that could come from anyone in the ring',
        'Verification': 'Verifier knows someone in ring signed, but not who',
        'Used in': 'Monero, other privacy-focused cryptocurrencies',
        'Advantage': 'Provides plausible deniability for transactions'
    }
    
    for key, description in concept.items():
        print(f"{key:12}: {description}")
    
    print(f"\nRing Signature Example:")
    print(f"Ring members: Alice, Bob, Carol, Dave, Eve")
    print(f"Real signer: Alice (but nobody knows this)")
    print(f"Signature proves: 'Someone in this group signed'")
    print(f"Privacy result: Alice's transaction# Public-Private Keys 🔐

## Introduction

Imagine you have a magical mailbox with two special keys: one key (public) that anyone can use to put mail IN the box, but only you have the other key (private) that can take mail OUT. This is the essence of public-private key cryptography - the revolutionary system that makes secure blockchain transactions possible without ever sharing secrets.

This cryptographic innovation, also known as asymmetric cryptography, solved one of the greatest challenges in secure communication: how can two parties who have never met exchange information securely over an insecure network? The answer transformed not just blockchain, but the entire internet.

## The Fundamental Problem: Key Distribution 🗝️

### Traditional Cryptography Challenge

Before public-key cryptography, all encryption was **symmetric**:

```
Traditional Symmetric Encryption:
Alice and Bob need the SAME secret key

Step 1: Alice and Bob must somehow share a secret key
Step 2: Alice encrypts message with secret key
Step 3: Alice sends encrypted message to Bob
Step 4: Bob decrypts message with the same secret key

PROBLEM: How do Alice and Bob share the secret key securely?
```

**The Chicken-and-Egg Problem:**
- Need secure communication to share the secret key
- But need the secret key to have secure communication!

### The Revolutionary Solution: Asymmetric Keys

Public-key cryptography elegantly solves this with **two different keys**:

```
Asymmetric Encryption:
Each person has a KEY PAIR (public + private)

Alice's Keys:        Bob's Keys:
- Public Key A       - Public Key B
- Private Key A      - Private Key B

Alice can encrypt TO Bob using Bob's PUBLIC key
Only Bob can decrypt using his PRIVATE key
```

## How Public-Private Key Cryptography Works 🔧

### Key Generation

The magic starts with **mathematical relationships** between the two keys:

```python
# Conceptual example (simplified)
import random

def generate_keypair():
    """
    Simplified key generation (NOT secure - educational only!)
    Real implementation uses complex mathematical functions
    """
    # In reality, this involves:
    # - Large prime numbers (RSA)
    # - Elliptic curve mathematics (ECDSA)
    # - Complex modular arithmetic
    
    private_key = random.randint(1, 1000000)  # Secret number
    public_key = (private_key * 17) % 1000003  # Mathematical relationship
    
    return private_key, public_key

# Generate keypair
private, public = generate_keypair()
print(f"Private Key: {private} (KEEP SECRET!)")
print(f"Public Key:  {public} (SHARE FREELY!)")
```

### The Mathematical Magic

The security relies on **mathematical one-way functions**:

```
Easy Direction:    Private Key → Public Key (fast computation)
Hard Direction:    Public Key → Private Key (practically impossible)

Examples:
- RSA: Based on factoring large prime numbers
- ECDSA: Based on elliptic curve discrete logarithm problem  
- Ed25519: Based on twisted Edwards curves
```

### Core Properties

1. **Related but Different**: Keys are mathematically related but distinct
2. **Computationally Infeasible**: Can't derive private from public key
3. **Bidirectional Operations**: Either key can be used for encryption/decryption
4. **Signature Capability**: Private key can create signatures only public key can verify

## Real Cryptographic Systems 🛡️

### RSA (Rivest-Shamir-Adleman)

**How RSA Works:**

```python
# RSA Key Generation (simplified educational version)
def simple_rsa_keygen():
    """
    Educational RSA - DO NOT USE FOR REAL SECURITY!
    Real RSA uses 2048+ bit numbers
    """
    # Step 1: Choose two prime numbers
    p = 61  # In reality, this would be hundreds of digits long
    q = 53
    
    # Step 2: Calculate n = p * q
    n = p * q  # 61 * 53 = 3233
    
    # Step 3: Calculate φ(n) = (p-1)(q-1)  
    phi = (p - 1) * (q - 1)  # 60 * 52 = 3120
    
    # Step 4: Choose e (public exponent)
    e = 17  # Common choice, coprime with φ(n)
    
    # Step 5: Calculate d (private exponent)
    # d is the modular inverse of e mod φ(n)
    d = pow(e, -1, phi)  # d = 2753
    
    # Public key: (n, e)
    # Private key: (n, d) 
    return (n, e), (n, d)

# Generate RSA keypair
public_key, private_key = simple_rsa_keygen()
print(f"RSA Public Key:  n={public_key[0]}, e={public_key[1]}")
print(f"RSA Private Key: n={private_key[0]}, d={private_key[1]}")

# RSA Encryption/Decryption
def rsa_encrypt(message_int, public_key):
    n, e = public_key
    return pow(message_int, e, n)

def rsa_decrypt(ciphertext, private_key):
    n, d = private_key
    return pow(ciphertext, d, n)

# Example
message = 42  # In reality, we'd convert text to numbers
encrypted = rsa_encrypt(message, public_key)
decrypted = rsa_decrypt(encrypted, private_key)

print(f"\nRSA Example:")
print(f"Original:  {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
```

**RSA Security:**
- Security based on difficulty of factoring large numbers
- Current recommendation: 2048-bit keys minimum
- 4096-bit keys for high-security applications

### Elliptic Curve Cryptography (ECC)

**Used by:** Bitcoin, Ethereum, most modern blockchains

```python
# Conceptual ECC explanation
def explain_elliptic_curves():
    """
    Elliptic curves: y² = x³ + ax + b
    
    Bitcoin uses secp256k1 curve: y² = x³ + 7
    """
    
    # Key properties of elliptic curves:
    properties = {
        'Point Addition': 'Adding two points gives another point on curve',
        'Scalar Multiplication': 'Multiplying point by number (private key)',
        'One-Way Function': 'Easy: k*G = P, Hard: Given P and G, find k',
        'Discrete Log Problem': 'Foundation of ECC security'
    }
    
    print("Elliptic Curve Cryptography (Bitcoin's secp256k1):")
    for prop, desc in properties.items():
        print(f"  {prop}: {desc}")
    
    # Bitcoin's approach
    print(f"\nBitcoin Key Generation:")
    print(f"1. Private Key: Random 256-bit number (k)")
    print(f"2. Public Key:  k * G (where G is generator point)")
    print(f"3. Address:     hash(Public Key)")

explain_elliptic_curves()
```

**ECC Advantages:**
- Smaller key sizes for same security level
- Faster computation than RSA
- Lower memory and bandwidth requirements
- Perfect for mobile and blockchain applications

**Security Comparison:**
```
Security Level | RSA Key Size | ECC Key Size | Ratio
80-bit        | 1024 bits    | 160 bits     | 6.4:1
112-bit       | 2048 bits    | 224 bits     | 9.1:1  
128-bit       | 3072 bits    | 256 bits     | 12:1
256-bit       | 15360 bits   | 512 bits     | 30:1
```

### Ed25519 (EdDSA)

**Used by:** Solana, Monero, some newer cryptocurrencies

```python
# Ed25519 properties
def ed25519_overview():
    """
    Ed25519: Modern elliptic curve signature scheme
    """
    advantages = {
        'Security': 'Designed to avoid security pitfalls',
        'Performance': 'Very fast signature generation/verification', 
        'Deterministic': 'Same input always gives same signature',
        'Small Keys': '32-byte public keys, 64-byte signatures',
        'Side-Channel Resistance': 'Resistant to timing attacks'
    }
    
    print("Ed25519 (EdDSA) Advantages:")
    for feature, description in advantages.items():
        print(f"  {feature}: {description}")

ed25519_overview()
```

## Blockchain Applications 🔗

### Bitcoin Address Generation

```python
import hashlib

def bitcoin_address_generation():
    """
    How Bitcoin creates addresses from public keys
    """
    # Step 1: Start with a private key (256-bit number)
    private_key = "18e14a7b6a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321725"
    print(f"1. Private Key: {private_key}")
    
    # Step 2: Generate public key (in reality, this uses elliptic curve math)
    # For demonstration, we'll simulate the process
    public_key_x = "50863ad64a87ae8a2fe83c1af1a8403cb53f53e486d8511dad8a04887e5b2352"
    public_key_y = "2cd470243453a299fa9e77237716103abc11a1df38855ed6f2ee187e9c582ba6"
    
    # Compressed public key (33 bytes)
    if int(public_key_y, 16) % 2 == 0:
        compressed_pubkey = "02" + public_key_x
    else:
        compressed_pubkey = "03" + public_key_x
    
    print(f"2. Compressed Public Key: {compressed_pubkey}")
    
    # Step 3: SHA-256 hash of public key
    pubkey_bytes = bytes.fromhex(compressed_pubkey)
    sha256_hash = hashlib.sha256(pubkey_bytes).digest()
    print(f"3. SHA-256 Hash: {sha256_hash.hex()}")
    print(f"3. SHA-256 Hash: {sha256_hash.hex()}")
    
    # Step 4: RIPEMD-160 hash
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_hash)
    pubkey_hash = ripemd160.digest()
    print(f"4. RIPEMD-160 Hash: {pubkey_hash.hex()}")
    
    # Step 5: Add version byte (0x00 for main network)
    versioned_payload = b'\x00' + pubkey_hash
    print(f"5. With Version Byte: {versioned_payload.hex()}")
    
    # Step 6: Double SHA-256 for checksum
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
    print(f"6. Checksum: {checksum.hex()}")
    
    # Step 7: Concatenate and encode in Base58
    address_bytes = versioned_payload + checksum
    print(f"7. Address Bytes: {address_bytes.hex()}")
    
    # Base58 encoding (simplified representation)
    print(f"8. Bitcoin Address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa (example)")
    print(f"   (Real implementation requires Base58 encoding)")

bitcoin_address_generation()
```

### Ethereum Address Generation

```python
def ethereum_address_generation():
    """
    Ethereum uses a simpler address generation process
    """
    # Step 1: Private key (same as Bitcoin)
    private_key = "18e14a7b6a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321725"
    print(f"1. Private Key: {private_key}")
    
    # Step 2: Generate public key (64 bytes, uncompressed)
    # Elliptic curve multiplication: public_key = private_key * G
    public_key_x = "50863ad64a87ae8a2fe83c1af1a8403cb53f53e486d8511dad8a04887e5b2352"
    public_key_y = "2cd470243453a299fa9e77237716103abc11a1df38855ed6f2ee187e9c582ba6"
    public_key = public_key_x + public_key_y
    print(f"2. Public Key (uncompressed): {public_key}")
    
    # Step 3: Keccak-256 hash (not SHA-256!)
    from Crypto.Hash import keccak
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(bytes.fromhex(public_key))
    hash_result = keccak_hash.hexdigest()
    print(f"3. Keccak-256 Hash: {hash_result}")
    
    # Step 4: Take last 20 bytes as address
    ethereum_address = "0x" + hash_result[-40:]  # Last 40 hex chars = 20 bytes
    print(f"4. Ethereum Address: {ethereum_address}")

ethereum_address_generation()
```

### Wallet Key Management

```python
class SimpleWallet:
    """
    Simplified blockchain wallet for educational purposes
    """
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.address = None
    
    def generate_keys(self):
        """Generate new keypair"""
        # In reality, this would use cryptographically secure random numbers
        import secrets
        
        # Generate 256-bit private key
        self.private_key = secrets.randbits(256)
        
        # Generate public key (simplified - real implementation uses ECC)
        self.public_key = pow(self.private_key, 65537, 2**256 - 189)
        
        # Generate address (simplified hash)
        addr_data = f"{self.public_key}".encode()
        self.address = hashlib.sha256(addr_data).hexdigest()[:40]
        
        print(f"Generated new wallet:")
        print(f"Private Key: {hex(self.private_key)}")
        print(f"Public Key:  {hex(self.public_key)}")
        print(f"Address:     0x{self.address}")
    
    def sign_transaction(self, transaction_data):
        """Create digital signature (simplified)"""
        if not self.private_key:
            raise ValueError("No private key available")
        
        # Hash the transaction
        tx_hash = hashlib.sha256(transaction_data.encode()).digest()
        
        # Sign with private key (simplified - real implementation uses ECDSA)
        signature = pow(int.from_bytes(tx_hash, 'big'), self.private_key, 2**256 - 189)
        
        return hex(signature)
    
    def export_private_key(self):
        """Export private key (WARNING: Keep secure!)"""
        if not self.private_key:
            return None
        return hex(self.private_key)
    
    def import_private_key(self, private_key_hex):
        """Import existing private key"""
        self.private_key = int(private_key_hex, 16)
        # Regenerate public key and address
        self.public_key = pow(self.private_key, 65537, 2**256 - 189)
        addr_data = f"{self.public_key}".encode()
        self.address = hashlib.sha256(addr_data).hexdigest()[:40]
        
        print(f"Imported wallet:")
        print(f"Address: 0x{self.address}")

# Example wallet usage
wallet = SimpleWallet()
wallet.generate_keys()

# Sign a transaction
transaction = "Send 10 ETH from Alice to Bob"
signature = wallet.sign_transaction(transaction)
print(f"\nTransaction: {transaction}")
print(f"Signature: {signature[:32]}...")
```

## Key Security and Management 🔒

### Private Key Security Best Practices

```python
def demonstrate_key_security():
    """
    Show the importance of private key security
    """
    scenarios = {
        'Lost Private Key': {
            'consequence': 'Funds permanently inaccessible',
            'real_example': '$140M in Bitcoin lost on hard drives',
            'prevention': 'Multiple secure backups, hardware wallets'
        },
        'Stolen Private Key': {
            'consequence': 'Complete loss of funds, identity theft',
            'real_example': 'Exchange hacks, phishing attacks', 
            'prevention': 'Hardware wallets, never share keys'
        },
        'Weak Random Generation': {
            'consequence': 'Keys predictable, funds stolen',
            'real_example': 'Bad random number generators compromised',
            'prevention': 'Use cryptographically secure random sources'
        },
        'Side-Channel Attacks': {
            'consequence': 'Key extraction through power/timing analysis',
            'real_example': 'Hardware wallet vulnerabilities',
            'prevention': 'Constant-time algorithms, shielded devices'
        }
    }
    
    print("Private Key Security Threats:")
    print("=" * 50)
    
    for threat, details in scenarios.items():
        print(f"\n{threat}:")
        print(f"  Consequence: {details['consequence']}")
        print(f"  Real Example: {details['real_example']}")
        print(f"  Prevention: {details['prevention']}")

demonstrate_key_security()
```

### Hardware vs Software Wallets

```python
def wallet_security_comparison():
    """
    Compare different wallet security approaches
    """
    wallet_types = {
        'Paper Wallet': {
            'security': 'High (offline)',
            'convenience': 'Very Low',
            'cost': 'Free',
            'vulnerability': 'Physical damage, loss, theft'
        },
        'Software Wallet (Hot)': {
            'security': 'Medium (online)',
            'convenience': 'High',
            'cost': 'Free',
            'vulnerability': 'Malware, keyloggers, network attacks'
        },
        'Hardware Wallet (Cold)': {
            'security': 'Very High (offline)',
            'convenience': 'Medium', 
            'cost': '$50-200',
            'vulnerability': 'Physical attacks, supply chain'
        },
        'Multi-Signature Wallet': {
            'security': 'Highest (distributed)',
            'convenience': 'Low',
            'cost': 'Transaction fees',
            'vulnerability': 'Coordination complexity'
        }
    }
    
    print("Wallet Security Comparison:")
    print("Type".ljust(20) + " | Security | Convenience | Cost | Main Vulnerability")
    print("-" * 80)
    
    for wallet_type, props in wallet_types.items():
        print(f"{wallet_type:20} | {props['security']:8} | {props['convenience']:11} | "
              f"{props['cost']:8} | {props['vulnerability']}")

wallet_security_comparison()
```

### Key Derivation and HD Wallets

```python
class HDWallet:
    """
    Hierarchical Deterministic (HD) Wallet implementation
    Generates multiple keys from single seed
    """
    def __init__(self, seed_phrase):
        self.seed = self.phrase_to_seed(seed_phrase)
        self.master_private_key = self.generate_master_key()
        self.accounts = {}
    
    def phrase_to_seed(self, phrase):
        """Convert mnemonic phrase to seed (simplified)"""
        # Real implementation uses PBKDF2 with 2048 iterations
        seed = hashlib.sha512(phrase.encode()).digest()
        return seed
    
    def generate_master_key(self):
        """Generate master private key from seed"""
        # Simplified - real implementation uses HMAC-SHA512
        master_key = int.from_bytes(self.seed[:32], 'big')
        return master_key
    
    def derive_child_key(self, parent_key, index):
        """Derive child key from parent (simplified)"""
        # Real HD wallet derivation is more complex
        child_data = f"{parent_key}{index}".encode()
        child_hash = hashlib.sha256(child_data).digest()
        child_key = int.from_bytes(child_hash, 'big')
        return child_key
    
    def generate_account(self, account_index):
        """Generate new account with multiple addresses"""
        account_key = self.derive_child_key(self.master_private_key, account_index)
        addresses = []
        
        # Generate 5 addresses for this account
        for addr_index in range(5):
            address_key = self.derive_child_key(account_key, addr_index)
            # Convert to address (simplified)
            addr_data = f"{address_key}".encode()
            address = hashlib.sha256(addr_data).hexdigest()[:40]
            addresses.append(f"0x{address}")
        
        self.accounts[account_index] = {
            'account_key': hex(account_key),
            'addresses': addresses
        }
        
        return addresses
    
    def get_backup_phrase(self):
        """Get mnemonic backup phrase"""
        # In reality, this would be generated during wallet creation
        words = ["abandon", "ability", "able", "about", "above", "absent", 
                "absorb", "abstract", "absurd", "abuse", "access", "accident"]
        return " ".join(words)

# Example HD Wallet usage
seed_phrase = "abandon ability able about above absent absorb abstract absurd abuse access accident"
hd_wallet = HDWallet(seed_phrase)

print("HD Wallet Example:")
print(f"Seed Phrase: {seed_phrase}")
print(f"Backup Phrase: {hd_wallet.get_backup_phrase()}")

# Generate first account
account_0_addresses = hd_wallet.generate_account(0)
print(f"\nAccount 0 Addresses:")
for i, addr in enumerate(account_0_addresses):
    print(f"  Address {i}: {addr}")
```

## Multi-Signature Systems 🔐

### How Multi-Sig Works

```python
class MultiSigWallet:
    """
    Multi-signature wallet requiring multiple keys to authorize transactions
    """
    def __init__(self, required_signatures, total_signers):
        self.required_sigs = required_signatures
        self.total_signers = total_signers
        self.signers = {}
        self.pending_transactions = {}
        
    def add_signer(self, name, public_key):
        """Add authorized signer"""
        self.signers[name] = public_key
        print(f"Added signer: {name}")
    
    def create_transaction(self, tx_id, transaction_data):
        """Create new transaction requiring signatures"""
        self.pending_transactions[tx_id] = {
            'data': transaction_data,
            'signatures': {},
            'approved': False
        }
        print(f"Created transaction {tx_id}: {transaction_data}")
    
    def sign_transaction(self, tx_id, signer_name, signature):
        """Signer approves transaction"""
        if tx_id not in self.pending_transactions:
            return False, "Transaction not found"
        
        if signer_name not in self.signers:
            return False, "Unauthorized signer"
        
        tx = self.pending_transactions[tx_id]
        tx['signatures'][signer_name] = signature
        
        # Check if we have enough signatures
        sig_count = len(tx['signatures'])
        if sig_count >= self.required_sigs:
            tx['approved'] = True
            return True, f"Transaction approved! ({sig_count}/{self.required_sigs})"
        else:
            return True, f"Signature recorded ({sig_count}/{self.required_sigs})"
    
    def execute_transaction(self, tx_id):
        """Execute approved transaction"""
        if tx_id not in self.pending_transactions:
            return False, "Transaction not found"
        
        tx = self.pending_transactions[tx_id]
        if not tx['approved']:
            sig_count = len(tx['signatures'])
            return False, f"Need {self.required_sigs - sig_count} more signatures"
        
        # Execute transaction (simplified)
        print(f"Executing: {tx['data']}")
        del self.pending_transactions[tx_id]
        return True, "Transaction executed successfully"

# Example: 2-of-3 multi-sig wallet
multisig = MultiSigWallet(required_signatures=2, total_signers=3)

# Add signers
multisig.add_signer("Alice", "pubkey_alice_123...")
multisig.add_signer("Bob", "pubkey_bob_456...")  
multisig.add_signer("Carol", "pubkey_carol_789...")

# Create transaction
multisig.create_transaction("tx_001", "Send 100 ETH to 0x1234...")

# Signers approve (need 2 out of 3)
success, msg = multisig.sign_transaction("tx_001", "Alice", "signature_alice")
print(msg)

success, msg = multisig.sign_transaction("tx_001", "Bob", "signature_bob")
print(msg)

# Execute approved transaction
success, msg = multisig.execute_transaction("tx_001")
print(msg)
```

### Multi-Sig Use Cases

```python
def multisig_use_cases():
    """
    Real-world applications of multi-signature wallets
    """
    use_cases = {
        'Corporate Treasury (3-of-5)': {
            'scenario': 'Company needs multiple executives to approve large expenditures',
            'signers': 'CEO, CFO, CTO, Board Member 1, Board Member 2',
            'threshold': '3 signatures required',
            'benefit': 'Prevents single person from draining funds'
        },
        'Joint Account (2-of-2)': {
            'scenario': 'Married couple sharing cryptocurrency holdings',
            'signers': 'Spouse A, Spouse B', 
            'threshold': 'Both signatures required',
            'benefit': 'Both parties must agree to transactions'
        },
        'Escrow Service (2-of-3)': {
            'scenario': 'Buyer and seller with neutral arbitrator',
            'signers': 'Buyer, Seller, Arbitrator',
            'threshold': '2 signatures required',
            'benefit': 'Dispute resolution without central authority'
        },
        'DAO Governance (7-of-12)': {
            'scenario': 'Decentralized organization managing treasury',
            'signers': '12 elected council members',
            'threshold': '7 signatures required (majority)',
            'benefit': 'Democratic control of organizational funds'
        }
    }
    
    print("Multi-Signature Wallet Use Cases:")
    print("=" * 50)
    
    for use_case, details in use_cases.items():
        print(f"\n{use_case}:")
        for key, value in details.items():
            print(f"  {key.capitalize()}: {value}")

multisig_use_cases()
```

## Key Exchange and Agreement 🤝

### Diffie-Hellman Key Exchange

```python
def diffie_hellman_demo():
    """
    Demonstrate how two parties can agree on a shared secret
    without directly sharing it
    """
    print("Diffie-Hellman Key Exchange Demo")
    print("=" * 40)
    
    # Public parameters (known to everyone)
    p = 23  # Prime number (in reality, this is hundreds of digits)
    g = 5   # Generator (primitive root modulo p)
    
    print(f"Public Parameters:")
    print(f"  p (prime): {p}")
    print(f"  g (generator): {g}")
    
    # Alice's keys
    alice_private = 6  # Alice's secret
    alice_public = pow(g, alice_private, p)  # g^a mod p
    
    # Bob's keys  
    bob_private = 15   # Bob's secret
    bob_public = pow(g, bob_private, p)      # g^b mod p
    
    print(f"\nAlice:")
    print(f"  Private key: {alice_private} (secret)")
    print(f"  Public key:  {alice_public} (shared)")
    
    print(f"\nBob:")
    print(f"  Private key: {bob_private} (secret)")
    print(f"  Public key:  {bob_public} (shared)")
    
    # Both compute shared secret
    alice_shared = pow(bob_public, alice_private, p)    # (g^b)^a mod p
    bob_shared = pow(alice_public, bob_private, p)      # (g^a)^b mod p
    
    print(f"\nShared Secret Calculation:")
    print(f"  Alice computes: {bob_public}^{alice_private} mod {p} = {alice_shared}")
    print(f"  Bob computes:   {alice_public}^{bob_private} mod {p} = {bob_shared}")
    print(f"  Secrets match:  {alice_shared == bob_shared}")
    
    # The magic: (g^a)^b = (g^b)^a = g^(ab) mod p
    print(f"\nMathematical proof: g^(a*b) mod p = g^({alice_private}*{bob_private}) mod {p} = {pow(g, alice_private * bob_private, p)}")

diffie_hellman_demo()
```

### Elliptic Curve Diffie-Hellman (ECDH)

```python
def ecdh_explanation():
    """
    Explain ECDH used in modern blockchain systems
    """
    print("Elliptic Curve Diffie-Hellman (ECDH)")
    print("=" * 40)
    
    explanation = {
        'Classical DH': 'Uses modular exponentiation: g^x mod p',
        'ECDH': 'Uses elliptic curve point multiplication: x * G',
        'Advantage': 'Smaller keys for same security level',
        'Bitcoin Usage': 'BIP32 key derivation, Lightning Network',
        'Ethereum Usage': 'Node communication, wallet protocols'
    }
    
    for concept, description in explanation.items():
        print(f"{concept:15}: {description}")
    
    print(f"\nECDH Process:")
    print(f"1. Alice: private_a * G = public_A (point on curve)")
    print(f"2. Bob:   private_b * G = public_B (point on curve)")
    print(f"3. Alice: private_a * public_B = shared_secret")
    print(f"4. Bob:   private_b * public_A = shared_secret")
    print(f"5. Both get same point due to: private_a * (private_b * G) = private_b * (private_a * G)")

ecdh_explanation()
```

## Performance and Security Analysis ⚡

### Key Size vs Security Comparison

```python
def security_level_comparison():
    """
    Compare different cryptographic systems' security levels
    """
    import matplotlib.pyplot as plt
    
    # Security levels and corresponding key sizes
    security_data = {
        'RSA': {
            80: 1024,
            112: 2048, 
            128: 3072,
            192: 7680,
            256: 15360
        },
        'ECC': {
            80: 160,
            112: 224,
            128: 256, 
            192: 384,
            256: 512
        },
        'AES (Symmetric)': {
            80: 80,
            112: 112,
            128: 128,
            192: 192, 
            256: 256
        }
    }
    
    print("Security Level vs Key Size Comparison")
    print("=" * 50)
    print("Security | RSA (bits) | ECC (bits) | AES (bits) | ECC Advantage")
    print("-" * 65)
    
    for security_level in [80, 112, 128, 192, 256]:
        rsa_size = security_data['RSA'][security_level]
        ecc_size = security_data['ECC'][security_level]
        aes_size = security_data['AES'][security_level]
        ratio = rsa_size / ecc_size
        
        print(f"{security_level:8} | {rsa_size:10} | {ecc_size:10} | {aes_size:10} | {ratio:.1f}x smaller")

security_level_comparison()
```

### Performance Benchmarking

```python
import time
import secrets

def benchmark_key_operations():
    """
    Benchmark key generation and operations
    """
    iterations = 1000
    
    # Simulate RSA key generation (simplified)
    def simulate_rsa_keygen():
        # Real RSA is much more complex
        p = secrets.randbits(1024)
        q = secrets.randbits(1024) 
        return p * q
    
    # Simulate ECC key generation
    def simulate_ecc_keygen():
        # Real ECC uses elliptic curve math
        return secrets.randbits(256)
    
    # Benchmark key generation
    print("Key Generation Performance:")
    print("=" * 30)
    
    # RSA benchmark
    start = time.time()
    for _ in range(iterations // 10):  # Fewer iterations as RSA is slower
        simulate_rsa_keygen()
    rsa_time = time.time() - start
    
    # ECC benchmark  
    start = time.time()
    for _ in range(iterations):
        simulate_ecc_keygen()
    ecc_time = time.time() - start
    
    print(f"RSA (2048-bit):  {rsa_time:.4f}s for {iterations//10} keys")
    print(f"ECC (256-bit):   {ecc_time:.4f}s for {iterations} keys")
    print(f"ECC is ~{(rsa_time * 10) / ecc_time:.1f}x faster")
    
    # Memory usage comparison
    print(f"\nMemory Usage:")
    print(f"RSA Public Key:  256 bytes (2048 bits)")
    print(f"RSA Private Key: 1024+ bytes")
    print(f"ECC Public Key:  33 bytes (compressed)")
    print(f"ECC Private Key: 32 bytes")

benchmark_key_operations()
```

## Common Vulnerabilities and Attacks 🛡️

### Weak Random Number Generation

```python
def demonstrate_weak_rng():
    """
    Show dangers of weak random number generation
    """
    import random
    
    print("Weak Random Number Generation Dangers")
    print("=" * 45)
    
    # BAD: Using predictable random
    print("❌ INSECURE: Using Python's random module")
    random.seed(12345)  # Predictable seed
    weak_keys = [random.getrandbits(256) for _ in range(5)]
    
    # Attacker with same seed can predict keys
    random.seed(12345)  # Same seed  
    predicted_keys = [random.getrandbits(256) for _ in range(5)]
    
    print(f"Original keys match predicted: {weak_keys == predicted_keys}")
    
    # GOOD: Using cryptographically secure random
    print(f"\n✅ SECURE: Using secrets module")
    secure_keys = [secrets.randbits(256) for _ in range(5)]
    more_secure_keys = [secrets.randbits(256) for _ in range(5)]
    
    print(f"Secure keys are different: {secure_keys != more_secure_keys}")
    
    # Real-world consequences
    print(f"\nReal-world Examples:")
    print(f"• 2010: Android Bitcoin wallet bug - weak random")
    print(f"• 2013: Blockchain.info incident - predictable keys") 
    print(f"• 2018: Ethereum address collisions - poor entropy")

demonstrate_weak_rng()
```

### Side-Channel Attacks

```python
def timing_attack_demo():
    """
    Demonstrate timing attack vulnerability
    """
    import time
    
    def vulnerable_key_check(input_key, real_key):
        """
        VULNERABLE: Stops comparing at first difference
        """
        for i in range(min(len(input_key), len(real_key))):
            if input_key[i] != real_key[i]:
                return False
        return len(input_key) == len(real_key)
    
    def secure_key_check(input_key, real_key):
        """
        SECURE: Always checks full key length
        """
        if len(input_key) != len(real_key):
            return False
        
        result = True
        for i in range(len(real_key)):
            if input_key[i] != real_key[i]:
                result = False
        return result
    
    real_key = "supersecretkey123456"
    
    # Time vulnerable function
    wrong_key_short = "a"
    wrong_key_partial = "supersecret"  # Partially correct
    
    start = time.time()
    for _ in range(100000):
        vulnerable_key_check(wrong_key_short, real_key)
    time_short = time.time() - start
    
    start = time.time() 
    for _ in range(100000):
        vulnerable_key_check(wrong_key_partial, real_key)
    time_partial = time.time() - start
    
    print("Timing Attack Demonstration:")
    print(f"Short wrong key time:    {time_short:.6f}s")
    print(f"Partial match time:      {time_partial:.6f}s")
    print(f"Timing difference:       {abs(time_partial - time_short):.6f}s")
    print(f"Attacker can detect partial matches!")

timing_attack_demo()
```

## Advanced Applications 🚀

### Threshold Cryptography

```python
def threshold_cryptography_demo():
    """
    Demonstrate threshold signatures (t-of-n)
    """
    print("Threshold Cryptography (Shamir's Secret Sharing)")
    print("=" * 50)
    
    def shamir_share_secret(secret, threshold, num_shares):
        """
        Split secret into shares where any 'threshold' can reconstruct
        """
        import random
        
        # Simplified version for demonstration
        shares = []
        coefficients = [secret] + [random.randint(1, 1000) for _ in range(threshold - 1)]
        
        for i in range(1, num_shares + 1):
            # Evaluate polynomial at point i
            y = sum(coeff * (i ** power) for power, coeff in enumerate(coefficients)) % 1009
            shares.append((i, y))
        
        return shares
    
    def reconstruct_secret(shares, threshold):
        """
        Reconstruct secret from threshold number of shares
        """
        if len(shares) < threshold:
            return None
        
        # Lagrange interpolation (simplified)
        # In reality, this is more complex modular arithmetic
        secret = 0
        for i, (xi, yi) in enumerate(shares[:threshold]):
            term = yi
            for j, (xj, _) in enumerate(shares[:threshold]):
                if i != j:
                    term = (term * (0 - xj)) // (xi - xj)
            secret += term
        
        return abs(secret) % 1009
    
    # Example: 3-of-5 threshold scheme
    secret = 42  # Private key or seed
    threshold = 3
    num_shares = 5
    
    print(f"Original secret: {secret}")
    print(f"Threshold: {threshold} of {num_shares} shares needed")
    
    # Create shares
    shares = shamir_share_secret(secret, threshold, num_shares)
    print(f"\nGenerated shares:")
    for i, (x, y) in enumerate(shares):
        print(f"  Share {i+1}: ({x}, {y})")
    
    # Reconstruct with minimum threshold
    subset = shares[:threshold]
    reconstructed = reconstruct_secret(subset, threshold)
    print(f"\nReconstructed with {threshold} shares: {reconstructed}")
    print(f"Successful reconstruction: {reconstructed == secret}")

threshold_cryptography_demo()
```

### Ring Signatures (Privacy)

```python
def ring_signature_explanation():
    """
    Explain ring signatures used in privacy coins
    """
    print("Ring Signatures for Privacy")
    print("=" * 30)
    
    concept = {
        'Purpose': 'Hide the real signer among a group',
        'Process': 'Signer creates signature that could come from anyone in the ring',
        'Verification': 'Verifier knows someone in ring signed, but not who',
        'Used in': 'Monero, other privacy-focused cryptocurrencies',
        'Advantage': 'Provides plausible deniability for transactions'
    }
    
    for key, description in concept.items():
        print(f"{key:12}: {description}")
    
    print(f"\nRing Signature Example:")
    print(f"Ring members: Alice, Bob, Carol, Dave, Eve")
    print(f"Real signer: Alice (but nobody knows this)")
    print(f"Signature proves: 'Someone in this group signed'")
    print(f"Privacy result: Alice's transaction is hidden among decoys")

ring_signature_explanation()
```

### Zero-Knowledge Proofs with Keys

```python
def zk_proof_with_keys():
    """
    Demonstrate how public-private keys enable zero-knowledge proofs
    """
    print("Zero-Knowledge Proofs with Public-Private Keys")
    print("=" * 50)
    
    # Simple example: Prove you know private key without revealing it
    def create_commitment(private_key, nonce):
        """Create a commitment to prove key knowledge later"""
        commitment_data = f"{private_key}{nonce}".encode()
        return hashlib.sha256(commitment_data).hexdigest()
    
    def verify_commitment(commitment, private_key, nonce):
        """Verify the commitment matches"""
        expected = hashlib.sha256(f"{private_key}{nonce}".encode()).hexdigest()
        return commitment == expected
    
    # Alice wants to prove she knows the private key for address X
    # without revealing the private key
    
    alice_private = 12345
    alice_public = pow(2, alice_private, 1009)  # Simplified public key
    
    # Step 1: Alice creates commitment with random nonce
    nonce = secrets.randbits(128)
    commitment = create_commitment(alice_private, nonce)
    
    print(f"Alice's public key: {alice_public}")
    print(f"Alice's commitment: {commitment[:16]}...")
    
    # Step 2: Challenge (in real ZK, this would be more complex)
    challenge = "prove_you_know_private_key"
    
    # Step 3: Alice reveals nonce (but not private key)
    print(f"Challenge: {challenge}")
    print(f"Alice reveals nonce: {hex(nonce)}")
    
    # Step 4: Verifier checks commitment
    is_valid = verify_commitment(commitment, alice_private, nonce)
    print(f"Commitment verified: {is_valid}")
    print(f"Alice proved she knows private key without revealing it!")

zk_proof_with_keys()
```

## Practical Exercises and Labs 🔬

### Exercise 1: Build a Simple Cryptocurrency Wallet

```python
class SimpleCryptoWallet:
    """
    Complete cryptocurrency wallet with key management
    """
    def __init__(self, name):
        self.name = name
        self.private_key = None
        self.public_key = None
        self.address = None
        self.balance = 0
        self.transaction_history = []
    
    def generate_new_wallet(self):
        """Generate new wallet with keypair"""
        # Generate cryptographically secure private key
        self.private_key = secrets.randbits(256)
        
        # Generate public key (simplified ECC simulation)
        # Real implementation would use elliptic curve multiplication
        self.public_key = pow(2, self.private_key, 2**256 - 189)
        
        # Generate address from public key
        pubkey_bytes = self.public_key.to_bytes(32, 'big')
        address_hash = hashlib.sha256(pubkey_bytes).hexdigest()
        self.address = "1" + address_hash[:34]  # Bitcoin-style address
        
        print(f"Generated new wallet for {self.name}")
        print(f"Address: {self.address}")
        return self.address
    
    def get_public_info(self):
        """Return publicly shareable information"""
        return {
            'name': self.name,
            'address': self.address,
            'public_key': hex(self.public_key) if self.public_key else None
        }
    
    def sign_message(self, message):
        """Sign a message with private key"""
        if not self.private_key:
            raise ValueError("No private key available")
        
        # Hash the message
        message_hash = hashlib.sha256(message.encode()).digest()
        message_int = int.from_bytes(message_hash, 'big')
        
        # Sign (simplified - real implementation uses ECDSA)
        signature = pow(message_int, self.private_key, 2**256 - 189)
        return hex(signature)
    
    def verify_signature(self, message, signature, public_key):
        """Verify a signature against a public key"""
        try:
            # Hash the message
            message_hash = hashlib.sha256(message.encode()).digest()
            message_int = int.from_bytes(message_hash, 'big')
            
            # Verify (simplified)
            signature_int = int(signature, 16)
            expected = pow(signature_int, 65537, 2**256 - 189)  # Public exponent
            
            return expected == message_int
        except:
            return False
    
    def create_transaction(self, recipient_address, amount):
        """Create a signed transaction"""
        if self.balance < amount:
            return None, "Insufficient balance"
        
        transaction = {
            'from': self.address,
            'to': recipient_address,
            'amount': amount,
            'timestamp': time.time()
        }
        
        # Sign transaction
        tx_string = f"{transaction['from']}{transaction['to']}{transaction['amount']}{transaction['timestamp']}"
        signature = self.sign_message(tx_string)
        transaction['signature'] = signature
        
        return transaction, "Transaction created"
    
    def backup_wallet(self):
        """Create wallet backup (WARNING: Store securely!)"""
        if not self.private_key:
            return None
        
        backup = {
            'name': self.name,
            'private_key': hex(self.private_key),
            'address': self.address,
            'backup_date': time.time()
        }
        return backup
    
    def restore_wallet(self, backup):
        """Restore wallet from backup"""
        self.name = backup['name']
        self.private_key = int(backup['private_key'], 16)
        self.address = backup['address']
        
        # Regenerate public key
        self.public_key = pow(2, self.private_key, 2**256 - 189)
        
        print(f"Wallet restored for {self.name}")
        return True

# Example usage
print("=== Cryptocurrency Wallet Demo ===")

# Create wallets
alice = SimpleCryptoWallet("Alice")
bob = SimpleCryptoWallet("Bob")

alice_addr = alice.generate_new_wallet()
bob_addr = bob.generate_new_wallet()

# Simulate receiving funds
alice.balance = 100
print(f"Alice's balance: {alice.balance} coins")

# Create transaction
transaction, msg = alice.create_transaction(bob_addr, 25)
print(f"\nTransaction: {msg}")
if transaction:
    print(f"From: {transaction['from'][:20]}...")
    print(f"To:   {transaction['to'][:20]}...")
    print(f"Amount: {transaction['amount']}")
    print(f"Signature: {transaction['signature'][:32]}...")

# Backup and restore
backup = alice.backup_wallet()
print(f"\nWallet backup created (private key length: {len(backup['private_key'])} chars)")

# Create new wallet and restore
alice_restored = SimpleCryptoWallet("Alice Restored")
alice_restored.restore_wallet(backup)
print(f"Addresses match: {alice.address == alice_restored.address}")
```

### Exercise 2: Multi-Party Key Generation

```python
class DistributedKeyGeneration:
    """
    Simulate distributed key generation for multi-party computation
    """
    def __init__(self, parties, threshold):
        self.parties = parties
        self.threshold = threshold
        self.party_secrets = {}
        self.party_shares = {}
        self.public_keys = {}
    
    def round1_generate_secrets(self):
        """Each party generates their secret polynomial"""
        print("Round 1: Secret Generation")
        print("-" * 25)
        
        for party in self.parties:
            # Each party generates a secret polynomial
            secret = secrets.randbits(128)
            coefficients = [secret] + [secrets.randbits(128) for _ in range(self.threshold - 1)]
            
            self.party_secrets[party] = {
                'secret': secret,
                'coefficients': coefficients
            }
            
            print(f"{party} generated secret polynomial")
    
    def round2_share_distribution(self):
        """Parties distribute shares to each other"""
        print(f"\nRound 2: Share Distribution") 
        print("-" * 27)
        
        # Initialize share storage
        for party in self.parties:
            self.party_shares[party] = {}
        
        # Each party computes shares for others
        for dealer in self.parties:
            coeffs = self.party_secrets[dealer]['coefficients']
            
            for recipient_idx, recipient in enumerate(self.parties, 1):
                # Evaluate polynomial at recipient's index
                share = sum(coeff * (recipient_idx ** power) for power, coeff in enumerate(coeffs)) % (2**128)
                
                self.party_shares[recipient][dealer] = share
                
                if dealer != recipient:
                    print(f"{dealer} → {recipient}: share sent")
    
    def round3_key_derivation(self):
        """Each party derives their final private key share"""
        print(f"\nRound 3: Key Derivation")
        print("-" * 22)
        
        final_shares = {}
        
        for party in self.parties:
            # Combine all shares received from other parties
            party_share = sum(self.party_shares[party].values()) % (2**128)
            final_shares[party] = party_share
            
            # Generate corresponding public key share
            # (Simplified - real implementation uses elliptic curves)
            public_share = pow(2, party_share, 2**128 - 1)
            self.public_keys[party] = public_share
            
            print(f"{party} derived final key share")
        
        return final_shares
    
    def verify_setup(self):
        """Verify the distributed key generation was successful"""
        print(f"\nVerification Phase")
        print("-" * 18)
        
        # In real DKG, parties would verify each other's commitments
        print(f"✅ All {len(self.parties)} parties have key shares")
        print(f"✅ Threshold: {self.threshold} parties needed for signing")
        print(f"✅ Public keys generated for verification")
        
        return True

# Example: 3-of-5 distributed key generation
parties = ["Alice", "Bob", "Carol", "Dave", "Eve"]
threshold = 3

print("=== Distributed Key Generation Demo ===")
dkg = DistributedKeyGeneration(parties, threshold)

# Run DKG protocol
dkg.round1_generate_secrets()
dkg.round2_share_distribution()
final_shares = dkg.round3_key_derivation()
dkg.verify_setup()

print(f"\nResult: Distributed private key created")
print(f"Any {threshold} parties can cooperatively sign transactions")
```

### Exercise 3: Key Recovery System

```python
class SocialKeyRecovery:
    """
    Social recovery system for cryptocurrency wallets
    """
    def __init__(self, owner, guardians, threshold):
        self.owner = owner
        self.guardians = guardians
        self.threshold = threshold
        self.recovery_requests = {}
        self.guardian_approvals = {}
    
    def setup_recovery(self, master_seed):
        """Setup recovery shares with guardians"""
        print(f"Setting up social recovery for {self.owner}")
        print(f"Guardians: {', '.join(self.guardians)}")
        print(f"Recovery threshold: {self.threshold} of {len(self.guardians)}")
        
        # Split master seed using Shamir's Secret Sharing
        shares = self.split_secret(master_seed, self.threshold, len(self.guardians))
        
        # Distribute shares to guardians
        self.guardian_shares = {}
        for i, guardian in enumerate(self.guardians):
            self.guardian_shares[guardian] = shares[i]
            print(f"Recovery share given to {guardian}")
    
    def split_secret(self, secret, threshold, num_shares):
        """Simplified secret sharing"""
        import random
        
        # Generate random coefficients for polynomial
        coefficients = [secret] + [random.randint(1, 1000) for _ in range(threshold - 1)]
        
        # Generate shares
        shares = []
        for i in range(1, num_shares + 1):
            y = sum(coeff * (i ** power) for power, coeff in enumerate(coefficients)) % 10007
            shares.append((i, y))
        
        return shares
    
    def initiate_recovery(self, new_owner_address):
        """Owner initiates recovery process"""
        recovery_id = hashlib.sha256(f"{self.owner}{new_owner_address}{time.time()}".encode()).hexdigest()[:16]
        
        self.recovery_requests[recovery_id] = {
            'new_owner': new_owner_address,
            'initiated': time.time(),
            'approvals': set(),
            'status': 'pending'
        }
        
        print(f"Recovery initiated by {self.owner}")
        print(f"Recovery ID: {recovery_id}")
        print(f"New owner address: {new_owner_address}")
        
        return recovery_id
    
    def guardian_approve(self, recovery_id, guardian_name, guardian_share):
        """Guardian approves recovery request"""
        if recovery_id not in self.recovery_requests:
            return False, "Invalid recovery request"
        
        if guardian_name not in self.guardians:
            return False, "Unauthorized guardian"
        
        request = self.recovery_requests[recovery_id]
        
        # Verify guardian has valid share
        expected_share = self.guardian_shares.get(guardian_name)
        if expected_share != guardian_share:
            return False, "Invalid guardian share"
        
        # Add approval
        request['approvals'].add(guardian_name)
        
        print(f"Guardian {guardian_name} approved recovery")
        print(f"Approvals: {len(request['approvals'])}/{self.threshold}")
        
        # Check if threshold reached
        if len(request['approvals']) >= self.threshold:
            request['status'] = 'approved'
            return True, "Recovery approved - sufficient guardians"
        
        return True, f"Approval recorded - need {self.threshold - len(request['approvals'])} more"
    
    def execute_recovery(self, recovery_id):
        """Execute approved recovery"""
        if recovery_id not in self.recovery_requests:
            return False, "Invalid recovery request"
        
        request = self.recovery_requests[recovery_id]
        
        if request['status'] != 'approved':
            return False, "Recovery not yet approved"
        
        if len(request['approvals']) < self.threshold:
            return False, "Insufficient approvals"
        
        # Collect shares from approving guardians
        approving_guardians = list(request['approvals'])[:self.threshold]
        recovery_shares = [self.guardian_shares[guardian] for guardian in approving_guardians]
        
        # Reconstruct master seed
        recovered_seed = self.reconstruct_secret(recovery_shares, self.threshold)
        
        print(f"Recovery executed successfully!")
        print(f"Master seed reconstructed from {self.threshold} guardian shares")
        print(f"Wallet control transferred to: {request['new_owner']}")
        
        # In real implementation, would generate new keys from recovered seed
        return True, recovered_seed
    
    def reconstruct_secret(self, shares, threshold):
        """Reconstruct secret from threshold shares"""
        if len(shares) < threshold:
            return None
        
        # Lagrange interpolation (simplified)
        secret = 0
        for i, (xi, yi) in enumerate(shares[:threshold]):
            term = yi
            for j, (xj, _) in enumerate(shares[:threshold]):
                if i != j:
                    term = (term * (0 - xj)) // (xi - xj)
            secret += term
        
        return abs(secret) % 10007

# Example usage
print("=== Social Key Recovery Demo ===")

# Setup recovery system
owner = "Alice"
guardians = ["Bob", "Carol", "Dave", "Eve", "Frank"]
threshold = 3

recovery_system = SocialKeyRecovery(owner, guardians, threshold)

# Setup with master seed
master_seed = 12345  # In reality, this would be a 256-bit seed
recovery_system.setup_recovery(master_seed)

print(f"\n--- Recovery Scenario ---")
print("Alice lost her phone and needs to recover wallet")

# Initiate recovery
new_address = "0x742d35Cc6634C0532925a3b8D4C4Db4C8b"
recovery_id = recovery_system.initiate_recovery(new_address)

# Guardians approve recovery
print(f"\nGuardians approving recovery:")
guardians_to_approve = ["Bob", "Carol", "Dave"]  # 3 out of 5

for guardian in guardians_to_approve:
    guardian_share = recovery_system.guardian_shares[guardian]
    success, message = recovery_system.guardian_approve(recovery_id, guardian, guardian_share)
    print(f"{guardian}: {message}")

# Execute recovery
success, recovered_seed = recovery_system.execute_recovery(recovery_id)
print(f"\nRecovered seed matches original: {recovered_seed == master_seed}")
```

## Quiz: Test Your Knowledge 🧠

### Question 1: Key Properties
Which property makes public-key cryptography secure?

A) Public and private keys are identical  
B) Private key can be easily derived from public key  
C) It's computationally infeasible to derive private key from public key  
D) Keys are generated using simple multiplication

<details>
<summary>Click for answer</summary>

**Answer: C) It's computationally infeasible to derive private key from public key**

This is the foundation of public-key security. While the keys are mathematically related, the relationship is based on one-way mathematical functions that are easy to compute in one direction but practically impossible to reverse without the private key.
</details>

### Question 2: Multi-Signature Analysis
A 3-of-5 multi-signature wallet means:

A) 3 people own the wallet, 5 people can access it  
B) 3 signatures are required out of 5 possible signers  
C) The wallet has 3 addresses and 5 private keys  
D) 5 signatures are needed, but only 3 are checked

<details>
<summary>Click for answer</summary>

**Answer: B) 3 signatures are required out of 5 possible signers**

This is a threshold signature scheme where any 3 of the 5 authorized signers can approve a transaction. It provides security (no single point of failure) while maintaining usability (don't need all 5 signatures).
</details>

### Question 3: Key Size Comparison
For equivalent security, which requires the smallest key size?

A) RSA  
B) Elliptic Curve Cryptography (ECC)  
C) Diffie-Hellman  
D) All require the same key size

<details>
<summary>Click for answer</summary>

**Answer: B) Elliptic Curve Cryptography (ECC)**

ECC provides the same security level with much smaller keys. For example:
- 128-bit security: RSA needs 3072 bits, ECC needs only 256 bits
- This makes ECC ideal for mobile devices and blockchain applications
</details>

### Question 4: Blockchain Address Generation
In Bitcoin, the address is generated by:

A) Using the private key directly  
B) Hashing the public key (with additional steps)  
C) Combining private and public keys  
D) Random generation

<details>
<summary>Click for answer</summary>

**Answer: B) Hashing the public key (with additional steps)**

Bitcoin addresses are created by:
1. Taking the public key
2. SHA-256 hashing it
3. RIPEMD-160 hashing the result  
4. Adding version bytes and checksum
5. Base58 encoding the final result

This creates a shorter, more user-friendly address while maintaining security.
</details>

## Summary: Key Takeaways 🎯

### Essential Concepts Mastered

1. **Asymmetric Cryptography**: Two related but different keys solve the key distribution problem
2. **Mathematical Foundation**: Security based on one-way mathematical functions  
3. **Key Generation**: Cryptographically secure random numbers are critical
4. **Blockchain Applications**: Address generation, transaction signing, wallet security
5. **Multi-Signature Systems**: Distributed control and enhanced security
6. **Key Management**: Backup, recovery, and security best practices

### Cryptographic Systems Compared

| System | Key Size | Speed | Security | Blockchain Use |
|--------|----------|--------|----------|----------------|
| **RSA** | Large (2048+ bits) | Slow | High | Legacy systems |
| **ECC** | Small (256 bits) | Fast | High | Bitcoin, Ethereum |
| **Ed25519** | Small (256 bits) | Very Fast | Very High | Solana, modern chains |

### Security Best Practices

- ✅ **Use hardware wallets** for key storage
- ✅ **Generate keys with cryptographically secure randomness**
- ✅ **Implement multi-signature** for high-value wallets
- ✅ **Create secure backups** with social recovery
- ✅ **Never share private keys** with anyone
- ❌ **Don't store keys on internet-connected devices**
- ❌ **Don't use predictable key generation methods**
- ❌ **Don't implement crypto yourself** - use established libraries

### Real-World Impact

Public-private key cryptography enables:
- **Trustless transactions** without intermediaries
- **Global financial access** without traditional banking
- **Self-sovereign identity** and asset control
- **Programmable money** through smart contracts
- **Privacy-preserving** financial systems

## Next Steps in Your Cryptography Journey 🚀

You now understand the mathematical foundation that makes blockchain possible! Continue with:

➡️ [Digital Signatures](digital-signatures.md) - Learn how to prove authenticity and prevent tampering  
➡️ [Merkle Trees](merkle-trees.md) - Efficient verification of large datasets  
➡️ [Bitcoin Deep Dive](../02-bitcoin/bitcoin-basics.md) - See these concepts in action

## Additional Resources 📚

### Technical References
- [RSA Algorithm - Original Paper](https://people.csail.mit.edu/rivest/Rsapaper.pdf)
- [Elliptic Curve Cryptography - NIST Guide](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf)
- [secp256k1 Curve Parameters](https://www.secg.org/sec2-v2.pdf)

### Interactive Tools
- [RSA Key Generator](https://travistidwell.com/jsencrypt/demo/)
- [ECC Visualization](https://cdn.rawgit.com/andreacorbellini/ecc/920b29a/interactive/reals-add.html)
- [Bitcoin Address Generator](https://www.bitaddress.org) (Use offline only!)

### Academic Papers
- "New Directions in Cryptography" - Diffie & Hellman (1976)
- "A Method for Obtaining Digital Signatures" - Rivest, Shamir & Adleman (1978) 
- "Elliptic Curves in Cryptography" - Koblitz (1987)

---

**🎯 Learning Objective Achieved**: You now understand how public-private key cryptography enables secure, trustless interactions in blockchain systems!

**⏰ Estimated Reading Time**: 45-50 minutes  
**🎖️ Badge Progress**: Crypto Master (50% Complete)

**Ready to learn about proving authenticity?** Continue to [Digital Signatures](digital-signatures.md) to discover how blockchain ensures non-repudiation!# Public-Private Keys 🔐

## Introduction

Imagine you have a magical mailbox with two special keys: one key (public) that anyone can use to put mail IN the box, but only you have the other key (private) that can take mail OUT. This is the essence of public-private key cryptography - the revolutionary system that makes secure blockchain transactions possible without ever sharing secrets.

This cryptographic innovation, also known as asymmetric cryptography, solved one of the greatest challenges in secure communication: how can two parties who have never met exchange information securely over an insecure network? The answer transformed not just blockchain, but the entire internet.

## The Fundamental Problem: Key Distribution 🗝️

### Traditional Cryptography Challenge

Before public-key cryptography, all encryption was **symmetric**:

```
Traditional Symmetric Encryption:
Alice and Bob need the SAME secret key

Step 1: Alice and Bob must somehow share a secret key
Step 2: Alice encrypts message with secret key
Step 3: Alice sends encrypted message to Bob
Step 4: Bob decrypts message with the same secret key

PROBLEM: How do Alice and Bob share the secret key securely?
```

**The Chicken-and-Egg Problem:**
- Need secure communication to share the secret key
- But need the secret key to have secure communication!

### The Revolutionary Solution: Asymmetric Keys

Public-key cryptography elegantly solves this with **two different keys**:

```
Asymmetric Encryption:
Each person has a KEY PAIR (public + private)

Alice's Keys:        Bob's Keys:
- Public Key A       - Public Key B
- Private Key A      - Private Key B

Alice can encrypt TO Bob using Bob's PUBLIC key
Only Bob can decrypt using his PRIVATE key
```

## How Public-Private Key Cryptography Works 🔧

### Key Generation

The magic starts with **mathematical relationships** between the two keys:

```python
# Conceptual example (simplified)
import random

def generate_keypair():
    """
    Simplified key generation (NOT secure - educational only!)
    Real implementation uses complex mathematical functions
    """
    # In reality, this involves:
    # - Large prime numbers (RSA)
    # - Elliptic curve mathematics (ECDSA)
    # - Complex modular arithmetic
    
    private_key = random.randint(1, 1000000)  # Secret number
    public_key = (private_key * 17) % 1000003  # Mathematical relationship
    
    return private_key, public_key

# Generate keypair
private, public = generate_keypair()
print(f"Private Key: {private} (KEEP SECRET!)")
print(f"Public Key:  {public} (SHARE FREELY!)")
```

### The Mathematical Magic

The security relies on **mathematical one-way functions**:

```
Easy Direction:    Private Key → Public Key (fast computation)
Hard Direction:    Public Key → Private Key (practically impossible)

Examples:
- RSA: Based on factoring large prime numbers
- ECDSA: Based on elliptic curve discrete logarithm problem  
- Ed25519: Based on twisted Edwards curves
```

### Core Properties

1. **Related but Different**: Keys are mathematically related but distinct
2. **Computationally Infeasible**: Can't derive private from public key
3. **Bidirectional Operations**: Either key can be used for encryption/decryption
4. **Signature Capability**: Private key can create signatures only public key can verify

## Real Cryptographic Systems 🛡️

### RSA (Rivest-Shamir-Adleman)

**How RSA Works:**

```python
# RSA Key Generation (simplified educational version)
def simple_rsa_keygen():
    """
    Educational RSA - DO NOT USE FOR REAL SECURITY!
    Real RSA uses 2048+ bit numbers
    """
    # Step 1: Choose two prime numbers
    p = 61  # In reality, this would be hundreds of digits long
    q = 53
    
    # Step 2: Calculate n = p * q
    n = p * q  # 61 * 53 = 3233
    
    # Step 3: Calculate φ(n) = (p-1)(q-1)  
    phi = (p - 1) * (q - 1)  # 60 * 52 = 3120
    
    # Step 4: Choose e (public exponent)
    e = 17  # Common choice, coprime with φ(n)
    
    # Step 5: Calculate d (private exponent)
    # d is the modular inverse of e mod φ(n)
    d = pow(e, -1, phi)  # d = 2753
    
    # Public key: (n, e)
    # Private key: (n, d) 
    return (n, e), (n, d)

# Generate RSA keypair
public_key, private_key = simple_rsa_keygen()
print(f"RSA Public Key:  n={public_key[0]}, e={public_key[1]}")
print(f"RSA Private Key: n={private_key[0]}, d={private_key[1]}")

# RSA Encryption/Decryption
def rsa_encrypt(message_int, public_key):
    n, e = public_key
    return pow(message_int, e, n)

def rsa_decrypt(ciphertext, private_key):
    n, d = private_key
    return pow(ciphertext, d, n)

# Example
message = 42  # In reality, we'd convert text to numbers
encrypted = rsa_encrypt(message, public_key)
decrypted = rsa_decrypt(encrypted, private_key)

print(f"\nRSA Example:")
print(f"Original:  {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
```

**RSA Security:**
- Security based on difficulty of factoring large numbers
- Current recommendation: 2048-bit keys minimum
- 4096-bit keys for high-security applications

### Elliptic Curve Cryptography (ECC)

**Used by:** Bitcoin, Ethereum, most modern blockchains

```python
# Conceptual ECC explanation
def explain_elliptic_curves():
    """
    Elliptic curves: y² = x³ + ax + b
    
    Bitcoin uses secp256k1 curve: y² = x³ + 7
    """
    
    # Key properties of elliptic curves:
    properties = {
        'Point Addition': 'Adding two points gives another point on curve',
        'Scalar Multiplication': 'Multiplying point by number (private key)',
        'One-Way Function': 'Easy: k*G = P, Hard: Given P and G, find k',
        'Discrete Log Problem': 'Foundation of ECC security'
    }
    
    print("Elliptic Curve Cryptography (Bitcoin's secp256k1):")
    for prop, desc in properties.items():
        print(f"  {prop}: {desc}")
    
    # Bitcoin's approach
    print(f"\nBitcoin Key Generation:")
    print(f"1. Private Key: Random 256-bit number (k)")
    print(f"2. Public Key:  k * G (where G is generator point)")
    print(f"3. Address:     hash(Public Key)")

explain_elliptic_curves()
```

**ECC Advantages:**
- Smaller key sizes for same security level
- Faster computation than RSA
- Lower memory and bandwidth requirements
- Perfect for mobile and blockchain applications

**Security Comparison:**
```
Security Level | RSA Key Size | ECC Key Size | Ratio
80-bit        | 1024 bits    | 160 bits     | 6.4:1
112-bit       | 2048 bits    | 224 bits     | 9.1:1  
128-bit       | 3072 bits    | 256 bits     | 12:1
256-bit       | 15360 bits   | 512 bits     | 30:1
```

### Ed25519 (EdDSA)

**Used by:** Solana, Monero, some newer cryptocurrencies

```python
# Ed25519 properties
def ed25519_overview():
    """
    Ed25519: Modern elliptic curve signature scheme
    """
    advantages = {
        'Security': 'Designed to avoid security pitfalls',
        'Performance': 'Very fast signature generation/verification', 
        'Deterministic': 'Same input always gives same signature',
        'Small Keys': '32-byte public keys, 64-byte signatures',
        'Side-Channel Resistance': 'Resistant to timing attacks'
    }
    
    print("Ed25519 (EdDSA) Advantages:")
    for feature, description in advantages.items():
        print(f"  {feature}: {description}")

ed25519_overview()
```

## Blockchain Applications 🔗

### Bitcoin Address Generation

```python
import hashlib

def bitcoin_address_generation():
    """
    How Bitcoin creates addresses from public keys
    """
    # Step 1: Start with a private key (256-bit number)
    private_key = "18e14a7b6a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321725"
    print(f"1. Private Key: {private_key}")
    
    # Step 2: Generate public key (in reality, this uses elliptic curve math)
    # For demonstration, we'll simulate the process
    public_key_x = "50863ad64a87ae8a2fe83c1af1a8403cb53f53e486d8511dad8a04887e5b2352"
    public_key_y = "2cd470243453a299fa9e77237716103abc11a1df38855ed6f2ee187e9c582ba6"
    
    # Compressed public key (33 bytes)
    if int(public_key_y, 16) % 2 == 0:
        compressed_pubkey = "02" + public_key_x
    else:
        compressed_pubkey = "03" + public_key_x
    
    print(f"2. Compressed Public Key: {compressed_pubkey}")
    
    # Step 3: SHA-256 hash of public key
    pubkey_bytes = bytes.fromhex(compressed_pubkey)
    sha256_hash = hashlib.sha256(pubkey_bytes).digest()
    print(f"3. SHA-256 Hash: {sha256_hash.hex()}")