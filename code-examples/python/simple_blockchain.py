"""
Simple Blockchain Implementation in Python
Educational example showing core blockchain concepts
"""

import hashlib
import json
import time
from typing import List, Dict, Any, Optional


class Block:
    """
    Represents a single block in the blockchain
    """
    
    def __init__(
        self,
        index: int,
        transactions: List[Dict[str, Any]],
        previous_hash: str,
        nonce: int = 0
    ):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Calculate SHA-256 hash of the block
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """
        Mine the block using proof-of-work
        """
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"✅ Block mined: {self.hash}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert block to dictionary
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class Transaction:
    """
    Represents a transaction
    """
    
    def __init__(
        self,
        sender: str,
        recipient: str,
        amount: float
    ):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
    
    def calculate_hash(self) -> str:
        """
        Calculate hash of the transaction
        """
        tx_string = json.dumps({
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp
        }, sort_keys=True)
        
        return hashlib.sha256(tx_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert transaction to dictionary
        """
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "hash": self.calculate_hash()
        }
    
    def is_valid(self) -> bool:
        """
        Validate transaction
        """
        if self.sender == self.recipient:
            return False
        
        if self.amount <= 0:
            return False
        
        return True


class Blockchain:
    """
    Represents the blockchain
    """
    
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = 100
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """
        Create the first block in the blockchain
        """
        genesis_transactions = [{
            "sender": None,
            "recipient": "genesis",
            "amount": 0,
            "timestamp": time.time()
        }]
        
        genesis_block = Block(0, genesis_transactions, "0")
        self.chain.append(genesis_block)
        
        print("🎉 Genesis block created!")
    
    def get_latest_block(self) -> Block:
        """
        Get the most recent block
        """
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """
        Add a transaction to pending transactions
        """
        if not transaction.is_valid():
            print("❌ Invalid transaction")
            return False
        
        # Check if sender has sufficient balance
        balance = self.get_balance(transaction.sender)
        if balance < transaction.amount:
            print(f"❌ Insufficient balance: {balance} < {transaction.amount}")
            return False
        
        self.pending_transactions.append(transaction)
        print(f"✅ Transaction added: {transaction.sender} -> {transaction.recipient}: {transaction.amount}")
        return True
    
    def mine_pending_transactions(self, mining_reward_address: str) -> None:
        """
        Mine all pending transactions into a new block
        """
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
        print(f"⛏️  Mining block {new_block.index}...")
        new_block.mine_block(self.difficulty)
        
        # Add to chain
        self.chain.append(new_block)
        
        # Clear pending transactions
        self.pending_transactions = []
        
        print(f"✨ Block {new_block.index} added to chain!")
    
    def get_balance(self, address: str) -> float:
        """
        Calculate balance for a given address
        """
        balance = 0.0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('sender') == address:
                    balance -= transaction.get('amount', 0)
                
                if transaction.get('recipient') == address:
                    balance += transaction.get('amount', 0)
        
        return balance
    
    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ Block {i} hash is invalid")
                return False
            
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ Block {i} is not linked correctly")
                return False
            
            # Check proof of work
            if not current_block.hash.startswith("0" * self.difficulty):
                print(f"❌ Block {i} doesn't meet difficulty requirement")
                return False
        
        return True
    
    def get_chain_info(self) -> Dict[str, Any]:
        """
        Get blockchain statistics
        """
        return {
            "blocks": len(self.chain),
            "difficulty": self.difficulty,
            "pending_transactions": len(self.pending_transactions),
            "is_valid": self.is_chain_valid()
        }
    
    def print_chain(self) -> None:
        """
        Print the entire blockchain
        """
        print("\n" + "="*60)
        print("📊 BLOCKCHAIN CONTENTS")
        print("="*60)
        
        for i, block in enumerate(self.chain):
            print(f"\n🔗 Block {i}")
            print(f"  Hash:          {block.hash}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Timestamp:     {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
            print(f"  Nonce:         {block.nonce}")
            print(f"  Transactions:  {len(block.transactions)}")
            
            for j, tx in enumerate(block.transactions):
                sender = tx.get('sender', 'None')
                recipient = tx.get('recipient', 'None')
                amount = tx.get('amount', 0)
                print(f"    {j+1}. {sender} -> {recipient}: {amount}")
        
        print("="*60 + "\n")


def demo():
    """
    Demonstrate blockchain functionality
    """
    print("\n" + "🚀 "*20)
    print("SIMPLE BLOCKCHAIN DEMONSTRATION")
    print("🚀 "*20 + "\n")
    
    # Create blockchain
    blockchain = Blockchain(difficulty=2)
    
    # Display initial state
    print(f"📊 Initial blockchain info: {blockchain.get_chain_info()}")
    
    # Create some transactions
    print("\n📝 Creating transactions...")
    tx1 = Transaction("Alice", "Bob", 50)
    tx2 = Transaction("Bob", "Charlie", 25)
    tx3 = Transaction("Charlie", "Alice", 10)
    
    # Add transactions
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    blockchain.add_transaction(tx3)
    
    # Mine block 1
    print("\n⛏️  Mining block 1...")
    blockchain.mine_pending_transactions("Miner1")
    
    # Check balances
    print("\n💰 Balances after mining block 1:")
    print(f"  Alice:   {blockchain.get_balance('Alice')}")
    print(f"  Bob:     {blockchain.get_balance('Bob')}")
    print(f"  Charlie: {blockchain.get_balance('Charlie')}")
    print(f"  Miner1:  {blockchain.get_balance('Miner1')}")
    
    # Add more transactions
    print("\n📝 Creating more transactions...")
    tx4 = Transaction("Alice", "Bob", 20)
    blockchain.add_transaction(tx4)
    
    # Mine block 2
    print("\n⛏️  Mining block 2...")
    blockchain.mine_pending_transactions("Miner2")
    
    # Final balances
    print("\n💰 Final balances:")
    print(f"  Alice:   {blockchain.get_balance('Alice')}")
    print(f"  Bob:     {blockchain.get_balance('Bob')}")
    print(f"  Charlie: {blockchain.get_balance('Charlie')}")
    print(f"  Miner1:  {blockchain.get_balance('Miner1')}")
    print(f"  Miner2:  {blockchain.get_balance('Miner2')}")
    
    # Display blockchain
    blockchain.print_chain()
    
    # Validate blockchain
    print(f"✅ Blockchain valid: {blockchain.is_chain_valid()}")
    
    # Try to tamper with the blockchain
    print("\n🔨 Attempting to tamper with block 1...")
    print("⚠️  WARNING: This is for educational demonstration only!")
    print("⚠️  In a real distributed network, this attack wouldn't work because:")
    print("    - Other nodes would reject the tampered block")
    print("    - The attacker would need to control 51%+ of the network")
    print("    - All subsequent blocks would need to be recalculated")
    blockchain.chain[1].transactions[0]['amount'] = 999999
    print(f"❌ Blockchain valid after tampering: {blockchain.is_chain_valid()}")
    
    # Display final info
    print(f"\n📊 Final blockchain info: {blockchain.get_chain_info()}")


if __name__ == "__main__":
    demo()
