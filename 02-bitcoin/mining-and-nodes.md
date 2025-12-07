# Bitcoin Mining and Nodes ⛏️

## Introduction

Bitcoin mining and node operations are the backbone of the Bitcoin network. Miners secure the network through Proof of Work, while nodes validate transactions and maintain the blockchain. Understanding these processes is crucial to comprehending how Bitcoin maintains its decentralized, trustless nature.

## Bitcoin Mining Fundamentals ⚙️

### What is Bitcoin Mining?

Bitcoin mining is the process of:
- **Collecting transactions** from the mempool
- **Creating a block** with these transactions  
- **Finding a valid nonce** that makes the block hash meet the difficulty target
- **Broadcasting the block** to the network for validation
- **Earning rewards** (block reward + transaction fees)

### The Mining Process

```python
import hashlib
import time
import json
from typing import Dict, List

class BitcoinMiner:
    def __init__(self, name: str, hash_rate: float):
        self.name = name
        self.hash_rate = hash_rate  # Hashes per second
        self.blocks_mined = 0
        self.total_earnings = 0
        self.mining_pool = None
    
    def create_block_header(self, transactions: List[str], prev_block_hash: str, target_bits: int) -> dict:
        """Create block header for mining"""
        # Calculate Merkle root from transactions
        merkle_root = self.calculate_merkle_root(transactions)
        
        header = {
            'version': 0x20000000,  # Version 2
            'previous_hash': prev_block_hash,
            'merkle_root': merkle_root,
            'timestamp': int(time.time()),
            'bits': target_bits,  # Difficulty target
            'nonce': 0
        }
        
        return header
    
    def calculate_merkle_root(self, transactions: List[str]) -> str:
        """Simplified Merkle root calculation"""
        if not transactions:
            return '0' * 64
        
        # Hash all transactions
        tx_hashes = [hashlib.sha256(tx.encode()).hexdigest() for tx in transactions]
        
        # Build Merkle tree
        while len(tx_hashes) > 1:
            next_level = []
            for i in range(0, len(tx_hashes), 2):
                left = tx_hashes[i]
                right = tx_hashes[i + 1] if i + 1 < len(tx_hashes) else tx_hashes[i]
                combined = left + right
                parent_hash = hashlib.sha256(combined.encode()).hexdigest()
                next_level.append(parent_hash)
            tx_hashes = next_level
        
        return tx_hashes[0]
    
    def hash_block_header(self, header: dict) -> str:
        """Calculate double SHA-256 hash of block header"""
        header_string = json.dumps(header, sort_keys=True)
        hash1 = hashlib.sha256(header_string.encode()).digest()
        hash2 = hashlib.sha256(hash1).digest()
        return hash2.hex()
    
    def mine_block(self, transactions: List[str], prev_block_hash: str, difficulty_bits: int, max_attempts: int = 1000000) -> dict:
        """Mine a block by finding valid nonce"""
        header = self.create_block_header(transactions, prev_block_hash, difficulty_bits)
        target = 2 ** (256 - difficulty_bits)
        
        print(f"🔨 {self.name} mining block...")
        print(f"   Transactions: {len(transactions)}")
        print(f"   Difficulty: {difficulty_bits} bits")
        print(f"   Target: {target:064x}"[:32] + "...")
        
        start_time = time.time()
        
        for nonce in range(max_attempts):
            header['nonce'] = nonce
            block_hash = self.hash_block_header(header)
            
            if int(block_hash, 16) < target:
                # Found valid block!
                mining_time = time.time() - start_time
                hash_rate_achieved = nonce / mining_time if mining_time > 0 else 0
                
                block_reward = 6.25  # Current Bitcoin reward
                tx_fees = len(transactions) * 0.0001  # Simplified fee calculation
                total_reward = block_reward + tx_fees
                
                self.blocks_mined += 1
                self.total_earnings += total_reward
                
                return {
                    'success': True,
                    'block_hash': block_hash,
                    'nonce': nonce,
                    'mining_time': mining_time,
                    'hash_rate_achieved': hash_rate_achieved,
                    'reward': total_reward,
                    'header': header
                }
        
        return {
            'success': False,
            'attempts': max_attempts,
            'message': 'Max attempts reached without finding valid block'
        }

# Demo mining process
print("⛏️ Bitcoin Mining Process Demo")
print("=" * 50)

# Create a miner
alice_miner = BitcoinMiner("Alice's Mining Rig", 110e12)  # 110 TH/s

# Sample transactions in mempool
sample_transactions = [
    "coinbase: 6.25 BTC to Alice",  # Coinbase transaction
    "Bob sends 2.5 BTC to Carol",
    "Dave sends 1.0 BTC to Eve",
    "Frank sends 0.5 BTC to Grace"
]

# Previous block hash (simplified)
prev_hash = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"

# Mine a block with easy difficulty for demo
result = alice_miner.mine_block(sample_transactions, prev_hash, 20)  # Easy difficulty

if result['success']:
    print(f"✅ Block mined successfully!")
    print(f"   Block hash: {result['block_hash']}")
    print(f"   Nonce found: {result['nonce']:,}")
    print(f"   Mining time: {result['mining_time']:.2f} seconds")
    print(f"   Hash rate: {result['hash_rate_achieved']/1e6:.2f} MH/s")
    print(f"   Reward earned: {result['reward']} BTC")
else:
    print(f"❌ Mining failed: {result['message']}")
```

