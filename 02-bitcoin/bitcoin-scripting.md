# Bitcoin Scripting 📜

## Introduction

Bitcoin Script is the programming language that defines the spending conditions for every bitcoin transaction. Unlike traditional programming languages, Bitcoin Script is deliberately simple, stack-based, and designed for security and verifiability. Understanding Bitcoin Script is essential for grasping how Bitcoin achieves programmable money while maintaining security.

## Script Fundamentals 🧮

### What is Bitcoin Script?

Bitcoin Script is:
- **Stack-based**: Uses a Last-In-First-Out (LIFO) data structure
- **Forth-like**: Similar to the Forth programming language
- **Deliberately limited**: No loops, recursion, or complex operations
- **Deterministic**: Same input always produces same output
- **Stateless**: No persistent memory between executions

### Script Execution Model

```python
class ScriptStack:
    """Simple implementation of Bitcoin Script stack"""
    
    def __init__(self):
        self.stack = []
        self.operations = 0
        self.max_operations = 201  # Bitcoin's op limit
    
    def push(self, item):
        """Push item onto stack"""
        self.stack.append(item)
        print(f"  PUSH {item} → {self.stack}")
    
    def pop(self):
        """Pop item from stack"""
        if not self.stack:
            raise ValueError("Cannot pop from empty stack")
        item = self.stack.pop()
        print(f"  POP {item} ← {self.stack}")
        return item
    
    def peek(self):
        """Look at top item without popping"""
        return self.stack[-1] if self.stack else None
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def execute_op(self, op_name, operation_func):
        """Execute an operation with limits"""
        self.operations += 1
        if self.operations > self.max_operations:
            raise ValueError("Too many operations")
        
        print(f"  OP_{op_name}")
        operation_func()
        return True

# Demo basic stack operations
print("📜 Bitcoin Script Stack Demo")
print("=" * 50)

stack = ScriptStack()
print("Initial stack:", stack.stack)

# Basic stack operations
stack.push("Hello")
stack.push("World")
stack.push(42)

item = stack.pop()
print(f"Popped item: {item}")
print(f"Final stack: {stack.stack}")
```

### Basic Script Operations

```python
class BitcoinScriptInterpreter:
    """Simplified Bitcoin Script interpreter"""
    
    def __init__(self):
        self.stack = []
        self.alt_stack = []
        
    def execute_script(self, script_ops: list) -> bool:
        """Execute a Bitcoin script"""
        print(f"\n🔄 Executing Script: {' '.join(script_ops)}")
        print("=" * 40)
        
        for op in script_ops:
            if not self.execute_operation(op):
                return False
                
        # Script succeeds if stack has exactly one element that is "true"
        if len(self.stack) == 1 and self.is_true(self.stack[0]):
            print("✅ Script execution: SUCCESS")
            return True
        else:
            print("❌ Script execution: FAILED")
            return False
    
    def execute_operation(self, op: str) -> bool:
        """Execute a single operation"""
        print(f"\nExecuting: {op}")
        print(f"Stack before: {self.stack}")
        
        # Data operations (push data onto stack)
        if op.startswith('<') and op.endswith('>'):
            data = op[1:-1]  # Remove < >
            self.stack.append(data)
        
        # Stack operations
        elif op == 'OP_DUP':
            if not self.stack:
                return False
            self.stack.append(self.stack[-1])
        
        elif op == 'OP_DROP':
            if not self.stack:
                return False
            self.stack.pop()
        
        elif op == 'OP_SWAP':
            if len(self.stack) < 2:
                return False
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
        
        # Arithmetic operations
        elif op == 'OP_ADD':
            if len(self.stack) < 2:
                return False
            b = int(self.stack.pop())
            a = int(self.stack.pop())
            self.stack.append(str(a + b))
        
        elif op == 'OP_SUB':
            if len(self.stack) < 2:
                return False
            b = int(self.stack.pop())
            a = int(self.stack.pop())
            self.stack.append(str(a - b))
        
        # Comparison operations
        elif op == 'OP_EQUAL':
            if len(self.stack) < 2:
                return False
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append('1' if a == b else '0')
        
        elif op == 'OP_EQUALVERIFY':
            if len(self.stack) < 2:
                return False
            b = self.stack.pop()
            a = self.stack.pop()
            if a != b:
                return False
            # If equal, continue (don't push result)
        
        # Crypto operations (simplified)
        elif op == 'OP_HASH160':
            if not self.stack:
                return False
            data = self.stack.pop()
            # Simplified: just add "hashed_" prefix
            hashed = f"hashed_{data}"
            self.stack.append(hashed)
        
        elif op == 'OP_CHECKSIG':
            if len(self.stack) < 2:
                return False
            pubkey = self.stack.pop()
            signature = self.stack.pop()
            # Simplified signature verification
            is_valid = len(signature) > 0 and len(pubkey) > 0
            self.stack.append('1' if is_valid else '0')
        
        # Constants
        elif op == 'OP_0' or op == 'OP_FALSE':
            self.stack.append('0')
        
        elif op == 'OP_1' or op == 'OP_TRUE':
            self.stack.append('1')
        
        else:
            print(f"Unknown operation: {op}")
            return False
        
        print(f"Stack after: {self.stack}")
        return True
    
    def is_true(self, value) -> bool:
        """Check if a value is considered 'true' in Bitcoin Script"""
        return value != '0' and value != ''

# Demo script execution
print("\n🔄 Bitcoin Script Execution Demo")
print("=" * 50)

interpreter = BitcoinScriptInterpreter()

# Example 1: Simple arithmetic
arithmetic_script = ['<5>', '<3>', 'OP_ADD', '<8>', 'OP_EQUAL']
print("Example 1: Arithmetic (5 + 3 == 8)")
result1 = interpreter.execute_script(arithmetic_script)

# Reset interpreter for next example
interpreter = BitcoinScriptInterpreter()

# Example 2: Stack manipulation
stack_script = ['<hello>', 'OP_DUP', '<hello>', 'OP_EQUALVERIFY', 'OP_1']
print("\nExample 2: Stack manipulation")
result2 = interpreter.execute_script(stack_script)
```

