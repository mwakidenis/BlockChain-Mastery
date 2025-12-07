# Ethereum Virtual Machine (EVM) 🖥️⚡

## Introduction

The Ethereum Virtual Machine (EVM) is the heart of Ethereum - a **Turing-complete virtual computer** that executes smart contracts across thousands of nodes worldwide. It's a stack-based, 256-bit machine that maintains global state and processes transactions deterministically. Understanding the EVM is crucial for smart contract development, optimization, and security.

## EVM Architecture Overview 🏗️

### Core Components

The EVM consists of several key components that work together:

```python
class EthereumVirtualMachine:
    def __init__(self):
        # Stack (256-bit words, max 1024 items)
        self.stack = []
        self.max_stack_size = 1024
        
        # Memory (byte-addressed, dynamically sized)
        self.memory = bytearray()
        
        # Storage (persistent, key-value store)
        self.storage = {}
        
        # Program Counter
        self.pc = 0
        
        # Gas tracking
        self.gas_available = 0
        self.gas_used = 0
        
        # Execution context
        self.call_stack = []
        self.return_data = b''
        
        # World state
        self.accounts = {}
        
    def load_bytecode(self, bytecode: bytes):
        """Load contract bytecode for execution"""
        self.bytecode = bytecode
        self.pc = 0
    
    def execute_opcode(self, opcode: int) -> bool:
        """Execute a single opcode"""
        if opcode == 0x01:  # ADD
            return self._op_add()
        elif opcode == 0x02:  # MUL
            return self._op_mul()
        elif opcode == 0x50:  # POP
            return self._op_pop()
        elif opcode == 0x51:  # MLOAD
            return self._op_mload()
        elif opcode == 0x52:  # MSTORE
            return self._op_mstore()
        elif opcode == 0x54:  # SLOAD
            return self._op_sload()
        elif opcode == 0x55:  # SSTORE
            return self._op_sstore()
        else:
            return False  # Unknown opcode
    
    def _op_add(self) -> bool:
        """ADD operation: pop two values, push sum"""
        if len(self.stack) < 2:
            return False
        
        a = self.stack.pop()
        b = self.stack.pop()
        result = (a + b) % (2**256)  # 256-bit arithmetic
        self.stack.append(result)
        self.gas_used += 3
        return True
    
    def _op_mul(self) -> bool:
        """MUL operation: pop two values, push product"""
        if len(self.stack) < 2:
            return False
        
        a = self.stack.pop()
        b = self.stack.pop()
        result = (a * b) % (2**256)
        self.stack.append(result)
        self.gas_used += 5
        return True
    
    def _op_sstore(self) -> bool:
        """SSTORE operation: store value in persistent storage"""
        if len(self.stack) < 2:
            return False
        
        key = self.stack.pop()
        value = self.stack.pop()
        self.storage[key] = value
        self.gas_used += 20000  # High cost for storage writes
        return True
    
    def _op_sload(self) -> bool:
        """SLOAD operation: load value from persistent storage"""
        if len(self.stack) < 1:
            return False
        
        key = self.stack.pop()
        value = self.storage.get(key, 0)
        self.stack.append(value)
        self.gas_used += 800
        return True

# Demo basic EVM operations
print("🖥️ EVM Architecture Demo")
print("=" * 50)

evm = EthereumVirtualMachine()

# Set up initial state
evm.gas_available = 100000
evm.stack = [10, 20]  # Initial stack values

print(f"Initial State:")
print(f"  Stack: {evm.stack}")
print(f"  Gas Available: {evm.gas_available:,}")

# Execute ADD operation
print(f"\nExecuting ADD operation (0x01):")
success = evm.execute_opcode(0x01)
print(f"  Success: {success}")
print(f"  Stack: {evm.stack}")
print(f"  Gas Used: {evm.gas_used}")

# Execute MUL operation
evm.stack.append(5)  # Add another value
print(f"\nExecuting MUL operation (0x02):")
print(f"  Stack before: {evm.stack}")
success = evm.execute_opcode(0x02)
print(f"  Success: {success}")
print(f"  Stack after: {evm.stack}")
print(f"  Gas Used: {evm.gas_used}")
```

## EVM Memory Model 💾

### Stack, Memory, and Storage

The EVM uses three different data locations:

