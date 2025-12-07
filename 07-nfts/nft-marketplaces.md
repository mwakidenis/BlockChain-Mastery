# NFT Marketplaces 🏪

Learn how NFT marketplaces work and how to integrate your NFT collection with platforms like OpenSea.

## How Marketplaces Work

### Core Functions

1. **Listing**: Sellers list NFTs for sale
2. **Discovery**: Buyers browse listings
3. **Trading**: Execute trades on-chain
4. **Royalties**: Distribute creator royalties

### Fee Structure

| Marketplace | Trading Fee | Creator Royalty |
|-------------|-------------|-----------------|
| **OpenSea** | 2.5% | 0-10% |
| **Rarible** | 1-2.5% | 0-50% |
| **LooksRare** | 2% | 0-10% |
| **Blur** | 0.5% | 0-10% |

## Marketplace Contract

### Basic Marketplace

```solidity
contract NFTMarketplace {
    struct Listing {
        address seller;
        address nftContract;
        uint256 tokenId;
        uint256 price;
        bool active;
    }
    
    mapping(bytes32 => Listing) public listings;
    uint256 public feePercent = 25; // 2.5%
    
    event Listed(address indexed seller, address indexed nftContract, uint256 indexed tokenId, uint256 price);
    event Sold(address indexed buyer, address indexed nftContract, uint256 indexed tokenId, uint256 price);
    
    function list(address nftContract, uint256 tokenId, uint256 price) external {
        IERC721 nft = IERC721(nftContract);
        require(nft.ownerOf(tokenId) == msg.sender, "Not owner");
        require(nft.isApprovedForAll(msg.sender, address(this)), "Not approved");
        
        bytes32 listingId = keccak256(abi.encodePacked(nftContract, tokenId));
        
        listings[listingId] = Listing({
            seller: msg.sender,
            nftContract: nftContract,
            tokenId: tokenId,
            price: price,
            active: true
        });
        
        emit Listed(msg.sender, nftContract, tokenId, price);
    }
    
    function buy(address nftContract, uint256 tokenId) external payable {
        bytes32 listingId = keccak256(abi.encodePacked(nftContract, tokenId));
        Listing storage listing = listings[listingId];
        
        require(listing.active, "Not listed");
        require(msg.value >= listing.price, "Insufficient payment");
        
        listing.active = false;
        
        // Calculate fees
        uint256 fee = (listing.price * feePercent) / 1000;
        uint256 sellerAmount = listing.price - fee;
        
        // Transfer NFT
        IERC721(nftContract).safeTransferFrom(listing.seller, msg.sender, tokenId);
        
        // Transfer funds
        payable(listing.seller).transfer(sellerAmount);
        
        emit Sold(msg.sender, nftContract, tokenId, listing.price);
    }
    
    function cancel(address nftContract, uint256 tokenId) external {
        bytes32 listingId = keccak256(abi.encodePacked(nftContract, tokenId));
        Listing storage listing = listings[listingId];
        
        require(listing.seller == msg.sender, "Not seller");
        require(listing.active, "Not active");
        
        listing.active = false;
    }
}
```

### Auction System

```solidity
contract NFTAuction {
    struct Auction {
        address seller;
        address nftContract;
        uint256 tokenId;
        uint256 startPrice;
        uint256 highestBid;
        address highestBidder;
        uint256 endTime;
        bool active;
    }
    
    mapping(bytes32 => Auction) public auctions;
    
    function createAuction(
        address nftContract,
        uint256 tokenId,
        uint256 startPrice,
        uint256 duration
    ) external {
        bytes32 auctionId = keccak256(abi.encodePacked(nftContract, tokenId));
        
        auctions[auctionId] = Auction({
            seller: msg.sender,
            nftContract: nftContract,
            tokenId: tokenId,
            startPrice: startPrice,
            highestBid: 0,
            highestBidder: address(0),
            endTime: block.timestamp + duration,
            active: true
        });
        
        IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);
    }
    
    function bid(address nftContract, uint256 tokenId) external payable {
        bytes32 auctionId = keccak256(abi.encodePacked(nftContract, tokenId));
        Auction storage auction = auctions[auctionId];
        
        require(auction.active, "Auction not active");
        require(block.timestamp < auction.endTime, "Auction ended");
        require(msg.value > auction.highestBid, "Bid too low");
        require(msg.value >= auction.startPrice, "Below start price");
        
        // Refund previous bidder
        if (auction.highestBidder != address(0)) {
            payable(auction.highestBidder).transfer(auction.highestBid);
        }
        
        auction.highestBid = msg.value;
        auction.highestBidder = msg.sender;
    }
    
    function endAuction(address nftContract, uint256 tokenId) external {
        bytes32 auctionId = keccak256(abi.encodePacked(nftContract, tokenId));
        Auction storage auction = auctions[auctionId];
        
        require(auction.active, "Auction not active");
        require(block.timestamp >= auction.endTime, "Auction not ended");
        
        auction.active = false;
        
        if (auction.highestBidder != address(0)) {
            // Transfer NFT to winner
            IERC721(nftContract).transferFrom(
                address(this),
                auction.highestBidder,
                tokenId
            );
            
            // Transfer funds to seller
            payable(auction.seller).transfer(auction.highestBid);
        } else {
            // No bids, return NFT
            IERC721(nftContract).transferFrom(
                address(this),
                auction.seller,
                tokenId
            );
        }
    }
}
```

## OpenSea Integration

### Make Collection OpenSea Compatible

