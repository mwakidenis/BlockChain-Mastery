# Ethereum Accounts and Gas ⚡⛽

## Introduction

Ethereum's account-based model and gas system are fundamental innovations that make the platform both secure and economically viable. Unlike Bitcoin's UTXO model, Ethereum uses persistent accounts with balances, and unlike traditional systems, it uses gas to meter computational resources and prevent abuse.

## Ethereum Account Types 👤

### 1. Externally Owned Accounts (EOAs)

EOAs are controlled by private keys and represent regular users:

```python
# Example EOA structure
class ExternallyOwnedAccount:
    def __init__(self, private_key: str):
        self.address = self.derive_address(private_key)
        self.private_key = private_key
        self.balance = 0  # Wei
        self.nonce = 0    # Transaction counter
        
    def derive_address(self, private_key: str) -> str:
        """Derive Ethereum address from private key"""
        # Simplified: Real implementation uses ECDSA + Keccak256
        import hashlib
        public_key = f"pub_key_from_{private_key}"
        address = hashlib.sha256(public_key.encode()).hexdigest()[:40]
        return f"0x{address}"
    
    def sign_transaction(self, transaction: dict) -> dict:
        """Sign transaction with private key"""
        transaction['signature'] = f"sig_{self.private_key}_{transaction['nonce']}"
        transaction['from'] = self.address
        return transaction

# Demo EOA operations
print("👤 Externally Owned Account Demo")
print("=" * 50)

# Create EOA
alice = ExternallyOwnedAccount("alice_private_key_123")
print(f"Alice's Address: {alice.address}")
print(f"Alice's Balance: {alice.balance} Wei")

# Create and sign transaction
transaction = {
    'to': '0x742d35Cc6635C0532925a3b8D8Cf97E',
    'value': 1000000000000000000,  # 1 ETH in Wei
    'gas': 21000,
    'gas_price': 20000000000,  # 20 Gwei
    'nonce': alice.nonce
}

signed_tx = alice.sign_transaction(transaction)
print(f"\nSigned Transaction:")
for key, value in signed_tx.items():
    print(f"  {key}: {value}")
```

### 2. Contract Accounts

Contract accounts are controlled by code and can hold ETH and execute logic:

```python
class ContractAccount:
    def __init__(self, creator_address: str, contract_code: str):
        self.address = self.generate_contract_address(creator_address)
        self.balance = 0
        self.code = contract_code
        self.storage = {}  # Persistent storage
        self.creator = creator_address
        
    def generate_contract_address(self, creator: str) -> str:
        """Generate contract address deterministically"""
        import hashlib
        # Simplified: Real implementation uses RLP encoding
        contract_data = f"{creator}_contract"
        address = hashlib.sha256(contract_data.encode()).hexdigest()[:40]
        return f"0x{address}"
    
    def execute_function(self, function_name: str, params: dict) -> dict:
        """Execute contract function"""
        if function_name == "store":
            key = params.get('key')
            value = params.get('value')
            self.storage[key] = value
            return {'success': True, 'gas_used': 20000}
        
        elif function_name == "retrieve":
            key = params.get('key')
            value = self.storage.get(key, 0)
            return {'success': True, 'value': value, 'gas_used': 800}
        
        return {'success': False, 'error': 'Function not found'}

# Demo contract account
print("\n📜 Contract Account Demo")
print("=" * 50)

# Deploy simple storage contract
storage_contract = ContractAccount(
    creator_address="0x742d35Cc6635C0532925a3b8D8Cf97E",
    contract_code="PUSH1 0x42 PUSH1 0x00 SSTORE"  # Simplified bytecode
)

print(f"Contract Address: {storage_contract.address}")
print(f"Created by: {storage_contract.creator}")
print(f"Code: {storage_contract.code}")

# Execute contract functions
store_result = storage_contract.execute_function("store", {'key': 'balance', 'value': 1000})
print(f"\nStore operation: {store_result}")

retrieve_result = storage_contract.execute_function("retrieve", {'key': 'balance'})
print(f"Retrieve operation: {retrieve_result}")

print(f"\nContract Storage: {storage_contract.storage}")
```

## Account State Structure 📊

Each Ethereum account has four components:

```python
class EthereumAccountState:
    def __init__(self, address: str):
        self.address = address
        self.balance = 0      # Account balance in Wei
        self.nonce = 0        # Transaction counter (prevents replay)
        self.storage_root = ""  # Root of storage trie (contracts only)
        self.code_hash = ""     # Hash of contract code (contracts only)
    
    def get_state_info(self) -> dict:
        """Get complete account state"""
        return {
            'address': self.address,
            'balance_wei': self.balance,
            'balance_eth': self.balance / 10**18,
            'nonce': self.nonce,
            'storage_root': self.storage_root,
            'code_hash': self.code_hash,
            'is_contract': bool(self.code_hash)
        }
    
    def update_balance(self, amount: int):
        """Update account balance"""
        self.balance += amount
    
    def increment_nonce(self):
        """Increment transaction nonce"""
        self.nonce += 1

# Demo account state
print("\n📊 Account State Demo")
print("=" * 50)

# Create accounts with different states
eoa_state = EthereumAccountState("0x742d35Cc6635C0532925a3b8D8Cf97E")
eoa_state.balance = 5000000000000000000  # 5 ETH
eoa_state.nonce = 42

contract_state = EthereumAccountState("0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984")
contract_state.balance = 1000000000000000000  # 1 ETH
contract_state.code_hash = "0x123abc..."
contract_state.storage_root = "0x456def..."

accounts = [eoa_state, contract_state]

for account in accounts:
    state = account.get_state_info()
    print(f"\nAccount: {state['address'][:10]}...")
    print(f"  Balance: {state['balance_eth']} ETH")
    print(f"  Nonce: {state['nonce']}")
    print(f"  Type: {'Contract' if state['is_contract'] else 'EOA'}")
    if state['is_contract']:
        print(f"  Code Hash: {state['code_hash']}")
        print(f"  Storage Root: {state['storage_root']}")
```

## Gas System Deep Dive ⛽

### Gas Fundamentals

Gas serves three critical purposes:
1. **Resource Metering**: Prevents infinite loops and DoS attacks
2. **Economic Incentives**: Pays miners/validators for computation
3. **Priority System**: Higher gas prices get faster inclusion

```python
class GasSystem:
    def __init__(self):
        # Gas costs for EVM operations (simplified)
        self.operation_costs = {
            # Arithmetic
            'ADD': 3, 'MUL': 5, 'SUB': 3, 'DIV': 5,
            'MOD': 5, 'ADDMOD': 8, 'MULMOD': 8,
            
            # Comparison & Bitwise
            'LT': 3, 'GT': 3, 'EQ': 3, 'AND': 3, 'OR': 3, 'XOR': 3,
            
            # Memory & Storage
            'MLOAD': 3, 'MSTORE': 3, 'SLOAD': 800, 'SSTORE': 20000,
            
            # System Operations
            'CALL': 700, 'CREATE': 32000, 'SELFDESTRUCT': 5000,
            'SHA3': 30, 'BALANCE': 400, 'BLOCKHASH': 20,
            
            # Stack Operations
            'PUSH1': 3, 'POP': 2, 'DUP1': 3, 'SWAP1': 3,
            
            # Jump Operations
            'JUMP': 8, 'JUMPI': 10, 'JUMPDEST': 1
        }
        
        self.base_transaction_cost = 21000
        self.data_cost_zero = 4      # Cost per zero byte in transaction data
        self.data_cost_nonzero = 16  # Cost per non-zero byte
    
    def calculate_transaction_gas(self, transaction: dict) -> dict:
        """Calculate gas cost for a transaction"""
        gas_used = self.base_transaction_cost
        
        # Calculate data costs
        data = transaction.get('data', b'')
        for byte in data:
            if byte == 0:
                gas_used += self.data_cost_zero
            else:
                gas_used += self.data_cost_nonzero
        
        # Contract creation additional cost
        if transaction.get('to') is None:  # Contract creation
            gas_used += self.operation_costs['CREATE']
        
        return {
            'base_cost': self.base_transaction_cost,
            'data_cost': gas_used - self.base_transaction_cost,
            'total_gas': gas_used
        }
    
    def estimate_contract_execution(self, operations: list) -> dict:
        """Estimate gas for contract execution"""
        total_gas = 0
        operation_breakdown = {}
        
        for op in operations:
            cost = self.operation_costs.get(op, 0)
            total_gas += cost
            
            if op in operation_breakdown:
                operation_breakdown[op] += cost
            else:
                operation_breakdown[op] = cost
        
        return {
            'total_gas': total_gas,
            'operations': operation_breakdown,
            'estimated_cost_eth': total_gas * 20e-9  # Assuming 20 Gwei
        }

# Demo gas calculations
print("\n⛽ Gas System Demo")
print("=" * 50)

gas_system = GasSystem()

# Example 1: Simple ETH transfer
eth_transfer = {
    'to': '0x742d35Cc6635C0532925a3b8D8Cf97E',
    'value': 1000000000000000000,  # 1 ETH
    'data': b''
}

transfer_gas = gas_system.calculate_transaction_gas(eth_transfer)
print("ETH Transfer:")
print(f"  Base Cost: {transfer_gas['base_cost']:,} gas")
print(f"  Data Cost: {transfer_gas['data_cost']:,} gas")
print(f"  Total Gas: {transfer_gas['total_gas']:,} gas")

# Example 2: Contract creation with data
contract_creation = {
    'to': None,  # Contract creation
    'value': 0,
    'data': b'\x60\x60\x40\x52' + b'\x00' * 100  # Bytecode with zeros
}

creation_gas = gas_system.calculate_transaction_gas(contract_creation)
print(f"\nContract Creation:")
print(f"  Base Cost: {creation_gas['base_cost']:,} gas")
print(f"  Data Cost: {creation_gas['data_cost']:,} gas") 
print(f"  Total Gas: {creation_gas['total_gas']:,} gas")

# Example 3: Smart contract execution
contract_operations = ['SLOAD', 'SLOAD', 'ADD', 'SSTORE', 'CALL']
execution_estimate = gas_system.estimate_contract_execution(contract_operations)

print(f"\nSmart Contract Execution:")
print(f"  Operations: {', '.join(contract_operations)}")
print(f"  Total Gas: {execution_estimate['total_gas']:,}")
print(f"  Estimated Cost: {execution_estimate['estimated_cost_eth']:.6f} ETH")
print(f"  Breakdown: {execution_estimate['operations']}")
```