```python
class EVMMemoryModel:
    def __init__(self):
        self.stack = []           # Stack (volatile)
        self.memory = bytearray() # Memory (volatile) 
        self.storage = {}         # Storage (persistent)
        
    def demonstrate_memory_types(self):
        """Show different memory types and their characteristics"""
        print("💾 EVM Memory Model Demo")
        print("=" * 50)
        
        # Stack operations
        print("Stack (LIFO, 256-bit words):")
        self.stack.append(0x42)
        self.stack.append(0x123456789ABCDEF)
        print(f"  After PUSH operations: {[hex(x) for x in self.stack]}")
        
        value = self.stack.pop()
        print(f"  After POP: {hex(value)} (popped), {[hex(x) for x in self.stack]} (remaining)")
        
        # Memory operations
        print(f"\nMemory (byte-addressed, volatile):")
        # Store 32-byte word at offset 0
        word = 0x123456789ABCDEF.to_bytes(32, 'big')
        self.memory.extend(word)
        print(f"  Stored 32-byte word at offset 0")
        print(f"  Memory size: {len(self.memory)} bytes")
        print(f"  Memory content: {self.memory[:8].hex()}...")
        
        # Load from memory
        loaded = int.from_bytes(self.memory[0:32], 'big')
        print(f"  Loaded value: {hex(loaded)}")
        
        # Storage operations  
        print(f"\nStorage (key-value, persistent):")
        self.storage[0x01] = 0x42
        self.storage[0x02] = 0x123456789ABCDEF
        print(f"  Stored values in storage")
        for key, value in self.storage.items():
            print(f"    Key: {hex(key)}, Value: {hex(value)}")
        
        # Gas costs comparison
        print(f"\nGas Costs Comparison:")
        costs = {
            'Stack operations (PUSH/POP)': '3 gas',
            'Memory operations (MLOAD/MSTORE)': '3-96 gas',
            'Storage operations (SLOAD)': '800 gas',
            'Storage operations (SSTORE)': '5,000-20,000 gas'
        }
        
        for operation, cost in costs.items():
            print(f"  {operation:30}: {cost}")

# Run memory model demo
memory_model = EVMMemoryModel()
memory_model.demonstrate_memory_types()
```

## EVM Bytecode and Opcodes 📜

### Understanding EVM Assembly

```python
class EVMBytecodeAnalyzer:
    def __init__(self):
        # Opcode mappings (partial)
        self.opcodes = {
            0x00: ('STOP', 0, 0),
            0x01: ('ADD', 2, 1),
            0x02: ('MUL', 2, 1),
            0x10: ('LT', 2, 1),
            0x50: ('POP', 1, 0),
            0x51: ('MLOAD', 1, 1),
            0x52: ('MSTORE', 2, 0),
            0x54: ('SLOAD', 1, 1),
            0x55: ('SSTORE', 2, 0),
            0x60: ('PUSH1', 0, 1),
            0x61: ('PUSH2', 0, 1),
            0x80: ('DUP1', 1, 2),
            0x90: ('SWAP1', 2, 2),
            0xA0: ('LOG0', 2, 0),
            0xF3: ('RETURN', 2, 0),
            0xFD: ('REVERT', 2, 0)
        }
    
    def disassemble_bytecode(self, bytecode: bytes) -> list:
        """Disassemble bytecode into human-readable opcodes"""
        instructions = []
        i = 0
        
        while i < len(bytecode):
            opcode = bytecode[i]
            
            if opcode in self.opcodes:
                name, stack_in, stack_out = self.opcodes[opcode]
                
                # Handle PUSH instructions
                if name.startswith('PUSH'):
                    push_bytes = int(name[4:]) if name[4:] else 1
                    if i + push_bytes < len(bytecode):
                        data = bytecode[i+1:i+1+push_bytes]
                        instructions.append({
                            'opcode': opcode,
                            'name': name,
                            'data': data.hex(),
                            'stack_effect': f"-{stack_in} +{stack_out}"
                        })
                        i += push_bytes + 1
                    else:
                        break
                else:
                    instructions.append({
                        'opcode': opcode,
                        'name': name,
                        'data': None,
                        'stack_effect': f"-{stack_in} +{stack_out}"
                    })
                    i += 1
            else:
                instructions.append({
                    'opcode': opcode,
                    'name': 'UNKNOWN',
                    'data': None,
                    'stack_effect': 'unknown'
                })
                i += 1
                
        return instructions
    
    def analyze_contract_bytecode(self, bytecode_hex: str):
        """Analyze real contract bytecode"""
        print("📜 Bytecode Analysis Demo")
        print("=" * 50)
        
        bytecode = bytes.fromhex(bytecode_hex)
        instructions = self.disassemble_bytecode(bytecode)
        
        print(f"Contract Bytecode: {bytecode_hex}")
        print(f"Length: {len(bytecode)} bytes")
        print(f"\nDisassembled Instructions:")
        
        for i, instr in enumerate(instructions[:10]):  # Show first 10 instructions
            data_str = f" {instr['data']}" if instr['data'] else ""
            print(f"  {i:2d}: {instr['name']}{data_str} ({instr['stack_effect']})")
        
        if len(instructions) > 10:
            print(f"  ... and {len(instructions) - 10} more instructions")

# Demo bytecode analysis
print("\n📜 EVM Bytecode and Opcodes Demo")
print("=" * 50)

analyzer = EVMBytecodeAnalyzer()

# Simple contract bytecode (stores 42 at storage slot 0)
simple_contract = "6042600055"  # PUSH1 42 PUSH1 00 SSTORE
analyzer.analyze_contract_bytecode(simple_contract)

# More complex example
print(f"\n" + "-" * 50)
complex_contract = "608060405234801561001057600080fd5b5060405161020e38038061020e"
analyzer.analyze_contract_bytecode(complex_contract)
```

