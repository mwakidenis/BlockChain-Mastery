# Connecting to Blockchain 🔗

Learn how to connect your applications to blockchain networks using Web3 providers, RPC endpoints, and various connection methods.

## 📋 Table of Contents

1. [Web3 Providers](#web3-providers)
2. [RPC Endpoints](#rpc-endpoints)
3. [Network Configuration](#network-configuration)
4. [Reading Blockchain Data](#reading-blockchain-data)
5. [Connection Best Practices](#connection-best-practices)

---

## Web3 Providers

### What is a Provider?

A **provider** is an abstraction of a connection to the Ethereum network. It provides a consistent interface for interacting with the blockchain.

### Types of Providers

#### 1. Browser Provider (MetaMask)

```javascript
import { ethers } from 'ethers';

// Check if MetaMask is installed
if (typeof window.ethereum !== 'undefined') {
    // Request account access
    await window.ethereum.request({ method: 'eth_requestAccounts' });
    
    // Create provider
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    
    // Get signer for transactions
    const signer = provider.getSigner();
    
    console.log('Connected to:', await signer.getAddress());
} else {
    console.log('Please install MetaMask!');
}
```

#### 2. JSON-RPC Provider

```javascript
// Connect to a specific network
const provider = new ethers.providers.JsonRpcProvider('https://eth-mainnet.alchemyapi.io/v2/YOUR-API-KEY');

// Get network information
const network = await provider.getNetwork();
console.log('Connected to:', network.name);

// Get block number
const blockNumber = await provider.getBlockNumber();
console.log('Current block:', blockNumber);
```

#### 3. Infura Provider

```javascript
const provider = new ethers.providers.InfuraProvider('mainnet', 'YOUR-INFURA-PROJECT-ID');

// Or with WebSocket for event listening
const wsProvider = new ethers.providers.InfuraWebSocketProvider(
    'mainnet',
    'YOUR-INFURA-PROJECT-ID'
);
```

#### 4. Alchemy Provider

```javascript
const provider = new ethers.providers.AlchemyProvider('mainnet', 'YOUR-ALCHEMY-API-KEY');

// Alchemy WebSocket
const wsProvider = new ethers.providers.AlchemyWebSocketProvider(
    'mainnet',
    'YOUR-ALCHEMY-API-KEY'
);
```

#### 5. Fallback Provider

```javascript
// Create multiple providers for redundancy
const providers = [
    new ethers.providers.InfuraProvider('mainnet', INFURA_KEY),
    new ethers.providers.AlchemyProvider('mainnet', ALCHEMY_KEY),
    new ethers.providers.EtherscanProvider('mainnet', ETHERSCAN_KEY)
];

const fallbackProvider = new ethers.providers.FallbackProvider(providers);
```

---

## RPC Endpoints

### Public RPC Endpoints

#### Ethereum Mainnet
```javascript
const endpoints = {
    // Infura
    infura: 'https://mainnet.infura.io/v3/YOUR-PROJECT-ID',
    
    // Alchemy
    alchemy: 'https://eth-mainnet.alchemyapi.io/v2/YOUR-API-KEY',
    
    // Public (rate-limited)
    public: 'https://eth.llamarpc.com'
};

const provider = new ethers.providers.JsonRpcProvider(endpoints.alchemy);
```

#### Testnets

```javascript
const testnetEndpoints = {
    // Sepolia
    sepolia: 'https://sepolia.infura.io/v3/YOUR-PROJECT-ID',
    
    // Goerli
    goerli: 'https://goerli.infura.io/v3/YOUR-PROJECT-ID',
    
    // Mumbai (Polygon testnet)
    mumbai: 'https://rpc-mumbai.maticvigil.com'
};
```

#### Other Networks

```javascript
const networkEndpoints = {
    // Polygon
    polygon: 'https://polygon-rpc.com',
    
    // Binance Smart Chain
    bsc: 'https://bsc-dataseed.binance.org',
    
    // Arbitrum
    arbitrum: 'https://arb1.arbitrum.io/rpc',
    
    // Optimism
    optimism: 'https://mainnet.optimism.io'
};
```

### Setting Up Your Own Node

```bash
# Using Geth
geth --http --http.addr "0.0.0.0" --http.port 8545

# Using Hardhat
npx hardhat node

# Using Ganache
ganache-cli -p 8545
```

```javascript
// Connect to local node
const provider = new ethers.providers.JsonRpcProvider('http://localhost:8545');
```

---

## Network Configuration

### Detecting Network

```javascript
async function detectNetwork() {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const network = await provider.getNetwork();
    
    console.log('Network Name:', network.name);
    console.log('Chain ID:', network.chainId);
    
    return network;
}

// Chain IDs
const CHAIN_IDS = {
    MAINNET: 1,
    GOERLI: 5,
    SEPOLIA: 11155111,
    POLYGON: 137,
    MUMBAI: 80001,
    BSC: 56,
    ARBITRUM: 42161,
    OPTIMISM: 10
};
```

### Switching Networks

```javascript
async function switchNetwork(chainId) {
    try {
        await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: ethers.utils.hexValue(chainId) }]
        });
    } catch (error) {
        // If network doesn't exist, add it
        if (error.code === 4902) {
            await addNetwork(chainId);
        }
    }
}

async function addNetwork(chainId) {
    const networks = {
        137: {
            chainId: '0x89',
            chainName: 'Polygon Mainnet',
            nativeCurrency: {
                name: 'MATIC',
                symbol: 'MATIC',
                decimals: 18
            },
            rpcUrls: ['https://polygon-rpc.com'],
            blockExplorerUrls: ['https://polygonscan.com']
        }
    };
    
    await window.ethereum.request({
        method: 'wallet_addEthereumChain',
        params: [networks[chainId]]
    });
}
```

### Listening to Network Changes

```javascript
if (window.ethereum) {
    // Listen for network changes
    window.ethereum.on('chainChanged', (chainId) => {
        console.log('Network changed to:', parseInt(chainId, 16));
        // Reload the page or update state
        window.location.reload();
    });
    
    // Listen for account changes
    window.ethereum.on('accountsChanged', (accounts) => {
        if (accounts.length === 0) {
            console.log('Please connect to MetaMask');
        } else {
            console.log('Account changed to:', accounts[0]);
        }
    });
}
```

---

## Reading Blockchain Data

### Getting Block Information

```javascript
async function getBlockInfo() {
    const provider = new ethers.providers.JsonRpcProvider(RPC_URL);
    
    // Latest block
    const blockNumber = await provider.getBlockNumber();
    console.log('Current block:', blockNumber);
    
    // Block details
    const block = await provider.getBlock(blockNumber);
    console.log('Block hash:', block.hash);
    console.log('Timestamp:', block.timestamp);
    console.log('Transactions:', block.transactions.length);
    
    // Block with transactions
    const blockWithTx = await provider.getBlockWithTransactions(blockNumber);
    console.log('First transaction:', blockWithTx.transactions[0]);
}
```

### Getting Account Information

```javascript
async function getAccountInfo(address) {
    const provider = new ethers.providers.JsonRpcProvider(RPC_URL);
    
    // Get balance
    const balance = await provider.getBalance(address);
    console.log('Balance:', ethers.utils.formatEther(balance), 'ETH');
    
    // Get transaction count (nonce)
    const txCount = await provider.getTransactionCount(address);
    console.log('Transaction count:', txCount);
    
    // Get code (for contracts)
    const code = await provider.getCode(address);
    console.log('Is contract:', code !== '0x');
}
```

### Getting Transaction Information

```javascript
async function getTransactionInfo(txHash) {
    const provider = new ethers.providers.JsonRpcProvider(RPC_URL);
    
    // Get transaction
    const tx = await provider.getTransaction(txHash);
    console.log('From:', tx.from);
    console.log('To:', tx.to);
    console.log('Value:', ethers.utils.formatEther(tx.value));
    console.log('Gas price:', ethers.utils.formatUnits(tx.gasPrice, 'gwei'));
    
    // Get transaction receipt
    const receipt = await provider.getTransactionReceipt(txHash);
    console.log('Status:', receipt.status); // 1 = success, 0 = failed
    console.log('Block number:', receipt.blockNumber);
    console.log('Gas used:', receipt.gasUsed.toString());
}
```

### Reading Smart Contract Data

```javascript
async function readContract() {
    const provider = new ethers.providers.JsonRpcProvider(RPC_URL);
    
    // Contract ABI (simplified)
    const abi = [
        "function name() view returns (string)",
        "function symbol() view returns (string)",
        "function balanceOf(address) view returns (uint256)"
    ];
    
    const contractAddress = '0x...';
    const contract = new ethers.Contract(contractAddress, abi, provider);
    
    // Read contract data
    const name = await contract.name();
    const symbol = await contract.symbol();
    const balance = await contract.balanceOf('0x...');
    
    console.log(`Token: ${name} (${symbol})`);
    console.log('Balance:', ethers.utils.formatUnits(balance, 18));
}
```

### Listening to Events

```javascript
async function listenToEvents() {
    const provider = new ethers.providers.WebSocketProvider(WS_URL);
    
    const abi = ["event Transfer(address indexed from, address indexed to, uint256 value)"];
    const contract = new ethers.Contract(contractAddress, abi, provider);
    
    // Listen to Transfer events
    contract.on("Transfer", (from, to, value, event) => {
        console.log('Transfer:', {
            from,
            to,
            value: ethers.utils.formatUnits(value, 18),
            txHash: event.transactionHash
        });
    });
    
    // Listen to new blocks
    provider.on("block", (blockNumber) => {
        console.log('New block:', blockNumber);
    });
}
```

### Filtering Events

```javascript
async function filterEvents() {
    const provider = new ethers.providers.JsonRpcProvider(RPC_URL);
    
    const abi = ["event Transfer(address indexed from, address indexed to, uint256 value)"];
    const contract = new ethers.Contract(contractAddress, abi, provider);
    
    // Create filter
    const filter = contract.filters.Transfer(
        null,  // from any address
        '0x...'  // to specific address
    );
    
    // Query past events
    const events = await contract.queryFilter(filter, -10000); // Last 10000 blocks
    
    events.forEach(event => {
        console.log('Transfer:', {
            from: event.args.from,
            to: event.args.to,
            value: ethers.utils.formatUnits(event.args.value, 18),
            block: event.blockNumber
        });
    });
}
```

---

## Connection Best Practices

### 1. Error Handling

```javascript
async function connectWithErrorHandling() {
    try {
        if (typeof window.ethereum === 'undefined') {
            throw new Error('MetaMask is not installed');
        }
        
        const provider = new ethers.providers.Web3Provider(window.ethereum);
        
        // Request accounts
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        
        const network = await provider.getNetwork();
        
        // Verify correct network
        if (network.chainId !== 1) {
            throw new Error('Please switch to Ethereum Mainnet');
        }
        
        return provider;
        
    } catch (error) {
        if (error.code === 4001) {
            console.log('User rejected connection');
        } else if (error.code === -32002) {
            console.log('Connection request already pending');
        } else {
            console.error('Connection error:', error.message);
        }
        throw error;
    }
}
```

### 2. Connection State Management (React)

```javascript
import { useState, useEffect } from 'react';

function useWeb3Provider() {
    const [provider, setProvider] = useState(null);
    const [account, setAccount] = useState(null);
    const [chainId, setChainId] = useState(null);
    const [error, setError] = useState(null);
    
    const connect = async () => {
        try {
            if (!window.ethereum) {
                throw new Error('No wallet found');
            }
            
            const provider = new ethers.providers.Web3Provider(window.ethereum);
            await window.ethereum.request({ method: 'eth_requestAccounts' });
            
            const signer = provider.getSigner();
            const address = await signer.getAddress();
            const network = await provider.getNetwork();
            
            setProvider(provider);
            setAccount(address);
            setChainId(network.chainId);
            setError(null);
            
        } catch (err) {
            setError(err.message);
        }
    };
    
    useEffect(() => {
        if (window.ethereum) {
            window.ethereum.on('accountsChanged', (accounts) => {
                setAccount(accounts[0] || null);
            });
            
            window.ethereum.on('chainChanged', () => {
                window.location.reload();
            });
        }
        
        return () => {
            if (window.ethereum.removeListener) {
                window.ethereum.removeListener('accountsChanged', () => {});
                window.ethereum.removeListener('chainChanged', () => {});
            }
        };
    }, []);
    
    return { provider, account, chainId, error, connect };
}
```

### 3. Rate Limiting

```javascript
class RateLimitedProvider {
    constructor(provider, requestsPerSecond = 10) {
        this.provider = provider;
        this.requestsPerSecond = requestsPerSecond;
        this.queue = [];
        this.processing = false;
    }
    
    async request(method, params) {
        return new Promise((resolve, reject) => {
            this.queue.push({ method, params, resolve, reject });
            this.processQueue();
        });
    }
    
    async processQueue() {
        if (this.processing || this.queue.length === 0) return;
        
        this.processing = true;
        const { method, params, resolve, reject } = this.queue.shift();
        
        try {
            const result = await this.provider.send(method, params);
            resolve(result);
        } catch (error) {
            reject(error);
        }
        
        setTimeout(() => {
            this.processing = false;
            this.processQueue();
        }, 1000 / this.requestsPerSecond);
    }
}
```

### 4. Caching

```javascript
class CachedProvider {
    constructor(provider, cacheDuration = 60000) {
        this.provider = provider;
        this.cache = new Map();
        this.cacheDuration = cacheDuration;
    }
    
    async getBlock(blockNumber) {
        const cacheKey = `block_${blockNumber}`;
        const cached = this.cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < this.cacheDuration) {
            return cached.data;
        }
        
        const block = await this.provider.getBlock(blockNumber);
        this.cache.set(cacheKey, {
            data: block,
            timestamp: Date.now()
        });
        
        return block;
    }
}
```

### 5. Connection Retry Logic

```javascript
async function connectWithRetry(maxRetries = 3, delay = 1000) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            const provider = new ethers.providers.JsonRpcProvider(RPC_URL);
            await provider.getNetwork(); // Test connection
            return provider;
        } catch (error) {
            console.log(`Connection attempt ${i + 1} failed:`, error.message);
            if (i < maxRetries - 1) {
                await new Promise(resolve => setTimeout(resolve, delay * (i + 1)));
            }
        }
    }
    throw new Error('Failed to connect after multiple attempts');
}
```

---

## Complete Connection Example

```javascript
class Web3Connection {
    constructor() {
        this.provider = null;
        this.signer = null;
        this.account = null;
        this.chainId = null;
    }
    
    async connect() {
        if (!window.ethereum) {
            throw new Error('No Web3 wallet detected');
        }
        
        try {
            // Create provider
            this.provider = new ethers.providers.Web3Provider(window.ethereum);
            
            // Request account access
            await window.ethereum.request({ method: 'eth_requestAccounts' });
            
            // Get signer
            this.signer = this.provider.getSigner();
            this.account = await this.signer.getAddress();
            
            // Get network
            const network = await this.provider.getNetwork();
            this.chainId = network.chainId;
            
            // Setup listeners
            this.setupListeners();
            
            return {
                provider: this.provider,
                signer: this.signer,
                account: this.account,
                chainId: this.chainId
            };
            
        } catch (error) {
            console.error('Connection failed:', error);
            throw error;
        }
    }
    
    setupListeners() {
        window.ethereum.on('accountsChanged', (accounts) => {
            this.account = accounts[0];
            this.onAccountChanged(accounts[0]);
        });
        
        window.ethereum.on('chainChanged', (chainId) => {
            this.chainId = parseInt(chainId, 16);
            this.onChainChanged(this.chainId);
        });
    }
    
    onAccountChanged(account) {
        console.log('Account changed:', account);
        // Implement your logic
    }
    
    onChainChanged(chainId) {
        console.log('Chain changed:', chainId);
        window.location.reload();
    }
    
    disconnect() {
        this.provider = null;
        this.signer = null;
        this.account = null;
        this.chainId = null;
    }
}

// Usage
const web3 = new Web3Connection();
await web3.connect();
```

---

## Resources

- [Ethers.js Documentation](https://docs.ethers.io/)
- [Infura](https://infura.io/)
- [Alchemy](https://www.alchemy.com/)
- [ChainList](https://chainlist.org/) - RPC endpoints

**Next**: [Ethers.js vs Web3.js](ethers-vs-web3js.md) →