## Standard Transaction Scripts 💳

### 1. Pay-to-Public-Key-Hash (P2PKH)

```python
def demonstrate_p2pkh():
    """Demonstrate P2PKH script execution"""
    
    print("\n💳 Pay-to-Public-Key-Hash (P2PKH) Demo")
    print("=" * 50)
    
    # P2PKH is the most common Bitcoin transaction type
    # Locking script: OP_DUP OP_HASH160 <pubkey_hash> OP_EQUALVERIFY OP_CHECKSIG
    # Unlocking script: <signature> <public_key>
    
    # Simulate a P2PKH transaction
    alice_pubkey = "alice_public_key_abc123"
    alice_pubkey_hash = "hashed_alice_public_key_abc123"
    alice_signature = "alice_signature_xyz789"
    
    print("Alice's P2PKH Address Creation:")
    print(f"  1. Public Key: {alice_pubkey}")
    print(f"  2. Hash160(PubKey): {alice_pubkey_hash}")
    print(f"  3. Address: 1..." + alice_pubkey_hash[:8])
    
    print(f"\nP2PKH Locking Script (sent to Alice):")
    locking_script = ['OP_DUP', 'OP_HASH160', f'<{alice_pubkey_hash}>', 'OP_EQUALVERIFY', 'OP_CHECKSIG']
    print(f"  {' '.join(locking_script)}")
    
    print(f"\nP2PKH Unlocking Script (Alice spending):")
    unlocking_script = [f'<{alice_signature}>', f'<{alice_pubkey}>']
    print(f"  {' '.join(unlocking_script)}")
    
    # Execute combined script
    combined_script = unlocking_script + locking_script
    
    interpreter = BitcoinScriptInterpreter()
    print(f"\nCombined Script Execution:")
    success = interpreter.execute_script(combined_script)
    
    print(f"\nP2PKH Properties:")
    print(f"  - Most common transaction type (~85% of transactions)")
    print(f"  - Requires signature + public key to spend") 
    print(f"  - Public key revealed only when spending")
    print(f"  - Address starts with '1' on mainnet")

demonstrate_p2pkh()
```

### 2. Pay-to-Script-Hash (P2SH)

