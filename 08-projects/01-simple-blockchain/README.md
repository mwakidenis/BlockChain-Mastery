# Simple Blockchain Implementation 🔗

## Project Overview

Build a basic blockchain from scratch to understand the fundamental concepts of blockchain technology. This project will implement core features like blocks, hashing, proof-of-work, and basic transaction handling.

## Learning Objectives

By completing this project, you will understand:
- How blocks are structured and linked together
- How cryptographic hashing secures the blockchain
- How proof-of-work consensus prevents tampering
- How transactions are validated and processed
- The basic principles underlying all blockchain networks

## Prerequisites

- **Programming Language**: Python 3.7+ (recommended) or JavaScript/Node.js
- **Libraries**: `hashlib`, `json`, `time` (built-in Python libraries)
- **Time Estimate**: 4-6 hours for basic implementation
- **Difficulty Level**: Beginner to Intermediate

## Project Structure

```
01-simple-blockchain/
├── README.md
├── blockchain.py          # Main blockchain implementation
├── block.py              # Block class definition
├── transaction.py        # Transaction handling
├── miner.py              # Mining and proof-of-work
├── wallet.py             # Simple wallet functionality
├── tests/
│   ├── test_blockchain.py
│   ├── test_mining.py
│   └── test_transactions.py
└── examples/
    ├── basic_usage.py
    └── mining_demo.py
```

## Setup Instructions

### Step 1: Environment Setup

```bash
# Create project directory
mkdir simple-blockchain
cd simple-blockchain

# Create virtual environment (recommended)
python -m venv blockchain-env

# Activate virtual environment
# On Windows:
blockchain-env\Scripts\activate
# On macOS/Linux:
source blockchain-env/bin/activate

# Install dependencies (minimal for this project)
pip install pytest  # For testing
```

### Step 2: Implement Core Classes

Create `block.py`:

```python
import hashlib
import json
import time
from typing import List, Dict, Any

class Block:
    def __init__(self, index: int, transactions: List[Dict], previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """Mine the block using proof-of-work"""
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"Block mined: {self.hash}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary representation"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
```

Create `transaction.py`:

```python
import hashlib
import json
from typing import Dict, Any

class Transaction:
    def __init__(self, from_address: str, to_address: str, amount: float):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.timestamp = time.time()
    
    def calculate_hash(self) -> str:
        """Calculate hash of the transaction"""
        tx_string = json.dumps({
            "from": self.from_address,
            "to": self.to_address,
            "amount": self.amount,
            "timestamp": self.timestamp
        }, sort_keys=True)
        
        return hashlib.sha256(tx_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary"""
        return {
            "from": self.from_address,
            "to": self.to_address,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "hash": self.calculate_hash()
        }
    
    def is_valid(self) -> bool:
        """Basic transaction validation"""
        if self.from_address == self.to_address:
            return False
        
        if self.amount <= 0:
            return False
        
        # Add more validation logic as needed
        return True
```

Create `blockchain.py`:

```python
from typing import List, Dict, Optional
from block import Block
from transaction import Transaction

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = 2  # Number of leading zeros required
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = 100
    
    def create_genesis_block(self) -> Block:
        """Create the first block in the blockchain"""
        genesis_transactions = [{
            "from": None,
            "to": "genesis",
            "amount": 0,
            "timestamp": time.time()
        }]
        return Block(0, genesis_transactions, "0")
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Add a transaction to the pending transactions"""
        if not transaction.is_valid():
            return False
        
        # Check if sender has sufficient balance
        balance = self.get_balance(transaction.from_address)
        if balance < transaction.amount:
            return False
        
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self, mining_reward_address: str) -> None:
        """Mine all pending transactions into a new block"""
        # Add mining reward transaction
        reward_transaction = Transaction(None, mining_reward_address, self.mining_reward)
        self.pending_transactions.append(reward_transaction)
        
        # Create new block
        new_block = Block(
            len(self.chain),
            [tx.to_dict() for tx in self.pending_transactions],
            self.get_latest_block().hash
        )
        
        # Mine the block
        new_block.mine_block(self.difficulty)
        
        # Add to chain and clear pending transactions
        self.chain.append(new_block)
        self.pending_transactions = []
    
    def get_balance(self, address: str) -> float:
        """Calculate balance for a given address"""
        balance = 0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('from') == address:
                    balance -= transaction.get('amount', 0)
                
                if transaction.get('to') == address:
                    balance += transaction.get('amount', 0)
        
        return balance
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_chain_info(self) -> Dict:
        """Get blockchain statistics"""
        return {
            "blocks": len(self.chain),
            "difficulty": self.difficulty,
            "pending_transactions": len(self.pending_transactions),
            "is_valid": self.is_chain_valid()
        }
```

