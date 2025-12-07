# NFT Metadata & IPFS 📦

Learn how to structure NFT metadata and store it on decentralized storage systems like IPFS.

## Metadata Structure

### OpenSea Standard

```json
{
  "name": "Cool Cat #1234",
  "description": "One of 10,000 unique Cool Cats",
  "image": "ipfs://QmXyz.../1234.png",
  "external_url": "https://coolcats.com/1234",
  "attributes": [
    {
      "trait_type": "Background",
      "value": "Blue"
    },
    {
      "trait_type": "Body",
      "value": "Orange"
    },
    {
      "trait_type": "Hat",
      "value": "Cowboy"
    },
    {
      "display_type": "number",
      "trait_type": "Generation",
      "value": 1
    }
  ]
}
```

### Attribute Types

```json
{
  "attributes": [
    {
      "trait_type": "Level",
      "value": 5
    },
    {
      "display_type": "boost_number",
      "trait_type": "Stamina Increase",
      "value": 10
    },
    {
      "display_type": "boost_percentage",
      "trait_type": "Speed Boost",
      "value": 25
    },
    {
      "display_type": "date",
      "trait_type": "Birthday",
      "value": 1640995200
    }
  ]
}
```

## IPFS Storage

### What is IPFS?

**IPFS (InterPlanetary File System)** is a peer-to-peer distributed file system for storing and sharing files.

### Why IPFS for NFTs?

- ✅ **Decentralized**: No single point of failure
- ✅ **Permanent**: Content-addressed storage
- ✅ **Immutable**: Files can't be changed
- ✅ **Efficient**: Deduplication

### IPFS URI Format

```
ipfs://QmXyz.../metadata.json
```

Resolves to:
```
https://ipfs.io/ipfs/QmXyz.../metadata.json
https://gateway.pinata.cloud/ipfs/QmXyz.../metadata.json
```

## Uploading to IPFS

### Using Pinata

```javascript
const pinataSDK = require('@pinata/sdk');
const fs = require('fs');

const pinata = new pinataSDK(PINATA_API_KEY, PINATA_SECRET);

// Upload image
async function uploadImage(filePath) {
    const readableStream = fs.createReadStream(filePath);
    const options = {
        pinataMetadata: {
            name: 'NFT Image'
        }
    };
    
    const result = await pinata.pinFileToIPFS(readableStream, options);
    console.log('Image CID:', result.IpfsHash);
    return result.IpfsHash;
}

// Upload metadata
async function uploadMetadata(metadata) {
    const options = {
        pinataMetadata: {
            name: 'NFT Metadata'
        }
    };
    
    const result = await pinata.pinJSONToIPFS(metadata, options);
    console.log('Metadata CID:', result.IpfsHash);
    return result.IpfsHash;
}

// Complete upload flow
async function uploadNFT() {
    // 1. Upload image
    const imageCID = await uploadImage('./images/nft.png');
    
    // 2. Create metadata
    const metadata = {
        name: "My NFT",
        description: "An awesome NFT",
        image: `ipfs://${imageCID}`,
        attributes: [
            { trait_type: "Rarity", value: "Rare" }
        ]
    };
    
    // 3. Upload metadata
    const metadataCID = await uploadMetadata(metadata);
    
    return `ipfs://${metadataCID}`;
}
```

### Using NFT.Storage

```javascript
import { NFTStorage, File } from 'nft.storage';

const client = new NFTStorage({ token: NFT_STORAGE_KEY });

async function storeNFT(imagePath, name, description) {
    const imageFile = await fs.promises.readFile(imagePath);
    
    const metadata = await client.store({
        name: name,
        description: description,
        image: new File([imageFile], 'nft.png', { type: 'image/png' }),
        attributes: [
            { trait_type: "Type", value: "Cool" }
        ]
    });
    
    console.log('Metadata URL:', metadata.url);
    return metadata.url;
}
```

## Generating Metadata

### Batch Generation

```javascript
const fs = require('fs');

function generateMetadata(tokenId, traits) {
    return {
        name: `Cool Cat #${tokenId}`,
        description: "Part of the Cool Cats collection",
        image: `ipfs://QmBase/${tokenId}.png`,
        attributes: Object.entries(traits).map(([trait_type, value]) => ({
            trait_type,
            value
        }))
    };
}

async function generateCollection(count) {
    for (let i = 1; i <= count; i++) {
        const traits = {
            "Background": randomChoice(backgrounds),
            "Body": randomChoice(bodies),
            "Eyes": randomChoice(eyes),
            "Hat": randomChoice(hats)
        };
        
        const metadata = generateMetadata(i, traits);
        
        // Save to file
        fs.writeFileSync(
            `./metadata/${i}.json`,
            JSON.stringify(metadata, null, 2)
        );
    }
}

