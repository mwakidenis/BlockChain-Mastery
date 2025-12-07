# Layer 2 Scaling Solutions ⚡

Layer 2 solutions scale Ethereum by processing transactions off-chain while inheriting Ethereum's security.

## Why Layer 2?

Ethereum's limitations:
- ⚠️ **Low TPS**: ~15 transactions/second
- ⚠️ **High Fees**: $5-$50+ per transaction
- ⚠️ **Slow Finality**: 15+ seconds

Layer 2 benefits:
- ✅ **Higher TPS**: 1,000-4,000 TPS
- ✅ **Lower Fees**: $0.01-$1 per transaction
- ✅ **Faster**: Near-instant confirmation

## Types of Layer 2

### 1. Optimistic Rollups

**How it works**: Assume transactions are valid, challenge if fraud detected

**Popular Chains**:
- **Optimism**
- **Arbitrum**
- **Base** (Coinbase)

**Characteristics**:
- 7-day withdrawal period
- EVM compatible
- Lower fees than L1

```solidity
// Same Solidity code works on Optimistic Rollups
contract MyContract {
    function transfer(address to, uint256 amount) public {
        // Standard EVM code
    }
}
```

### 2. ZK-Rollups

**How it works**: Use zero-knowledge proofs to prove transaction validity

**Popular Chains**:
- **zkSync Era**
- **StarkNet**
- **Polygon zkEVM**

**Characteristics**:
- Fast withdrawals (minutes)
- Higher security
- More complex to develop

### 3. Sidechains

**How it works**: Independent blockchain with own consensus

**Popular Chains**:
- **Polygon PoS**
- **Gnosis Chain**

**Characteristics**:
- Own validators
- Faster & cheaper
- Lower security than rollups

### 4. State Channels

**How it works**: Off-chain transactions, settle on-chain

**Examples**:
- **Lightning Network** (Bitcoin)
- **Raiden** (Ethereum)

**Use Cases**:
- Micropayments
- Gaming
- Instant transfers

## Comparison Table

| Solution | Type | TPS | Finality | Fees | EVM Compat |
|----------|------|-----|----------|------|------------|
| **Optimism** | Optimistic | 2,000 | 7 days | Low | ✅ Yes |
| **Arbitrum** | Optimistic | 4,000 | 7 days | Low | ✅ Yes |
| **zkSync** | ZK-Rollup | 2,000 | Minutes | Low | ⚠️ Partial |
| **Polygon** | Sidechain | 7,000 | Seconds | Very Low | ✅ Yes |
| **StarkNet** | ZK-Rollup | 300 | Minutes | Low | ❌ Cairo |

## Deploying to Layer 2

### Arbitrum Deployment

```javascript
// hardhat.config.js
module.exports = {
  networks: {
    arbitrum: {
      url: "https://arb1.arbitrum.io/rpc",
      accounts: [PRIVATE_KEY],
      chainId: 42161
    },
    arbitrumGoerli: {
      url: "https://goerli-rollup.arbitrum.io/rpc",
      accounts: [PRIVATE_KEY],
      chainId: 421613
    }
  }
};
```

```bash
# Deploy to Arbitrum
npx hardhat run scripts/deploy.js --network arbitrum
```

### Optimism Deployment

```javascript
// hardhat.config.js
module.exports = {
  networks: {
    optimism: {
      url: "https://mainnet.optimism.io",
      accounts: [PRIVATE_KEY],
      chainId: 10
    }
  }
};
```

## Bridging Assets

### Using Official Bridges

```javascript
import { ethers } from 'ethers';

// Bridge ETH from L1 to Arbitrum
async function bridgeToArbitrum(amount) {
    const l1Bridge = new ethers.Contract(
        ARBITRUM_L1_BRIDGE,
        BRIDGE_ABI,
        l1Signer
    );
    
    const tx = await l1Bridge.depositETH({
        value: ethers.utils.parseEther(amount)
    });
    
    await tx.wait();
    console.log('Bridged to Arbitrum');
}

// Withdraw from L2 to L1
async function withdrawFromArbitrum(amount) {
    const l2Bridge = new ethers.Contract(
        ARBITRUM_L2_BRIDGE,
        BRIDGE_ABI,
        l2Signer
    );
    
    const tx = await l2Bridge.withdraw(
        ethers.utils.parseEther(amount)
    );
    
    await tx.wait();
    console.log('Withdrawal initiated (7 day wait)');
}
```

## L2-Specific Features

### Arbitrum Retryable Tickets

```solidity
// Send message from L1 to L2
interface IInbox {
    function createRetryableTicket(
        address to,
        uint256 l2CallValue,
        uint256 maxSubmissionCost,
        address excessFeeRefundAddress,
        address callValueRefundAddress,
        uint256 gasLimit,
        uint256 maxFeePerGas,
        bytes calldata data
    ) external payable returns (uint256);
}
```

### Optimism Cross-Domain Messaging

```solidity
// L1 to L2 message
interface ICrossDomainMessenger {
    function sendMessage(
        address _target,
        bytes memory _message,
        uint32 _gasLimit
    ) external;
}

contract L1Contract {
    ICrossDomainMessenger messenger = ICrossDomainMessenger(0x...');
    
    function sendToL2(address l2Target, bytes memory data) public {
        messenger.sendMessage(l2Target, data, 1000000);
    }
}
```

## Gas Optimization for L2

```solidity
// L2 gas is cheaper, but still optimize
contract L2Optimized {
    // Use calldata for arrays (even cheaper on L2)
    function batchProcess(uint256[] calldata ids) external {
        for (uint i = 0; i < ids.length; i++) {
            process(ids[i]);
        }
    }
    
    // Pack storage efficiently
    struct User {
        uint128 balance;  // Packed
        uint128 lastUpdate;  // Packed
    }
}
```

## Development Tips

1. **Test on Testnet**: Always test L2-specific features
2. **Monitor Gas**: L2 gas patterns differ from L1
3. **Bridge Security**: Use official bridges
4. **Withdrawal Times**: Plan for delays
5. **Block Times**: L2 blocks are faster

## Popular L2 Protocols

### DeFi on L2
- **Uniswap V3** (Optimism, Arbitrum, Polygon)
- **Aave V3** (Multi-chain)
- **Curve** (Various L2s)

### NFTs on L2
- **OpenSea** (Polygon, Arbitrum)
- **IMX** (StarkEx)

## Resources

- [L2Beat](https://l2beat.com/) - L2 metrics
- [Arbitrum Docs](https://docs.arbitrum.io/)
- [Optimism Docs](https://docs.optimism.io/)
- [zkSync Docs](https://docs.zksync.io/)

**Next**: [Cross-Chain Bridges](cross-chain-bridges.md) →