```python
def demonstrate_p2sh():
    """Demonstrate P2SH script execution"""
    
    print("\n🏛️ Pay-to-Script-Hash (P2SH) Demo")
    print("=" * 50)
    
    # P2SH allows complex spending conditions
    # Locking script: OP_HASH160 <script_hash> OP_EQUAL
    # Unlocking script: <data> ... <data> <redeem_script>
    
    # Example: 2-of-3 multisig using P2SH
    redeem_script = ['OP_2', '<alice_pubkey>', '<bob_pubkey>', '<carol_pubkey>', 'OP_3', 'OP_CHECKMULTISIG']
    redeem_script_str = ' '.join(redeem_script)
    script_hash = f"hashed_{redeem_script_str}"
    
    print("Creating P2SH Address:")
    print(f"  1. Redeem Script: {redeem_script_str}")
    print(f"  2. Script Hash: {script_hash}")
    print(f"  3. P2SH Address: 3..." + script_hash[:8])
    
    print(f"\nP2SH Locking Script:")
    locking_script = ['OP_HASH160', f'<{script_hash}>', 'OP_EQUAL']
    print(f"  {' '.join(locking_script)}")
    
    print(f"\nP2SH Unlocking Script (2 signatures provided):")
    unlocking_script = ['<alice_sig>', '<bob_sig>', f'<{redeem_script_str}>']
    print(f"  {' '.join(unlocking_script)}")
    
    print(f"\nP2SH Benefits:")
    print(f"  - Moves complexity from sender to receiver")
    print(f"  - Enables multisig without revealing details upfront")
    print(f"  - Sender only needs to know the script hash")
    print(f"  - Address starts with '3' on mainnet")
    print(f"  - Redeem script revealed only when spending")

demonstrate_p2sh()
```

### 3. Multi-signature Scripts

```python
class MultisigScript:
    """Multi-signature script implementation"""
    
    def __init__(self, required_sigs: int, total_keys: int, public_keys: list):
        self.required_sigs = required_sigs
        self.total_keys = total_keys
        self.public_keys = public_keys
        
        if len(public_keys) != total_keys:
            raise ValueError("Number of keys doesn't match total_keys")
        if required_sigs > total_keys:
            raise ValueError("Required signatures can't exceed total keys")
    
    def create_locking_script(self) -> list:
        """Create multisig locking script"""
        script = [f'OP_{self.required_sigs}']
        
        for pubkey in self.public_keys:
            script.append(f'<{pubkey}>')
        
        script.extend([f'OP_{self.total_keys}', 'OP_CHECKMULTISIG'])
        return script
    
    def create_unlocking_script(self, signatures: list) -> list:
        """Create multisig unlocking script"""
        if len(signatures) < self.required_sigs:
            raise ValueError(f"Need at least {self.required_sigs} signatures")
        
        # Bitcoin quirk: OP_CHECKMULTISIG pops extra item from stack
        script = ['OP_0']  # Dummy value due to off-by-one bug
        
        # Add required number of signatures
        for i in range(self.required_sigs):
            script.append(f'<{signatures[i]}>')
        
        return script
    
    def get_script_info(self) -> dict:
        """Get information about the multisig setup"""
        return {
            'type': f'{self.required_sigs}-of-{self.total_keys} MultiSig',
            'required_signatures': self.required_sigs,
            'total_keys': self.total_keys,
            'public_keys': self.public_keys,
            'security_level': 'High' if self.required_sigs > 1 else 'Standard'
        }

# Demo multisig
print("\n🏛️ Multi-Signature Script Demo")
print("=" * 50)

# Create 2-of-3 multisig
pubkeys = ['alice_pubkey_123', 'bob_pubkey_456', 'carol_pubkey_789']
multisig = MultisigScript(2, 3, pubkeys)

info = multisig.get_script_info()
print(f"MultiSig Setup: {info['type']}")
print(f"Security: {info['security_level']}")

locking_script = multisig.create_locking_script()
print(f"\nLocking Script: {' '.join(locking_script)}")

# Spending scenario: Alice and Bob sign
signatures = ['alice_signature_abc', 'bob_signature_def']
unlocking_script = multisig.create_unlocking_script(signatures)
print(f"Unlocking Script: {' '.join(unlocking_script)}")

print(f"\nMultiSig Use Cases:")
use_cases = [
    "Corporate treasury (requires multiple executives)",
    "Escrow services (buyer + seller + arbiter)",
    "Personal security (multiple devices/locations)",
    "Exchange cold storage (multiple security officers)",
    "Family inheritance (multiple family members)"
]

for use_case in use_cases:
    print(f"  - {use_case}")
```