## EVM Execution Model ⚙️

### Transaction Processing and State Changes

```python
class EVMExecutionEngine:
    def __init__(self):
        self.global_state = {}
        self.block_context = {
            'number': 18000000,
            'timestamp': 1692000000,
            'gas_limit': 30000000,
            'coinbase': '0x742d35Cc6635C0532925a3b8D8Cf97E'
        }
    
    def execute_transaction(self, tx: dict) -> dict:
        """Execute a transaction through the EVM"""
        print(f"⚙️ Executing Transaction")
        print(f"   From: {tx['from']}")
        print(f"   To: {tx.get('to', 'Contract Creation')}")
        print(f"   Value: {tx.get('value', 0)} Wei")
        print(f"   Gas Limit: {tx['gas_limit']:,}")
        
        # Initialize execution context
        context = {
            'caller': tx['from'],
            'origin': tx['from'],
            'gas_available': tx['gas_limit'],
            'gas_used': 0,
            'value': tx.get('value', 0),
            'data': tx.get('data', b''),
            'block': self.block_context
        }
        
        # Basic transaction validation
        if not self._validate_transaction(tx):
            return {'success': False, 'error': 'Invalid transaction'}
        
        # Execute transaction
        if tx.get('to'):
            # Call to existing account
            result = self._execute_call(tx, context)
        else:
            # Contract creation
            result = self._execute_creation(tx, context)
        
        # Update global state
        self._update_state(tx, result)
        
        return result
    
    def _validate_transaction(self, tx: dict) -> bool:
        """Basic transaction validation"""
        # Check sender has sufficient balance
        sender_account = self.global_state.get(tx['from'], {'balance': 0, 'nonce': 0})
        total_cost = tx.get('value', 0) + (tx['gas_limit'] * tx.get('gas_price', 0))
        
        if sender_account['balance'] < total_cost:
            return False
        
        # Check nonce ordering
        if tx.get('nonce', 0) != sender_account['nonce']:
            return False
        
        return True
    
    def _execute_call(self, tx: dict, context: dict) -> dict:
        """Execute call to existing account"""
        target = tx['to']
        target_account = self.global_state.get(target, {'balance': 0, 'code': b'', 'storage': {}})
        
        # Transfer value if specified
        if tx.get('value', 0) > 0:
            context['gas_used'] += 9000  # Value transfer cost
        
        # Execute code if contract
        if target_account.get('code'):
            code_result = self._execute_code(target_account['code'], context)
            context['gas_used'] += code_result['gas_used']
            
            if not code_result['success']:
                return {
                    'success': False,
                    'error': code_result['error'],
                    'gas_used': context['gas_used']
                }
        
        return {
            'success': True,
            'gas_used': context['gas_used'],
            'return_data': b'',
            'state_changes': []
        }
    
    def _execute_creation(self, tx: dict, context: dict) -> dict:
        """Execute contract creation"""
        # Generate contract address
        import hashlib
        creator_nonce = self.global_state.get(tx['from'], {'nonce': 0})['nonce']
        contract_data = f"{tx['from']}{creator_nonce}"
        contract_address = "0x" + hashlib.sha256(contract_data.encode()).hexdigest()[:40]
        
        context['gas_used'] += 32000  # Contract creation cost
        
        # Execute constructor code
        constructor_code = tx.get('data', b'')
        if constructor_code:
            code_result = self._execute_code(constructor_code, context)
            context['gas_used'] += code_result['gas_used']
            
            if code_result['success']:
                # Store deployed code
                self.global_state[contract_address] = {
                    'balance': tx.get('value', 0),
                    'code': code_result.get('return_data', b''),
                    'storage': {},
                    'nonce': 1
                }
            else:
                return {
                    'success': False,
                    'error': code_result['error'],
                    'gas_used': context['gas_used']
                }
        
        return {
            'success': True,
            'contract_address': contract_address,
            'gas_used': context['gas_used'],
            'state_changes': [f"Created contract at {contract_address}"]
        }
    
    def _execute_code(self, code: bytes, context: dict) -> dict:
        """Execute EVM bytecode"""
        # Simplified execution - in reality much more complex
        if len(code) == 0:
            return {'success': True, 'gas_used': 0, 'return_data': b''}
        
        # Estimate gas based on code complexity
        gas_per_byte = 200  # Simplified
        estimated_gas = len(code) * gas_per_byte
        
        if estimated_gas > context['gas_available']:
            return {
                'success': False,
                'error': 'Out of gas',
                'gas_used': context['gas_available']
            }
        
        return {
            'success': True,
            'gas_used': estimated_gas,
            'return_data': b'success'
        }
    
    def _update_state(self, tx: dict, result: dict):
        """Update global state after transaction execution"""
        # Update sender nonce and balance
        sender = self.global_state.get(tx['from'], {'balance': 0, 'nonce': 0})
        sender['nonce'] += 1
        sender['balance'] -= result['gas_used'] * tx.get('gas_price', 0)
        self.global_state[tx['from']] = sender
        
        # Transfer value if successful
        if result['success'] and tx.get('value', 0) > 0 and tx.get('to'):
            recipient = self.global_state.get(tx['to'], {'balance': 0, 'nonce': 0})
            recipient['balance'] += tx['value']
            self.global_state[tx['to']] = recipient
            sender['balance'] -= tx['value']

# Demo EVM execution
print("\n⚙️ EVM Execution Model Demo")
print("=" * 50)

evm_engine = EVMExecutionEngine()

# Initialize some accounts
evm_engine.global_state = {
    '0x742d35Cc6635C0532925a3b8D8Cf97E': {
        'balance': 5000000000000000000,  # 5 ETH
        'nonce': 0,
        'code': b'',
        'storage': {}
    }
}

# Example 1: Simple ETH transfer
print("Example 1: ETH Transfer")
eth_transfer_tx = {
    'from': '0x742d35Cc6635C0532925a3b8D8Cf97E',
    'to': '0x8ba1f109551bD432803012645Hac136c',
    'value': 1000000000000000000,  # 1 ETH
    'gas_limit': 21000,
    'gas_price': 20000000000,  # 20 Gwei
    'nonce': 0
}

result = evm_engine.execute_transaction(eth_transfer_tx)
print(f"Result: {result}")

# Example 2: Contract creation
print(f"\nExample 2: Contract Creation")
contract_creation_tx = {
    'from': '0x742d35Cc6635C0532925a3b8D8Cf97E',
    'to': None,  # Contract creation
    'value': 0,
    'data': bytes.fromhex('6042600055'),  # Simple storage contract
    'gas_limit': 100000,
    'gas_price': 20000000000,
    'nonce': 1
}

result = evm_engine.execute_transaction(contract_creation_tx)
print(f"Result: {result}")
```