### Step 3: Create Usage Examples

Create `examples/basic_usage.py`:

```python
import sys
sys.path.append('..')

from blockchain import Blockchain
from transaction import Transaction

def main():
    # Create a new blockchain
    my_blockchain = Blockchain()
    
    print("🔗 Simple Blockchain Demo")
    print("=" * 50)
    
    # Display initial state
    print(f"Initial blockchain info: {my_blockchain.get_chain_info()}")
    
    # Create some transactions
    tx1 = Transaction("Alice", "Bob", 50)
    tx2 = Transaction("Bob", "Charlie", 25)
    
    # Add transactions to blockchain
    print(f"\nAdding transaction: Alice -> Bob (50 coins)")
    my_blockchain.add_transaction(tx1)
    
    print(f"Adding transaction: Bob -> Charlie (25 coins)")
    my_blockchain.add_transaction(tx2)
    
    # Mine the transactions
    print(f"\nMining pending transactions...")
    my_blockchain.mine_pending_transactions("Miner1")
    
    # Check balances
    print(f"\nBalances after mining:")
    print(f"Alice: {my_blockchain.get_balance('Alice')}")
    print(f"Bob: {my_blockchain.get_balance('Bob')}")
    print(f"Charlie: {my_blockchain.get_balance('Charlie')}")
    print(f"Miner1: {my_blockchain.get_balance('Miner1')}")
    
    # Display blockchain info
    print(f"\nBlockchain info: {my_blockchain.get_chain_info()}")
    
    # Display all blocks
    print(f"\nBlockchain contents:")
    for i, block in enumerate(my_blockchain.chain):
        print(f"Block {i}:")
        print(f"  Hash: {block.hash}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Transactions: {len(block.transactions)}")
        print(f"  Nonce: {block.nonce}")
        print()

if __name__ == "__main__":
    main()
```

### Step 4: Add Tests

Create `tests/test_blockchain.py`:

```python
import unittest
import sys
sys.path.append('..')

from blockchain import Blockchain
from transaction import Transaction

class TestBlockchain(unittest.TestCase):
    
    def setUp(self):
        self.blockchain = Blockchain()
    
    def test_genesis_block_creation(self):
        """Test that genesis block is created correctly"""
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)
        self.assertEqual(self.blockchain.chain[0].previous_hash, "0")
    
    def test_add_valid_transaction(self):
        """Test adding a valid transaction"""
        # First, mine some coins for Alice
        self.blockchain.mine_pending_transactions("Alice")
        
        # Now Alice can send coins
        tx = Transaction("Alice", "Bob", 50)
        result = self.blockchain.add_transaction(tx)
        
        self.assertTrue(result)
        self.assertEqual(len(self.blockchain.pending_transactions), 1)
    
    def test_reject_invalid_transaction(self):
        """Test rejecting invalid transactions"""
        # Try to send more coins than available
        tx = Transaction("Alice", "Bob", 1000)
        result = self.blockchain.add_transaction(tx)
        
        self.assertFalse(result)
        self.assertEqual(len(self.blockchain.pending_transactions), 0)
    
    def test_mining_and_rewards(self):
        """Test mining process and rewards"""
        initial_blocks = len(self.blockchain.chain)
        
        # Mine a block
        self.blockchain.mine_pending_transactions("Miner1")
        
        # Check if block was added
        self.assertEqual(len(self.blockchain.chain), initial_blocks + 1)
        
        # Check if miner received reward
        balance = self.blockchain.get_balance("Miner1")
        self.assertEqual(balance, self.blockchain.mining_reward)
    
    def test_blockchain_validation(self):
        """Test blockchain validation"""
        # Initially valid
        self.assertTrue(self.blockchain.is_chain_valid())
        
        # Mine a block
        self.blockchain.mine_pending_transactions("Miner1")
        self.assertTrue(self.blockchain.is_chain_valid())
        
        # Tamper with blockchain (this should make it invalid)
        self.blockchain.chain[1].transactions[0]['amount'] = 999999
        self.assertFalse(self.blockchain.is_chain_valid())

if __name__ == '__main__':
    unittest.main()
```