## Advanced Script Features 🚀

### 1. Time Locks

```python
def demonstrate_timelocks():
    """Demonstrate Bitcoin timelock mechanisms"""
    
    print("\n⏰ Bitcoin Timelock Demo")
    print("=" * 50)
    
    timelock_types = {
        'Absolute Timelock (nLockTime)': {
            'description': 'Transaction invalid before specific time/block',
            'field': 'Transaction nLockTime field',
            'granularity': 'Block height or Unix timestamp',
            'example': 'Inheritance: funds locked for 1 year',
            'script': 'Standard script + nLockTime = 700000'
        },
        'Relative Timelock (CSV)': {
            'description': 'Output unspendable for time after confirmation',
            'field': 'OP_CHECKSEQUENCEVERIFY in script',
            'granularity': 'Blocks or 512-second intervals',
            'example': 'Lightning Network: contest period',
            'script': '<144> OP_CHECKSEQUENCEVERIFY OP_DROP ...'
        },
        'Hash Timelock (HTLC)': {
            'description': 'Spend with secret OR wait for timeout',
            'field': 'Complex script with OP_IF branches',
            'granularity': 'Block-based with hash condition',
            'example': 'Atomic swaps, Lightning payments',
            'script': 'OP_IF OP_HASH160 <hash> OP_EQUAL OP_ELSE <timeout> CSV OP_ENDIF'
        }
    }
    
    for timelock_type, details in timelock_types.items():
        print(f"\n{timelock_type}:")
        print(f"  Description: {details['description']}")
        print(f"  Mechanism: {details['field']}")
        print(f"  Granularity: {details['granularity']}")
        print(f"  Example: {details['example']}")
        print(f"  Script: {details['script']}")

demonstrate_timelocks()
```

### 2. Conditional Scripts (OP_IF)

```python
def demonstrate_conditional_scripts():
    """Demonstrate conditional script execution"""
    
    print("\n🔀 Conditional Script Demo")
    print("=" * 50)
    
    # Example: Either provide secret or wait for timeout
    conditional_script = [
        'OP_IF',
        '  OP_HASH160', '<secret_hash>', 'OP_EQUALVERIFY',  # If branch: provide secret
        'OP_ELSE', 
        '  <144>', 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',     # Else branch: wait 144 blocks
        'OP_ENDIF',
        'OP_CHECKSIG'  # In both cases, valid signature required
    ]
    
    print("Hash Time Lock Contract (HTLC) Script:")
    for line in conditional_script:
        print(f"  {line}")
    
    print(f"\nSpending Scenarios:")
    
    scenarios = {
        'Immediate Spend (with secret)': {
            'condition': 'OP_IF branch (TRUE)',
            'requirements': 'Secret + Signature',
            'unlocking_script': '<secret> <signature> <pubkey> OP_1',
            'use_case': 'Lightning Network payment'
        },
        'Delayed Spend (timeout)': {
            'condition': 'OP_ELSE branch (FALSE)', 
            'requirements': 'Wait 144 blocks + Signature',
            'unlocking_script': '<signature> <pubkey> OP_0',
            'use_case': 'Refund after timeout'
        }
    }
    
    for scenario, details in scenarios.items():
        print(f"\n{scenario}:")
        print(f"  Condition: {details['condition']}")
        print(f"  Requirements: {details['requirements']}")
        print(f"  Unlocking: {details['unlocking_script']}")
        print(f"  Use Case: {details['use_case']}")

demonstrate_conditional_scripts()
```

### 3. Atomic Swaps