## Gas Price and Fee Markets 💰

### EIP-1559: Fee Market Reform

Since August 2021, Ethereum uses EIP-1559 fee structure:

```python
class EIP1559FeeCalculator:
    def __init__(self):
        self.base_fee = 20e9  # Base fee in Wei (20 Gwei)
        self.max_priority_fee = 2e9  # Priority fee (2 Gwei)
        self.target_gas_per_block = 15_000_000
        self.max_gas_per_block = 30_000_000
        
    def calculate_transaction_fee(self, gas_used: int, max_fee_per_gas: int, 
                                max_priority_fee_per_gas: int) -> dict:
        """Calculate transaction fee under EIP-1559"""
        
        # Effective gas price calculation
        effective_gas_price = min(
            max_fee_per_gas,
            self.base_fee + max_priority_fee_per_gas
        )
        
        # Fee breakdown
        priority_fee = min(max_priority_fee_per_gas, effective_gas_price - self.base_fee)
        base_fee_paid = effective_gas_price - priority_fee
        
        total_fee = gas_used * effective_gas_price
        burned_fee = gas_used * base_fee_paid  # Burned (removed from circulation)
        miner_tip = gas_used * priority_fee    # Goes to validator
        
        return {
            'gas_used': gas_used,
            'effective_gas_price_gwei': effective_gas_price / 1e9,
            'total_fee_eth': total_fee / 1e18,
            'burned_fee_eth': burned_fee / 1e18,
            'miner_tip_eth': miner_tip / 1e18,
            'fee_breakdown': {
                'base_fee_gwei': base_fee_paid / 1e9,
                'priority_fee_gwei': priority_fee / 1e9
            }
        }
    
    def update_base_fee(self, gas_used_in_block: int) -> float:
        """Update base fee based on block utilization"""
        if gas_used_in_block > self.target_gas_per_block:
            # Block is fuller than target, increase base fee
            utilization = gas_used_in_block / self.target_gas_per_block
            self.base_fee *= (1 + 0.125 * (utilization - 1))
        elif gas_used_in_block < self.target_gas_per_block:
            # Block is less full than target, decrease base fee
            utilization = gas_used_in_block / self.target_gas_per_block
            self.base_fee *= (1 - 0.125 * (1 - utilization))
        
        return self.base_fee / 1e9  # Return in Gwei

# Demo EIP-1559 fee calculation
print("\n💰 EIP-1559 Fee Market Demo")
print("=" * 50)

fee_calc = EIP1559FeeCalculator()

# Transaction parameters
gas_used = 50000
max_fee_per_gas = int(30e9)      # 30 Gwei max
max_priority_fee = int(2e9)       # 2 Gwei priority

fee_result = fee_calc.calculate_transaction_fee(
    gas_used, max_fee_per_gas, max_priority_fee
)

print(f"Transaction Fee Breakdown:")
print(f"  Gas Used: {fee_result['gas_used']:,}")
print(f"  Effective Gas Price: {fee_result['effective_gas_price_gwei']:.1f} Gwei")
print(f"  Total Fee: {fee_result['total_fee_eth']:.6f} ETH")
print(f"  Burned (Base Fee): {fee_result['burned_fee_eth']:.6f} ETH")
print(f"  Miner Tip: {fee_result['miner_tip_eth']:.6f} ETH")

# Simulate base fee adjustment over several blocks
print(f"\nBase Fee Adjustment Simulation:")
print(f"Initial Base Fee: {fee_calc.base_fee / 1e9:.1f} Gwei")

# Simulate varying block utilization
block_gas_usage = [25_000_000, 18_000_000, 12_000_000, 28_000_000, 15_000_000]

for i, gas_used in enumerate(block_gas_usage, 1):
    new_base_fee = fee_calc.update_base_fee(gas_used)
    utilization = (gas_used / fee_calc.target_gas_per_block) * 100
    print(f"  Block {i}: {gas_used:,} gas ({utilization:.1f}% full) → {new_base_fee:.1f} Gwei")
```