## EVM State Management 🗃️

### World State and Merkle Patricia Trees

```python
class EVMStateManager:
    def __init__(self):
        self.accounts = {}
        self.state_root = "0x" + "0" * 64  # 256-bit root hash
    
    def create_account(self, address: str, account_type: str = 'EOA'):
        """Create new account with initial state"""
        self.accounts[address] = {
            'balance': 0,
            'nonce': 0,
            'code_hash': '0x' + '0' * 64,
            'storage_root': '0x' + '0' * 64,
            'account_type': account_type,
            'storage': {} if account_type == 'contract' else None
        }
    
    def update_balance(self, address: str, amount: int):
        """Update account balance"""
        if address in self.accounts:
            self.accounts[address]['balance'] += amount
            self._update_state_root()
    
    def set_contract_code(self, address: str, code: bytes):
        """Set contract code and update code hash"""
        if address in self.accounts:
            import hashlib
            code_hash = hashlib.sha256(code).hexdigest()
            self.accounts[address]['code_hash'] = f"0x{code_hash}"
            self.accounts[address]['code'] = code
            self._update_state_root()
    
    def update_storage(self, address: str, key: int, value: int):
        """Update contract storage"""
        if address in self.accounts and self.accounts[address]['storage'] is not None:
            self.accounts[address]['storage'][key] = value
            self._update_storage_root(address)
            self._update_state_root()
    
    def _update_storage_root(self, address: str):
        """Update storage root for contract"""
        import hashlib
        storage = self.accounts[address]['storage']
        storage_data = str(sorted(storage.items())).encode()
        storage_root = hashlib.sha256(storage_data).hexdigest()
        self.accounts[address]['storage_root'] = f"0x{storage_root}"
    
    def _update_state_root(self):
        """Update global state root"""
        import hashlib
        state_data = str(sorted(self.accounts.items())).encode()
        self.state_root = "0x" + hashlib.sha256(state_data).hexdigest()
    
    def get_account_state(self, address: str) -> dict:
        """Get complete account state"""
        return self.accounts.get(address, {})
    
    def demonstrate_state_transitions(self):
        """Show how state changes with transactions"""
        print("🗃️ EVM State Management Demo")
        print("=" * 50)
        
        print("Initial State Root:", self.state_root)
        
        # Create accounts
        print("\n1. Creating accounts...")
        self.create_account("0x742d35Cc6635C0532925a3b8D8Cf97E", "EOA")
        self.create_account("0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", "contract")
        print("State Root after account creation:", self.state_root)
        
        # Update balances
        print("\n2. Updating balances...")
        self.update_balance("0x742d35Cc6635C0532925a3b8D8Cf97E", 5000000000000000000)
        print("State Root after balance update:", self.state_root)
        
        # Deploy contract code
        print("\n3. Deploying contract code...")
        contract_code = bytes.fromhex("6080604052348015600f57600080fd5b50")
        self.set_contract_code("0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", contract_code)
        print("State Root after code deployment:", self.state_root)
        
        # Update contract storage
        print("\n4. Updating contract storage...")
        self.update_storage("0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", 0, 42)
        self.update_storage("0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", 1, 123)
        print("State Root after storage update:", self.state_root)
        
        # Show final account states
        print("\n5. Final Account States:")
        for address, account in self.accounts.items():
            print(f"\n  Address: {address}")
            print(f"    Type: {account['account_type']}")
            print(f"    Balance: {account['balance']} Wei")
            print(f"    Nonce: {account['nonce']}")
            print(f"    Code Hash: {account['code_hash'][:10]}...")
            print(f"    Storage Root: {account['storage_root'][:10]}...")
            if account.get('storage'):
                print(f"    Storage: {account['storage']}")

# Demo state management
state_manager = EVMStateManager()
state_manager.demonstrate_state_transitions()
```

