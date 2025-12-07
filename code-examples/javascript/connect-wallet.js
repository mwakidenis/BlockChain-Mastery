/**
 * Web3 Wallet Connection Examples
 * Using ethers.js v6
 */

// ============================================
// 1. BASIC METAMASK CONNECTION
// ============================================

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
        
        // Create provider
        const provider = new ethers.BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();
        const address = await signer.getAddress();
        
        console.log('Signer address:', address);
        
        // Get balance
        const balance = await provider.getBalance(address);
        const balanceInEth = ethers.formatEther(balance);
        
        console.log('Balance:', balanceInEth, 'ETH');
        
        return { provider, signer, address, balance: balanceInEth };
    } catch (error) {
        console.error('Error connecting to MetaMask:', error);
    }
}

// ============================================
// 2. LISTEN TO ACCOUNT CHANGES
// ============================================

function listenToAccountChanges() {
    if (window.ethereum) {
        window.ethereum.on('accountsChanged', (accounts) => {
            console.log('Account changed:', accounts[0]);
            // Reload page or update UI
            window.location.reload();
        });
        
        window.ethereum.on('chainChanged', (chainId) => {
            console.log('Network changed:', chainId);
            // Reload page when network changes
            window.location.reload();
        });
    }
}

// ============================================
// 3. SWITCH NETWORK
// ============================================

async function switchNetwork(chainId) {
    try {
        await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: `0x${chainId.toString(16)}` }],
        });
    } catch (error) {
        // This error code indicates that the chain has not been added to MetaMask
        if (error.code === 4902) {
            console.log('Network not added, attempting to add...');
            await addNetwork(chainId);
        } else {
            console.error('Error switching network:', error);
        }
    }
}

// ============================================
// 4. ADD CUSTOM NETWORK
// ============================================

async function addNetwork(chainId) {
    const networks = {
        137: { // Polygon
            chainId: '0x89',
            chainName: 'Polygon Mainnet',
            nativeCurrency: {
                name: 'MATIC',
                symbol: 'MATIC',
                decimals: 18
            },
            rpcUrls: ['https://polygon-rpc.com/'],
            blockExplorerUrls: ['https://polygonscan.com/']
        },
        80001: { // Mumbai Testnet
            chainId: '0x13881',
            chainName: 'Mumbai Testnet',
            nativeCurrency: {
                name: 'MATIC',
                symbol: 'MATIC',
                decimals: 18
            },
            rpcUrls: ['https://rpc-mumbai.maticvigil.com/'],
            blockExplorerUrls: ['https://mumbai.polygonscan.com/']
        }
    };
    
    try {
        await window.ethereum.request({
            method: 'wallet_addEthereumChain',
            params: [networks[chainId]],
        });
    } catch (error) {
        console.error('Error adding network:', error);
    }
}

// ============================================
// 5. READ SMART CONTRACT DATA
// ============================================

async function readContract() {
    const provider = new ethers.BrowserProvider(window.ethereum);
    
    // ERC-20 Token ABI (partial)
    const tokenABI = [
        "function name() view returns (string)",
        "function symbol() view returns (string)",
        "function decimals() view returns (uint8)",
        "function totalSupply() view returns (uint256)",
        "function balanceOf(address) view returns (uint256)"
    ];
    
    // Example: Read USDC on Ethereum
    const tokenAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
    const contract = new ethers.Contract(tokenAddress, tokenABI, provider);
    
    try {
        const name = await contract.name();
        const symbol = await contract.symbol();
        const decimals = await contract.decimals();
        const totalSupply = await contract.totalSupply();
        
        console.log('Token Name:', name);
        console.log('Symbol:', symbol);
        console.log('Decimals:', decimals);
        console.log('Total Supply:', ethers.formatUnits(totalSupply, decimals));
        
        // Get user's balance
        const signer = await provider.getSigner();
        const address = await signer.getAddress();
        const balance = await contract.balanceOf(address);
        
        console.log('Your Balance:', ethers.formatUnits(balance, decimals), symbol);
    } catch (error) {
        console.error('Error reading contract:', error);
    }
}

// ============================================
// 6. SEND TRANSACTION
// ============================================