## Mining Hardware Evolution 🖥️

### Mining Hardware Generations

```python
def show_mining_hardware_evolution():
    """Display evolution of Bitcoin mining hardware"""
    
    print("\n🖥️ Bitcoin Mining Hardware Evolution")
    print("=" * 50)
    
    hardware_eras = {
        'CPU Era (2009-2010)': {
            'hardware': 'Desktop processors',
            'hash_rate': '1-10 MH/s',
            'efficiency': '~1000 J/GH',
            'cost': '$500-2000',
            'description': 'Early Bitcoin mining on regular computers'
        },
        'GPU Era (2010-2013)': {
            'hardware': 'Graphics cards',
            'hash_rate': '100-800 MH/s', 
            'efficiency': '~5 J/GH',
            'cost': '$200-600',
            'description': 'Gaming GPUs repurposed for Bitcoin mining'
        },
        'FPGA Era (2012-2013)': {
            'hardware': 'Field-Programmable Gate Arrays',
            'hash_rate': '800 MH/s - 25 GH/s',
            'efficiency': '~20 J/GH',
            'cost': '$500-15000',
            'description': 'Custom programmable chips for mining'
        },
        'ASIC Era (2013-Present)': {
            'hardware': 'Application-Specific Integrated Circuits',
            'hash_rate': '1 TH/s - 200+ TH/s',
            'efficiency': '30-20 J/TH',
            'cost': '$1000-8000',
            'description': 'Purpose-built mining chips'
        }
    }
    
    for era, specs in hardware_eras.items():
        print(f"\n{era}:")
        print(f"  Hardware: {specs['hardware']}")
        print(f"  Hash Rate: {specs['hash_rate']}")
        print(f"  Efficiency: {specs['efficiency']}")
        print(f"  Cost: {specs['cost']}")
        print(f"  Description: {specs['description']}")

show_mining_hardware_evolution()
```

### Modern Mining Operations