```python
def demonstrate_atomic_swap():
    """Demonstrate atomic swap using Bitcoin Script"""
    
    print("\n🔄 Atomic Swap Demo")
    print("=" * 50)
    
    # Atomic swap allows trustless exchange between different cryptocurrencies
    # Uses Hash Time Lock Contracts (HTLCs)
    
    swap_scenario = {
        'participants': ['Alice (has Bitcoin)', 'Bob (has Litecoin)'],
        'goal': 'Alice gets Litecoin, Bob gets Bitcoin',
        'challenge': 'No trusted third party',
        'solution': 'Hash Time Lock Contracts'
    }
    
    print("Atomic Swap Scenario:")
    for key, value in swap_scenario.items():
        if isinstance(value, list):
            print(f"  {key.capitalize()}: {', '.join(value)}")
        else:
            print(f"  {key.capitalize()}: {value}")
    
    print(f"\nAtomic Swap Process:")
    swap_steps = [
        "1. Alice generates secret S and hash H = SHA256(S)",
        "2. Alice creates Bitcoin HTLC: 'Bob can claim with S, or Alice refunds after 48h'",
        "3. Bob creates Litecoin HTLC: 'Alice can claim with S, or Bob refunds after 24h'",
        "4. Alice claims Litecoin by revealing S",
        "5. Bob uses revealed S to claim Bitcoin",
        "6. Swap complete: Alice has Litecoin, Bob has Bitcoin"
    ]
    
    for step in swap_steps:
        print(f"  {step}")
    
    # HTLC script structure
    htlc_script = [
        'OP_IF',
        '  OP_HASH256', '<hash_of_secret>', 'OP_EQUALVERIFY',
        '  <counterparty_pubkey>', 'OP_CHECKSIG',
        'OP_ELSE',
        '  <timeout_blocks>', 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',
        '  <refund_pubkey>', 'OP_CHECKSIG',
        'OP_ENDIF'
    ]
    
    print(f"\nHTLC Script Structure:")
    for line in htlc_script:
        print(f"  {line}")
    
    print(f"\nSecurity Properties:")
    properties = [
        "Either both swaps happen or neither happens (atomicity)",
        "No counterparty can steal funds without providing value",
        "Timeouts prevent funds from being locked forever",
        "Works across different blockchain networks"
    ]
    
    for prop in properties:
        print(f"  ✓ {prop}")

demonstrate_atomic_swap()
```

## Script Security and Limitations 🔒

### Script Security Features

```python
def analyze_script_security():
    """Analyze Bitcoin Script security features and limitations"""
    
    print("\n🔒 Bitcoin Script Security Analysis")
    print("=" * 50)
    
    security_features = {
        'No Infinite Loops': {
            'description': 'No loop constructs prevent infinite execution',
            'benefit': 'Guarantees script termination',
            'limitation': 'Cannot implement complex algorithms'
        },
        'Operation Limits': {
            'description': 'Maximum 201 operations per script',
            'benefit': 'Prevents resource exhaustion attacks',
            'limitation': 'Restricts complex script functionality'
        },
        'Stack Size Limits': {
            'description': 'Maximum 520 bytes per item, 1000 items total',
            'benefit': 'Prevents memory exhaustion',
            'limitation': 'Cannot process large data structures'
        },
        'No External Access': {
            'description': 'Scripts cannot access external data/network',
            'benefit': 'Deterministic execution across all nodes',
            'limitation': 'Cannot respond to external events'
        },
        'Disabled Operations': {
            'description': 'Many opcodes disabled for security (OP_CAT, etc)',
            'benefit': 'Reduces attack surface',
            'limitation': 'Less expressive than needed for some use cases'
        }
    }
    
    print("Security Features & Trade-offs:")
    for feature, details in security_features.items():
        print(f"\n{feature}:")
        print(f"  Description: {details['description']}")
        print(f"  Benefit: {details['benefit']}")
        print(f"  Limitation: {details['limitation']}")

analyze_script_security()
```

### Common Script Patterns and Attacks