## EVM Precompiled Contracts 🔧

### Built-in Cryptographic Functions

```python
class EVMPrecompiles:
    """EVM precompiled contracts for cryptographic operations"""
    
    def __init__(self):
        self.precompiles = {
            0x01: self.ecrecover,
            0x02: self.sha256hash,
            0x03: self.ripemd160hash,
            0x04: self.identity,
            0x05: self.modexp,
            0x06: self.ecadd,
            0x07: self.ecmul,
            0x08: self.ecpairing
        }
    
    def call_precompile(self, address: int, input_data: bytes) -> dict:
        """Call a precompiled contract"""
        if address in self.precompiles:
            try:
                result = self.precompiles[address](input_data)
                return {
                    'success': True,
                    'output': result['output'],
                    'gas_used': result['gas_used']
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e),
                    'gas_used': 0
                }
        else:
            return {
                'success': False,
                'error': 'Precompile not found',
                'gas_used': 0
            }
    
    def ecrecover(self, input_data: bytes) -> dict:
        """Elliptic curve signature recovery"""
        # Simplified implementation
        if len(input_data) < 128:
            raise ValueError("Invalid input length")
        
        # In real implementation, this would:
        # 1. Extract hash, v, r, s from input
        # 2. Recover public key from signature
        # 3. Return Ethereum address
        
        return {
            'output': b'0x742d35Cc6635C0532925a3b8D8Cf97E123456789',
            'gas_used': 3000
        }
    
    def sha256hash(self, input_data: bytes) -> dict:
        """SHA-256 hash function"""
        import hashlib
        hash_result = hashlib.sha256(input_data).digest()
        
        # Gas cost: 60 + 12 per word of input
        gas_cost = 60 + (len(input_data) + 31) // 32 * 12
        
        return {
            'output': hash_result,
            'gas_used': gas_cost
        }
    
    def ripemd160hash(self, input_data: bytes) -> dict:
        """RIPEMD-160 hash function"""
        # Simplified - would use actual RIPEMD-160
        import hashlib
        hash_result = hashlib.sha1(input_data).digest()[:20]
        
        gas_cost = 600 + (len(input_data) + 31) // 32 * 120
        
        return {
            'output': hash_result,
            'gas_used': gas_cost
        }
    
    def identity(self, input_data: bytes) -> dict:
        """Identity function (returns input unchanged)"""
        gas_cost = 15 + (len(input_data) + 31) // 32 * 3
        
        return {
            'output': input_data,
            'gas_used': gas_cost
        }
    
    def modexp(self, input_data: bytes) -> dict:
        """Modular exponentiation"""
        # Simplified implementation
        if len(input_data) < 96:
            raise ValueError("Invalid input length")
        
        # Extract base_len, exp_len, mod_len from first 96 bytes
        # Then extract base, exponent, modulus
        
        # Simulate complex calculation
        result = b'\x00' * 32  # Placeholder result
        gas_cost = 200  # Simplified gas calculation
        
        return {
            'output': result,
            'gas_used': gas_cost
        }
    
    def ecadd(self, input_data: bytes) -> dict:
        """Elliptic curve point addition"""
        # For BN254 curve used in zk-SNARKs
        if len(input_data) != 128:
            raise ValueError("Invalid input length")
        
        # Simulate elliptic curve addition
        result = b'\x00' * 64  # (x, y) coordinates
        
        return {
            'output': result,
            'gas_used': 150
        }
    
    def ecmul(self, input_data: bytes) -> dict:
        """Elliptic curve scalar multiplication"""
        if len(input_data) != 96:
            raise ValueError("Invalid input length")
        
        result = b'\x00' * 64  # (x, y) coordinates
        
        return {
            'output': result,
            'gas_used': 6000
        }
    
    def ecpairing(self, input_data: bytes) -> dict:
        """Elliptic curve pairing check"""
        if len(input_data) % 192 != 0:
            raise ValueError("Invalid input length")
        
        pairs = len(input_data) // 192
        gas_cost = 45000 + pairs * 34000
        
        # Return 1 for valid pairing, 0 for invalid
        result = b'\x00' * 31 + b'\x01'
        
        return {
            'output': result,
            'gas_used': gas_cost
        }
    
    def demonstrate_precompiles(self):
        """Demo precompiled contract usage"""
        print("🔧 EVM Precompiled Contracts Demo")
        print("=" * 50)
        
        test_cases = [
            (0x01, b'test_signature_data' + b'\x00' * 110, "ECRECOVER"),
            (0x02, b'hello world', "SHA256"),
            (0x03, b'hello world', "RIPEMD160"),
            (0x04, b'identity test', "IDENTITY"),
            (0x05, b'\x01' * 96, "MODEXP")
        ]
        
        for address, input_data, name in test_cases:
            print(f"\n{name} (0x{address:02x}):")
            result = self.call_precompile(address, input_data)
            print(f"  Success: {result['success']}")
            if result['success']:
                print(f"  Gas Used: {result['gas_used']:,}")
                print(f"  Output: {result['output'][:20].hex()}...")
            else:
                print(f"  Error: {result['error']}")

# Demo precompiles
precompiles = EVMPrecompiles()
precompiles.demonstrate_precompiles()
```