```python
class MiningFarm:
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.miners = []
        self.electricity_cost_per_kwh = 0.05  # $0.05 per kWh
        
    def add_miner(self, model: str, hash_rate: float, power_watts: int, cost: float):
        """Add mining hardware to farm"""
        miner = {
            'model': model,
            'hash_rate': hash_rate,  # TH/s
            'power_consumption': power_watts,
            'purchase_cost': cost,
            'efficiency': power_watts / hash_rate  # W/TH
        }
        self.miners.append(miner)
        
    def calculate_daily_metrics(self, btc_price: float, network_hash_rate: float, block_reward: float) -> dict:
        """Calculate daily mining metrics"""
        total_hash_rate = sum(m['hash_rate'] for m in self.miners) * 1e12  # Convert TH/s to H/s
        total_power = sum(m['power_consumption'] for m in self.miners)  # Watts
        
        # Daily block rewards (assuming pool mining)
        network_hash_rate_hs = network_hash_rate * 1e18  # EH/s to H/s
        hash_rate_share = total_hash_rate / network_hash_rate_hs
        blocks_per_day = 144  # 6 blocks/hour * 24 hours
        daily_btc_earned = hash_rate_share * blocks_per_day * block_reward
        
        # Daily costs
        daily_power_kwh = (total_power * 24) / 1000  # Convert Wh to kWh
        daily_electricity_cost = daily_power_kwh * self.electricity_cost_per_kwh
        
        # Profitability
        daily_revenue = daily_btc_earned * btc_price
        daily_profit = daily_revenue - daily_electricity_cost
        
        return {
            'total_hash_rate_th': total_hash_rate / 1e12,
            'total_power_kw': total_power / 1000,
            'daily_btc_earned': daily_btc_earned,
            'daily_revenue_usd': daily_revenue,
            'daily_electricity_cost_usd': daily_electricity_cost,
            'daily_profit_usd': daily_profit,
            'profit_margin_percent': (daily_profit / daily_revenue * 100) if daily_revenue > 0 else 0,
            'break_even_btc_price': daily_electricity_cost / daily_btc_earned if daily_btc_earned > 0 else float('inf')
        }
    
    def get_farm_stats(self):
        """Get overall farm statistics"""
        if not self.miners:
            return {}
            
        total_hash_rate = sum(m['hash_rate'] for m in self.miners)
        total_power = sum(m['power_consumption'] for m in self.miners)
        total_cost = sum(m['purchase_cost'] for m in self.miners)
        avg_efficiency = total_power / total_hash_rate
        
        return {
            'miner_count': len(self.miners),
            'total_hash_rate_th': total_hash_rate,
            'total_power_kw': total_power / 1000,
            'total_hardware_cost_usd': total_cost,
            'average_efficiency_w_per_th': avg_efficiency,
            'location': self.location,
            'electricity_cost_per_kwh': self.electricity_cost_per_kwh
        }

# Demo mining farm
print("\n🏭 Modern Mining Farm Demo")
print("=" * 50)

# Create mining farm
texas_farm = MiningFarm("Texas Mining Co", "Texas, USA")

# Add various miners (based on real hardware specs)
miners_inventory = [
    ('Antminer S19 Pro', 110, 3250, 5000),    # 110 TH/s, 3250W, $5000
    ('Antminer S19j Pro', 104, 3068, 4500),   # 104 TH/s, 3068W, $4500
    ('Whatsminer M30S++', 112, 3472, 5200),   # 112 TH/s, 3472W, $5200
]

# Deploy 100 miners of each type
for model, hash_rate, power, cost in miners_inventory:
    for _ in range(100):
        texas_farm.add_miner(model, hash_rate, power, cost)

# Calculate metrics with current market conditions (example values)
btc_price = 45000        # $45,000 per BTC
network_hash_rate = 400  # 400 EH/s
block_reward = 6.25      # 6.25 BTC per block

farm_stats = texas_farm.get_farm_stats()
daily_metrics = texas_farm.calculate_daily_metrics(btc_price, network_hash_rate, block_reward)

print(f"Farm: {texas_farm.name}")
print(f"Location: {farm_stats['location']}")
print(f"Hardware: {farm_stats['miner_count']} miners")
print(f"Total Hash Rate: {farm_stats['total_hash_rate_th']:,.0f} TH/s")
print(f"Total Power: {farm_stats['total_power_kw']:,.0f} kW")
print(f"Hardware Investment: ${farm_stats['total_hardware_cost_usd']:,.0f}")

print(f"\nDaily Operations (BTC @ ${btc_price:,}):")
print(f"  BTC Earned: {daily_metrics['daily_btc_earned']:.8f}")
print(f"  Revenue: ${daily_metrics['daily_revenue_usd']:,.2f}")
print(f"  Electricity Cost: ${daily_metrics['daily_electricity_cost_usd']:,.2f}")
print(f"  Profit: ${daily_metrics['daily_profit_usd']:,.2f}")
print(f"  Profit Margin: {daily_metrics['profit_margin_percent']:.1f}%")
print(f"  Break-even BTC Price: ${daily_metrics['break_even_btc_price']:,.2f}")
```

