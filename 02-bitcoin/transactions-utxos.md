# Bitcoin Transactions and UTXOs 🔄

## Introduction

Bitcoin transactions are the heart of the Bitcoin network - they represent the transfer of value from one party to another. Unlike traditional banking where accounts have balances, Bitcoin uses a unique system called **UTXOs (Unspent Transaction Outputs)** to track ownership. Understanding this model is crucial to mastering Bitcoin.

## The UTXO Model 🧩

### What is a UTXO?

A **UTXO (Unspent Transaction Output)** is like a digital coin or bill that:
- Has a specific value (amount of bitcoin)
- Has ownership rules (who can spend it)
- Can only be spent once (consumed entirely when used)
- Must be spent completely (no partial spending)

### UTXO vs Account Model

```
Traditional Bank Account Model:
Alice: $100
Bob: $50
(When Alice sends $30 to Bob)
Alice: $70
Bob: $80

Bitcoin UTXO Model:
Alice has: [UTXO1: 0.6 BTC] [UTXO2: 0.4 BTC]
Bob has: [UTXO3: 0.2 BTC]

(When Alice sends 0.3 BTC to Bob)
Alice creates transaction:
- Input: UTXO2 (0.4 BTC) ← consumed
- Output1: 0.3 BTC to Bob ← new UTXO
- Output2: 0.1 BTC to Alice (change) ← new UTXO

Result:
Alice has: [UTXO1: 0.6 BTC] [Change UTXO: 0.1 BTC]
Bob has: [UTXO3: 0.2 BTC] [New UTXO: 0.3 BTC]
```

## Transaction Structure 📋

### Basic Transaction Anatomy

```python
import hashlib
import json
from typing import List, Dict, Tuple
import time

class TransactionInput:
    def __init__(self, prev_tx_hash: str, output_index: int, script_sig: str = "", sequence: int = 0xffffffff):
        self.prev_tx_hash = prev_tx_hash  # Points to previous transaction
        self.output_index = output_index  # Which output in that transaction
        self.script_sig = script_sig      # Unlocking script (signature + pubkey)
        self.sequence = sequence          # For replace-by-fee and timelocks
    
    def to_dict(self) -> dict:
        return {
            'prev_tx_hash': self.prev_tx_hash,
            'output_index': self.output_index,
            'script_sig': self.script_sig,
            'sequence': self.sequence
        }

class TransactionOutput:
    def __init__(self, amount: int, script_pubkey: str):
        self.amount = amount              # Amount in satoshis (1 BTC = 100,000,000 satoshis)
        self.script_pubkey = script_pubkey  # Locking script (spending conditions)
    
    def to_dict(self) -> dict:
        return {
            'amount': self.amount,
            'script_pubkey': self.script_pubkey
        }

class BitcoinTransaction:
    def __init__(self):
        self.version = 2              # Transaction version
        self.inputs: List[TransactionInput] = []
        self.outputs: List[TransactionOutput] = []
        self.locktime = 0            # When transaction can be included in block
        self.txid = None
    
    def add_input(self, prev_tx_hash: str, output_index: int, script_sig: str = ""):
        """Add input that spends a previous output"""
        tx_input = TransactionInput(prev_tx_hash, output_index, script_sig)
        self.inputs.append(tx_input)
    
    def add_output(self, amount_btc: float, recipient_address: str):
        """Add output that creates new UTXO"""
        amount_satoshis = int(amount_btc * 100000000)
        # Simplified P2PKH script
        script_pubkey = f"OP_DUP OP_HASH160 {recipient_address} OP_EQUALVERIFY OP_CHECKSIG"
        tx_output = TransactionOutput(amount_satoshis, script_pubkey)
        self.outputs.append(tx_output)
    
    def calculate_fee(self) -> int:
        """Calculate transaction fee (input total - output total)"""
        # Note: In real implementation, you'd need to look up input values
        # For demo, we'll assume this is calculated elsewhere
        return 10000  # 0.0001 BTC fee
    
    def serialize_for_signing(self) -> str:
        """Serialize transaction for signature creation"""
        tx_data = {
            'version': self.version,
            'inputs': [inp.to_dict() for inp in self.inputs],
            'outputs': [out.to_dict() for out in self.outputs],
            'locktime': self.locktime
        }
        return json.dumps(tx_data, sort_keys=True)
    
    def calculate_txid(self) -> str:
        """Calculate transaction ID (double SHA-256 of serialized tx)"""
        serialized = self.serialize_for_signing()
        hash1 = hashlib.sha256(serialized.encode()).digest()
        hash2 = hashlib.sha256(hash1).digest()
        # TXID is displayed in reverse byte order
        self.txid = hash2[::-1].hex()
        return self.txid
    
    def get_size_estimate(self) -> int:
        """Estimate transaction size in bytes"""
        # Very rough estimate
        base_size = 10  # version + locktime + input/output counts
        input_size = len(self.inputs) * 148  # Average input size
        output_size = len(self.outputs) * 34  # Average output size
        return base_size + input_size + output_size

# Demo transaction creation
print("💸 Bitcoin Transaction Creation Demo")
print("=" * 60)

# Create a transaction where Alice sends 0.5 BTC to Bob
tx = BitcoinTransaction()

# Add input: Alice is spending a UTXO she received earlier
tx.add_input(
    prev_tx_hash="a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456",
    output_index=0
)

# Add outputs
tx.add_output(0.5, "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2")  # 0.5 BTC to Bob
tx.add_output(0.4999, "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")  # 0.4999 BTC change to Alice

txid = tx.calculate_txid()
estimated_size = tx.get_size_estimate()

print(f"Transaction Created:")
print(f"  TXID: {txid}")
print(f"  Inputs: {len(tx.inputs)}")
print(f"  Outputs: {len(tx.outputs)}")
print(f"  Estimated Size: {estimated_size} bytes")
print(f"  Estimated Fee: {tx.calculate_fee() / 100000000:.8f} BTC")

# Show input details
print(f"\nInputs (UTXOs being spent):")
for i, inp in enumerate(tx.inputs):
    print(f"  Input {i}: {inp.prev_tx_hash[:16]}...:{inp.output_index}")

# Show output details  
print(f"\nOutputs (New UTXOs created):")
for i, out in enumerate(tx.outputs):
    btc_amount = out.amount / 100000000
    print(f"  Output {i}: {btc_amount} BTC")
    print(f"    Script: {out.script_pubkey[:50]}...")
```