## EVM Debugging and Analysis Tools 🔍

### Tools for EVM Development

```python
class EVMDebugger:
    def __init__(self):
        self.trace = []
        self.gas_tracker = {}
        
    def trace_execution(self, bytecode: bytes, initial_stack: list = None):
        """Trace EVM execution step by step"""
        print("🔍 EVM Execution Trace")
        print("=" * 50)
        
        stack = initial_stack or []
        memory = bytearray()
        storage = {}
        pc = 0
        gas_used = 0
        
        print(f"Initial State:")
        print(f"  Stack: {stack}")
        print(f"  PC: {pc}")
        print(f"  Gas Used: {gas_used}")
        
        step = 0
        while pc < len(bytecode) and step < 10:  # Limit steps for demo
            opcode = bytecode[pc]
            
            print(f"\nStep {step}:")
            print(f"  PC: {pc}, Opcode: 0x{opcode:02x}")
            
            if opcode == 0x60:  # PUSH1
                if pc + 1 < len(bytecode):
                    value = bytecode[pc + 1]
                    stack.append(value)
                    pc += 2
                    gas_used += 3
                    print(f"  PUSH1 {value} → Stack: {stack}")
                else:
                    break
                    
            elif opcode == 0x01:  # ADD
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    result = a + b
                    stack.append(result)
                    gas_used += 3
                    print(f"  ADD {a} + {b} = {result} → Stack: {stack}")
                else:
                    print(f"  ADD failed: insufficient stack")
                    break
                pc += 1
                
            elif opcode == 0x55:  # SSTORE
                if len(stack) >= 2:
                    key = stack.pop()
                    value = stack.pop()
                    storage[key] = value
                    gas_used += 20000
                    print(f"  SSTORE key={key}, value={value} → Storage: {storage}")
                else:
                    print(f"  SSTORE failed: insufficient stack")
                    break
                pc += 1
                
            else:
                print(f"  Unknown opcode: 0x{opcode:02x}")
                break
                
            print(f"  Gas Used: {gas_used}")
            step += 1
        
        return {
            'final_stack': stack,
            'final_storage': storage,
            'gas_used': gas_used,
            'steps': step
        }
    
    def analyze_gas_usage(self, contract_calls: list):
        """Analyze gas usage patterns"""
        print("\n🔍 Gas Usage Analysis")
        print("=" * 50)
        
        total_gas = 0
        operation_counts = {}
        
        for call in contract_calls:
            operations = call.get('operations', [])
            gas = call.get('gas_used', 0)
            total_gas += gas
            
            print(f"\nContract Call:")
            print(f"  Function: {call.get('function', 'unknown')}")
            print(f"  Gas Used: {gas:,}")
            print(f"  Operations: {operations}")
            
            for op in operations:
                operation_counts[op] = operation_counts.get(op, 0) + 1
        
        print(f"\nOverall Analysis:")
        print(f"  Total Calls: {len(contract_calls)}")
        print(f"  Total Gas: {total_gas:,}")
        print(f"  Average Gas/Call: {total_gas // len(contract_calls):,}")
        
        print(f"\nOperation Frequency:")
        for op, count in sorted(operation_counts.items()):
            print(f"  {op}: {count} times")
    
    def suggest_optimizations(self, storage_operations: list):
        """Suggest gas optimizations"""
        print("\n🔍 Optimization Suggestions")
        print("=" * 50)
        
        sstore_count = storage_operations.count('SSTORE')
        sload_count = storage_operations.count('SLOAD')
        
        suggestions = []
        
        if sstore_count > 3:
            suggestions.append("Consider packing multiple values into single storage slot")
        
        if sload_count > 5:
            suggestions.append("Cache frequently read storage values in memory")
        
        if 'SSTORE' in storage_operations and 'SLOAD' in storage_operations:
            suggestions.append("Use events for data that doesn't need to be read by contracts")
        
        if len(suggestions) == 0:
            suggestions.append("Code appears to be well-optimized!")
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")

# Demo debugging tools
debugger = EVMDebugger()

# Example 1: Trace simple bytecode execution
print("Example 1: Bytecode Execution Trace")
simple_bytecode = bytes([0x60, 0x2A, 0x60, 0x00, 0x55])  # PUSH1 42, PUSH1 0, SSTORE
result = debugger.trace_execution(simple_bytecode)

# Example 2: Gas analysis
print("\nExample 2: Gas Usage Analysis")
contract_calls = [
    {'function': 'transfer', 'gas_used': 51000, 'operations': ['SLOAD', 'SSTORE', 'SSTORE']},
    {'function': 'approve', 'gas_used': 46000, 'operations': ['SSTORE']},
    {'function': 'mint', 'gas_used': 71000, 'operations': ['SLOAD', 'SSTORE', 'SSTORE', 'CALL']}
]
debugger.analyze_gas_usage(contract_calls)

# Example 3: Optimization suggestions
storage_ops = ['SLOAD', 'SLOAD', 'SLOAD', 'SSTORE', 'SSTORE', 'SSTORE', 'SSTORE']
debugger.suggest_optimizations(storage_ops)
```