## Bitcoin Nodes 🌐

### Types of Bitcoin Nodes

```python
class BitcoinNode:
    def __init__(self, node_type: str, has_full_blockchain: bool = True):
        self.node_type = node_type
        self.has_full_blockchain = has_full_blockchain
        self.peer_connections = []
        self.mempool = []  # Unconfirmed transactions
        self.blockchain_size_gb = 400  # Current blockchain size
        self.is_mining = False
        
    def validate_transaction(self, transaction: dict) -> bool:
        """Validate transaction against consensus rules"""
        validation_steps = [
            'Check transaction format',
            'Verify input signatures', 
            'Check input UTXOs exist',
            'Verify no double spending',
            'Check transaction fees',
            'Validate script execution'
        ]
        
        print(f"  Validating transaction {transaction.get('txid', 'unknown')[:8]}...")
        for step in validation_steps:
            print(f"    ✓ {step}")
        
        # Simplified validation (always pass for demo)
        return True
    
    def validate_block(self, block: dict) -> bool:
        """Validate block against consensus rules"""
        validation_steps = [
            'Check block header format',
            'Verify proof of work',
            'Check timestamp validity',
            'Validate Merkle root',
            'Check all transactions',
            'Verify block size limits',
            'Check coinbase transaction'
        ]
        
        print(f"  Validating block {block.get('hash', 'unknown')[:8]}...")
        for step in validation_steps:
            print(f"    ✓ {step}")
            
        # Validate each transaction in block
        for tx in block.get('transactions', []):
            if not self.validate_transaction(tx):
                return False
        
        return True
    
    def relay_transaction(self, transaction: dict):
        """Relay valid transaction to peers"""
        if self.validate_transaction(transaction):
            self.mempool.append(transaction)
            print(f"  Transaction added to mempool and relayed to {len(self.peer_connections)} peers")
    
    def get_node_info(self) -> dict:
        """Get node information"""
        return {
            'type': self.node_type,
            'full_blockchain': self.has_full_blockchain,
            'blockchain_size_gb': self.blockchain_size_gb if self.has_full_blockchain else 0,
            'mempool_size': len(self.mempool),
            'peer_connections': len(self.peer_connections),
            'is_mining': self.is_mining
        }

# Demo different node types
print("\n🌐 Bitcoin Node Types Demo")
print("=" * 50)

node_types = {
    'Full Node': {
        'description': 'Stores complete blockchain, validates all transactions',
        'storage': '400+ GB',
        'bandwidth': 'High (uploading blocks to peers)',
        'security': 'Highest (independent verification)',
        'use_case': 'Merchants, privacy-conscious users, developers'
    },
    'Pruned Node': {
        'description': 'Validates all transactions, keeps recent blocks only',
        'storage': '5-10 GB',
        'bandwidth': 'Medium (downloads full chain initially)',
        'security': 'High (full validation)',
        'use_case': 'Resource-constrained full validation'
    },
    'SPV Node (Light Client)': {
        'description': 'Downloads block headers only, trusts miners',
        'storage': '<100 MB',
        'bandwidth': 'Low (headers and relevant transactions)',
        'security': 'Medium (relies on network majority)',
        'use_case': 'Mobile wallets, quick sync'
    },
    'Mining Node': {
        'description': 'Full node that also mines new blocks',
        'storage': '400+ GB',
        'bandwidth': 'Very High (broadcasting new blocks)',
        'security': 'Highest (secures network)',
        'use_case': 'Professional miners, mining pools'
    }
}

for node_type, details in node_types.items():
    print(f"\n{node_type}:")
    print(f"  Description: {details['description']}")
    print(f"  Storage: {details['storage']}")
    print(f"  Bandwidth: {details['bandwidth']}")
    print(f"  Security: {details['security']}")
    print(f"  Use Case: {details['use_case']}")

# Create example nodes
full_node = BitcoinNode("Full Node", True)
light_node = BitcoinNode("SPV Node", False)
light_node.blockchain_size_gb = 0.1

print(f"\nNode Comparison:")
nodes = [full_node, light_node]
for node in nodes:
    info = node.get_node_info()
    print(f"  {info['type']}: {info['blockchain_size_gb']} GB storage, {info['peer_connections']} peers")
```

