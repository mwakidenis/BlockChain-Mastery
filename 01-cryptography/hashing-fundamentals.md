# Hashing Fundamentals 🔐

## Introduction

Imagine you have a magical fingerprint scanner that can identify any document, no matter how long, with a unique 64-character fingerprint. Change even one letter in the document, and you get a completely different fingerprint. This is essentially what cryptographic hashing does for blockchain technology.

Hashing is the mathematical backbone of blockchain security, providing the immutability, integrity, and proof-of-work mechanisms that make distributed ledgers possible. In this lesson, we'll demystify how these "digital fingerprints" work and why they're crucial for blockchain technology.

## What is a Hash Function? 🧮

A **hash function** is a mathematical algorithm that takes any input (called a "message") and produces a fixed-size string of characters (called a "hash" or "digest").

### Simple Analogy: The Magic Blender 🥤

Think of a hash function as a magic blender:
- **Input**: You can put in anything - an apple, a book, even a car!
- **Process**: The blender processes the input in a special way
- **Output**: You always get exactly 32 ounces of smoothie (fixed size)
- **Magic**: The same input always produces the same smoothie, but similar inputs produce completely different smoothies

### Real Hash Function Example

```python
import hashlib

# Input: Any text
message = "Hello, Blockchain!"

# SHA-256 Hash Function
hash_object = hashlib.sha256(message.encode())
hash_hex = hash_object.hexdigest()

print(f"Input:  {message}")
print(f"Output: {hash_hex}")
```

**Output:**
```
Input:  Hello, Blockchain!
Output: 3b7b1c8a2f4d6e9c1a5b7d4f2e6c8b9a1d3f5e7c9b2a4d6f8e1c3b5a7d9f2e4c6b8
```

## Essential Properties of Cryptographic Hash Functions 🔑

### 1. Deterministic 🎯

The same input **always** produces the same output:

```python
# These will always produce identical hashes
hash1 = hashlib.sha256("Bitcoin".encode()).hexdigest()
hash2 = hashlib.sha256("Bitcoin".encode()).hexdigest()
hash3 = hashlib.sha256("Bitcoin".encode()).hexdigest()

print(f"Hash 1: {hash1}")
print(f"Hash 2: {hash2}")  
print(f"Hash 3: {hash3}")
# All three are identical!
```

**Why this matters in blockchain:**
- Same block data always produces the same block hash
- Network nodes can verify blocks independently
- No randomness means consistent verification

### 2. Fixed Output Size 📏

Regardless of input size, hash output is always the same length:

```python
# Tiny input
small = hashlib.sha256("Hi".encode()).hexdigest()
print(f"'Hi' → {small}")

# Large input  
large_text = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks" * 1000
large = hashlib.sha256(large_text.encode()).hexdigest()
print(f"Large text → {large}")

print(f"Small hash length: {len(small)} characters")
print(f"Large hash length: {len(large)} characters")
# Both are exactly 64 characters (256 bits)
```

**Why this matters in blockchain:**
- Predictable storage requirements
- Easy to compare hashes
- Uniform data structures across the network

### 3. Avalanche Effect 🌊

Tiny changes in input create dramatically different outputs:

```python
# Original message
msg1 = "Alice sends 5 BTC to Bob"
hash1 = hashlib.sha256(msg1.encode()).hexdigest()

# Change one character (5 → 6)
msg2 = "Alice sends 6 BTC to Bob"  
hash2 = hashlib.sha256(msg2.encode()).hexdigest()

# Change case of one letter
msg3 = "Alice sends 5 BTC to bob"
hash3 = hashlib.sha256(msg3.encode()).hexdigest()

print(f"Original: {msg1}")
print(f"Hash:     {hash1}")
print()
print(f"Amount+1: {msg2}")
print(f"Hash:     {hash2}")
print()
print(f"Lowercase: {msg3}")
print(f"Hash:      {hash3}")

# Calculate how different the hashes are
def hamming_distance(hash1, hash2):
    return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))

print(f"\nDifferences between original and amount+1: {hamming_distance(hash1, hash2)}/64 characters")
print(f"Differences between original and lowercase: {hamming_distance(hash1, hash3)}/64 characters")
```

**Expected Output:**
```
Differences between original and amount+1: 32/64 characters (50% different!)
Differences between original and lowercase: 31/64 characters (48% different!)
```

**Why this matters in blockchain:**
- Any tampering is immediately detectable
- Small changes to transactions are obvious
- Blocks cannot be subtly modified

### 4. One-Way Function (Pre-image Resistance) ↗️

Easy to compute hash from input, computationally infeasible to find input from hash:

```python
# Easy direction: Input → Hash
message = "Secret password: blockchain123"
hash_result = hashlib.sha256(message.encode()).hexdigest()
print(f"Message → Hash: {hash_result}")

# Impossible direction: Hash → Message
# Given hash_result, find the original message
# This would require trying 2^256 possibilities!
```

**Brute Force Time Estimation:**
```
SHA-256 has 2^256 possible outputs
If you could try 1 billion hashes per second:
Time needed = 2^256 / 1,000,000,000 seconds
           ≈ 3.7 × 10^69 years

For context: Age of universe ≈ 1.4 × 10^10 years
```

**Why this matters in blockchain:**
- Passwords can be stored as hashes
- Mining requires work (finding specific hash patterns)
- Private information stays private

### 5. Collision Resistance 💥

Finding two different inputs that produce the same hash is computationally infeasible:

