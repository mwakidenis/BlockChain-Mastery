# Project 2: Basic Cryptocurrency Wallet 💼

Build a simple cryptocurrency wallet application to send and receive ETH and ERC-20 tokens.

## 🎯 Learning Objectives

- Connect to Ethereum using Web3
- Manage private keys securely
- Send and receive transactions
- Display token balances
- View transaction history

## 📋 Requirements

### Core Features

1. **Wallet Creation**
   - Generate new wallet
   - Import existing wallet (private key/mnemonic)
   - Export wallet (with warnings)

2. **Balance Display**
   - Show ETH balance
   - Show ERC-20 token balances
   - Real-time price updates (optional)

3. **Send Transactions**
   - Send ETH
   - Send ERC-20 tokens
   - Set gas price
   - Transaction confirmation

4. **Transaction History**
   - List past transactions
   - Transaction details
   - Status tracking

### Bonus Features

- QR code generation/scanning
- Multiple wallets
- Address book
- Token swap integration
- Hardware wallet support

## 🛠️ Technology Stack

- **Frontend**: React.js / Vue.js
- **Web3 Library**: ethers.js
- **Storage**: LocalStorage (encrypted)
- **Styling**: Tailwind CSS / Material-UI

## 📚 Getting Started

### Setup

```bash
# Create React app
npx create-react-app crypto-wallet
cd crypto-wallet

# Install dependencies
npm install ethers
npm install @metamask/eth-sig-util
```

### Basic Wallet Structure

```javascript
import { ethers } from 'ethers';

class Wallet {
    constructor() {
        this.provider = null;
        this.wallet = null;
    }
    
    // Create new wallet
    createWallet() {
        this.wallet = ethers.Wallet.createRandom();
        return {
            address: this.wallet.address,
            privateKey: this.wallet.privateKey,
            mnemonic: this.wallet.mnemonic.phrase
        };
    }
    
    // Import wallet from private key
    importWallet(privateKey) {
        this.wallet = new ethers.Wallet(privateKey);
        return this.wallet.address;
    }
    
    // Get balance
    async getBalance(address) {
        if (!this.provider) {
            this.provider = ethers.getDefaultProvider('homestead');
        }
        const balance = await this.provider.getBalance(address);
        return ethers.utils.formatEther(balance);
    }
    
    // Send transaction
    async sendTransaction(to, amount) {
        const tx = {
            to: to,
            value: ethers.utils.parseEther(amount)
        };
        
        const transaction = await this.wallet.sendTransaction(tx);
        await transaction.wait();
        
        return transaction.hash;
    }
}
```

## 🎨 UI Components

### Wallet Dashboard
- Balance display
- Address with copy button
- Send/Receive buttons

### Send Form
- Recipient address input
- Amount input
- Gas price selector
- Confirm button

### Transaction List
- Date/Time
- From/To addresses
- Amount
- Status

## 🔒 Security Considerations

1. ✅ **Never expose private keys**
2. ✅ **Encrypt stored data**
3. ✅ **Use HTTPS only**
4. ✅ **Validate addresses**
5. ✅ **Show warnings for exports**
6. ✅ **Implement seed phrase backup**

## 📖 Resources

- [ethers.js Wallet Documentation](https://docs.ethers.io/v5/api/signer/#Wallet)
- [BIP39 Mnemonic](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)

## ✅ Completion Checklist

- [ ] Create new wallet
- [ ] Import existing wallet
- [ ] Display ETH balance
- [ ] Send ETH transaction
- [ ] View transaction history
- [ ] Add token support
- [ ] Implement security measures
- [ ] Test on testnet