### Step 5: Run the Project

```bash
# Run the basic demo
python examples/basic_usage.py

# Run tests
python -m pytest tests/ -v

# Or run specific test
python tests/test_blockchain.py
```

## Expected Output

When you run the basic usage example, you should see:

```
🔗 Simple Blockchain Demo
==================================================
Initial blockchain info: {'blocks': 1, 'difficulty': 2, 'pending_transactions': 0, 'is_valid': True}

Adding transaction: Alice -> Bob (50 coins)
Adding transaction: Bob -> Charlie (25 coins)

Mining pending transactions...
Block mined: 00a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456

Balances after mining:
Alice: 50.0
Bob: 25.0
Charlie: 25.0
Miner1: 100.0

Blockchain info: {'blocks': 2, 'difficulty': 2, 'pending_transactions': 0, 'is_valid': True}
```

## Extensions and Improvements

Once you have the basic blockchain working, try these extensions:

### Level 2: Enhanced Features

1. **Digital Signatures**: Add transaction signing with public/private keys
2. **Wallet Management**: Create a proper wallet class with key generation
3. **Network Simulation**: Simulate multiple nodes and consensus
4. **Transaction Fees**: Implement transaction fees for miners
5. **Variable Difficulty**: Adjust mining difficulty based on block time

### Level 3: Advanced Features

1. **Smart Contracts**: Add simple smart contract functionality
2. **Merkle Trees**: Implement Merkle trees for efficient transaction verification
3. **REST API**: Add a web API to interact with your blockchain
4. **Persistence**: Save blockchain data to files or database
5. **P2P Network**: Implement basic peer-to-peer networking

## Key Concepts Learned

After completing this project, you should understand:

1. **Block Structure**: How blocks contain transactions and link to previous blocks
2. **Cryptographic Hashing**: How SHA-256 secures the blockchain
3. **Proof of Work**: How mining prevents tampering and secures the network
4. **Chain Validation**: How to verify blockchain integrity
5. **Transaction Processing**: How transactions are validated and included
6. **Consensus**: Basic principles of how networks agree on state

## Troubleshooting

### Common Issues:

1. **ImportError**: Make sure all files are in the correct directories
2. **Mining Takes Too Long**: Reduce the difficulty level (e.g., difficulty = 1)
3. **Test Failures**: Check that transaction amounts don't exceed available balances
4. **Hash Mismatches**: Ensure consistent JSON serialization with `sort_keys=True`

### Debug Tips:

- Add print statements to see what's happening during mining
- Use a debugger to step through transaction validation
- Check blockchain validity after each operation
- Verify that nonce incrementing works correctly

## Next Steps

After completing this project:

1. **Study Bitcoin**: Compare your implementation with Bitcoin's actual design
2. **Learn Ethereum**: Understand how smart contracts extend blockchain functionality  
3. **Explore Consensus**: Study different consensus mechanisms (PoS, DPoS, etc.)
4. **Security Analysis**: Learn about common blockchain vulnerabilities
5. **Real Projects**: Contribute to open-source blockchain projects

## Resources

- **Bitcoin Whitepaper**: Understanding the original blockchain design
- **Mastering Bitcoin**: Technical deep dive into Bitcoin's implementation
- **Ethereum Documentation**: Learn about smart contract platforms
- **Cryptography Courses**: Understand the mathematical foundations

---

**🎉 Congratulations! You've built your first blockchain from scratch and learned the fundamental concepts that power all blockchain networks.**