## Mining Pools 🏊‍♀️

### Pool Mining Economics

```python
class MiningPool:
    def __init__(self, name: str, fee_percentage: float):
        self.name = name
        self.fee_percentage = fee_percentage
        self.miners = {}
        self.total_hash_rate = 0
        self.blocks_found = 0
        self.payout_method = "PPLNS"  # Pay Per Last N Shares
        
    def add_miner(self, miner_id: str, hash_rate: float):
        """Add miner to pool"""
        self.miners[miner_id] = {
            'hash_rate': hash_rate,
            'shares_submitted': 0,
            'blocks_found': 0,
            'total_earnings': 0
        }
        self.total_hash_rate += hash_rate
        
    def find_block(self, block_reward: float, tx_fees: float):
        """Simulate finding a block and distribute rewards"""
        total_reward = block_reward + tx_fees
        pool_fee = total_reward * self.fee_percentage
        distributable_reward = total_reward - pool_fee
        
        self.blocks_found += 1
        
        print(f"\n🎉 {self.name} found block #{self.blocks_found}!")
        print(f"   Total Reward: {total_reward:.8f} BTC")
        print(f"   Pool Fee ({self.fee_percentage*100}%): {pool_fee:.8f} BTC")
        print(f"   Distributed: {distributable_reward:.8f} BTC")
        print(f"   Payout Method: {self.payout_method}")
        
        # Distribute rewards based on hash rate contribution
        for miner_id, miner_data in self.miners.items():
            contribution_ratio = miner_data['hash_rate'] / self.total_hash_rate
            payout = distributable_reward * contribution_ratio
            miner_data['total_earnings'] += payout
            
            print(f"   {miner_id}: {contribution_ratio*100:.2f}% → {payout:.8f} BTC")
    
    def get_pool_stats(self):
        """Get pool statistics"""
        return {
            'name': self.name,
            'total_hash_rate_th': self.total_hash_rate / 1e12,
            'miner_count': len(self.miners),
            'blocks_found': self.blocks_found,
            'pool_fee_percent': self.fee_percentage * 100,
            'payout_method': self.payout_method
        }

# Demo mining pool
print("\n🏊‍♀️ Mining Pool Demo")
print("=" * 50)

# Create mining pool
pool = MiningPool("BTC Mining Pool", 0.015)  # 1.5% fee

# Add miners of different sizes
miners = [
    ("Home Miner Alice", 110e12),        # 110 TH/s
    ("Small Farm Bob", 1100e12),         # 1.1 PH/s
    ("Medium Farm Carol", 11000e12),     # 11 PH/s
    ("Large Farm Dave", 110000e12),      # 110 PH/s
]

for miner_name, hash_rate in miners:
    pool.add_miner(miner_name, hash_rate)

pool_stats = pool.get_pool_stats()
print(f"Pool: {pool_stats['name']}")
print(f"Total Hash Rate: {pool_stats['total_hash_rate_th']:,.0f} TH/s")
print(f"Miners: {pool_stats['miner_count']}")
print(f"Pool Fee: {pool_stats['pool_fee_percent']}%")

# Simulate finding blocks
for block_num in range(3):
    pool.find_block(6.25, 0.5)  # 6.25 BTC reward + 0.5 BTC fees

# Show final earnings
print(f"\nFinal Miner Earnings:")
for miner_id, miner_data in pool.miners.items():
    print(f"  {miner_id}: {miner_data['total_earnings']:.8f} BTC")
```