## UTXO Management 💼

### UTXO Set and Wallet Management

```python
class UTXO:
    def __init__(self, txid: str, output_index: int, amount: int, script_pubkey: str, address: str):
        self.txid = txid
        self.output_index = output_index
        self.amount = amount  # in satoshis
        self.script_pubkey = script_pubkey
        self.address = address
        self.is_spent = False
        self.block_height = None
        self.confirmations = 0
    
    def to_dict(self) -> dict:
        return {
            'txid': self.txid,
            'output_index': self.output_index,
            'amount_btc': self.amount / 100000000,
            'address': self.address,
            'confirmations': self.confirmations,
            'is_spent': self.is_spent
        }

class UTXOSet:
    def __init__(self):
        self.utxos: Dict[str, UTXO] = {}  # Key: txid:index
        self.spent_utxos: Dict[str, UTXO] = {}
    
    def add_utxo(self, utxo: UTXO):
        """Add new UTXO to the set"""
        key = f"{utxo.txid}:{utxo.output_index}"
        self.utxos[key] = utxo
    
    def spend_utxo(self, txid: str, output_index: int) -> UTXO:
        """Mark UTXO as spent and return it"""
        key = f"{txid}:{output_index}"
        if key not in self.utxos:
            raise ValueError(f"UTXO {key} not found")
        
        utxo = self.utxos[key]
        utxo.is_spent = True
        
        # Move to spent set
        self.spent_utxos[key] = utxo
        del self.utxos[key]
        
        return utxo
    
    def get_balance(self, address: str = None) -> int:
        """Get total balance (optionally for specific address)"""
        total = 0
        for utxo in self.utxos.values():
            if address is None or utxo.address == address:
                total += utxo.amount
        return total
    
    def get_utxos_for_address(self, address: str) -> List[UTXO]:
        """Get all UTXOs for a specific address"""
        return [utxo for utxo in self.utxos.values() if utxo.address == address]
    
    def select_utxos_for_amount(self, target_amount: int, address: str) -> Tuple[List[UTXO], int]:
        """Select UTXOs to spend for target amount (coin selection)"""
        available_utxos = self.get_utxos_for_address(address)
        available_utxos.sort(key=lambda u: u.amount, reverse=True)  # Largest first
        
        selected = []
        total_selected = 0
        
        for utxo in available_utxos:
            selected.append(utxo)
            total_selected += utxo.amount
            
            if total_selected >= target_amount:
                break
        
        if total_selected < target_amount:
            raise ValueError(f"Insufficient funds. Need {target_amount}, have {total_selected}")
        
        return selected, total_selected
    
    def get_stats(self) -> dict:
        """Get UTXO set statistics"""
        return {
            'total_utxos': len(self.utxos),
            'total_spent': len(self.spent_utxos),
            'total_value_btc': self.get_balance() / 100000000,
            'average_utxo_size': sum(u.amount for u in self.utxos.values()) / len(self.utxos) / 100000000 if self.utxos else 0
        }

# Demo UTXO management
print("\n🧩 UTXO Set Management Demo")
print("=" * 60)

utxo_set = UTXOSet()
alice_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
bob_address = "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"

# Add some UTXOs for Alice
utxo1 = UTXO("abc123", 0, 50000000, "script1", alice_address)  # 0.5 BTC
utxo2 = UTXO("def456", 1, 30000000, "script2", alice_address)  # 0.3 BTC
utxo3 = UTXO("ghi789", 0, 20000000, "script3", bob_address)    # 0.2 BTC

utxo_set.add_utxo(utxo1)
utxo_set.add_utxo(utxo2)
utxo_set.add_utxo(utxo3)

print("Initial UTXO Set:")
stats = utxo_set.get_stats()
for key, value in stats.items():
    print(f"  {key}: {value}")

print(f"\nAlice's balance: {utxo_set.get_balance(alice_address) / 100000000} BTC")
print(f"Bob's balance: {utxo_set.get_balance(bob_address) / 100000000} BTC")

# Alice wants to send 0.6 BTC to Carol
try:
    selected_utxos, total = utxo_set.select_utxos_for_amount(60000000, alice_address)  # 0.6 BTC
    print(f"\nSelected UTXOs for 0.6 BTC payment:")
    for utxo in selected_utxos:
        print(f"  {utxo.txid[:8]}...:{utxo.output_index} = {utxo.amount/100000000} BTC")
    print(f"Total selected: {total/100000000} BTC")
    print(f"Change needed: {(total - 60000000)/100000000} BTC")
    
except ValueError as e:
    print(f"Error: {e}")
```