function randomChoice(array) {
    return array[Math.floor(Math.random() * array.length)];
}
```

### Rarity System

```javascript
class RarityGenerator {
    constructor() {
        this.traits = {
            background: [
                { value: "Blue", weight: 50 },
                { value: "Red", weight: 30 },
                { value: "Gold", weight: 20 }
            ],
            hat: [
                { value: "None", weight: 60 },
                { value: "Cap", weight: 30 },
                { value: "Crown", weight: 10 }
            ]
        };
    }
    
    selectTrait(traitName) {
        const options = this.traits[traitName];
        const totalWeight = options.reduce((sum, opt) => sum + opt.weight, 0);
        let random = Math.random() * totalWeight;
        
        for (const option of options) {
            if (random < option.weight) {
                return option.value;
            }
            random -= option.weight;
        }
    }
    
    generate() {
        return {
            background: this.selectTrait('background'),
            hat: this.selectTrait('hat')
        };
    }
}
```

## On-Chain vs Off-Chain Metadata

### Off-Chain (IPFS)

**Pros**:
- ✅ Cheaper (no storage costs)
- ✅ Can include large files
- ✅ Easy to implement

**Cons**:
- ❌ Requires IPFS pinning
- ❌ Gateway dependency

```solidity
function tokenURI(uint256 tokenId) public view returns (string memory) {
    return string(abi.encodePacked(baseURI, tokenId.toString(), ".json"));
}
```

### On-Chain

**Pros**:
- ✅ Fully decentralized
- ✅ No external dependencies
- ✅ Permanent

**Cons**:
- ❌ Expensive (gas costs)
- ❌ Size limitations

```solidity
contract OnChainNFT is ERC721 {
    mapping(uint256 => string) private _tokenURIs;
    
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        string memory json = Base64.encode(
            bytes(
                string(
                    abi.encodePacked(
                        '{"name": "NFT #',
                        tokenId.toString(),
                        '", "description": "On-chain NFT", "image": "data:image/svg+xml;base64,',
                        generateSVG(tokenId),
                        '"}'
                    )
                )
            )
        );
        
        return string(abi.encodePacked('data:application/json;base64,', json));
    }
    
    function generateSVG(uint256 tokenId) private pure returns (string memory) {
        // Generate SVG on-chain
        return Base64.encode(bytes('<svg>...</svg>'));
    }
}
```

## Dynamic NFTs

### Time-Based

```solidity
contract DynamicNFT is ERC721 {
    mapping(uint256 => uint256) public birthTime;
    
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        uint256 age = block.timestamp - birthTime[tokenId];
        string memory stage = getLifeStage(age);
        
        return string(abi.encodePacked(baseURI, stage, "/", tokenId.toString(), ".json"));
    }
    
    function getLifeStage(uint256 age) private pure returns (string memory) {
        if (age < 7 days) return "baby";
        if (age < 30 days) return "child";
        return "adult";
    }
}
```

### Evolving Metadata

```javascript
// Update metadata based on usage
async function evolveNFT(tokenId, newLevel) {
    const currentMetadata = await fetchMetadata(tokenId);
    
    const updatedMetadata = {
        ...currentMetadata,
        attributes: currentMetadata.attributes.map(attr => 
            attr.trait_type === "Level" 
                ? { ...attr, value: newLevel }
                : attr
        )
    };
    
    // Upload new metadata
    const newCID = await uploadMetadata(updatedMetadata);
    
    // Update on-chain pointer
    await contract.setTokenURI(tokenId, `ipfs://${newCID}`);
}
```

## Best Practices

1. ✅ **Use IPFS URIs** in smart contracts, not gateway URLs
2. ✅ **Pin content** on multiple services
3. ✅ **Validate metadata** before upload
4. ✅ **Use CIDv1** for better compatibility
5. ✅ **Include fallback** gateways
6. ✅ **Optimize images** for web viewing
7. ✅ **Document attributes** clearly
8. ✅ **Test metadata** rendering

## Tools

- **Pinata** - IPFS pinning service
- **NFT.Storage** - Free IPFS for NFTs
- **Infura IPFS** - IPFS API
- **Web3.Storage** - Decentralized storage

## Resources

- [OpenSea Metadata Standards](https://docs.opensea.io/docs/metadata-standards)
- [IPFS Documentation](https://docs.ipfs.io/)
- [NFT.Storage](https://nft.storage/)

**Next**: [NFT Marketplaces](nft-marketplaces.md) →