## Network Security and Consensus 🛡️

### 51% Attack Analysis

```python
def analyze_51_percent_attack():
    """Analyze the economics and feasibility of 51% attacks"""
    
    print("\n🛡️ 51% Attack Analysis")
    print("=" * 50)
    
    # Current network statistics (example values)
    network_stats = {
        'total_hash_rate_eh': 400,  # 400 EH/s
        'mining_hardware_efficiency': 30,  # J/TH (watts per terahash)
        'average_electricity_cost': 0.05,  # $0.05 per kWh
        'hardware_cost_per_th': 45,  # $45 per TH/s
        'btc_price': 45000,  # $45,000
        'daily_block_reward_btc': 144 * 6.25  # 144 blocks/day * 6.25 BTC
    }
    
    # Calculate 51% attack requirements
    required_hash_rate_eh = network_stats['total_hash_rate_eh'] * 0.51
    required_hash_rate_th = required_hash_rate_eh * 1000000  # Convert EH to TH
    
    # Hardware costs
    hardware_cost = required_hash_rate_th * network_stats['hardware_cost_per_th']
    
    # Daily electricity costs
    power_consumption_kw = required_hash_rate_th * network_stats['mining_hardware_efficiency'] / 1000
    daily_electricity_cost = power_consumption_kw * 24 * network_stats['average_electricity_cost']
    
    # Network rewards (what attacker gives up by attacking instead of honest mining)
    daily_network_rewards_usd = network_stats['daily_block_reward_btc'] * network_stats['btc_price']
    attacker_share = 0.51
    daily_opportunity_cost = daily_network_rewards_usd * attacker_share
    
    print(f"Network Hash Rate: {network_stats['total_hash_rate_eh']} EH/s")
    print(f"Required for 51%: {required_hash_rate_eh:.1f} EH/s")
    print(f"Hardware Cost: ${hardware_cost/1e9:.1f} billion")
    print(f"Daily Electricity: ${daily_electricity_cost/1e6:.1f} million")
    print(f"Daily Opportunity Cost: ${daily_opportunity_cost/1e6:.1f} million")
    
    total_daily_cost = (daily_electricity_cost + daily_opportunity_cost) / 1e6
    print(f"Total Daily Attack Cost: ${total_daily_cost:.1f} million")
    
    # Attack profitability analysis
    print(f"\nAttack Profitability Analysis:")
    print(f"  - Hardware investment: ${hardware_cost/1e9:.1f}B")
    print(f"  - Daily operating cost: ${total_daily_cost:.1f}M")
    print(f"  - Attack must steal > ${total_daily_cost:.1f}M/day to be profitable")
    print(f"  - Large exchanges have < ${total_daily_cost/10:.1f}M daily volume")
    print(f"  - Attack would crash BTC price, reducing spoils")
    print(f"  - Conclusion: Attack is economically irrational")

analyze_51_percent_attack()
```

### Difficulty Adjustment Deep Dive