```python
def demonstrate_script_patterns():
    """Show common Bitcoin Script patterns and potential attacks"""
    
    print("\n⚠️ Script Patterns and Security Considerations")
    print("=" * 50)
    
    patterns = {
        'Script Reuse Attack': {
            'description': 'Using same script/address multiple times',
            'vulnerability': 'Public key exposed after first spend',
            'mitigation': 'Generate new address for each transaction',
            'impact': 'Medium (quantum computer threat in future)'
        },
        'Script Size Attack': {
            'description': 'Creating oversized scripts to bloat blockchain',
            'vulnerability': 'Large scripts increase storage costs',
            'mitigation': 'Script size limits and fees',
            'impact': 'Low (limited by consensus rules)'
        },
        'Signature Grinding': {
            'description': 'Manipulating signatures to create specific patterns',
            'vulnerability': 'Could potentially influence block hashes',
            'mitigation': 'Proper randomness in signature generation',
            'impact': 'Very Low (requires enormous computational effort)'
        },
        'Script Complexity DoS': {
            'description': 'Complex scripts that are expensive to verify',
            'vulnerability': 'Could slow down network validation',
            'mitigation': 'Operation limits and SigOp counting',
            'impact': 'Low (built-in protections)'
        }
    }
    
    for pattern, details in patterns.items():
        print(f"\n{pattern}:")
        print(f"  Description: {details['description']}")
        print(f"  Vulnerability: {details['vulnerability']}")
        print(f"  Mitigation: {details['mitigation']}")
        print(f"  Impact: {details['impact']}")

demonstrate_script_patterns()
```

## Modern Script Developments 🆕

### SegWit and Script Improvements

```python
def explain_segwit_script_improvements():
    """Explain how SegWit improved Bitcoin scripting"""
    
    print("\n🆕 SegWit Script Improvements")
    print("=" * 50)
    
    segwit_improvements = {
        'Witness Data Separation': {
            'problem': 'Signatures counted toward block size limit',
            'solution': 'Move signatures to separate witness section',
            'benefit': 'More transactions per block',
            'script_impact': 'Same functionality, better efficiency'
        },
        'Transaction Malleability Fix': {
            'problem': 'Signatures could be modified without invalidating tx',
            'solution': 'Witness data not included in transaction ID',
            'benefit': 'Enables Lightning Network and other protocols',
            'script_impact': 'More reliable script-based protocols'
        },
        'Script Versioning': {
            'problem': 'Hard to upgrade script system',
            'solution': 'Witness programs can have version numbers',
            'benefit': 'Easier future script upgrades',
            'script_impact': 'Enables Taproot and future innovations'
        },
        'Quadratic Hashing Fix': {
            'problem': 'O(n²) signature verification complexity',
            'solution': 'New signature hashing algorithm',
            'benefit': 'Better scalability for large transactions',
            'script_impact': 'More efficient complex scripts'
        }
    }
    
    for improvement, details in segwit_improvements.items():
        print(f"\n{improvement}:")
        print(f"  Problem: {details['problem']}")
        print(f"  Solution: {details['solution']}")
        print(f"  Benefit: {details['benefit']}")
        print(f"  Script Impact: {details['script_impact']}")

explain_segwit_script_improvements()
```

### Taproot and Script Innovation

```python
def explain_taproot():
    """Explain Taproot improvements to Bitcoin scripting"""
    
    print("\n🌳 Taproot Script Innovation")
    print("=" * 50)
    
    taproot_features = {
        'Pay-to-Taproot (P2TR)': {
            'description': 'New output type combining key-spend and script-spend paths',
            'privacy': 'All spends look identical on-chain',
            'efficiency': 'Key-spend path is very efficient',
            'flexibility': 'Script-spend enables complex conditions'
        },
        'Schnorr Signatures': {
            'description': 'New signature scheme replacing ECDSA',
            'privacy': 'Multi-signature looks like single signature',
            'efficiency': 'Smaller signature size, batch verification',
            'flexibility': 'Signature aggregation and other advanced features'
        },
        'MAST (Merkelized Abstract Syntax Trees)': {
            'description': 'Complex scripts organized in Merkle trees',
            'privacy': 'Only executed script path revealed',
            'efficiency': 'Logarithmic scaling with script complexity',
            'flexibility': 'Unlimited script complexity'
        },
        'Script Path Spending': {
            'description': 'Alternative spending path using scripts',
            'privacy': 'Script only revealed when used',
            'efficiency': 'Pay only for what you use',
            'flexibility': 'Full Bitcoin Script compatibility'
        }
    }
    
    for feature, details in taproot_features.items():
        print(f"\n{feature}:")
        print(f"  Description: {details['description']}")
        print(f"  Privacy: {details['privacy']}")
        print(f"  Efficiency: {details['efficiency']}")
        print(f"  Flexibility: {details['flexibility']}")
    
    print(f"\nTaproot Benefits:")
    benefits = [
        "All transactions look similar (privacy)",
        "More efficient complex scripts",
        "Better scalability for advanced use cases",
        "Foundation for future script innovations"
    ]
    
    for benefit in benefits:
        print(f"  ✓ {benefit}")

explain_taproot()
```