## Transaction Types and Patterns 🔄

### 1. Simple Payment

```python
def create_simple_payment():
    """Most common transaction: A pays B"""
    print("\n💰 Simple Payment Transaction")
    print("-" * 40)
    
    tx = BitcoinTransaction()
    
    # Alice spends 1 BTC UTXO to send 0.7 BTC to Bob
    tx.add_input("prev_tx_hash_1", 0)
    tx.add_output(0.7, "bob_address")      # Payment to Bob
    tx.add_output(0.2999, "alice_address") # Change back to Alice
    # 0.0001 BTC fee (1 BTC - 0.7 BTC - 0.2999 BTC)
    
    print("Transaction pattern: 1 input → 2 outputs (payment + change)")
    print(f"Inputs: {len(tx.inputs)}, Outputs: {len(tx.outputs)}")

create_simple_payment()
```

### 2. Consolidation Transaction

```python
def create_consolidation():
    """Combine many small UTXOs into one large UTXO"""
    print("\n🔄 UTXO Consolidation Transaction")
    print("-" * 40)
    
    tx = BitcoinTransaction()
    
    # Combine 5 small UTXOs into 1 large one
    for i in range(5):
        tx.add_input(f"prev_tx_hash_{i}", 0)
    
    # Single output (minus fee)
    tx.add_output(0.4999, "alice_address")  # Consolidated amount
    
    print("Transaction pattern: Many inputs → 1 output (consolidation)")
    print(f"Inputs: {len(tx.inputs)}, Outputs: {len(tx.outputs)}")
    print("Purpose: Reduce wallet UTXO count, save on future fees")

create_consolidation()
```

### 3. Distribution Transaction

```python
def create_distribution():
    """Split one large UTXO into many smaller ones"""
    print("\n📤 UTXO Distribution Transaction")  
    print("-" * 40)
    
    tx = BitcoinTransaction()
    
    # One large input
    tx.add_input("large_utxo_hash", 0)
    
    # Multiple outputs (e.g., exchange paying out withdrawals)
    recipients = ["user1", "user2", "user3", "user4"]
    for i, recipient in enumerate(recipients):
        tx.add_output(0.1, f"{recipient}_address")
    
    print("Transaction pattern: 1 input → Many outputs (distribution)")
    print(f"Inputs: {len(tx.inputs)}, Outputs: {len(tx.outputs)}")
    print("Purpose: Batch payments, exchange withdrawals")

create_distribution()
```

## Transaction Fees and Priority 💸

### Fee Calculation