```python
class DifficultyAdjustment:
    def __init__(self):
        self.target_block_time = 600  # 10 minutes in seconds
        self.adjustment_period_blocks = 2016  # ~2 weeks
        self.max_adjustment_factor = 4  # 4x up or down maximum
        
    def calculate_new_difficulty(self, actual_time_seconds: int, current_difficulty: int) -> dict:
        """Calculate new difficulty based on actual vs target time"""
        target_time = self.adjustment_period_blocks * self.target_block_time
        
        # Raw adjustment factor
        raw_adjustment = target_time / actual_time_seconds
        
        # Clamp adjustment to prevent extreme changes
        if raw_adjustment > self.max_adjustment_factor:
            adjustment_factor = self.max_adjustment_factor
            clamped = True
        elif raw_adjustment < (1 / self.max_adjustment_factor):
            adjustment_factor = 1 / self.max_adjustment_factor
            clamped = True
        else:
            adjustment_factor = raw_adjustment
            clamped = False
        
        new_difficulty = int(current_difficulty * adjustment_factor)
        
        return {
            'target_time_hours': target_time / 3600,
            'actual_time_hours': actual_time_seconds / 3600,
            'raw_adjustment_factor': raw_adjustment,
            'final_adjustment_factor': adjustment_factor,
            'was_clamped': clamped,
            'old_difficulty': current_difficulty,
            'new_difficulty': new_difficulty,
            'percent_change': ((adjustment_factor - 1) * 100)
        }

# Demo difficulty adjustment
print("\n⚖️ Difficulty Adjustment Deep Dive")
print("=" * 50)

diff_calculator = DifficultyAdjustment()
current_difficulty = 50000000000000  # Example difficulty

scenarios = [
    ("Hash rate doubled (blocks too fast)", 604800),  # 7 days instead of 14
    ("Hash rate halved (blocks too slow)", 2419200),   # 28 days instead of 14  
    ("Extreme hash rate increase", 201600),            # 2.33 days (would be clamped)
    ("Normal variation", 1209600),                     # 14 days (no change)
]

for scenario_name, actual_time in scenarios:
    result = diff_calculator.calculate_new_difficulty(actual_time, current_difficulty)
    
    print(f"\n{scenario_name}:")
    print(f"  Expected: {result['target_time_hours']:.1f} hours")
    print(f"  Actual: {result['actual_time_hours']:.1f} hours")
    print(f"  Raw adjustment: {result['raw_adjustment_factor']:.2f}x")
    print(f"  Final adjustment: {result['final_adjustment_factor']:.2f}x")
    print(f"  Difficulty change: {result['percent_change']:+.1f}%")
    print(f"  Was clamped: {result['was_clamped']}")
```

## Running a Bitcoin Node 🖥️

### Node Setup Guide

```python
def bitcoin_node_setup_guide():
    """Guide for setting up a Bitcoin node"""
    
    print("\n🖥️ Bitcoin Node Setup Guide")
    print("=" * 50)
    
    setup_steps = {
        'Hardware Requirements': {
            'minimum': 'Raspberry Pi 4, 8GB RAM, 1TB SSD',
            'recommended': 'Desktop PC, 16GB RAM, 2TB SSD, fast internet',
            'professional': 'Server hardware, 32GB+ RAM, enterprise SSDs'
        },
        'Software Installation': [
            '1. Download Bitcoin Core from bitcoin.org',
            '2. Verify GPG signatures for security',
            '3. Install on your operating system',
            '4. Configure bitcoin.conf file',
            '5. Start initial blockchain download (~400GB)'
        ],
        'Configuration Options': {
            'Full Node': 'Complete verification, serves other nodes',
            'Pruned Node': 'Full verification, limited storage',
            'Mining Node': 'Full node + mining capability',
            'Lightning Node': 'Full node + Lightning Network'
        },
        'Security Considerations': [
            'Use dedicated hardware if possible',
            'Keep Bitcoin Core updated',
            'Use strong passwords/encryption',
            'Consider firewall configuration',
            'Regular backup of wallet.dat'
        ],
        'Network Contributions': [
            'Validates all transactions independently',
            'Helps new nodes sync to network',
            'Strengthens network decentralization',
            'Provides personal financial sovereignty'
        ]
    }
    
    for section, content in setup_steps.items():
        print(f"\n{section}:")
        if isinstance(content, dict):
            for key, value in content.items():
                print(f"  {key}: {value}")
        elif isinstance(content, list):
            for item in content:
                print(f"  {item}")
        else:
            print(f"  {content}")

bitcoin_node_setup_guide()
```

