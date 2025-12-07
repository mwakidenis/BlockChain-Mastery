# Wallet Integration 🦊

Learn how to integrate cryptocurrency wallets into your dApps, enabling users to connect, sign transactions, and interact with blockchain networks.

## Popular Wallets

- **MetaMask** 🦊 - Most popular browser extension
- **WalletConnect** 🔗 - Mobile wallet connection
- **Coinbase Wallet** - User-friendly option
- **Trust Wallet** - Mobile-first
- **Rainbow** 🌈 - Modern mobile wallet

## MetaMask Integration

### Basic Connection

```javascript
import { ethers } from 'ethers';

async function connectMetaMask() {
    // Check if MetaMask is installed
    if (typeof window.ethereum === 'undefined') {
        alert('Please install MetaMask!');
        return;
    }
    
    try {
        // Request account access
        const accounts = await window.ethereum.request({ 
            method: 'eth_requestAccounts' 
        });
        
        console.log('Connected account:', accounts[0]);
        
        // Create provider and signer
        const provider = new ethers.providers.Web3Provider(window.ethereum);
        const signer = provider.getSigner();
        
        return { provider, signer, account: accounts[0] };
        
    } catch (error) {
        if (error.code === 4001) {
            console.log('User rejected connection');
        } else {
            console.error('Connection error:', error);
        }
    }
}
```

### React Integration

```javascript
import { useState, useEffect } from 'react';
import { ethers } from 'ethers';

function WalletConnect() {
    const [account, setAccount] = useState(null);
    const [provider, setProvider] = useState(null);
    
    const connect = async () => {
        if (!window.ethereum) {
            alert('Please install MetaMask!');
            return;
        }
        
        try {
            const provider = new ethers.providers.Web3Provider(window.ethereum);
            await provider.send("eth_requestAccounts", []);
            
            const signer = provider.getSigner();
            const address = await signer.getAddress();
            
            setProvider(provider);
            setAccount(address);
        } catch (error) {
            console.error('Connection failed:', error);
        }
    };
    
    const disconnect = () => {
        setAccount(null);
        setProvider(null);
    };
    
    // Listen for account changes
    useEffect(() => {
        if (window.ethereum) {
            window.ethereum.on('accountsChanged', (accounts) => {
                if (accounts.length === 0) {
                    disconnect();
                } else {
                    setAccount(accounts[0]);
                }
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
    
    return (
        <div>
            {!account ? (
                <button onClick={connect}>Connect Wallet</button>
            ) : (
                <div>
                    <p>Connected: {account.slice(0, 6)}...{account.slice(-4)}</p>
                    <button onClick={disconnect}>Disconnect</button>
                </div>
            )}
        </div>
    );
}
```

## WalletConnect Integration

### Setup

```bash
npm install @walletconnect/web3-provider
```

### Implementation

```javascript
import WalletConnectProvider from '@walletconnect/web3-provider';
import { ethers } from 'ethers';

async function connectWalletConnect() {
    // Create WalletConnect Provider
    const wcProvider = new WalletConnectProvider({
        infuraId: "YOUR_INFURA_ID",
        qrcode: true,
        rpc: {
            1: "https://mainnet.infura.io/v3/YOUR_INFURA_ID",
            137: "https://polygon-rpc.com"
        }
    });
    
    try {
        // Enable session
        await wcProvider.enable();
        
        // Create ethers provider
        const provider = new ethers.providers.Web3Provider(wcProvider);
        const signer = provider.getSigner();
        const address = await signer.getAddress();
        
        console.log('Connected via WalletConnect:', address);
        
        // Subscribe to events
        wcProvider.on("accountsChanged", (accounts) => {
            console.log('Account changed:', accounts[0]);
        });
        
        wcProvider.on("chainChanged", (chainId) => {
            console.log('Chain changed:', chainId);
        });
        
        wcProvider.on("disconnect", () => {
            console.log('Disconnected');
        });
        
        return { provider, signer, address };
        
    } catch (error) {
        console.error('WalletConnect error:', error);
    }
}
```

## Multi-Wallet Support