## EVM Compatibility and Variations 🔄

### EVM-Compatible Blockchains

```python
class EVMCompatibility:
    def __init__(self):
        self.evm_chains = {
            'Ethereum': {
                'gas_limit': 30_000_000,
                'block_time': 12,
                'consensus': 'Proof of Stake',
                'features': ['Full EVM', 'All opcodes', 'All precompiles']
            },
            'Polygon': {
                'gas_limit': 30_000_000,
                'block_time': 2,
                'consensus': 'Proof of Stake',
                'features': ['Full EVM', 'Lower gas costs', 'Faster finality']
            },
            'BSC': {
                'gas_limit': 140_000_000,
                'block_time': 3,
                'consensus': 'Proof of Stake Authority',
                'features': ['Full EVM', 'Higher throughput', 'Centralized validators']
            },
            'Arbitrum': {
                'gas_limit': 32_000_000,
                'block_time': 0.25,
                'consensus': 'Optimistic Rollup',
                'features': ['Modified EVM', 'L2 scaling', 'Fraud proofs']
            },
            'Optimism': {
                'gas_limit': 15_000_000,
                'block_time': 2,
                'consensus': 'Optimistic Rollup',
                'features': ['Modified EVM', 'L2 scaling', 'Fault proofs']
            }
        }
    
    def compare_evm_chains(self):
        """Compare different EVM-compatible chains"""
        print("🔄 EVM-Compatible Blockchain Comparison")
        print("=" * 70)
        
        print(f"{'Chain':<12} {'Gas Limit':<12} {'Block Time':<12} {'Consensus':<20}")
        print("-" * 70)
        
        for chain, specs in self.evm_chains.items():
            print(f"{chain:<12} {specs['gas_limit']:,<12} {specs['block_time']:<12}s {specs['consensus']:<20}")
        
        print(f"\nKey Features by Chain:")
        for chain, specs in self.evm_chains.items():
            print(f"\n{chain}:")
            for feature in specs['features']:
                print(f"  • {feature}")
    
    def deployment_considerations(self):
        """Show deployment considerations across chains"""
        print("\n🔄 Multi-Chain Deployment Considerations")
        print("=" * 50)
        
        considerations = {
            'Gas Costs': {
                'Ethereum': 'Highest ($10-100+ per transaction)',
                'Polygon': 'Very low ($0.01-0.10 per transaction)',
                'BSC': 'Low ($0.10-1.00 per transaction)',
                'Arbitrum': 'Medium ($1-5 per transaction)',
                'Optimism': 'Medium ($1-5 per transaction)'
            },
            'Security': {
                'Ethereum': 'Highest (most decentralized)',
                'Polygon': 'High (shared security with Ethereum)',
                'BSC': 'Medium (fewer validators)',
                'Arbitrum': 'High (inherits Ethereum security)',
                'Optimism': 'High (inherits Ethereum security)'
            },
            'Transaction Speed': {
                'Ethereum': '12 seconds (1-5 minutes for finality)',
                'Polygon': '2 seconds (few seconds finality)',
                'BSC': '3 seconds (15 blocks finality)',
                'Arbitrum': '0.25 seconds (immediate)',
                'Optimism': '2 seconds (immediate)'
            }
        }
        
        for category, chains in considerations.items():
            print(f"\n{category}:")
            for chain, details in chains.items():
                print(f"  {chain:<12}: {details}")

# Demo EVM compatibility
compatibility = EVMCompatibility()
compatibility.compare_evm_chains()
compatibility.deployment_considerations()
```