async function sendTransaction(toAddress, amountInEth) {
    try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();
        
        // Create transaction
        const tx = {
            to: toAddress,
            value: ethers.parseEther(amountInEth.toString())
        };
        
        // Send transaction
        const transaction = await signer.sendTransaction(tx);
        console.log('Transaction sent:', transaction.hash);
        
        // Wait for confirmation
        const receipt = await transaction.wait();
        console.log('Transaction confirmed in block:', receipt.blockNumber);
        
        return receipt;
    } catch (error) {
        console.error('Error sending transaction:', error);
    }
}

// ============================================
// 7. INTERACT WITH SMART CONTRACT
// ============================================

async function transferTokens(tokenAddress, toAddress, amount) {
    try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();
        
        const tokenABI = [
            "function transfer(address to, uint256 amount) returns (bool)"
        ];
        
        const contract = new ethers.Contract(tokenAddress, tokenABI, signer);
        
        // Send transaction
        const tx = await contract.transfer(toAddress, ethers.parseUnits(amount, 18));
        console.log('Transaction sent:', tx.hash);
        
        // Wait for confirmation
        const receipt = await tx.wait();
        console.log('Transfer confirmed!');
        
        return receipt;
    } catch (error) {
        console.error('Error transferring tokens:', error);
    }
}

// ============================================
// 8. SIGN MESSAGE
// ============================================

async function signMessage(message) {
    try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();
        
        // Sign message
        const signature = await signer.signMessage(message);
        console.log('Signature:', signature);
        
        // Verify signature
        const address = await signer.getAddress();
        const recoveredAddress = ethers.verifyMessage(message, signature);
        
        console.log('Signer address:', address);
        console.log('Recovered address:', recoveredAddress);
        console.log('Valid signature:', address === recoveredAddress);
        
        return signature;
    } catch (error) {
        console.error('Error signing message:', error);
    }
}

// ============================================
// 9. GET TRANSACTION HISTORY
// ============================================

async function getTransactionHistory(address, startBlock = 0) {
    const provider = new ethers.BrowserProvider(window.ethereum);
    
    try {
        // Get current block
        const currentBlock = await provider.getBlockNumber();
        
        // Query recent transactions (last 1000 blocks)
        const endBlock = currentBlock;
        const fromBlock = Math.max(startBlock, currentBlock - 1000);
        
        // This would require an API or indexer like Etherscan API
        // For demo purposes, we'll just get the latest transaction
        const history = await provider.getTransactionCount(address);
        
        console.log('Transaction count:', history);
        
        return history;
    } catch (error) {
        console.error('Error getting transaction history:', error);
    }
}

// ============================================
// 10. LISTEN TO CONTRACT EVENTS
// ============================================

async function listenToTokenTransfers(tokenAddress, userAddress) {
    const provider = new ethers.BrowserProvider(window.ethereum);
    
    const tokenABI = [
        "event Transfer(address indexed from, address indexed to, uint256 value)"
    ];
    
    const contract = new ethers.Contract(tokenAddress, tokenABI, provider);
    
    // Filter for transfers involving user
    const filterFrom = contract.filters.Transfer(userAddress, null);
    const filterTo = contract.filters.Transfer(null, userAddress);
    
    // Listen to events
    contract.on(filterFrom, (from, to, amount, event) => {
        console.log('Sent:', ethers.formatEther(amount), 'to', to);
    });
    
    contract.on(filterTo, (from, to, amount, event) => {
        console.log('Received:', ethers.formatEther(amount), 'from', from);
    });
    
    console.log('Listening to Transfer events...');
}

// ============================================
// USAGE EXAMPLE
// ============================================

async function main() {
    // Connect wallet
    const wallet = await connectMetaMask();
    
    // Listen to changes
    listenToAccountChanges();
    
    // Read contract data
    await readContract();
    
    // Send transaction (commented out for safety)
    // await sendTransaction('0x...', 0.01);
    
    // Sign message
    await signMessage('Hello, Blockchain!');
}

// Export functions for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        connectMetaMask,
        switchNetwork,
        readContract,
        sendTransaction,
        transferTokens,
        signMessage
    };
}