```solidity
contract OpenSeaCompatible is ERC721 {
    // Contract-level metadata for OpenSea
    function contractURI() public pure returns (string memory) {
        return "ipfs://QmXyz.../collection.json";
    }
    
    // Override approval to enable OpenSea trading
    function isApprovedForAll(address owner, address operator)
        public
        view
        override
        returns (bool)
    {
        // OpenSea proxy registry
        if (operator == 0x58807baD0B376efc12F5AD86aAc70E78ed67deaE) {
            return true;
        }
        
        return super.isApprovedForAll(owner, operator);
    }
}
```

### Collection Metadata

```json
{
  "name": "My NFT Collection",
  "description": "A collection of unique digital art",
  "image": "ipfs://QmXyz.../banner.png",
  "external_link": "https://mynft.com",
  "seller_fee_basis_points": 500,
  "fee_recipient": "0x..."
}
```

## Off-Chain Orders (OpenSea Seaport)

```javascript
import { Seaport } from "@opensea/seaport-js";

const seaport = new Seaport(provider);

// Create listing
async function createListing(nftAddress, tokenId, price) {
    const order = await seaport.createOrder({
        offer: [{
            itemType: 2, // ERC721
            token: nftAddress,
            identifier: tokenId
        }],
        consideration: [{
            amount: ethers.utils.parseEther(price),
            recipient: await signer.getAddress()
        }]
    });
    
    return order;
}

// Fulfill order (buy)
async function fulfillOrder(order) {
    const tx = await seaport.fulfillOrder({
        order,
        accountAddress: await signer.getAddress()
    });
    
    return tx;
}
```

## Royalty Implementation

### EIP-2981

```solidity
import "@openzeppelin/contracts/token/common/ERC2981.sol";

contract NFTWithRoyalty is ERC721, ERC2981 {
    constructor() ERC721("MyNFT", "MNFT") {
        // 5% royalty to creator
        _setDefaultRoyalty(msg.sender, 500);
    }
    
    // Set per-token royalty
    function setTokenRoyalty(uint256 tokenId, address receiver, uint96 feeNumerator) 
        external 
        onlyOwner 
    {
        _setTokenRoyalty(tokenId, receiver, feeNumerator);
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

### Query Royalty Info

```javascript
async function getRoyaltyInfo(nftContract, tokenId, salePrice) {
    const [receiver, royaltyAmount] = await nftContract.royaltyInfo(
        tokenId,
        salePrice
    );
    
    console.log('Royalty receiver:', receiver);
    console.log('Royalty amount:', ethers.utils.formatEther(royaltyAmount));
    
    return { receiver, royaltyAmount };
}
```

## Building a Custom Marketplace

```javascript
import { ethers } from 'ethers';

class NFTMarketplace {
    constructor(provider, marketplaceAddress) {
        this.marketplace = new ethers.Contract(
            marketplaceAddress,
            MARKETPLACE_ABI,
            provider
        );
    }
    
    async listNFT(nftAddress, tokenId, price) {
        const signer = this.marketplace.signer;
        const nft = new ethers.Contract(nftAddress, ERC721_ABI, signer);
        
        // Approve marketplace
        await nft.setApprovalForAll(this.marketplace.address, true);
        
        // List
        const tx = await this.marketplace.list(
            nftAddress,
            tokenId,
            ethers.utils.parseEther(price)
        );
        
        await tx.wait();
        console.log('NFT listed!');
    }
    
    async buyNFT(nftAddress, tokenId, price) {
        const tx = await this.marketplace.buy(nftAddress, tokenId, {
            value: ethers.utils.parseEther(price)
        });
        
        await tx.wait();
        console.log('NFT purchased!');
    }
    
    async getListings() {
        const filter = this.marketplace.filters.Listed();
        const events = await this.marketplace.queryFilter(filter);
        
        return events.map(event => ({
            seller: event.args.seller,
            nftContract: event.args.nftContract,
            tokenId: event.args.tokenId.toString(),
            price: ethers.utils.formatEther(event.args.price)
        }));
    }
}
```

## Frontend Integration

```javascript
import React, { useState, useEffect } from 'react';

function MarketplaceUI() {
    const [listings, setListings] = useState([]);
    
    useEffect(() => {
        loadListings();
    }, []);
    
    async function loadListings() {
        const marketplace = new NFTMarketplace(provider, MARKETPLACE_ADDRESS);
        const items = await marketplace.getListings();
        setListings(items);
    }
    
    async function buyNFT(nftContract, tokenId, price) {
        const marketplace = new NFTMarketplace(provider, MARKETPLACE_ADDRESS);
        await marketplace.buyNFT(nftContract, tokenId, price);
        await loadListings();
    }
    
    return (
        <div>
            <h2>NFT Marketplace</h2>
            <div className="listings">
                {listings.map((item, i) => (
                    <div key={i} className="listing">
                        <img src={item.image} alt={item.name} />
                        <h3>{item.name}</h3>
                        <p>{item.price} ETH</p>
                        <button onClick={() => buyNFT(item.nftContract, item.tokenId, item.price)}>
                            Buy Now
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}
```

## Best Practices

1. ✅ **Gas Optimization**: Batch operations when possible
2. ✅ **Security**: Reentrancy guards on payments
3. ✅ **Royalties**: Implement EIP-2981
4. ✅ **Metadata**: Follow OpenSea standards
5. ✅ **Approvals**: Use setApprovalForAll efficiently
6. ✅ **Testing**: Thorough marketplace contract testing

## Resources

- [OpenSea Documentation](https://docs.opensea.io/)
- [Seaport Protocol](https://github.com/ProjectOpenSea/seaport)
- [EIP-2981 Royalty Standard](https://eips.ethereum.org/EIPS/eip-2981)

**Next**: Continue to [Projects](../08-projects/) →