## Gas Optimization Strategies 🎯

### Common Optimization Techniques

```python
class GasOptimization:
    @staticmethod
    def demonstrate_storage_patterns():
        """Show gas-efficient storage patterns"""
        print("💡 Gas Optimization: Storage Patterns")
        print("-" * 40)
        
        # Bad: Multiple storage writes
        print("❌ Inefficient (3 SSTORE operations):")
        operations_bad = ['SSTORE', 'SSTORE', 'SSTORE']  # 60,000 gas
        print(f"  Operations: {operations_bad}")
        print(f"  Gas Cost: {len(operations_bad) * 20000:,}")
        
        # Good: Pack data into single storage slot
        print("\n✅ Efficient (1 SSTORE operation):")
        operations_good = ['SSTORE']  # 20,000 gas
        print(f"  Operations: {operations_good} (packed data)")
        print(f"  Gas Cost: {len(operations_good) * 20000:,}")
        print(f"  Savings: {(len(operations_bad) - len(operations_good)) * 20000:,} gas")
    
    @staticmethod
    def demonstrate_loop_optimization():
        """Show gas-efficient loop patterns"""
        print("\n💡 Gas Optimization: Loop Patterns")
        print("-" * 40)
        
        # Simulate gas costs for different loop implementations
        array_size = 100
        
        # Bad: Reading array length in each iteration
        gas_bad = array_size * (800 + 3)  # SLOAD + LT for each iteration
        print(f"❌ Inefficient loop (read length each time): {gas_bad:,} gas")
        
        # Good: Cache array length
        gas_good = 800 + (array_size * 3)  # One SLOAD + LT for each iteration
        print(f"✅ Efficient loop (cached length): {gas_good:,} gas")
        print(f"Savings: {gas_bad - gas_good:,} gas")
    
    @staticmethod
    def demonstrate_function_modifiers():
        """Show impact of function visibility modifiers"""
        print("\n💡 Gas Optimization: Function Modifiers")
        print("-" * 40)
        
        modifiers = {
            'public': 700,      # Accessible from anywhere
            'external': 600,    # Only external calls
            'internal': 400,    # Only within contract/derived
            'private': 300      # Only within contract
        }
        
        for modifier, cost in modifiers.items():
            print(f"  {modifier:8s}: {cost:,} gas")
        
        print(f"💡 Tip: Use 'external' for functions only called externally")

# Run optimization demos
print("\n🎯 Gas Optimization Demonstrations")
print("=" * 50)

optimizer = GasOptimization()
optimizer.demonstrate_storage_patterns()
optimizer.demonstrate_loop_optimization()
optimizer.demonstrate_function_modifiers()
```

## Real-World Examples 🌍

### Gas Usage in Popular DApps

```python
def analyze_popular_dapp_gas():
    """Analyze gas usage in popular DApps"""
    print("\n🌍 Real-World Gas Usage Examples")
    print("=" * 50)
    
    dapp_operations = {
        'Uniswap V2 Swap': {
            'operations': ['SLOAD'] * 4 + ['SSTORE'] * 2 + ['CALL'] * 2,
            'typical_gas': 150000,
            'description': 'Token swap on DEX'
        },
        'OpenSea NFT Transfer': {
            'operations': ['SLOAD'] * 3 + ['SSTORE'] * 2,
            'typical_gas': 85000,
            'description': 'ERC-721 NFT transfer'
        },
        'Aave Lending': {
            'operations': ['SLOAD'] * 10 + ['SSTORE'] * 5 + ['CALL'] * 3,
            'typical_gas': 300000,
            'description': 'Supply/borrow on lending protocol'
        },
        'ENS Domain Registration': {
            'operations': ['CREATE'] + ['SSTORE'] * 3,
            'typical_gas': 180000,
            'description': 'Register .eth domain'
        }
    }
    
    # Calculate costs at different gas prices
    gas_prices = [10, 30, 50, 100]  # Gwei
    eth_price = 2000  # USD
    
    for dapp_name, info in dapp_operations.items():
        print(f"\n{dapp_name}:")
        print(f"  Description: {info['description']}")
        print(f"  Typical Gas: {info['typical_gas']:,}")
        print(f"  Cost at different gas prices:")
        
        for gas_price in gas_prices:
            cost_eth = (info['typical_gas'] * gas_price * 1e9) / 1e18
            cost_usd = cost_eth * eth_price
            print(f"    {gas_price:3d} Gwei: ${cost_usd:6.2f} ({cost_eth:.6f} ETH)")

analyze_popular_dapp_gas()
```

