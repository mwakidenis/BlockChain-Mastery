# ERC-1155 Multi-Token Standard 🎭

ERC-1155 allows a single contract to manage multiple token types, including both fungible and non-fungible tokens.

## Why ERC-1155?

- ✅ **Efficient**: Batch transfers save gas
- ✅ **Flexible**: Mix fungible & non-fungible
- ✅ **Scalable**: Perfect for gaming
- ✅ **Safe**: Built-in safety features

## Standard Interface

```solidity
interface IERC1155 {
    event TransferSingle(address indexed operator, address indexed from, address indexed to, uint256 id, uint256 value);
    event TransferBatch(address indexed operator, address indexed from, address indexed to, uint256[] ids, uint256[] values);
    event ApprovalForAll(address indexed account, address indexed operator, bool approved);
    
    function balanceOf(address account, uint256 id) external view returns (uint256);
    function balanceOfBatch(address[] calldata accounts, uint256[] calldata ids) external view returns (uint256[] memory);
    function setApprovalForAll(address operator, bool approved) external;
    function isApprovedForAll(address account, address operator) external view returns (bool);
    function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes calldata data) external;
    function safeBatchTransferFrom(address from, address to, uint256[] calldata ids, uint256[] calldata amounts, bytes calldata data) external;
}
```

## Basic Implementation

```solidity
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GameItems is ERC1155, Ownable {
    uint256 public constant GOLD = 0;
    uint256 public constant SILVER = 1;
    uint256 public constant SWORD = 2;
    uint256 public constant SHIELD = 3;
    
    constructor() ERC1155("https://game.example/api/item/{id}.json") {}
    
    function mint(address to, uint256 id, uint256 amount) public onlyOwner {
        _mint(to, id, amount, "");
    }
    
    function mintBatch(address to, uint256[] memory ids, uint256[] memory amounts) public onlyOwner {
        _mintBatch(to, ids, amounts, "");
    }
}
```

## Gaming Use Case

```solidity
contract RPGItems is ERC1155 {
    // Token IDs
    uint256 public constant HEALTH_POTION = 1;
    uint256 public constant MANA_POTION = 2;
    uint256 public constant LEGENDARY_SWORD = 1000;
    
    mapping(uint256 => bool) public isNFT;
    mapping(uint256 => uint256) public maxSupply;
    mapping(uint256 => uint256) public currentSupply;
    
    constructor() ERC1155("ipfs://.../{id}.json") {
        // Fungible items (unlimited supply)
        maxSupply[HEALTH_POTION] = type(uint256).max;
        maxSupply[MANA_POTION] = type(uint256).max;
        
        // NFT items (limited supply)
        isNFT[LEGENDARY_SWORD] = true;
        maxSupply[LEGENDARY_SWORD] = 100;
    }
    
    function craft(uint256 id, uint256 amount) public {
        require(currentSupply[id] + amount <= maxSupply[id], "Exceeds max supply");
        
        currentSupply[id] += amount;
        _mint(msg.sender, id, amount, "");
    }
}
```

## Batch Operations

### Batch Transfer

```javascript
async function batchTransfer(to, tokenIds, amounts) {
    const tx = await contract.safeBatchTransferFrom(
        await signer.getAddress(),
        to,
        tokenIds,
        amounts,
        "0x"
    );
    await tx.wait();
    console.log("Batch transferred!");
}

// Example: Transfer multiple items at once
await batchTransfer(
    recipientAddress,
    [1, 2, 3],      // Token IDs
    [100, 50, 1]    // Amounts
);
```

### Batch Minting

```solidity
function airdrop(address[] memory recipients, uint256 tokenId, uint256 amount) public {
    for (uint i = 0; i < recipients.length; i++) {
        _mint(recipients[i], tokenId, amount, "");
    }
}
```

## NFT Collection

```solidity
contract NFTCollection is ERC1155 {
    uint256 private _currentTokenId;
    mapping(uint256 => string) private _tokenURIs;
    
    function mintNFT(address to, string memory tokenURI) public returns (uint256) {
        _currentTokenId++;
        uint256 newTokenId = _currentTokenId;
        
        _mint(to, newTokenId, 1, "");
        _tokenURIs[newTokenId] = tokenURI;
        
        return newTokenId;
    }
    
    function uri(uint256 tokenId) public view override returns (string memory) {
        return _tokenURIs[tokenId];
    }
}
```

## Metadata

```json
{
  "name": "Legendary Sword",
  "description": "A powerful sword forged by ancient smiths",
  "image": "ipfs://QmXyz.../sword.png",
  "properties": {
    "attack": 100,
    "durability": 500,
    "rarity": "legendary"
  }
}
```

## JavaScript Integration

```javascript
import { ethers } from 'ethers';

const contract = new ethers.Contract(
    CONTRACT_ADDRESS,
    ERC1155_ABI,
    signer
);

// Check balance
async function getBalance(account, tokenId) {
    const balance = await contract.balanceOf(account, tokenId);
    console.log(`Balance of token ${tokenId}:`, balance.toString());
    return balance;
}

// Check multiple balances at once
async function getBatchBalances(accounts, tokenIds) {
    const balances = await contract.balanceOfBatch(accounts, tokenIds);
    return balances;
}

// Transfer tokens
async function transfer(to, tokenId, amount) {
    const tx = await contract.safeTransferFrom(
        await signer.getAddress(),
        to,
        tokenId,
        amount,
        "0x"
    );
    await tx.wait();
}
```

## ERC-721 vs ERC-1155

| Feature | ERC-721 | ERC-1155 |
|---------|---------|----------|
| **Token Types** | NFT only | NFT + Fungible |
| **Batch Transfer** | No | Yes |
| **Gas Efficiency** | Lower | Higher |
| **Use Case** | Art, Collectibles | Gaming, Tickets |
| **Complexity** | Simple | More complex |

## Resources

- [EIP-1155 Specification](https://eips.ethereum.org/EIPS/eip-1155)
- [OpenZeppelin ERC1155](https://docs.openzeppelin.com/contracts/erc1155)

**Next**: [Metadata Standards](metadata-standards.md) →