```python
class FeeCalculator:
    def __init__(self):
        # Fee rates in satoshis per byte
        self.fee_rates = {
            'slow': 1,      # Low priority, may take hours
            'standard': 5,   # Normal priority, ~30 minutes
            'fast': 20,     # High priority, next block
            'urgent': 50    # Very high priority, immediate
        }
    
    def calculate_fee(self, tx_size_bytes: int, priority: str = 'standard') -> int:
        """Calculate fee in satoshis"""
        rate = self.fee_rates.get(priority, self.fee_rates['standard'])
        return tx_size_bytes * rate
    
    def estimate_tx_size(self, num_inputs: int, num_outputs: int) -> int:
        """Estimate transaction size in bytes"""
        # Rough estimation
        base_size = 10  # Version, locktime, input/output counts
        input_size = num_inputs * 148  # Average input size (varies by script type)
        output_size = num_outputs * 34  # Average output size
        return base_size + input_size + output_size
    
    def recommend_fee(self, tx_size: int, mempool_congestion: str = 'normal') -> dict:
        """Recommend fee based on network conditions"""
        multiplier = {
            'low': 0.5,
            'normal': 1.0,
            'high': 2.0,
            'extreme': 5.0
        }.get(mempool_congestion, 1.0)
        
        recommendations = {}
        for priority, base_rate in self.fee_rates.items():
            adjusted_rate = int(base_rate * multiplier)
            fee_satoshis = tx_size * adjusted_rate
            
            recommendations[priority] = {
                'fee_satoshis': fee_satoshis,
                'fee_btc': fee_satoshis / 100000000,
                'rate_sat_per_byte': adjusted_rate,
                'estimated_time': {
                    'slow': '2-24 hours',
                    'standard': '10-60 minutes', 
                    'fast': '1-3 blocks (~10-30 min)',
                    'urgent': 'Next block (~10 min)'
                }[priority]
            }
        
        return recommendations

# Demo fee calculation
print("\n💸 Transaction Fee Calculation")
print("=" * 60)

fee_calc = FeeCalculator()

# Example transaction: 2 inputs, 2 outputs
tx_size = fee_calc.estimate_tx_size(2, 2)
print(f"Estimated transaction size: {tx_size} bytes")

# Get fee recommendations
recommendations = fee_calc.recommend_fee(tx_size, 'normal')

print(f"\nFee Recommendations (Normal network congestion):")
for priority, details in recommendations.items():
    print(f"{priority.capitalize():>8}: {details['fee_btc']:.8f} BTC "
          f"({details['fee_satoshis']:,} sats) - {details['estimated_time']}")

# Show impact of network congestion
print(f"\nNetwork Congestion Impact:")
congestion_levels = ['low', 'normal', 'high', 'extreme']
for level in congestion_levels:
    recs = fee_calc.recommend_fee(tx_size, level)
    standard_fee = recs['standard']['fee_btc']
    print(f"{level.capitalize():>7} congestion: {standard_fee:.8f} BTC")
```

### Fee Optimization Strategies

```python
def demonstrate_fee_optimization():
    """Show different fee optimization techniques"""
    
    print("\n⚡ Fee Optimization Strategies")
    print("=" * 60)
    
    strategies = {
        'UTXO Consolidation': {
            'description': 'Combine small UTXOs when fees are low',
            'benefit': 'Reduces future transaction sizes',
            'best_time': 'Weekend, low network activity',
            'example': '10 inputs → 1 output during low-fee period'
        },
        'Batch Payments': {
            'description': 'Send multiple payments in one transaction', 
            'benefit': 'Amortize base transaction cost',
            'best_time': 'When making multiple payments',
            'example': '1 input → 10 outputs vs 10 separate transactions'
        },
        'SegWit Usage': {
            'description': 'Use SegWit addresses (bech32)',
            'benefit': '~40% smaller transaction size',
            'best_time': 'Always (when supported)',
            'example': 'bc1... addresses instead of 1... or 3...'
        },
        'Replace-by-Fee (RBF)': {
            'description': 'Start with low fee, increase if needed',
            'benefit': 'Pay minimum necessary fee',
            'best_time': 'Non-urgent transactions',
            'example': 'Start at 1 sat/byte, bump to 5 if slow'
        },
        'Child-Pays-Parent (CPFP)': {
            'description': 'Receiver creates high-fee tx using unconfirmed UTXO',
            'benefit': 'Speeds up stuck transactions',
            'best_time': 'When receiving stuck payment',
            'example': 'High-fee transaction spending unconfirmed output'
        }
    }
    
    for strategy, details in strategies.items():
        print(f"\n{strategy}:")
        print(f"  Description: {details['description']}")
        print(f"  Benefit: {details['benefit']}")
        print(f"  Best Time: {details['best_time']}")
        print(f"  Example: {details['example']}")

demonstrate_fee_optimization()
```

## Advanced Transaction Features 🎛️

### 1. Multi-Signature Transactions

