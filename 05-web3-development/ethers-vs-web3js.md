# Ethers.js vs Web3.js ⚖️

A comprehensive comparison of the two most popular JavaScript libraries for Ethereum development.

## Overview

Both **Ethers.js** and **Web3.js** allow you to interact with Ethereum, but they have different philosophies and features.

## Quick Comparison

| Feature | Ethers.js | Web3.js |
|---------|-----------|---------|
| **Size** | ~88 KB | ~500 KB |
| **TypeScript** | Built-in | Community types |
| **License** | MIT | LGPL |
| **API Design** | Modern, clean | More complex |
| **Documentation** | Excellent | Good |
| **Maintenance** | Active | Active |
| **ENS Support** | Native | Plugin |
| **Community** | Growing | Established |

## Installation

```bash
# Ethers.js
npm install ethers

# Web3.js
npm install web3
```

## Basic Setup

### Ethers.js
```javascript
import { ethers } from 'ethers';

// Connect to provider
const provider = new ethers.providers.Web3Provider(window.ethereum);
const signer = provider.getSigner();
```

### Web3.js
```javascript
import Web3 from 'web3';

// Connect to provider
const web3 = new Web3(window.ethereum);
const accounts = await web3.eth.getAccounts();
```

## Reading Data

### Get Balance

**Ethers.js**:
```javascript
const balance = await provider.getBalance(address);
console.log(ethers.utils.formatEther(balance));
```

**Web3.js**:
```javascript
const balance = await web3.eth.getBalance(address);
console.log(web3.utils.fromWei(balance, 'ether'));
```

### Get Block

**Ethers.js**:
```javascript
const block = await provider.getBlock('latest');
console.log(block.number);
```

**Web3.js**:
```javascript
const block = await web3.eth.getBlock('latest');
console.log(block.number);
```

## Interacting with Contracts

### Reading Contract Data

**Ethers.js**:
```javascript
const abi = ["function balanceOf(address) view returns (uint256)"];
const contract = new ethers.Contract(address, abi, provider);

const balance = await contract.balanceOf(userAddress);
console.log(ethers.utils.formatUnits(balance, 18));
```

**Web3.js**:
```javascript
const contract = new web3.eth.Contract(abi, address);

const balance = await contract.methods.balanceOf(userAddress).call();
console.log(web3.utils.fromWei(balance, 'ether'));
```

### Writing to Contracts

**Ethers.js**:
```javascript
const contract = new ethers.Contract(address, abi, signer);

const tx = await contract.transfer(recipient, amount);
await tx.wait(); // Wait for confirmation
```

**Web3.js**:
```javascript
const contract = new web3.eth.Contract(abi, address);

await contract.methods
    .transfer(recipient, amount)
    .send({ from: accounts[0] });
```

## Sending Transactions

### Simple Transfer

**Ethers.js**:
```javascript
const tx = await signer.sendTransaction({
    to: recipient,
    value: ethers.utils.parseEther("1.0")
});

const receipt = await tx.wait();
console.log(receipt.transactionHash);
```

**Web3.js**:
```javascript
const receipt = await web3.eth.sendTransaction({
    from: accounts[0],
    to: recipient,
    value: web3.utils.toWei('1', 'ether')
});

console.log(receipt.transactionHash);
```

## Event Listening

**Ethers.js**:
```javascript
contract.on("Transfer", (from, to, amount, event) => {
    console.log(`Transfer: ${from} -> ${to}: ${amount}`);
});

// Query past events
const filter = contract.filters.Transfer(null, recipient);
const events = await contract.queryFilter(filter);
```

**Web3.js**:
```javascript
contract.events.Transfer({
    filter: { to: recipient }
}, (error, event) => {
    console.log(event.returnValues);
});

// Get past events
const events = await contract.getPastEvents('Transfer', {
    filter: { to: recipient },
    fromBlock: 0,
    toBlock: 'latest'
});
```

## Utilities

### Format Numbers

**Ethers.js**:
```javascript
// Parse (string to BigNumber)
const amount = ethers.utils.parseEther("1.0");
const tokens = ethers.utils.parseUnits("100", 18);

// Format (BigNumber to string)
const formatted = ethers.utils.formatEther(amount);
const tokenAmount = ethers.utils.formatUnits(tokens, 18);
```

**Web3.js**:
```javascript
// Convert
const amount = web3.utils.toWei('1', 'ether');
const formatted = web3.utils.fromWei(amount, 'ether');

// BN operations
const bn = web3.utils.toBN('1000000000000000000');
```

### Signing Messages

**Ethers.js**:
```javascript
const message = "Hello World";
const signature = await signer.signMessage(message);

// Verify
const address = ethers.utils.verifyMessage(message, signature);
```

**Web3.js**:
```javascript
const message = "Hello World";
const signature = await web3.eth.personal.sign(message, accounts[0]);

// Verify
const address = await web3.eth.personal.ecRecover(message, signature);
```

## When to Use Each

### Use Ethers.js if:
- ✅ Building new projects
- ✅ Want smaller bundle size
- ✅ Prefer modern API
- ✅ Need TypeScript support
- ✅ Want native ENS resolution

### Use Web3.js if:
- ✅ Working with legacy code
- ✅ Team familiar with it
- ✅ Need specific Web3 plugins
- ✅ Required by framework

## Migration Guide

### Web3.js to Ethers.js

```javascript
// Web3.js
const web3 = new Web3(window.ethereum);
const balance = await web3.eth.getBalance(address);
const formatted = web3.utils.fromWei(balance, 'ether');

// Ethers.js equivalent
const provider = new ethers.providers.Web3Provider(window.ethereum);
const balance = await provider.getBalance(address);
const formatted = ethers.utils.formatEther(balance);
```

## Best Practices

### Ethers.js
```javascript
// Always use try-catch
try {
    const tx = await contract.transfer(to, amount);
    await tx.wait(); // Always wait for confirmation
} catch (error) {
    console.error("Transaction failed:", error);
}

// Use human-readable ABI
const abi = [
    "function transfer(address to, uint amount)",
    "event Transfer(address indexed from, address indexed to, uint amount)"
];
```

### Web3.js
```javascript
// Handle promises properly
try {
    const receipt = await contract.methods
        .transfer(to, amount)
        .send({ from: account });
} catch (error) {
    console.error("Transaction failed:", error);
}
```

## Resources

- [Ethers.js Documentation](https://docs.ethers.io/)
- [Web3.js Documentation](https://web3js.readthedocs.io/)

**Next**: [Wallet Integration](wallet-integration.md) →