```javascript
class WalletManager {
    constructor() {
        this.provider = null;
        this.signer = null;
        this.account = null;
        this.walletType = null;
    }
    
    async connectMetaMask() {
        if (!window.ethereum) {
            throw new Error('MetaMask not installed');
        }
        
        const provider = new ethers.providers.Web3Provider(window.ethereum);
        await provider.send("eth_requestAccounts", []);
        
        this.provider = provider;
        this.signer = provider.getSigner();
        this.account = await this.signer.getAddress();
        this.walletType = 'metamask';
        
        return this.account;
    }
    
    async connectWalletConnect(infuraId) {
        const wcProvider = new WalletConnectProvider({
            infuraId: infuraId,
            qrcode: true
        });
        
        await wcProvider.enable();
        
        const provider = new ethers.providers.Web3Provider(wcProvider);
        
        this.provider = provider;
        this.signer = provider.getSigner();
        this.account = await this.signer.getAddress();
        this.walletType = 'walletconnect';
        
        return this.account;
    }
    
    async connectCoinbase() {
        // Implement Coinbase Wallet connection
    }
    
    disconnect() {
        if (this.walletType === 'walletconnect' && this.provider.provider.disconnect) {
            this.provider.provider.disconnect();
        }
        
        this.provider = null;
        this.signer = null;
        this.account = null;
        this.walletType = null;
    }
    
    isConnected() {
        return this.account !== null;
    }
}

// Usage
const wallet = new WalletManager();

// Connect with MetaMask
await wallet.connectMetaMask();

// Or connect with WalletConnect
await wallet.connectWalletConnect('YOUR_INFURA_ID');
```

## Handling Transactions

### Send Transaction

```javascript
async function sendTransaction(to, amount) {
    try {
        const tx = await signer.sendTransaction({
            to: to,
            value: ethers.utils.parseEther(amount)
        });
        
        console.log('Transaction sent:', tx.hash);
        
        // Wait for confirmation
        const receipt = await tx.wait();
        console.log('Transaction confirmed:', receipt);
        
        return receipt;
        
    } catch (error) {
        if (error.code === 4001) {
            console.log('User rejected transaction');
        } else if (error.code === 'INSUFFICIENT_FUNDS') {
            console.log('Insufficient funds');
        } else {
            console.error('Transaction failed:', error);
        }
    }
}
```

### Sign Message

```javascript
async function signMessage(message) {
    try {
        const signature = await signer.signMessage(message);
        console.log('Signature:', signature);
        
        // Verify signature
        const address = ethers.utils.verifyMessage(message, signature);
        console.log('Signer address:', address);
        
        return signature;
        
    } catch (error) {
        console.error('Signing failed:', error);
    }
}
```

### Sign Typed Data (EIP-712)

```javascript
async function signTypedData() {
    const domain = {
        name: 'MyDApp',
        version: '1',
        chainId: 1,
        verifyingContract: '0x...'
    };
    
    const types = {
        Mail: [
            { name: 'from', type: 'address' },
            { name: 'to', type: 'address' },
            { name: 'content', type: 'string' }
        ]
    };
    
    const value = {
        from: '0x...',
        to: '0x...',
        content: 'Hello!'
    };
    
    const signature = await signer._signTypedData(domain, types, value);
    console.log('Typed data signature:', signature);
    
    return signature;
}
```

## Network Management

### Switch Network

```javascript
async function switchNetwork(chainId) {
    try {
        await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: ethers.utils.hexValue(chainId) }]
        });
    } catch (error) {
        // Network not added, try adding it
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

## Add Token to Wallet

```javascript
async function addToken(tokenAddress, tokenSymbol, tokenDecimals, tokenImage) {
    try {
        const wasAdded = await window.ethereum.request({
            method: 'wallet_watchAsset',
            params: {
                type: 'ERC20',
                options: {
                    address: tokenAddress,
                    symbol: tokenSymbol,
                    decimals: tokenDecimals,
                    image: tokenImage
                }
            }
        });
        
        if (wasAdded) {
            console.log('Token added!');
        }
    } catch (error) {
        console.error('Failed to add token:', error);
    }
}
```

## Best Practices

### 1. Error Handling

```javascript
const ERROR_CODES = {
    USER_REJECTED: 4001,
    UNAUTHORIZED: 4100,
    UNSUPPORTED_METHOD: 4200,
    DISCONNECTED: 4900,
    CHAIN_DISCONNECTED: 4901
};