## Real-World Script Applications 🌍

### Lightning Network Scripts

```python
def explain_lightning_scripts():
    """Explain how Lightning Network uses Bitcoin scripts"""
    
    print("\n⚡ Lightning Network Script Usage")
    print("=" * 50)
    
    lightning_components = {
        'Funding Transaction': {
            'script_type': '2-of-2 MultiSig',
            'purpose': 'Lock funds in payment channel',
            'parties': 'Alice and Bob both must sign to spend',
            'on_chain_cost': 'One transaction to open channel'
        },
        'Commitment Transaction': {
            'script_type': 'Complex HTLC with timelocks',
            'purpose': 'Represent current channel state',
            'parties': 'Either party can broadcast to close',
            'on_chain_cost': 'Only if channel is force-closed'
        },
        'HTLC Output': {
            'script_type': 'Hash Time Lock Contract',
            'purpose': 'Route payments through intermediate nodes',
            'parties': 'Receiver with preimage or sender after timeout',
            'on_chain_cost': 'Only if payment fails and needs on-chain resolution'
        },
        'Penalty Transaction': {
            'script_type': 'Revocation-based script',
            'purpose': 'Punish broadcasting old channel state',
            'parties': 'Innocent party can claim all funds',
            'on_chain_cost': 'Triggered by attempted fraud'
        }
    }
    
    for component, details in lightning_components.items():
        print(f"\n{component}:")
        print(f"  Script Type: {details['script_type']}")
        print(f"  Purpose: {details['purpose']}")
        print(f"  Parties: {details['parties']}")
        print(f"  Cost: {details['on_chain_cost']}")
    
    # Example Lightning HTLC script
    lightning_htlc = [
        'OP_DUP OP_HASH160 <revocation_pubkey_hash> OP_EQUAL',
        'OP_IF',
        '  OP_CHECKSIG',  # Revocation path
        'OP_ELSE',
        '  <remote_htlc_pubkey> OP_SWAP OP_SIZE 32 OP_EQUAL',
        '  OP_NOTIF',
        '    OP_DROP 2 OP_SWAP <local_htlc_pubkey> 2 OP_CHECKMULTISIG',  # Timeout path
        '  OP_ELSE',
        '    OP_HASH160 <payment_hash> OP_EQUALVERIFY OP_CHECKSIG',     # Success path
        '  OP_ENDIF',
        'OP_ENDIF'
    ]
    
    print(f"\nExample Lightning HTLC Script:")
    for line in lightning_htlc:
        print(f"  {line}")

explain_lightning_scripts()
```

## Script Debugging and Development 🛠️

### Script Development Tools

```python
def script_development_guide():
    """Guide for developing and testing Bitcoin scripts"""
    
    print("\n🛠️ Script Development Guide")
    print("=" * 50)
    
    development_tools = {
        'btcdeb': {
            'description': 'Bitcoin Script debugger',
            'features': 'Step-by-step script execution',
            'use_case': 'Debug complex scripts',
            'availability': 'GitHub: bitcoin-core/btcdeb'
        },
        'Bitcoin Core': {
            'description': 'Reference implementation with script validation',
            'features': 'Full script interpreter',
            'use_case': 'Test scripts on testnet/regtest',
            'availability': 'bitcoin.org'
        },
        'Script Playgrounds': {
            'description': 'Online Bitcoin script simulators',
            'features': 'Visual stack manipulation',
            'use_case': 'Learn script basics',
            'availability': 'Various web-based tools'
        },
        'Custom Libraries': {
            'description': 'Programming language libraries',
            'features': 'Script creation and validation',
            'use_case': 'Integrate into applications',
            'availability': 'Python, JavaScript, Go, Rust'
        }
    }
    
    for tool, details in development_tools.items():
        print(f"\n{tool}:")
        print(f"  Description: {details['description']}")
        print(f"  Features: {details['features']}")
        print(f"  Use Case: {details['use_case']}")
        print(f"  Availability: {details['availability']}")
    
    print(f"\nBest Practices:")
    best_practices = [
        "Test scripts on testnet before mainnet",
        "Keep scripts simple and readable", 
        "Use standard patterns when possible",
        "Consider transaction fees for complex scripts",
        "Plan for failure modes and timeouts",
        "Review scripts for potential vulnerabilities"
    ]
    
    for practice in best_practices:
        print(f"  ✓ {practice}")

script_development_guide()
```