```python
def create_multisig_transaction():
    """Create a 2-of-3 multisig transaction"""
    print("\n🏛️ Multi-Signature Transaction")
    print("-" * 40)
    
    # 2-of-3 multisig requires 2 out of 3 signatures
    multisig_script = "OP_2 <pubkey1> <pubkey2> <pubkey3> OP_3 OP_CHECKMULTISIG"
    
    tx = BitcoinTransaction()
    tx.add_input("multisig_utxo_hash", 0)
    tx.add_output(0.9999, "recipient_address")
    
    print("Multisig properties:")
    print("  - Requires multiple signatures to spend")
    print("  - Increases security through shared control")
    print("  - Common for business accounts, escrow")
    print(f"  - Locking script: {multisig_script[:50]}...")

create_multisig_transaction()
```

### 2. Time-Locked Transactions

```python
def create_timelock_transaction():
    """Create transaction with time-based spending conditions"""
    print("\n⏰ Time-Locked Transaction")
    print("-" * 40)
    
    tx = BitcoinTransaction()
    
    # Absolute timelock: can't be included in block before specific time
    tx.locktime = 800000  # Block height or Unix timestamp
    
    tx.add_input("regular_utxo", 0)
    tx.add_output(0.5, "future_recipient")
    
    print("Timelock types:")
    print("  - Absolute (nLockTime): Transaction invalid before time/block")
    print("  - Relative (CSV): Output unspendable for time after confirmation")
    print(f"  - This tx locktime: {tx.locktime}")
    print("  - Use cases: Escrow, inheritance, payment channels")

create_timelock_transaction()
```

### 3. Replace-by-Fee (RBF)

```python
def demonstrate_rbf():
    """Show Replace-by-Fee functionality"""
    print("\n🔄 Replace-by-Fee (RBF) Demo")
    print("-" * 40)
    
    # Original transaction with low fee
    original_tx = BitcoinTransaction()
    original_tx.add_input("utxo_hash", 0)
    original_tx.add_output(0.1, "recipient")
    original_tx.add_output(0.8999, "change_address")  # Low fee (0.0001 BTC)
    
    # Signal RBF by setting sequence < 0xfffffffe
    original_tx.inputs[0].sequence = 0xfffffffd
    
    print("Original transaction:")
    print(f"  Fee: {0.0001} BTC (low)")
    print(f"  Sequence: {hex(original_tx.inputs[0].sequence)} (RBF enabled)")
    
    # Replacement transaction with higher fee
    replacement_tx = BitcoinTransaction()
    replacement_tx.add_input("utxo_hash", 0)  # Same input
    replacement_tx.add_output(0.1, "recipient")  # Same payment
    replacement_tx.add_output(0.8995, "change_address")  # Higher fee (0.0005 BTC)
    
    print("\nReplacement transaction:")
    print(f"  Fee: {0.0005} BTC (higher)")
    print(f"  Same inputs, adjusted change output")
    print("  - Miners prefer higher fee version")
    print("  - Original tx becomes invalid")

demonstrate_rbf()
```

## Transaction Verification 🔍

### Script Execution and Validation

