# Project 5: NFT Marketplace 🎨

Build a complete NFT marketplace where users can mint, list, buy, and sell NFTs.

## 🎯 Learning Objectives

- ERC-721 implementation
- IPFS integration
- Marketplace contracts
- NFT metadata
- Frontend for NFTs

## 📋 Features

### Smart Contracts

1. **NFT Contract**
   - Mint NFTs
   - Metadata URIs
   - Royalties

2. **Marketplace Contract**
   - List NFTs
   - Buy NFTs
   - Cancel listings
   - Fee collection

### Frontend

- Mint NFT interface
- Browse marketplace
- List your NFTs
- Buy NFTs
- Profile page

## 🛠️ Smart Contracts

```solidity
// NFT Contract
contract MyNFT is ERC721 {
    uint256 private _tokenIdCounter;
    mapping(uint256 => string) private _tokenURIs;
    
    function mint(string memory tokenURI) public returns (uint256) {
        uint256 tokenId = _tokenIdCounter++;
        _safeMint(msg.sender, tokenId);
        _tokenURIs[tokenId] = tokenURI;
        return tokenId;
    }
}

// Marketplace Contract
contract NFTMarketplace {
    struct Listing {
        address seller;
        uint256 price;
        bool active;
    }
    
    mapping(address => mapping(uint256 => Listing)) public listings;
    
    function list(address nft, uint256 tokenId, uint256 price) external {
        IERC721(nft).transferFrom(msg.sender, address(this), tokenId);
        
        listings[nft][tokenId] = Listing({
            seller: msg.sender,
            price: price,
            active: true
        });
    }
    
    function buy(address nft, uint256 tokenId) external payable {
        Listing storage listing = listings[nft][tokenId];
        require(listing.active, "Not listed");
        require(msg.value >= listing.price, "Insufficient payment");
        
        listing.active = false;
        
        IERC721(nft).transferFrom(address(this), msg.sender, tokenId);
        payable(listing.seller).transfer(msg.value);
    }
}
```

## ✅ Completion Checklist

- [ ] Create NFT contract
- [ ] Create marketplace contract
- [ ] Deploy contracts
- [ ] IPFS integration
- [ ] Minting interface
- [ ] Listing functionality
- [ ] Buying functionality
- [ ] Profile page
- [ ] Test thoroughly
