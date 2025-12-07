# Cross-Chain Bridges 🌉

Bridges enable asset and data transfer between different blockchain networks.

## Types of Bridges

### 1. Lock & Mint

**Mechanism**: Lock tokens on source chain, mint wrapped tokens on destination

```
Chain A: Lock 1 ETH
Chain B: Mint 1 WETH
```

### 2. Burn & Mint

**Mechanism**: Burn tokens on source, mint on destination

### 3. Liquidity Pools

**Mechanism**: Swap tokens from liquidity pools on both chains

## Popular Bridges

| Bridge | Type | Chains | TVL |
|--------|------|--------|-----|
| **Wormhole** | Lock & Mint | 20+ | $2B+ |
| **LayerZero** | Messaging | 40+ | N/A |
| **Hop Protocol** | AMM | L2s | $100M+ |
| **Multichain** | Lock & Mint | 60+ | $3B+ |
| **Axelar** | Proof-of-Stake | 40+ | $500M+ |

## Bridge Architecture

### Lock & Mint Bridge

```solidity
// Source Chain
contract SourceBridge {
    event TokensLocked(address indexed from, uint256 amount, bytes32 destinationChain);
    
    mapping(address => uint256) public lockedTokens;
    
    function lock(uint256 amount, bytes32 destinationChain) external {
        IERC20(sourceToken).transferFrom(msg.sender, address(this), amount);
        lockedTokens[msg.sender] += amount;
        
        emit TokensLocked(msg.sender, amount, destinationChain);
    }
    
    function unlock(address to, uint256 amount, bytes memory proof) external {
        // Verify proof from destination chain
        require(verifyProof(proof), "Invalid proof");
        
        lockedTokens[to] -= amount;
        IERC20(sourceToken).transfer(to, amount);
    }
}

// Destination Chain
contract DestinationBridge {
    event TokensMinted(address indexed to, uint256 amount);
    
    function mint(address to, uint256 amount, bytes memory proof) external {
        // Verify lock on source chain
        require(verifyProof(proof), "Invalid proof");
        
        IWrappedToken(wrappedToken).mint(to, amount);
        emit TokensMinted(to, amount);
    }
    
    function burn(uint256 amount) external {
        IWrappedToken(wrappedToken).burn(msg.sender, amount);
        
        // Emit event for relayers to unlock on source chain
    }
}
```

## LayerZero Integration

### Cross-Chain Messaging

```solidity
import "@layerzerolabs/solidity-examples/contracts/lzApp/NonblockingLzApp.sol";

contract CrossChainNFT is NonblockingLzApp, ERC721 {
    constructor(address _lzEndpoint) NonblockingLzApp(_lzEndpoint) ERC721("CrossChainNFT", "CCNFT") {}
    
    function sendNFT(
        uint16 _dstChainId,
        address _to,
        uint256 _tokenId
    ) public payable {
        // Burn NFT on source chain
        _burn(_tokenId);
        
        // Encode payload
        bytes memory payload = abi.encode(_to, _tokenId);
        
        // Send to destination chain
        _lzSend(
            _dstChainId,
            payload,
            payable(msg.sender),
            address(0),
            bytes(""),
            msg.value
        );
    }
    
    function _nonblockingLzReceive(
        uint16 _srcChainId,
        bytes memory _srcAddress,
        uint64 _nonce,
        bytes memory _payload
    ) internal override {
        // Decode payload
        (address to, uint256 tokenId) = abi.decode(_payload, (address, uint256));
        
        // Mint NFT on destination chain
        _safeMint(to, tokenId);
    }
}
```

## Bridge Security

### Common Vulnerabilities

1. **Validator Compromise**
2. **Smart Contract Bugs**
3. **Oracle Manipulation**
4. **Replay Attacks**

### Security Best Practices

```solidity
contract SecureBridge {
    using ECDSA for bytes32;
    
    mapping(bytes32 => bool) public processedTransactions;
    uint256 public minValidatorSignatures = 3;
    
    function bridgeTokens(
        uint256 amount,
        address recipient,
        bytes32 txHash,
        bytes[] memory signatures
    ) external {
        // Prevent replay attacks
        require(!processedTransactions[txHash], "Already processed");
        
        // Verify multiple validator signatures
        require(signatures.length >= minValidatorSignatures, "Not enough signatures");
        
        bytes32 message = keccak256(abi.encodePacked(amount, recipient, txHash));
        
        for (uint i = 0; i < signatures.length; i++) {
            address signer = message.toEthSignedMessageHash().recover(signatures[i]);
            require(isValidator(signer), "Invalid validator");
        }
        
        processedTransactions[txHash] = true;
        
        // Process bridge
        _mintWrappedToken(recipient, amount);
    }
}
```