function handleWalletError(error) {
    switch (error.code) {
        case ERROR_CODES.USER_REJECTED:
            return 'User rejected the request';
        case ERROR_CODES.UNAUTHORIZED:
            return 'Please connect your wallet';
        case ERROR_CODES.UNSUPPORTED_METHOD:
            return 'This method is not supported';
        case ERROR_CODES.DISCONNECTED:
            return 'Wallet disconnected';
        default:
            return 'An unknown error occurred';
    }
}
```

### 2. Loading States

```javascript
function TransactionButton() {
    const [loading, setLoading] = useState(false);
    
    const handleTransaction = async () => {
        setLoading(true);
        try {
            const tx = await sendTransaction(to, amount);
            await tx.wait();
            alert('Transaction successful!');
        } catch (error) {
            alert('Transaction failed: ' + error.message);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <button onClick={handleTransaction} disabled={loading}>
            {loading ? 'Processing...' : 'Send Transaction'}
        </button>
    );
}
```

### 3. Auto-Connect

```javascript
useEffect(() => {
    // Check if previously connected
    const previouslyConnected = localStorage.getItem('walletConnected');
    
    if (previouslyConnected && window.ethereum) {
        connectWallet().then(() => {
            console.log('Auto-connected');
        });
    }
}, []);

async function connectWallet() {
    // Connection logic...
    localStorage.setItem('walletConnected', 'true');
}

function disconnect() {
    // Disconnection logic...
    localStorage.removeItem('walletConnected');
}
```

## Complete Example

```javascript
import React, { useState, useEffect } from 'react';
import { ethers } from 'ethers';

function WalletManager() {
    const [provider, setProvider] = useState(null);
    const [signer, setSigner] = useState(null);
    const [account, setAccount] = useState(null);
    const [chainId, setChainId] = useState(null);
    const [balance, setBalance] = useState(null);
    
    const connect = async () => {
        if (!window.ethereum) {
            alert('Please install MetaMask!');
            return;
        }
        
        try {
            const provider = new ethers.providers.Web3Provider(window.ethereum);
            await provider.send("eth_requestAccounts", []);
            
            const signer = provider.getSigner();
            const address = await signer.getAddress();
            const network = await provider.getNetwork();
            const balance = await provider.getBalance(address);
            
            setProvider(provider);
            setSigner(signer);
            setAccount(address);
            setChainId(network.chainId);
            setBalance(ethers.utils.formatEther(balance));
            
            localStorage.setItem('walletConnected', 'true');
        } catch (error) {
            console.error('Connection failed:', error);
        }
    };
    
    const disconnect = () => {
        setProvider(null);
        setSigner(null);
        setAccount(null);
        setChainId(null);
        setBalance(null);
        localStorage.removeItem('walletConnected');
    };
    
    useEffect(() => {
        if (localStorage.getItem('walletConnected') === 'true') {
            connect();
        }
    }, []);
    
    useEffect(() => {
        if (!window.ethereum) return;
        
        window.ethereum.on('accountsChanged', (accounts) => {
            if (accounts.length === 0) {
                disconnect();
            } else {
                setAccount(accounts[0]);
            }
        });
        
        window.ethereum.on('chainChanged', () => {
            window.location.reload();
        });
        
        return () => {
            if (window.ethereum.removeListener) {
                window.ethereum.removeListener('accountsChanged', () => {});
                window.ethereum.removeListener('chainChanged', () => {});
            }
        };
    }, []);
    
    return (
        <div>
            {!account ? (
                <button onClick={connect}>Connect Wallet</button>
            ) : (
                <div>
                    <p>Address: {account.slice(0, 6)}...{account.slice(-4)}</p>
                    <p>Balance: {parseFloat(balance).toFixed(4)} ETH</p>
                    <p>Network: {chainId}</p>
                    <button onClick={disconnect}>Disconnect</button>
                </div>
            )}
        </div>
    );
}

export default WalletManager;
```

## Resources

- [MetaMask Documentation](https://docs.metamask.io/)
- [WalletConnect Documentation](https://docs.walletconnect.com/)
- [EIP-1193](https://eips.ethereum.org/EIPS/eip-1193) - Provider API

**Next**: Continue to [DeFi](../06-defi/) →