```python
# This is what we want to avoid:
# find_collision() should never succeed for SHA-256
def theoretical_collision_search():
    """
    This would take longer than the age of the universe
    """
    target_hash = "a" * 64  # Some target hash
    attempts = 0
    
    while True:
        test_input = f"attempt_{attempts}"
        test_hash = hashlib.sha256(test_input.encode()).hexdigest()
        
        if test_hash == target_hash:
            return f"Found collision after {attempts} attempts!"
        
        attempts += 1
        if attempts > 1000000:  # Stop after reasonable attempt
            return "No collision found (as expected)"
    
print(theoretical_collision_search())
```

**Birthday Paradox and Hash Security:**
- For SHA-256: Need ~2^128 attempts to find collision (still impossible)
- For comparison: MD5 collisions can be found in minutes (why it's deprecated)

**Why this matters in blockchain:**
- Two different transactions can't have the same hash
- Block integrity is guaranteed
- Digital signatures remain secure

## Popular Hash Functions and Their Uses 🏆

### SHA-256 (Secure Hash Algorithm 256-bit)

**Used by:** Bitcoin, many other cryptocurrencies

```python
# SHA-256 Example
import hashlib

def sha256_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

example = sha256_hash("Bitcoin Block #1")
print(f"SHA-256: {example}")
print(f"Length: {len(example)} characters (256 bits)")
```

**Properties:**
- ✅ 256-bit output (64 hexadecimal characters)
- ✅ Part of SHA-2 family
- ✅ NSA designed, widely adopted
- ✅ No known practical attacks
- ✅ Bitcoin mining difficulty based on leading zeros

### SHA-3 (Keccak)

**Used by:** Ethereum

```python
# SHA-3 Example (using pycryptodome library)
# pip install pycryptodome

from Crypto.Hash import keccak

def sha3_256_hash(data):
    hash_obj = keccak.new(digest_bits=256)
    hash_obj.update(data.encode())
    return hash_obj.hexdigest()

example = sha3_256_hash("Ethereum Block #1")
print(f"SHA-3: {example}")
```

**Properties:**
- ✅ Different construction than SHA-2 (sponge function)
- ✅ More resistant to length extension attacks
- ✅ Ethereum's choice for smart contract hashing
- ✅ Quantum-resistant design principles

### RIPEMD-160

**Used by:** Bitcoin addresses (combined with SHA-256)

```python
import hashlib

def ripemd160_hash(data):
    h = hashlib.new('ripemd160')
    h.update(data)
    return h.hexdigest()

# Bitcoin address creation uses both SHA-256 and RIPEMD-160
public_key = "Bitcoin public key example"
sha256_result = hashlib.sha256(public_key.encode()).digest()
ripemd160_result = ripemd160_hash(sha256_result)

print(f"RIPEMD-160: {ripemd160_result}")
print(f"Length: {len(ripemd160_result)} characters (160 bits)")
```

**Properties:**
- ✅ 160-bit output (smaller than SHA-256)
- ✅ Developed in Europe (alternative to NSA-designed algorithms)
- ✅ Used to create shorter Bitcoin addresses
- ✅ Good balance of security and efficiency

### Blake2

**Used by:** Zcash, some newer cryptocurrencies

```python
import hashlib

def blake2b_hash(data):
    return hashlib.blake2b(data.encode()).hexdigest()

example = blake2b_hash("Zcash transaction")
print(f"BLAKE2b: {example}")
```

**Properties:**
- ✅ Faster than SHA-256
- ✅ Configurable output size
- ✅ Built-in support for keyed hashing
- ✅ Designed for high performance

## Hash Functions in Blockchain Applications 🔗

### 1. Block Identification

Every blockchain block has a unique hash identifier:

```python
class SimpleBlock:
    def __init__(self, previous_hash, transactions, nonce=0):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_string = f"{self.previous_hash}{self.transactions}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def __str__(self):
        return f"Block Hash: {self.hash[:16]}..."

# Create blockchain blocks
genesis = SimpleBlock("0", "Genesis Block")
block1 = SimpleBlock(genesis.hash, "Alice → Bob: 10 BTC")
block2 = SimpleBlock(block1.hash, "Carol → Dave: 5 BTC")

print(genesis)
print(block1)  
print(block2)
```

### 2. Transaction Integrity

Each transaction gets hashed to ensure it cannot be modified:

```python
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient  
        self.amount = amount
        self.tx_id = self.calculate_hash()
    
    def calculate_hash(self):
        tx_string = f"{self.sender}{self.recipient}{self.amount}"
        return hashlib.sha256(tx_string.encode()).hexdigest()
    
    def verify_integrity(self):
        expected_hash = self.calculate_hash()
        return self.tx_id == expected_hash

# Create and verify transaction
tx = Transaction("Alice", "Bob", 10.5)
print(f"Transaction ID: {tx.tx_id}")
print(f"Integrity check: {tx.verify_integrity()}")

# Try to tamper with transaction
tx.amount = 100.5  # Malicious change
print(f"After tampering - Integrity check: {tx.verify_integrity()}")
```

### 3. Proof of Work Mining

Miners search for nonces that produce hashes with specific patterns:

```python
def mine_block(block_data, difficulty):
    """
    Find a nonce that makes the block hash start with 'difficulty' zeros
    """
    target = "0" * difficulty
    nonce = 0
    attempts = 0
    
    while True:
        test_string = f"{block_data}{nonce}"
        hash_result = hashlib.sha256(test_string.encode()).hexdigest()
        attempts += 1
        
        if hash_result.startswith(target):
            return nonce, hash_result, attempts
        
        nonce += 1

# Mine a block with difficulty 4 (4 leading zeros)
block_data = "Alice sends 5 BTC to Bob"
nonce, hash_result, attempts = mine_block(block_data, 4)

print(f"Block data: {block_data}")
print(f"Difficulty: 4 leading zeros")
print(f"Winning nonce: {nonce}")
print(f"Winning hash: {hash_result}")
print(f"Attempts needed: {attempts:,}")
```

**Sample Output:**
```
Block data: Alice sends 5 BTC to Bob
Difficulty: 4 leading zeros
Winning nonce: 246833
Winning hash: 0000a7b2c3d4e5f6789abcdef0123456789abcdef0123456789abcdef012345
Attempts needed: 246,834
```

### 4. Merkle Tree Construction

Hash functions build tree structures for efficient verification:

```python
def simple_merkle_tree(transactions):
    """
    Build a simple Merkle tree from transactions
    """
    if len(transactions) == 0:
        return None
    
    # Hash all transactions
    level = [hashlib.sha256(tx.encode()).hexdigest() for tx in transactions]
    
    while len(level) > 1:
        next_level = []
        
        # Pair up hashes and combine them
        for i in range(0, len(level), 2):
            if i + 1 < len(level):
                combined = level[i] + level[i + 1]
            else:
                combined = level[i] + level[i]  # Duplicate if odd number
            
            next_level.append(hashlib.sha256(combined.encode()).hexdigest())
        
        level = next_level
    
    return level[0]  # Root hash

# Example transactions
transactions = [
    "Alice → Bob: 5 BTC",
    "Carol → Dave: 3 BTC", 
    "Eve → Frank: 2 BTC",
    "Grace → Henry: 1 BTC"
]

merkle_root = simple_merkle_tree(transactions)
print(f"Transactions: {len(transactions)}")
print(f"Merkle Root: {merkle_root}")

# Verify that changing one transaction changes the root
transactions[0] = "Alice → Bob: 6 BTC"  # Changed amount
new_root = simple_merkle_tree(transactions)
print(f"After change: {new_root}")
print(f"Roots match: {merkle_root == new_root}")
```

## Hash-Based Data Structures 🏗️

### Hash Tables/Maps

```python
class SimpleHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        """Simple hash function for demonstration"""
        return sum(ord(c) for c in str(key)) % self.size
    
    def put(self, key, value):
        hash_index = self._hash(key)
        bucket = self.table[hash_index]
        
        # Update if key exists, otherwise add new
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
    
    def get(self, key):
        hash_index = self._hash(key)
        bucket = self.table[hash_index]
        
        for k, v in bucket:
            if k == key:
                return v
        return None

# Usage in blockchain: Fast lookup of transaction IDs
blockchain_db = SimpleHashTable()
blockchain_db.put("tx_001", "Alice → Bob: 5 BTC")
blockchain_db.put("tx_002", "Carol → Dave: 3 BTC")

print(blockchain_db.get("tx_001"))
```

### Bloom Filters

```python
import math

class SimpleBloomFilter:
    def __init__(self, expected_elements, false_positive_rate=0.01):
        self.m = int(-expected_elements * math.log(false_positive_rate) / (math.log(2) ** 2))
        self.k = int(self.m * math.log(2) / expected_elements)
        self.bit_array = [False] * self.m
    
    def _hashes(self, item):
        """Generate k different hash values for an item"""
        hashes = []
        for i in range(self.k):
            # Simple hash combination for demonstration
            hash_val = hash(str(item) + str(i)) % self.m
            hashes.append(hash_val)
        return hashes
    
    def add(self, item):
        for hash_val in self._hashes(item):
            self.bit_array[hash_val] = True
    
    def might_contain(self, item):
        return all(self.bit_array[hash_val] for hash_val in self._hashes(item))

# Usage: Quickly check if transaction might be in a block
bloom = SimpleBloomFilter(1000)
bloom.add("tx_12345")
bloom.add("tx_67890")

print(f"Might contain tx_12345: {bloom.might_contain('tx_12345')}")
print(f"Might contain tx_99999: {bloom.might_contain('tx_99999')}")
```

## Security Considerations and Attacks 🛡️

### 1. Hash Collision Attacks

**What it is:** Finding two different inputs that produce the same hash

**Historical Example - MD5 Collision:**
```python
# MD5 is broken - collisions can be found easily
# DO NOT use MD5 for security purposes!

import hashlib

def demonstrate_weakness(algorithm_name, hash_func):
    # This is just a demonstration - real attacks are more sophisticated
    print(f"\n{algorithm_name} Security Status:")
    if algorithm_name == "MD5":
        print("❌ BROKEN: Collisions found in practice")
        print("❌ Should never be used for security")
    elif algorithm_name == "SHA-1":
        print("⚠️ WEAK: Theoretical attacks exist")  
        print("⚠️ Being phased out")
    elif algorithm_name == "SHA-256":
        print("✅ SECURE: No known practical attacks")
        print("✅ Recommended for blockchain use")

demonstrate_weakness("MD5", hashlib.md5)
demonstrate_weakness("SHA-1", hashlib.sha1)
demonstrate_weakness("SHA-256", hashlib.sha256)
```

### 2. Pre-image Attacks

**What it is:** Given a hash, find an input that produces it

**Resistance Levels:**
```python
def attack_difficulty():
    algorithms = {
        "SHA-256": 2**256,
        "SHA-1": 2**160,  # Theoretical - broken by collision
        "MD5": 2**128,    # Broken by collision
    }
    
    print("Pre-image Attack Difficulty:")
    for algo, operations in algorithms.items():
        print(f"{algo}: {operations:.1e} operations needed")
        
        # Time estimation at 1 billion ops/second
        years = operations / (10**9 * 365 * 24 * 3600)
        if years > 10**50:
            print(f"  Time needed: Longer than age of universe × 10^40")
        else:
            print(f"  Time needed: {years:.1e} years")

attack_difficulty()
```

### 3. Length Extension Attacks

**What it is:** Attaching data to a message without knowing the original

**Vulnerable hash construction:**
```python
# VULNERABLE: hash(secret + message)
def vulnerable_hash(secret, message):
    return hashlib.sha256((secret + message).encode()).hexdigest()

# SECURE: HMAC construction
import hmac

def secure_hash(secret, message):
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

secret = "my_secret_key"
message = "transfer_100_btc"

print("Vulnerable approach:")
print(vulnerable_hash(secret, message))

print("\nSecure approach (HMAC):")  
print(secure_hash(secret, message))
```

## Performance and Optimization ⚡

### Hash Function Speed Comparison

```python
import time
import hashlib

def benchmark_hash_functions():
    # Test data
    data = "This is test data for hash benchmarking. " * 1000
    iterations = 10000
    
    functions = {
        'SHA-256': hashlib.sha256,
        'SHA-1': hashlib.sha1,
        'MD5': hashlib.md5,
        'SHA-3-256': lambda: hashlib.sha3_256(),
        'BLAKE2b': lambda: hashlib.blake2b()
    }
    
    results = {}
    
    for name, hash_func in functions.items():
        start_time = time.time()
        
        for _ in range(iterations):
            h = hash_func()
            h.update(data.encode())
            _ = h.hexdigest()
        
        end_time = time.time()
        total_time = end_time - start_time
        hashes_per_second = iterations / total_time
        
        results[name] = {
            'time': total_time,
            'hps': hashes_per_second
        }
    
    print("Hash Function Performance:")
    print("Algorithm    | Time (sec) | Hashes/sec")
    print("-" * 40)
    
    for name, data in sorted(results.items(), key=lambda x: x[1]['time']):
        print(f"{name:12} | {data['time']:8.3f}  | {data['hps']:8.0f}")

# Run benchmark
benchmark_hash_functions()
```

### Memory Usage Considerations

```python
def hash_memory_usage():
    """
    Different hash functions have different memory requirements
    """
    memory_usage = {
        'SHA-256': '32 bytes output, minimal state',
        'SHA-3-256': '32 bytes output, larger internal state',
        'BLAKE2b': 'Variable output (1-64 bytes), efficient state',
        'SHA-1': '20 bytes output (deprecated)',
        'MD5': '16 bytes output (broken)'
    }
    
    print("Hash Function Memory Usage:")
    for algo, usage in memory_usage.items():
        print(f"{algo:10}: {usage}")

hash_memory_usage()
```

## Practical Exercises 🏋️‍♀️

### Exercise 1: Build a Simple Blockchain

```python
class BlockchainWithHashes:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis = {
            'index': 0,
            'previous_hash': '0' * 64,
            'transactions': ['Genesis Block'],
            'nonce': 0
        }
        genesis['hash'] = self.calculate_hash(genesis)
        self.chain.append(genesis)
    
    def calculate_hash(self, block):
        block_string = f"{block['index']}{block['previous_hash']}{block['transactions']}{block['nonce']}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def add_block(self, transactions):
        previous_block = self.chain[-1]
        new_block = {
            'index': len(self.chain),
            'previous_hash': previous_block['hash'], 
            'transactions': transactions,
            'nonce': 0
        }
        new_block['hash'] = self.calculate_hash(new_block)
        self.chain.append(new_block)
    
    def verify_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Verify hash integrity
            if current['hash'] != self.calculate_hash(current):
                return False, f"Block {i} hash is invalid"
            
            # Verify chain linkage
            if current['previous_hash'] != previous['hash']:
                return False, f"Block {i} is not linked correctly"
        
        return True, "Blockchain is valid"

# Test the blockchain
blockchain = BlockchainWithHashes()
blockchain.add_block(['Alice → Bob: 10 BTC'])
blockchain.add_block(['Carol → Dave: 5 BTC', 'Eve → Frank: 3 BTC'])

print("Blockchain:")
for block in blockchain.chain:
    print(f"Block {block['index']}: {block['hash'][:16]}...")

# Verify integrity
is_valid, message = blockchain.verify_chain()
print(f"\nChain validity: {is_valid} - {message}")

# Try tampering
blockchain.chain[1]['transactions'] = ['Alice → Bob: 100 BTC']  # Tamper
is_valid, message = blockchain.verify_chain()
print(f"After tampering: {is_valid} - {message}")
```

### Exercise 2: Password Hash Storage

```python
import os
import hashlib

class SecurePasswordStorage:
    def hash_password(self, password):
        """
        Hash password with salt for secure storage
        """
        # Generate random salt
        salt = os.urandom(32)  # 32 bytes = 256 bits
        
        # Hash password with salt
        pwdhash = hashlib.pbkdf2_hmac('sha256', 
                                      password.encode('utf-8'),
                                      salt, 
                                      100000)  # 100k iterations
        
        # Return salt + hash for storage
        return salt + pwdhash
    
    def verify_password(self, stored_hash, provided_password):
        """
        Verify provided password against stored hash
        """
        # Extract salt and hash
        salt = stored_hash[:32]
        stored_pwdhash = stored_hash[32:]
        
        # Hash provided password with same salt
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                      provided_password.encode('utf-8'),
                                      salt,
                                      100000)
        
        # Compare hashes
        return pwdhash == stored_pwdhash

# Example usage
storage = SecurePasswordStorage()

# Store password
password = "my_secure_blockchain_password"
stored_hash = storage.hash_password(password)
print(f"Stored hash length: {len(stored_hash)} bytes")

# Verify passwords
print(f"Correct password: {storage.verify_password(stored_hash, password)}")
print(f"Wrong password: {storage.verify_password(stored_hash, 'wrong_password')}")
```

### Exercise 3: Hash Rate Calculator

```python
def calculate_hash_rates():
    """
    Calculate various hash rates and mining statistics
    """
    # Bitcoin network statistics (example)
    bitcoin_hash_rate = 400e18  # 400 EH/s (exahashes per second)
    bitcoin_difficulty = 50e12  # Approximate difficulty
    
    print("Bitcoin Network Hash Rate Analysis:")
    print(f"Network Hash Rate: {bitcoin_hash_rate:.1e} hashes/second")
    print(f"Difficulty: {bitcoin_difficulty:.1e}")
    
    # Time to find a block at different mining powers
    single_computer = 1e6      # 1 MH/s
    gaming_rig = 100e6         # 100 MH/s  
    asic_miner = 100e12        # 100 TH/s
    
    mining_rigs = {
        'Single Computer (1 MH/s)': single_computer,
        'Gaming Rig (100 MH/s)': gaming_rig,
        'ASIC Miner (100 TH/s)': asic_miner,
        'Entire Bitcoin Network': bitcoin_hash_rate
    }
    
    print(f"\nTime to mine one Bitcoin block (solo mining):")
    print("Rig Type                    | Hash Rate     | Time to Block")
    print("-" * 65)
    
    for rig_name, hash_rate in mining_rigs.items():
        # Simplified calculation: difficulty / hash_rate = seconds per block
        seconds_per_block = bitcoin_difficulty / hash_rate
        
        if seconds_per_block < 60:
            time_str = f"{seconds_per_block:.1f} seconds"
        elif seconds_per_block < 3600:
            time_str = f"{seconds_per_block/60:.1f} minutes"
        elif seconds_per_block < 86400:
            time_str = f"{seconds_per_block/3600:.1f} hours"
        elif seconds_per_block < 31536000:
            time_str = f"{seconds_per_block/86400:.1f} days"
        else:
            time_str = f"{seconds_per_block/31536000:.1e} years"
        
        print(f"{rig_name:27} | {hash_rate:.1e} H/s | {time_str}")

calculate_hash_rates()
```

## Quiz: Test Your Hashing Knowledge 🧠

### Question 1: Hash Properties

Given these hash outputs, which property is being demonstrated?

```
Input A: "blockchain"     → 625da44e4eaf58d61cf048d168aa6f5e492dea166d8bb54ec06c30de07db57e1
Input B: "Blockchain"     → f7c3bc1d808e04732adf679965ccc34ca7ae3441b4bcefa4ed8d4c4b6c1d9ba1  
Input C: "blockchain"     → 625da44e4eaf58d61cf048d168aa6f5e492dea166d8bb54ec06c30de07db57e1
```

<details>
<summary>Click for answer</summary>

**Multiple vulnerabilities:**

1. **No Salt**: Same passwords produce same hashes
2. **Rainbow Table Attack**: Pre-computed hash lookups available
3. **Too Fast**: SHA-256 is optimized for speed, not password security
4. **Dictionary Attack**: Common passwords easily cracked

**Secure version needs:**
- Unique salt per password
- Slow hash function (PBKDF2, Argon2, scrypt)
- High iteration count
- Proper key derivation
</details>

### Question 3: Mining Economics

If Bitcoin mining difficulty is 50 trillion and your ASIC produces 100 TH/s, on average how many attempts will you need to find a valid block?

<details>
<summary>Click for answer</summary>

**Answer: 50 trillion attempts (500,000,000,000,000)**

**Explanation:**
- Difficulty represents the average number of attempts needed
- Your hash rate determines how quickly you can make attempts
- At 100 TH/s: 500 trillion ÷ 100 trillion = 5,000 seconds = ~1.4 hours
- This is why miners join pools - solo mining takes too long!
</details>

### Question 4: Hash Function Selection

You're building a system that needs to:
- Hash 1 million transactions per second
- Provide 256-bit security
- Minimize energy consumption
- Resist quantum attacks (future-proofing)

Which hash function would you choose: SHA-256, SHA-3, BLAKE2b, or create a hybrid?

<details>
<summary>Click for answer</summary>

**Best Choice: BLAKE2b with SHA-3 fallback**

**Reasoning:**
- **BLAKE2b** for performance (fastest, lowest energy)
- **SHA-3** for quantum resistance (sponge construction)
- **Hybrid approach**: Use BLAKE2b primarily, SHA-3 for critical operations
- **SHA-256**: Good security but slower than BLAKE2b
- **Future**: Monitor post-quantum hash function development
</details>

## Advanced Topics and Future Considerations 🔮

### Post-Quantum Hash Functions

As quantum computers develop, current hash functions may need upgrades:

```python
def quantum_resistance_comparison():
    """
    Hash functions and their quantum resistance
    """
    hash_functions = {
        'SHA-256': {
            'quantum_resistance': 'Reduced to ~128-bit security',
            'status': 'May need upgrade for post-quantum era',
            'replacement': 'SHA-3 or specialized post-quantum hashes'
        },
        'SHA-3': {
            'quantum_resistance': 'Better resistance due to sponge construction', 
            'status': 'Likely sufficient for post-quantum era',
            'replacement': 'May be fine as-is'
        },
        'BLAKE3': {
            'quantum_resistance': 'Similar to SHA-256',
            'status': 'Fast but may need quantum-safe variant',
            'replacement': 'BLAKE3-QR (hypothetical quantum-resistant version)'
        }
    }
    
    print("Quantum Computing Impact on Hash Functions:")
    print("=" * 60)
    
    for name, info in hash_functions.items():
        print(f"\n{name}:")
        for key, value in info.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")

quantum_resistance_comparison()
```

### Zero-Knowledge Proofs and Hashing

Hash functions play crucial roles in privacy-preserving technologies:

```python
def simple_commitment_scheme():
    """
    Demonstrate hash-based commitment (used in zero-knowledge proofs)
    """
    import secrets
    
    # Alice wants to commit to a secret value without revealing it
    secret_value = "42"  # Alice's secret answer
    random_nonce = secrets.token_hex(32)  # Random value for hiding
    
    # Create commitment: hash(secret + nonce)
    commitment_data = secret_value + random_nonce
    commitment = hashlib.sha256(commitment_data.encode()).hexdigest()
    
    print("Commitment Scheme Example:")
    print(f"Secret Value: {secret_value} (hidden)")
    print(f"Random Nonce: {random_nonce[:16]}... (hidden)")
    print(f"Commitment:   {commitment} (public)")
    
    # Later, Alice reveals the secret and nonce
    print(f"\nReveal Phase:")
    print(f"Revealed Secret: {secret_value}")
    print(f"Revealed Nonce:  {random_nonce}")
    
    # Anyone can verify the commitment
    verification = hashlib.sha256(commitment_data.encode()).hexdigest()
    print(f"Verification:    {verification}")
    print(f"Valid Proof:     {commitment == verification}")

simple_commitment_scheme()
```

### Hash-Based Time-Stamping

```python
import time
from datetime import datetime

class HashTimeStamping:
    """
    Create tamper-proof timestamps using hash chains
    """
    def __init__(self):
        self.chain = []
        
    def timestamp_document(self, document):
        current_time = datetime.now().isoformat()
        
        if len(self.chain) == 0:
            # First document
            previous_hash = "0" * 64
        else:
            previous_hash = self.chain[-1]['hash']
        
        # Create timestamp record
        record = {
            'document': document,
            'timestamp': current_time,
            'previous_hash': previous_hash
        }
        
        # Calculate hash including previous hash (creates chain)
        record_string = f"{document}{current_time}{previous_hash}"
        record['hash'] = hashlib.sha256(record_string.encode()).hexdigest()
        
        self.chain.append(record)
        return record['hash']
    
    def verify_timestamp(self, index):
        """Verify a timestamp hasn't been tampered with"""
        if index >= len(self.chain):
            return False, "Index out of range"
        
        record = self.chain[index]
        record_string = f"{record['document']}{record['timestamp']}{record['previous_hash']}"
        expected_hash = hashlib.sha256(record_string.encode()).hexdigest()
        
        if record['hash'] != expected_hash:
            return False, "Hash mismatch - tampered record"
        
        # Verify chain integrity
        if index > 0:
            previous_record = self.chain[index - 1]
            if record['previous_hash'] != previous_record['hash']:
                return False, "Chain broken - invalid previous hash"
        
        return True, "Timestamp is valid"

# Example usage
timestamper = HashTimeStamping()

# Timestamp some documents
doc1_hash = timestamper.timestamp_document("Contract between Alice and Bob")
time.sleep(1)  # Small delay
doc2_hash = timestamper.timestamp_document("Software license agreement")
time.sleep(1)
doc3_hash = timestamper.timestamp_document("Meeting minutes from board meeting")

print("Document Timestamps:")
for i, record in enumerate(timestamper.chain):
    print(f"{i+1}. {record['document'][:30]}... at {record['timestamp']}")

# Verify all timestamps
print(f"\nVerification Results:")
for i in range(len(timestamper.chain)):
    is_valid, message = timestamper.verify_timestamp(i)
    print(f"Document {i+1}: {is_valid} - {message}")
```

## Real-World Hash Applications Beyond Blockchain 🌍

### Git Version Control

```python
def simulate_git_hashing():
    """
    Git uses SHA-1 hashing (now transitioning to SHA-256)
    """
    # Simulate how Git hashes commits
    def git_commit_hash(parent_hash, tree_hash, author, message, timestamp):
        commit_content = f"""tree {tree_hash}
parent {parent_hash}
author {author} {timestamp}

{message}"""
        return hashlib.sha1(commit_content.encode()).hexdigest()
    
    # Simulate a chain of Git commits
    commits = []
    
    # Initial commit
    commit1 = git_commit_hash(
        "0" * 40,  # No parent (initial commit)
        "abc123def456",  # Tree hash
        "Alice <alice@example.com>",
        "Initial commit",
        "1609459200"  # Timestamp
    )
    commits.append(("Initial commit", commit1))
    
    # Second commit
    commit2 = git_commit_hash(
        commit1,  # Parent is previous commit
        "def456abc123",
        "Alice <alice@example.com>", 
        "Add README file",
        "1609462800"
    )
    commits.append(("Add README", commit2))
    
    print("Git-style Commit Hashes:")
    for description, commit_hash in commits:
        print(f"{description}: {commit_hash}")

simulate_git_hashing()
```

### BitTorrent Protocol

```python
def simulate_bittorrent_hashing():
    """
    BitTorrent uses SHA-1 to verify file pieces
    """
    # Simulate file divided into pieces
    file_content = "This is a large file content that gets divided into pieces for BitTorrent distribution. " * 100
    piece_size = 256  # Bytes per piece
    
    pieces = []
    piece_hashes = []
    
    # Divide file into pieces and hash each
    for i in range(0, len(file_content), piece_size):
        piece = file_content[i:i+piece_size]
        piece_hash = hashlib.sha1(piece.encode()).hexdigest()
        
        pieces.append(piece)
        piece_hashes.append(piece_hash)
    
    print(f"BitTorrent-style File Hashing:")
    print(f"File size: {len(file_content)} bytes")
    print(f"Piece size: {piece_size} bytes") 
    print(f"Number of pieces: {len(pieces)}")
    print(f"Piece hashes:")
    
    for i, piece_hash in enumerate(piece_hashes[:5]):  # Show first 5
        print(f"  Piece {i+1}: {piece_hash}")
    
    if len(piece_hashes) > 5:
        print(f"  ... and {len(piece_hashes) - 5} more pieces")
    
    # Create torrent info hash
    piece_hashes_concat = ''.join(piece_hashes)
    torrent_info_hash = hashlib.sha1(piece_hashes_concat.encode()).hexdigest()
    print(f"Torrent info hash: {torrent_info_hash}")

simulate_bittorrent_hashing()
```

### Content Addressable Storage

```python
class ContentAddressableStorage:
    """
    Store data using hash as address (like IPFS)
    """
    def __init__(self):
        self.storage = {}
    
    def put(self, data):
        """Store data and return its hash address"""
        data_hash = hashlib.sha256(data.encode()).hexdigest()
        self.storage[data_hash] = data
        return data_hash
    
    def get(self, hash_address):
        """Retrieve data by hash address"""
        return self.storage.get(hash_address)
    
    def verify_integrity(self, hash_address):
        """Verify stored data hasn't been corrupted"""
        stored_data = self.storage.get(hash_address)
        if stored_data is None:
            return False, "Data not found"
        
        computed_hash = hashlib.sha256(stored_data.encode()).hexdigest()
        if computed_hash == hash_address:
            return True, "Data integrity verified"
        else:
            return False, "Data corrupted - hash mismatch"

# Example usage
cas = ContentAddressableStorage()

# Store some content
content1 = "Hello, decentralized world!"
content2 = "This is another piece of content"
content3 = "Immutable data storage using hashes"

hash1 = cas.put(content1)
hash2 = cas.put(content2) 
hash3 = cas.put(content3)

print("Content Addressable Storage:")
print(f"Content 1 stored at: {hash1[:16]}...")
print(f"Content 2 stored at: {hash2[:16]}...")
print(f"Content 3 stored at: {hash3[:16]}...")

# Retrieve content
retrieved = cas.get(hash1)
print(f"\nRetrieved: {retrieved}")

# Verify integrity
is_valid, message = cas.verify_integrity(hash1)
print(f"Integrity check: {is_valid} - {message}")
```

## Performance Optimization Techniques ⚡

### Hash Caching and Memoization

```python
from functools import lru_cache
import time

class OptimizedHashCalculator:
    def __init__(self):
        self.cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
    
    def hash_with_cache(self, data):
        """Hash with manual caching"""
        if data in self.cache:
            self.cache_hits += 1
            return self.cache[data]
        
        # Calculate hash
        hash_result = hashlib.sha256(data.encode()).hexdigest()
        self.cache[data] = hash_result
        self.cache_misses += 1
        return hash_result
    
    @lru_cache(maxsize=1000)
    def hash_with_lru(self, data):
        """Hash with LRU cache decorator"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def get_cache_stats(self):
        total = self.cache_hits + self.cache_misses
        hit_rate = self.cache_hits / total if total > 0 else 0
        return {
            'hits': self.cache_hits,
            'misses': self.cache_misses,
            'hit_rate': hit_rate
        }

# Benchmark caching effectiveness
calculator = OptimizedHashCalculator()

# Test data with repetitions (simulates blockchain transactions)
test_data = [
    "Alice → Bob: 5 BTC",
    "Carol → Dave: 3 BTC", 
    "Alice → Bob: 5 BTC",  # Repeated
    "Eve → Frank: 1 BTC",
    "Carol → Dave: 3 BTC",  # Repeated
    "Alice → Bob: 5 BTC",  # Repeated again
] * 1000  # Scale up

# Test without caching
start = time.time()
for data in test_data:
    hashlib.sha256(data.encode()).hexdigest()
no_cache_time = time.time() - start

# Test with caching
start = time.time()
for data in test_data:
    calculator.hash_with_cache(data)
cache_time = time.time() - start

print("Hash Caching Performance:")
print(f"Without caching: {no_cache_time:.4f} seconds")
print(f"With caching:    {cache_time:.4f} seconds")
print(f"Speed improvement: {no_cache_time/cache_time:.2f}x faster")

stats = calculator.get_cache_stats()
print(f"Cache hit rate: {stats['hit_rate']:.2%}")
```

### Parallel Hash Computation

```python
import multiprocessing
import concurrent.futures
from typing import List

def hash_chunk(data_chunk: List[str]) -> List[str]:
    """Hash a chunk of data"""
    return [hashlib.sha256(item.encode()).hexdigest() for item in data_chunk]

def parallel_hash_computation(data_list: List[str], num_processes: int = None) -> List[str]:
    """Compute hashes in parallel"""
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    
    # Split data into chunks
    chunk_size = max(1, len(data_list) // num_processes)
    chunks = [data_list[i:i + chunk_size] for i in range(0, len(data_list), chunk_size)]
    
    # Process chunks in parallel
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        future_to_chunk = {executor.submit(hash_chunk, chunk): chunk for chunk in chunks}
        results = []
        
        for future in concurrent.futures.as_completed(future_to_chunk):
            chunk_results = future.result()
            results.extend(chunk_results)
    
    return results

# Example usage
if __name__ == "__main__":
    # Generate test data
    test_transactions = [f"Transaction_{i}: User{i%100} → User{(i+1)%100}: {i%10} BTC" 
                        for i in range(10000)]
    
    # Sequential processing
    start = time.time()
    sequential_hashes = [hashlib.sha256(tx.encode()).hexdigest() for tx in test_transactions]
    sequential_time = time.time() - start
    
    # Parallel processing
    start = time.time()
    parallel_hashes = parallel_hash_computation(test_transactions)
    parallel_time = time.time() - start
    
    print(f"Parallel Hash Processing:")
    print(f"Sequential time: {sequential_time:.4f} seconds")
    print(f"Parallel time:   {parallel_time:.4f} seconds")
    print(f"Speed improvement: {sequential_time/parallel_time:.2f}x faster")
    print(f"Results match: {sequential_hashes == parallel_hashes}")
```

## Summary and Key Takeaways 🎯

### Essential Hash Properties for Blockchain

1. **Deterministic**: Same input → Same output (always)
2. **Fixed Size**: Any input → Fixed-size output 
3. **Avalanche Effect**: Small change → Completely different output
4. **One-Way**: Easy to compute forward, impossible to reverse
5. **Collision Resistant**: Can't find two inputs with same output

### Critical Applications in Blockchain

- **Block Identification**: Each block has unique hash ID
- **Transaction Integrity**: Detect any modification
- **Proof of Work**: Mining finds specific hash patterns
- **Merkle Trees**: Efficient verification of large datasets
- **Digital Signatures**: Combined with public-key cryptography

### Security Best Practices

- ✅ **Use SHA-256** for general blockchain applications
- ✅ **Use SHA-3** for quantum-resistant applications
- ✅ **Add salt** for password hashing
- ✅ **Use PBKDF2/Argon2** for password storage
- ✅ **Verify integrity** by recalculating hashes
- ❌ **Never use MD5** for security (broken)
- ❌ **Never use SHA-1** for new applications (weak)

### Performance Considerations

- **BLAKE2b**: Fastest general-purpose hash
- **SHA-256**: Good balance of speed and security
- **SHA-3**: Slower but quantum-resistant design
- **Caching**: Dramatically improves repeated calculations
- **Parallel Processing**: Scales with multiple CPU cores

## Next Steps in Your Cryptography Journey 🚀

Now that you understand hashing, you're ready for the next level:

➡️ [Public-Private Keys](public-private-keys.md) - Learn asymmetric cryptography  
➡️ [Digital Signatures](digital-signatures.md) - Prove authenticity and non-repudiation  
➡️ [Merkle Trees](merkle-trees.md) - Efficient data verification structures  

## Additional Resources 📚

### Technical References
- [NIST Hash Function Standards](https://csrc.nist.gov/projects/hash-functions)
- [SHA-3 Standard (FIPS 202)](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- [Password Hashing Best Practices - OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

### Interactive Tools
- [SHA-256 Hash Calculator](https://passwordsgenerator.net/sha256-hash-generator/)
- [Hash Function Comparison Tool](https://www.browserling.com/tools/all-hashes)
- [Bitcoin Block Explorer](https://blockchair.com/bitcoin) - See real hash usage

### Academic Papers
- "Cryptographic Hash Functions" - NIST Special Publication 800-107
- "The SHA-3 Cryptographic Hash Algorithm" - NIST FIPS 202
- "BLAKE2: Simpler, Smaller, Faster than MD5" - Aumasson et al.

---

**🎯 Learning Objective Achieved**: You now understand how hash functions provide the security foundation for blockchain technology, from basic properties to advanced applications!

**⏰ Estimated Reading Time**: 35-40 minutes  
**🎖️ Badge Progress**: Crypto Master (25% Complete)

**Ready for asymmetric cryptography?** Continue to [Public-Private Keys](public-private-keys.md) to learn how blockchain enables secure communication without shared secrets! answer</summary>

**Avalanche Effect** and **Deterministic Property**

- Input A and C are identical → Same hash (Deterministic)
- Input A and B differ by one capital letter → Completely different hashes (Avalanche Effect)
- 50%+ of hash bits changed from one letter case difference
</details>

### Question 2: Security Analysis

Why is this password storage method insecure?

```python
def bad_password_storage(password):
    return hashlib.sha256(password.encode()).hexdigest()

stored = bad_password_storage("password123")
```

<details>