## Account Security Best Practices 🔒

### Key Management and Security

```python
class AccountSecurity:
    @staticmethod
    def demonstrate_nonce_protection():
        """Show how nonces prevent replay attacks"""
        print("\n🔒 Security: Nonce Protection")
        print("-" * 40)
        
        class SecureAccount:
            def __init__(self, address: str):
                self.address = address
                self.nonce = 0
                self.processed_transactions = set()
            
            def process_transaction(self, tx: dict) -> dict:
                tx_nonce = tx.get('nonce')
                tx_signature = tx.get('signature')
                
                # Check nonce ordering
                if tx_nonce != self.nonce:
                    return {
                        'success': False,
                        'error': f'Invalid nonce. Expected {self.nonce}, got {tx_nonce}'
                    }
                
                # Check for replay attack
                if tx_signature in self.processed_transactions:
                    return {
                        'success': False,
                        'error': 'Transaction already processed (replay attack)'
                    }
                
                # Process transaction
                self.processed_transactions.add(tx_signature)
                self.nonce += 1
                
                return {'success': True, 'new_nonce': self.nonce}
        
        # Demo secure transaction processing
        account = SecureAccount("0x742d35Cc6635C0532925a3b8D8Cf97E")
        
        # Valid transaction sequence
        tx1 = {'nonce': 0, 'signature': 'sig_1', 'value': 100}
        tx2 = {'nonce': 1, 'signature': 'sig_2', 'value': 200}
        
        # Invalid transactions
        tx_replay = {'nonce': 2, 'signature': 'sig_1', 'value': 150}  # Replay
        tx_wrong_nonce = {'nonce': 5, 'signature': 'sig_3', 'value': 300}  # Wrong nonce
        
        transactions = [tx1, tx2, tx_replay, tx_wrong_nonce]
        
        for i, tx in enumerate(transactions, 1):
            result = account.process_transaction(tx)
            status = "✅ Success" if result['success'] else f"❌ {result['error']}"
            print(f"  TX{i}: {status}")
    
    @staticmethod
    def demonstrate_access_patterns():
        """Show secure access control patterns"""
        print("\n🔒 Security: Access Control Patterns")
        print("-" * 40)
        
        patterns = {
            'Owner Only': 'Only contract deployer can execute',
            'Role Based': 'Different roles have different permissions',
            'Multi-Signature': 'Multiple signatures required for execution',
            'Time Locks': 'Actions have mandatory delay periods',
            'Pausable': 'Emergency stop functionality'
        }
        
        for pattern, description in patterns.items():
            print(f"  {pattern:15s}: {description}")

# Run security demonstrations
security = AccountSecurity()
security.demonstrate_nonce_protection()
security.demonstrate_access_patterns()
```

## Summary and Next Steps 🎯

### Key Takeaways

1. **Account Types**: EOAs (user-controlled) vs Contract Accounts (code-controlled)
2. **Gas System**: Computational resource metering and economic incentives
3. **EIP-1559**: Modern fee market with base fee burning and priority fees
4. **Optimization**: Storage packing, loop caching, and modifier selection
5. **Security**: Nonce protection, access control, and best practices

### Practical Applications

- **Wallet Development**: Understanding account structures for secure key management
- **DApp Development**: Optimizing gas usage for better user experience
- **Smart Contract Auditing**: Identifying gas inefficiencies and security issues
- **Transaction Analysis**: Understanding fee structures and network dynamics

### Next Steps
- Deep dive into [Ethereum Virtual Machine](ethereum-virtual-machine.md) internals
- Explore [Ethereum 2.0](ethereum-2.md) and Proof of Stake
- Study [Smart Contracts](../04-smart-contracts/solidity-basics.md) development
- Practice with [Hands-on Projects](../08-projects/) to apply these concepts

---

**⚡ Understanding accounts and gas is crucial for anyone building on Ethereum - these fundamentals determine both the security and economics of every transaction and smart contract interaction.**