```python
class TransactionValidator:
    def __init__(self):
        self.utxo_set = UTXOSet()
    
    def verify_transaction(self, tx: BitcoinTransaction) -> dict:
        """Verify transaction against UTXO set and rules"""
        errors = []
        
        # 1. Check inputs exist and are unspent
        input_total = 0
        for tx_input in tx.inputs:
            utxo_key = f"{tx_input.prev_tx_hash}:{tx_input.output_index}"
            if utxo_key not in self.utxo_set.utxos:
                errors.append(f"Input {utxo_key} not found in UTXO set")
                continue
            
            utxo = self.utxo_set.utxos[utxo_key]
            input_total += utxo.amount
        
        # 2. Check outputs sum
        output_total = sum(output.amount for output in tx.outputs)
        
        # 3. Verify fee is reasonable
        fee = input_total - output_total
        if fee < 0:
            errors.append("Transaction creates money (negative fee)")
        elif fee > input_total * 0.1:  # More than 10% fee seems suspicious
            errors.append(f"Fee {fee/100000000:.8f} BTC seems excessive")
        
        # 4. Check for double spending
        # (In real implementation, check against mempool)
        
        # 5. Verify signatures (simplified)
        for i, tx_input in enumerate(tx.inputs):
            if not self._verify_signature(tx, i, tx_input.script_sig):
                errors.append(f"Invalid signature for input {i}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'input_total_btc': input_total / 100000000,
            'output_total_btc': output_total / 100000000,
            'fee_btc': fee / 100000000,
            'fee_rate_sat_per_byte': fee / tx.get_size_estimate() if tx.get_size_estimate() > 0 else 0
        }
    
    def _verify_signature(self, tx: BitcoinTransaction, input_index: int, script_sig: str) -> bool:
        """Simplified signature verification"""
        # In real Bitcoin, this involves:
        # 1. Parse script_sig to extract signature and pubkey
        # 2. Create signature hash from transaction data
        # 3. Verify signature against pubkey and hash
        # For demo, we'll assume signatures are valid if script_sig is not empty
        return len(script_sig) > 0

# Demo transaction verification
print("\n🔍 Transaction Verification Demo")
print("=" * 60)

validator = TransactionValidator()

# Add a UTXO to spend
test_utxo = UTXO("test_tx", 0, 100000000, "test_script", "test_address")  # 1 BTC
validator.utxo_set.add_utxo(test_utxo)

# Create valid transaction
valid_tx = BitcoinTransaction()
valid_tx.add_input("test_tx", 0, "valid_signature_and_pubkey")
valid_tx.add_output(0.5, "recipient")
valid_tx.add_output(0.4999, "change")  # 0.0001 BTC fee

# Verify valid transaction
result = validator.verify_transaction(valid_tx)
print("Valid transaction verification:")
for key, value in result.items():
    print(f"  {key}: {value}")

# Create invalid transaction (double spending)
invalid_tx = BitcoinTransaction()
invalid_tx.add_input("nonexistent_tx", 0, "signature")
invalid_tx.add_output(1.0, "recipient")

# Verify invalid transaction
result = validator.verify_transaction(invalid_tx)
print(f"\nInvalid transaction verification:")
for key, value in result.items():
    print(f"  {key}: {value}")
```

## UTXO Set Management 🗂️

### Blockchain State and UTXO Tracking

```python
class BlockchainState:
    """Simplified blockchain state with UTXO tracking"""
    
    def __init__(self):
        self.utxo_set = UTXOSet()
        self.block_height = 0
        self.mempool = []  # Unconfirmed transactions
    
    def apply_transaction(self, tx: BitcoinTransaction, block_height: int = None):
        """Apply transaction to UTXO set"""
        # Spend inputs (remove UTXOs)
        for tx_input in tx.inputs:
            try:
                spent_utxo = self.utxo_set.spend_utxo(tx_input.prev_tx_hash, tx_input.output_index)
                print(f"  Spent: {spent_utxo.txid[:8]}...:{spent_utxo.output_index} ({spent_utxo.amount/100000000:.8f} BTC)")
            except ValueError as e:
                print(f"  Error spending UTXO: {e}")
                return False
        
        # Create outputs (add new UTXOs)
        for i, tx_output in enumerate(tx.outputs):
            new_utxo = UTXO(
                txid=tx.txid,
                output_index=i,
                amount=tx_output.amount,
                script_pubkey=tx_output.script_pubkey,
                address=f"derived_address_{i}",  # Simplified
                
            )
            new_utxo.block_height = block_height or self.block_height
            new_utxo.confirmations = (self.block_height - new_utxo.block_height + 1) if block_height else 0
            
            self.utxo_set.add_utxo(new_utxo)
            print(f"  Created: {new_utxo.txid[:8]}...:{new_utxo.output_index} ({new_utxo.amount/100000000:.8f} BTC)")
        
        return True
    
    def get_balance(self, address: str) -> float:
        """Get balance for address in BTC"""
        return self.utxo_set.get_balance(address) / 100000000
    
    def simulate_block(self, transactions: List[BitcoinTransaction]):
        """Simulate processing a block of transactions"""
        self.block_height += 1
        print(f"\n📦 Processing Block {self.block_height}")
        print("-" * 40)
        
        for tx in transactions:
            print(f"\nApplying transaction {tx.txid[:8]}...")
            if self.apply_transaction(tx, self.block_height):
                print("  ✅ Transaction applied successfully")
            else:
                print("  ❌ Transaction failed to apply")
        
        # Update confirmations for existing UTXOs
        for utxo in self.utxo_set.utxos.values():
            if utxo.block_height is not None:
                utxo.confirmations = self.block_height - utxo.block_height + 1

# Demo blockchain state management
print("\n🗂️ Blockchain State Management Demo")
print("=" * 60)

blockchain = BlockchainState()

# Add initial UTXOs (like coinbase transactions)
genesis_utxo = UTXO("genesis", 0, 5000000000, "coinbase", "alice_address")  # 50 BTC
blockchain.utxo_set.add_utxo(genesis_utxo)

print(f"Initial state:")
print(f"  Alice balance: {blockchain.get_balance('alice_address')} BTC")
print(f"  UTXO set size: {len(blockchain.utxo_set.utxos)}")

# Create and apply some transactions
tx1 = BitcoinTransaction()
tx1.txid = "tx1_hash"
tx1.add_input("genesis", 0, "alice_signature")
tx1.add_output(25.0, "bob_address")    # 25 BTC to Bob
tx1.add_output(24.9999, "alice_address")  # 24.9999 BTC change to Alice

tx2 = BitcoinTransaction()
tx2.txid = "tx2_hash" 
tx2.add_input("tx1_hash", 0, "bob_signature")
tx2.add_output(10.0, "carol_address")   # 10 BTC to Carol
tx2.add_output(14.9999, "bob_address")  # 14.9999 BTC change to Bob

# Process transactions in a block
blockchain.simulate_block([tx1, tx2])

print(f"\nFinal balances:")
print(f"  Alice: {blockchain.get_balance('alice_address')} BTC")
print(f"  Bob: {blockchain.get_balance('bob_address')} BTC") 
print(f"  Carol: {blockchain.get_balance('carol_address')} BTC")

final_stats = blockchain.utxo_set.get_stats()
print(f"\nFinal UTXO set:")
for key, value in final_stats.items():
    print(f"  {key}: {value}")
```