## Quiz: Test Your Script Knowledge 📝

```python
def script_quiz():
    """Test understanding of Bitcoin Script"""
    
    print("\n🧠 Bitcoin Script Quiz")
    print("=" * 50)
    
    questions = [
        {
            'question': 'What type of data structure does Bitcoin Script use?',
            'options': ['A) Queue (FIFO)', 'B) Stack (LIFO)', 'C) Tree', 'D) Hash table'],
            'correct': 'B',
            'explanation': 'Bitcoin Script uses a stack (Last-In-First-Out) for all operations'
        },
        {
            'question': 'What does OP_DUP do in Bitcoin Script?',
            'options': ['A) Duplicates the blockchain', 'B) Copies the top stack item', 'C) Doubles a number', 'D) Creates a backup'],
            'correct': 'B',
            'explanation': 'OP_DUP duplicates the top item on the stack'
        },
        {
            'question': 'What is the most common Bitcoin transaction type?',
            'options': ['A) P2SH', 'B) MultiSig', 'C) P2PKH', 'D) P2TR'],
            'correct': 'C',
            'explanation': 'Pay-to-Public-Key-Hash (P2PKH) is used in ~85% of Bitcoin transactions'
        },
        {
            'question': 'Why doesn\'t Bitcoin Script allow loops?',
            'options': ['A) Too complex to implement', 'B) Would slow down transactions', 'C) Prevents infinite execution attacks', 'D) Not needed for payments'],
            'correct': 'C',
            'explanation': 'Loops could create infinite execution, so Bitcoin Script deliberately omits them for security'
        }
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for option in q['options']:
            print(f"  {option}")
        
        print(f"\nAnswer: {q['correct']}")
        print(f"Explanation: {q['explanation']}")
        print("-" * 50)

script_quiz()
```

## Summary 🎯

Bitcoin Script enables programmable money through a secure, limited scripting language:

### Core Concepts
- **Stack-based execution** with LIFO data structure
- **Deterministic operation** ensures network consensus  
- **Security through limitations** prevents many attack vectors
- **Standard patterns** handle most transaction types efficiently

### Transaction Types
- **P2PKH** (Pay-to-Public-Key-Hash): Most common, ~85% of transactions
- **P2SH** (Pay-to-Script-Hash): Enables complex conditions
- **MultiSig**: Requires multiple signatures for enhanced security
- **P2TR** (Pay-to-Taproot): Latest innovation for privacy and efficiency

### Advanced Features
- **Time locks** enable delayed or conditional spending
- **Hash locks** create atomic swaps and payment channels
- **Conditional execution** allows complex spending logic
- **Script composition** builds sophisticated financial contracts

### Real-World Applications
- **Lightning Network** uses HTLCs for instant payments
- **Atomic swaps** enable trustless cross-chain trading
- **Escrow services** use multisig for dispute resolution
- **Inheritance planning** uses timelocks for delayed access

### Modern Innovations
- **SegWit** improved efficiency and enabled new protocols
- **Taproot** enhanced privacy and script flexibility
- **Schnorr signatures** enable new cryptographic techniques
- **MAST** allows complex scripts without revealing unused branches

### Development Considerations
- **Security first**: Use proven patterns and extensive testing
- **Efficiency matters**: Complex scripts cost more in fees
- **Future compatibility**: Consider upgrade paths and versioning
- **User experience**: Balance functionality with usability

### Next Steps
- Explore [Ethereum Smart Contracts](../03-ethereum/ethereum-overview.md) for comparison
- Study [Digital Signatures](../01-cryptography/digital-signatures.md) in depth
- Learn about [Lightning Network](../09-advanced-topics/layer-2-solutions.md)
- Understand [DeFi Protocols](../06-defi/defi-overview.md) built on programmable money

---

**📜 Bitcoin Script proved that money could be programmable while remaining secure, laying the foundation for the entire smart contract revolution that followed.**