## Summary and Next Steps 🎯

### Key EVM Concepts Mastered

1. **Architecture**: Stack-based 256-bit virtual machine with deterministic execution
2. **Memory Model**: Stack (volatile), Memory (volatile), Storage (persistent)
3. **Bytecode**: Low-level opcodes that compile from high-level languages like Solidity
4. **Execution**: Transaction processing, state transitions, and gas metering
5. **Precompiles**: Built-in cryptographic functions for efficiency
6. **State Management**: Merkle Patricia Trees and global world state
7. **Debugging**: Tools and techniques for analyzing EVM execution
8. **Compatibility**: EVM variations across different blockchain networks

### Practical Applications

- **Smart Contract Development**: Understanding gas optimization and execution limits
- **Security Auditing**: Analyzing bytecode and execution patterns
- **DApp Performance**: Optimizing contract interactions and state management
- **Cross-Chain Development**: Deploying on multiple EVM-compatible networks
- **Protocol Design**: Building on top of EVM primitives

### Advanced Topics to Explore

- **EVM Assembly Programming**: Writing contracts directly in opcodes
- **Formal Verification**: Mathematical proofs of contract correctness
- **EVM Modifications**: Layer 2 implementations and custom EVMs
- **MEV (Maximal Extractable Value)**: Understanding execution ordering
- **EVM Equivalent vs Compatible**: Technical differences in implementations

### Next Steps
- Study [Ethereum 2.0](ethereum-2.md) and the transition to Proof of Stake
- Dive into [Smart Contracts](../04-smart-contracts/solidity-basics.md) development
- Practice with [Hands-on Projects](../08-projects/) using EVM concepts
- Explore [Advanced Topics](../09-advanced-topics/) like Layer 2 solutions

---

**🖥️ The EVM is the beating heart of Ethereum - mastering its internals unlocks the full potential of smart contract development and gives you the knowledge to build secure, efficient, and innovative decentralized applications.**