## Real-World Transaction Analysis 📊

### Transaction Pattern Analysis

```python
def analyze_transaction_patterns():
    """Analyze common Bitcoin transaction patterns"""
    
    print("\n📊 Real-World Transaction Pattern Analysis")
    print("=" * 60)
    
    patterns = {
        'Simple Payment': {
            'structure': '1 input → 2 outputs (payment + change)',
            'percentage': '60%',
            'use_case': 'Person-to-person payments',
            'avg_size': '226 bytes',
            'privacy': 'Low - obvious change detection'
        },
        'Consolidation': {
            'structure': 'Many inputs → 1 output',
            'percentage': '15%',
            'use_case': 'Wallet maintenance, UTXO cleanup',
            'avg_size': '400+ bytes',
            'privacy': 'Very low - all inputs owned by same entity'
        },
        'Distribution': {
            'structure': '1 input → Many outputs',
            'percentage': '10%',
            'use_case': 'Exchange withdrawals, payroll',
            'avg_size': '300+ bytes',
            'privacy': 'Medium - recipients not obviously linked'
        },
        'Exchange Trading': {
            'structure': 'Complex multi-input/output',
            'percentage': '10%',
            'use_case': 'Hot wallet operations',
            'avg_size': '500+ bytes',
            'privacy': 'Low - exchange patterns detectable'
        },
        'CoinJoin': {
            'structure': 'Equal outputs, multiple participants',
            'percentage': '3%',
            'use_case': 'Privacy enhancement',
            'avg_size': '800+ bytes',
            'privacy': 'High - breaks transaction graph analysis'
        },
        'Other': {
            'structure': 'Various complex patterns',
            'percentage': '2%',
            'use_case': 'Smart contracts, special scripts',
            'avg_size': 'Variable',
            'privacy': 'Variable'
        }
    }
    
    for pattern, details in patterns.items():
        print(f"\n{pattern} ({details['percentage']}):")
        print(f"  Structure: {details['structure']}")
        print(f"  Use Case: {details['use_case']}")
        print(f"  Avg Size: {details['avg_size']}")
        print(f"  Privacy: {details['privacy']}")

analyze_transaction_patterns()
```

### Fee Market Analysis

```python
def analyze_fee_market():
    """Analyze Bitcoin fee market dynamics"""
    
    print("\n💰 Bitcoin Fee Market Analysis")
    print("=" * 60)
    
    # Historical fee data (example)
    fee_periods = {
        'Bear Market (2018-2019)': {
            'avg_fee_sat_per_byte': 2,
            'typical_tx_fee_usd': 0.25,
            'confirmation_time': '10-20 minutes',
            'description': 'Very low fees, excess block space'
        },
        'Bull Market Peak (2017)': {
            'avg_fee_sat_per_byte': 50,
            'typical_tx_fee_usd': 25.0,
            'confirmation_time': '2-12 hours',
            'description': 'Extreme congestion, fee market stress test'
        },
        'Bull Market Peak (2021)': {
            'avg_fee_sat_per_byte': 30,
            'typical_tx_fee_usd': 15.0,
            'confirmation_time': '30-60 minutes',
            'description': 'High demand, institutional adoption'
        },
        'Normal Market (2023)': {
            'avg_fee_sat_per_byte': 10,
            'typical_tx_fee_usd': 2.0,
            'confirmation_time': '10-30 minutes',
            'description': 'Balanced fee market, SegWit adoption'
        }
    }
    
    print("Historical Fee Market Conditions:")
    for period, data in fee_periods.items():
        print(f"\n{period}:")
        print(f"  Avg fee rate: {data['avg_fee_sat_per_byte']} sat/byte")
        print(f"  Typical tx cost: ${data['typical_tx_fee_usd']}")
        print(f"  Confirmation time: {data['confirmation_time']}")
        print(f"  Description: {data['description']}")
    
    print(f"\n💡 Fee Market Insights:")
    print(f"  - Fees vary 100x+ based on network demand")
    print(f"  - SegWit adoption reduced average transaction size")
    print(f"  - Lightning Network reduces on-chain transaction load")
    print(f"  - Batch payments and consolidation optimize fees")
    print(f"  - Weekend/night fees typically lower")

analyze_fee_market()
```