## Quiz: Test Your Mining Knowledge 📝

```python
def mining_quiz():
    """Test understanding of Bitcoin mining and nodes"""
    
    print("\n🧠 Bitcoin Mining & Nodes Quiz")
    print("=" * 50)
    
    questions = [
        {
            'question': 'What determines Bitcoin mining difficulty?',
            'options': ['A) Price of Bitcoin', 'B) Network hash rate', 'C) Number of transactions', 'D) Block size'],
            'correct': 'B',
            'explanation': 'Difficulty adjusts every 2016 blocks to maintain 10-minute block times regardless of network hash rate'
        },
        {
            'question': 'What happens if a mining pool controls 51% of hash rate?',
            'options': ['A) They earn 51% of rewards', 'B) They can reverse transactions', 'C) They control Bitcoin', 'D) Nothing special'],
            'correct': 'B',
            'explanation': '51% control allows double-spending attacks and transaction censorship, but is economically irrational'
        },
        {
            'question': 'What is the main difference between full nodes and SPV nodes?',
            'options': ['A) Mining capability', 'B) Storage requirements', 'C) Internet speed', 'D) CPU power'],
            'correct': 'B',
            'explanation': 'Full nodes store the entire blockchain (~400GB), SPV nodes only store block headers (~100MB)'
        },
        {
            'question': 'Why do miners join mining pools?',
            'options': ['A) Higher hash rates', 'B) Lower electricity costs', 'C) More consistent payouts', 'D) Better hardware'],
            'correct': 'C',
            'explanation': 'Pools provide steady income instead of lottery-like solo mining payouts'
        }
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for option in q['options']:
            print(f"  {option}")
        
        print(f"\nAnswer: {q['correct']}")
        print(f"Explanation: {q['explanation']}")
        print("-" * 50)

mining_quiz()
```

## Summary 🎯

Bitcoin mining and nodes form the foundation of network security and decentralization:

### Mining Fundamentals
- **Proof of Work** secures the network through computational difficulty
- **Mining hardware** evolved from CPUs to specialized ASICs
- **Mining pools** provide consistent returns for smaller miners
- **Difficulty adjustment** maintains 10-minute block times

### Network Security
- **Economic security** makes attacks prohibitively expensive
- **51% attacks** are theoretically possible but economically irrational
- **Decentralization** through global distribution of mining power
- **Consensus rules** enforced by all network participants

### Node Operations
- **Full nodes** provide independent transaction verification
- **Different node types** serve different use cases and resource constraints
- **Network effects** strengthen with more nodes and miners
- **Personal sovereignty** through running your own node

### Real-World Impact
- **Energy consumption** secures the most valuable decentralized network
- **Geographic distribution** provides global resilience
- **Economic incentives** align network security with participant rewards
- **Innovation** drives efficiency improvements in mining hardware

### Next Steps
- Learn about [Bitcoin Scripting](bitcoin-scripting.md) for programmable money
- Explore [Ethereum Mining](../03-ethereum/ethereum-overview.md) differences
- Study [Consensus Mechanisms](../00-fundamentals/consensus-mechanisms.md) in detail
- Understand [Cryptographic Hash Functions](../01-cryptography/hashing-fundamentals.md)

---

**⛏️ Bitcoin mining transformed from a hobbyist activity to a global industry, securing the network through computational proof while maintaining decentralization through economic incentives.**