## Using Bridges (Frontend)

```javascript
import { ethers } from 'ethers';

class BridgeClient {
    async bridgeTokens(fromChain, toChain, token, amount) {
        // Connect to source chain
        const sourceProvider = new ethers.providers.JsonRpcProvider(fromChain.rpc);
        const sourceSigner = sourceProvider.getSigner();
        
        const bridge = new ethers.Contract(
            fromChain.bridgeAddress,
            BRIDGE_ABI,
            sourceSigner
        );
        
        // Approve tokens
        const tokenContract = new ethers.Contract(token, ERC20_ABI, sourceSigner);
        await tokenContract.approve(bridge.address, amount);
        
        // Initiate bridge
        const tx = await bridge.lock(amount, toChain.chainId);
        await tx.wait();
        
        console.log('Bridge initiated, waiting for confirmations...');
        
        // Listen for minting on destination chain
        await this.waitForBridgeCompletion(toChain, tx.hash);
    }
    
    async waitForBridgeCompletion(destChain, txHash) {
        const provider = new ethers.providers.JsonRpcProvider(destChain.rpc);
        const bridge = new ethers.Contract(
            destChain.bridgeAddress,
            BRIDGE_ABI,
            provider
        );
        
        // Poll for mint event
        const filter = bridge.filters.TokensMinted();
        
        return new Promise((resolve) => {
            bridge.on(filter, (to, amount, event) => {
                console.log('Tokens minted on destination chain!');
                resolve(event);
            });
        });
    }
}
```

## Bridge Aggregators

### Socket API Example

```javascript
async function getBestBridgeRoute(fromChain, toChain, token, amount) {
    const response = await fetch('https://api.socket.tech/v2/quote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            fromChainId: fromChain,
            toChainId: toChain,
            fromTokenAddress: token,
            toTokenAddress: token,
            fromAmount: amount,
            userAddress: userAddress
        })
    });
    
    const data = await response.json();
    
    // Returns best routes across multiple bridges
    return data.routes;
}
```

## Bridge Risks

### Historical Exploits

- **Ronin Bridge** (2022): $625M stolen
- **Wormhole** (2022): $325M stolen  
- **BNB Bridge** (2022): $570M stolen

### Risk Mitigation

1. ✅ Use reputable bridges
2. ✅ Bridge only what you need
3. ✅ Verify destination address
4. ✅ Check bridge TVL and audits
5. ✅ Use bridge aggregators for better rates

## Alternative: Intent-Based Bridging

```solidity
// Users express intent, solvers fulfill
contract IntentBridge {
    struct Intent {
        address user;
        uint256 amount;
        uint256 destChain;
        uint256 minReceive;
        uint256 deadline;
    }
    
    mapping(bytes32 => Intent) public intents;
    
    function createIntent(
        uint256 amount,
        uint256 destChain,
        uint256 minReceive,
        uint256 deadline
    ) external {
        bytes32 intentId = keccak256(abi.encodePacked(
            msg.sender,
            amount,
            destChain,
            block.timestamp
        ));
        
        intents[intentId] = Intent(
            msg.sender,
            amount,
            destChain,
            minReceive,
            deadline
        );
        
        // Lock tokens
        IERC20(token).transferFrom(msg.sender, address(this), amount);
    }
    
    function fulfillIntent(bytes32 intentId, bytes memory proof) external {
        Intent memory intent = intents[intentId];
        
        // Verify solver fulfilled on dest chain
        require(verifyFulfillment(proof), "Invalid proof");
        
        // Release tokens to solver
        IERC20(token).transfer(msg.sender, intent.amount);
    }
}
```

## Resources

- [L2Beat Bridges](https://l2beat.com/bridges)
- [LayerZero Docs](https://layerzero.network/developers)
- [Wormhole Docs](https://docs.wormhole.com/)
- [Bridge Security Best Practices](https://ethereum.org/en/developers/docs/bridges/)

**Next**: [DAO Governance](dao-governance.md) →