## Quiz: Test Your UTXO Knowledge 📝

```python
def utxo_quiz():
    """Test understanding of UTXOs and transactions"""
    
    print("\n🧠 UTXO and Transaction Quiz")
    print("=" * 60)
    
    questions = [
        {
            'question': 'What happens when you spend a UTXO?',
            'options': ['A) UTXO amount is reduced', 'B) UTXO is consumed entirely', 'C) UTXO is marked as used', 'D) UTXO balance updates'],
            'correct': 'B',
            'explanation': 'UTXOs must be spent completely - they cannot be partially spent'
        },
        {
            'question': 'If Alice has UTXOs worth 0.8 BTC and 0.3 BTC, and wants to send 0.5 BTC to Bob, what happens?',
            'options': ['A) 0.8 BTC UTXO is partially spent', 'B) Both UTXOs are consumed', 'C) One UTXO is consumed, change is created', 'D) Transaction is impossible'],
            'correct': 'C',
            'explanation': 'Alice spends the 0.8 BTC UTXO, sends 0.5 BTC to Bob, and receives ~0.3 BTC change (minus fees)'
        },
        {
            'question': 'What creates higher transaction fees?',
            'options': ['A) More UTXOs being spent (inputs)', 'B) Larger BTC amounts', 'C) Newer wallet addresses', 'D) Weekend transactions'],
            'correct': 'A',
            'explanation': 'Transaction size (and thus fees) depends mainly on number of inputs and outputs, not BTC amount'
        },
        {
            'question': 'What is the purpose of UTXO consolidation?',
            'options': ['A) Increase privacy', 'B) Reduce future transaction fees', 'C) Speed up confirmations', 'D) Hide transaction history'],
            'correct': 'B',
            'explanation': 'Consolidating many small UTXOs into one large UTXO reduces the size (and cost) of future transactions'
        }
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for option in q['options']:
            print(f"  {option}")
        
        print(f"\nAnswer: {q['correct']}")
        print(f"Explanation: {q['explanation']}")
        print("-" * 50)

utxo_quiz()
```

## Summary 🎯

Understanding Bitcoin transactions and UTXOs is fundamental to mastering Bitcoin:

### Key Concepts

**UTXO Model:**
- Bitcoin tracks ownership through Unspent Transaction Outputs
- Each UTXO has a value and spending conditions
- UTXOs must be spent completely (no partial spending)
- Change is created through new UTXOs back to the sender

**Transaction Structure:**
- **Inputs** reference and spend previous UTXOs
- **Outputs** create new UTXOs for recipients
- **Scripts** define spending conditions (who can spend)
- **Fees** = Total inputs - Total outputs

**Fee Economics:**
- Fees based on transaction size (bytes), not amount
- More inputs/outputs = larger transaction = higher fees  
- Network congestion drives fee markets
- Optimization strategies can significantly reduce costs

**Practical Implications:**
- Wallet software manages UTXO selection automatically
- Understanding UTXOs helps optimize transaction costs
- Fee estimation requires network condition awareness
- Advanced features like RBF provide fee flexibility

### Real-World Applications

- **Payments**: Most transactions are simple person-to-person transfers
- **Consolidation**: Combining small UTXOs to reduce future fees
- **Distribution**: Exchanges and services making batch payments
- **Privacy**: CoinJoin and other techniques obscure transaction graphs

### Next Steps
- Learn about [Bitcoin Mining and Nodes](mining-and-nodes.md) 
- Understand [Bitcoin Scripting](bitcoin-scripting.md) language
- Study [Digital Signatures](../01-cryptography/digital-signatures.md) for transaction security
- Explore [Ethereum Account Model](../03-ethereum/accounts-and-gas.md) as an alternative

---

**🔄 The UTXO model is Bitcoin's elegant solution to digital ownership - every satoshi has a history and every transaction creates new possibilities.**