# ERC-721 Standard 📜

The ERC-721 standard defines non-fungible tokens (NFTs) on Ethereum. Each token is unique and cannot be replaced with another.

## Standard Interface

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC721 {
    // Events
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);
    
    // Required functions
    function balanceOf(address owner) external view returns (uint256 balance);
    function ownerOf(uint256 tokenId) external view returns (address owner);
    function safeTransferFrom(address from, address to, uint256 tokenId) external;
    function transferFrom(address from, address to, uint256 tokenId) external;
    function approve(address to, uint256 tokenId) external;
    function getApproved(uint256 tokenId) external view returns (address operator);
    function setApprovalForAll(address operator, bool approved) external;
    function isApprovedForAll(address owner, address operator) external view returns (bool);
}
```

## Basic Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721, Ownable {
    uint256 private _tokenIdCounter;
    string private _baseTokenURI;
    
    constructor() ERC721("MyNFT", "MNFT") {}
    
    function mint(address to) public onlyOwner {
        _tokenIdCounter++;
        _safeMint(to, _tokenIdCounter);
    }
    
    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }
    
    function setBaseURI(string memory baseURI) public onlyOwner {
        _baseTokenURI = baseURI;
    }
    
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "Token does not exist");
        return string(abi.encodePacked(_baseURI(), Strings.toString(tokenId), ".json"));
    }
}
```

## Advanced Features

### Minting with Metadata

```solidity
contract NFTWithMetadata is ERC721 {
    struct TokenMetadata {
        string name;
        string description;
        string image;
    }
    
    mapping(uint256 => TokenMetadata) public metadata;
    
    function mintWithMetadata(
        address to,
        string memory name,
        string memory description,
        string memory image
    ) public {
        uint256 tokenId = _tokenIdCounter++;
        _safeMint(to, tokenId);
        
        metadata[tokenId] = TokenMetadata(name, description, image);
    }
}
```

### Royalties (EIP-2981)

```solidity
import "@openzeppelin/contracts/token/common/ERC2981.sol";

contract NFTWithRoyalties is ERC721, ERC2981 {
    constructor() ERC721("MyNFT", "MNFT") {
        // Set 5% royalty
        _setDefaultRoyalty(owner(), 500); // 500 = 5%
    }
    
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC2981)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

### Enumerable Extension

```solidity
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

contract EnumerableNFT is ERC721Enumerable {
    // Track all tokens by owner
    function tokensOfOwner(address owner) public view returns (uint256[] memory) {
        uint256 balance = balanceOf(owner);
        uint256[] memory tokens = new uint256[](balance);
        
        for (uint256 i = 0; i < balance; i++) {
            tokens[i] = tokenOfOwnerByIndex(owner, i);
        }
        
        return tokens;
    }
}
```

## Minting Strategies

### Fixed Supply

```solidity
contract FixedSupplyNFT is ERC721 {
    uint256 public constant MAX_SUPPLY = 10000;
    uint256 private _tokenIdCounter;
    
    function mint() public payable {
        require(_tokenIdCounter < MAX_SUPPLY, "Max supply reached");
        require(msg.value >= 0.05 ether, "Insufficient payment");
        
        _tokenIdCounter++;
        _safeMint(msg.sender, _tokenIdCounter);
    }
}
```

### Whitelist Minting

```solidity
contract WhitelistNFT is ERC721, Ownable {
    mapping(address => bool) public whitelist;
    mapping(address => bool) public hasMinted;
    
    function addToWhitelist(address[] memory addresses) public onlyOwner {
        for (uint i = 0; i < addresses.length; i++) {
            whitelist[addresses[i]] = true;
        }
    }
    
    function mint() public {
        require(whitelist[msg.sender], "Not whitelisted");
        require(!hasMinted[msg.sender], "Already minted");
        
        hasMinted[msg.sender] = true;
        _safeMint(msg.sender, _tokenIdCounter++);
    }
}
```

### Dutch Auction

```solidity
contract DutchAuctionNFT is ERC721 {
    uint256 public startPrice = 1 ether;
    uint256 public endPrice = 0.1 ether;
    uint256 public startTime;
    uint256 public duration = 1 days;
    
    constructor() {
        startTime = block.timestamp;
    }
    
    function getCurrentPrice() public view returns (uint256) {
        if (block.timestamp >= startTime + duration) {
            return endPrice;
        }
        
        uint256 elapsed = block.timestamp - startTime;
        uint256 decrease = ((startPrice - endPrice) * elapsed) / duration;
        
        return startPrice - decrease;
    }
    
    function mint() public payable {
        uint256 price = getCurrentPrice();
        require(msg.value >= price, "Insufficient payment");
        
        _safeMint(msg.sender, _tokenIdCounter++);
        
        // Refund excess
        if (msg.value > price) {
            payable(msg.sender).transfer(msg.value - price);
        }
    }
}
```

## Interacting with ERC-721

### JavaScript/TypeScript

```javascript
import { ethers } from 'ethers';

// Connect to contract
const nftContract = new ethers.Contract(
    NFT_ADDRESS,
    NFT_ABI,
    signer
);

// Mint NFT
async function mintNFT() {
    const tx = await nftContract.mint({
        value: ethers.utils.parseEther("0.05")
    });
    await tx.wait();
    console.log("NFT minted!");
}

// Get token owner
async function getOwner(tokenId) {
    const owner = await nftContract.ownerOf(tokenId);
    console.log("Owner:", owner);
    return owner;
}

// Transfer NFT
async function transferNFT(to, tokenId) {
    const tx = await nftContract.transferFrom(
        await signer.getAddress(),
        to,
        tokenId
    );
    await tx.wait();
    console.log("NFT transferred!");
}

// Get all tokens owned by address
async function getTokensOfOwner(owner) {
    const balance = await nftContract.balanceOf(owner);
    const tokens = [];
    
    for (let i = 0; i < balance; i++) {
        const tokenId = await nftContract.tokenOfOwnerByIndex(owner, i);
        tokens.push(tokenId.toString());
    }
    
    return tokens;
}

// Get token metadata
async function getMetadata(tokenId) {
    const uri = await nftContract.tokenURI(tokenId);
    const response = await fetch(uri);
    const metadata = await response.json();
    
    return metadata;
}
```

## Testing

```javascript
const { expect } = require("chai");

describe("NFT Contract", function() {
    let nft, owner, addr1;
    
    beforeEach(async function() {
        [owner, addr1] = await ethers.getSigners();
        const NFT = await ethers.getContractFactory("MyNFT");
        nft = await NFT.deploy();
    });
    
    it("Should mint NFT", async function() {
        await nft.mint(addr1.address);
        expect(await nft.ownerOf(1)).to.equal(addr1.address);
    });
    
    it("Should transfer NFT", async function() {
        await nft.mint(owner.address);
        await nft.transferFrom(owner.address, addr1.address, 1);
        expect(await nft.ownerOf(1)).to.equal(addr1.address);
    });
    
    it("Should track balance", async function() {
        await nft.mint(addr1.address);
        await nft.mint(addr1.address);
        expect(await nft.balanceOf(addr1.address)).to.equal(2);
    });
});
```

## Gas Optimization

### Batch Minting

```solidity
function batchMint(address to, uint256 quantity) public {
    for (uint256 i = 0; i < quantity; i++) {
        _safeMint(to, _tokenIdCounter++);
    }
}
```

### ERC721A (Optimized)

```solidity
import "erc721a/contracts/ERC721A.sol";

contract OptimizedNFT is ERC721A {
    constructor() ERC721A("MyNFT", "MNFT") {}
    
    // Batch mint with O(1) cost per token
    function mint(uint256 quantity) public payable {
        _safeMint(msg.sender, quantity);
    }
}
```

## Security Considerations

1. **Reentrancy**: Use OpenZeppelin's ReentrancyGuard
2. **Access Control**: Properly restrict minting functions
3. **Integer Overflow**: Use Solidity 0.8+ or SafeMath
4. **Metadata Validation**: Validate IPFS hashes
5. **Gas Limits**: Be careful with loops

## Resources

- [EIP-721 Specification](https://eips.ethereum.org/EIPS/eip-721)
- [OpenZeppelin ERC721](https://docs.openzeppelin.com/contracts/erc721)
- [ERC721A](https://www.erc721a.org/)

**Next**: [ERC-1155 Standard](erc1155-standard.md) →
