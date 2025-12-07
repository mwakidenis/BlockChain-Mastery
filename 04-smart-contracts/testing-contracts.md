# Testing Smart Contracts 🧪

Comprehensive testing is essential for smart contract development. This guide covers testing strategies, frameworks, and best practices to ensure your contracts work correctly and securely.

## 📋 Table of Contents

1. [Why Test Smart Contracts?](#why-test-smart-contracts)
2. [Testing Frameworks](#testing-frameworks)
3. [Unit Testing](#unit-testing)
4. [Integration Testing](#integration-testing)
5. [Test Coverage](#test-coverage)
6. [Gas Optimization Testing](#gas-optimization-testing)
7. [Continuous Integration](#continuous-integration)

---

## Why Test Smart Contracts?

Smart contracts are **immutable** and handle **real value**. Testing is critical because:

- ✅ **Prevent financial losses** - Bugs can cost millions
- ✅ **Ensure correctness** - Verify expected behavior
- ✅ **Document functionality** - Tests serve as documentation
- ✅ **Enable refactoring** - Change code with confidence
- ✅ **Meet audit requirements** - Professional audits require tests

---

## Testing Frameworks

### 1. Hardhat (Recommended) ⚡

**Most popular modern framework**

**Installation**:
```bash
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
npx hardhat init
```

**Basic Test Structure**:
```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("MyToken", function() {
    let token;
    let owner;
    let addr1;
    
    beforeEach(async function() {
        [owner, addr1] = await ethers.getSigners();
        const Token = await ethers.getContractFactory("MyToken");
        token = await Token.deploy();
    });
    
    it("Should set the right owner", async function() {
        expect(await token.owner()).to.equal(owner.address);
    });
});
```

### 2. Foundry 🔨

**Fast, Rust-based framework**

**Installation**:
```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
forge init my-project
```

**Test in Solidity**:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "../src/MyToken.sol";

contract MyTokenTest is Test {
    MyToken token;
    address owner = address(1);
    
    function setUp() public {
        vm.prank(owner);
        token = new MyToken();
    }
    
    function testOwner() public {
        assertEq(token.owner(), owner);
    }
    
    function testFuzz_Transfer(uint256 amount) public {
        vm.assume(amount > 0 && amount < token.totalSupply());
        // Test with random amounts
    }
}
```

### 3. Truffle 🍫

**Classic framework**

```bash
npm install -g truffle
truffle init
```

**Test Structure**:
```javascript
const MyToken = artifacts.require("MyToken");

contract("MyToken", accounts => {
    it("should put 10000 tokens in the first account", async () => {
        const instance = await MyToken.deployed();
        const balance = await instance.balanceOf(accounts[0]);
        assert.equal(balance.valueOf(), 10000);
    });
});
```

---

## Unit Testing

### Basic Test Structure

```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Token Contract", function() {
    let Token;
    let token;
    let owner;
    let addr1;
    let addr2;
    
    beforeEach(async function() {
        // Get signers
        [owner, addr1, addr2] = await ethers.getSigners();
        
        // Deploy contract
        Token = await ethers.getContractFactory("Token");
        token = await Token.deploy(1000);
        await token.deployed();
    });
    
    describe("Deployment", function() {
        it("Should set the right owner", async function() {
            expect(await token.owner()).to.equal(owner.address);
        });
        
        it("Should assign total supply to owner", async function() {
            const ownerBalance = await token.balanceOf(owner.address);
            expect(await token.totalSupply()).to.equal(ownerBalance);
        });
    });
    
    describe("Transactions", function() {
        it("Should transfer tokens between accounts", async function() {
            // Transfer 50 tokens from owner to addr1
            await token.transfer(addr1.address, 50);
            expect(await token.balanceOf(addr1.address)).to.equal(50);
            
            // Transfer 50 tokens from addr1 to addr2
            await token.connect(addr1).transfer(addr2.address, 50);
            expect(await token.balanceOf(addr2.address)).to.equal(50);
        });
        
        it("Should fail if sender doesn't have enough tokens", async function() {
            const initialBalance = await token.balanceOf(owner.address);
            
            await expect(
                token.connect(addr1).transfer(owner.address, 1)
            ).to.be.revertedWith("Insufficient balance");
            
            expect(await token.balanceOf(owner.address)).to.equal(initialBalance);
        });
        
        it("Should emit Transfer event", async function() {
            await expect(token.transfer(addr1.address, 50))
                .to.emit(token, "Transfer")
                .withArgs(owner.address, addr1.address, 50);
        });
    });
});
```

### Testing Access Control

```javascript
describe("Access Control", function() {
    it("Should allow only owner to mint", async function() {
        await expect(
            token.connect(addr1).mint(addr1.address, 100)
        ).to.be.revertedWith("Ownable: caller is not the owner");
    });
    
    it("Should allow owner to mint", async function() {
        await token.mint(addr1.address, 100);
        expect(await token.balanceOf(addr1.address)).to.equal(100);
    });
    
    it("Should allow owner to transfer ownership", async function() {
        await token.transferOwnership(addr1.address);
        expect(await token.owner()).to.equal(addr1.address);
    });
});
```

### Testing Edge Cases

```javascript
describe("Edge Cases", function() {
    it("Should handle zero address", async function() {
        await expect(
            token.transfer(ethers.constants.AddressZero, 50)
        ).to.be.revertedWith("Transfer to zero address");
    });
    
    it("Should handle zero amount", async function() {
        await expect(
            token.transfer(addr1.address, 0)
        ).to.be.revertedWith("Amount must be greater than 0");
    });
    
    it("Should handle maximum uint256", async function() {
        const maxUint = ethers.constants.MaxUint256;
        // Test behavior with maximum values
    });
});
```

### Testing State Changes

```javascript
describe("State Management", function() {
    it("Should correctly update balances after transfer", async function() {
        const ownerInitial = await token.balanceOf(owner.address);
        const addr1Initial = await token.balanceOf(addr1.address);
        
        await token.transfer(addr1.address, 50);
        
        expect(await token.balanceOf(owner.address))
            .to.equal(ownerInitial.sub(50));
        expect(await token.balanceOf(addr1.address))
            .to.equal(addr1Initial.add(50));
    });
    
    it("Should maintain total supply after transfers", async function() {
        const totalSupply = await token.totalSupply();
        
        await token.transfer(addr1.address, 100);
        await token.connect(addr1).transfer(addr2.address, 50);
        
        expect(await token.totalSupply()).to.equal(totalSupply);
    });
});
```

---

## Integration Testing

### Testing Contract Interactions

```javascript
describe("DEX Integration", function() {
    let factory;
    let router;
    let token;
    let weth;
    
    beforeEach(async function() {
        // Deploy all contracts
        const Factory = await ethers.getContractFactory("UniswapV2Factory");
        factory = await Factory.deploy(owner.address);
        
        const WETH = await ethers.getContractFactory("WETH");
        weth = await WETH.deploy();
        
        const Router = await ethers.getContractFactory("UniswapV2Router");
        router = await Router.deploy(factory.address, weth.address);
        
        const Token = await ethers.getContractFactory("Token");
        token = await Token.deploy(ethers.utils.parseEther("1000"));
    });
    
    it("Should create liquidity pool", async function() {
        await token.approve(router.address, ethers.utils.parseEther("100"));
        
        await router.addLiquidityETH(
            token.address,
            ethers.utils.parseEther("100"),
            0,
            0,
            owner.address,
            Date.now() + 1000,
            { value: ethers.utils.parseEther("1") }
        );
        
        const pairAddress = await factory.getPair(token.address, weth.address);
        expect(pairAddress).to.not.equal(ethers.constants.AddressZero);
    });
});
```

### Testing Time-Dependent Functions

```javascript
describe("Time-based Functions", function() {
    it("Should vest tokens over time", async function() {
        await token.startVesting(addr1.address, ethers.utils.parseEther("100"));
        
        // Fast forward time
        await ethers.provider.send("evm_increaseTime", [30 * 24 * 60 * 60]); // 30 days
        await ethers.provider.send("evm_mine");
        
        await token.connect(addr1).claimVested();
        const balance = await token.balanceOf(addr1.address);
        expect(balance).to.be.gt(0);
    });
});
```

### Testing Events

```javascript
describe("Events", function() {
    it("Should emit multiple events in correct order", async function() {
        const tx = await token.complexOperation(addr1.address, 100);
        const receipt = await tx.wait();
        
        expect(receipt.events.length).to.equal(3);
        expect(receipt.events[0].event).to.equal("Approval");
        expect(receipt.events[1].event).to.equal("Transfer");
        expect(receipt.events[2].event).to.equal("OperationComplete");
    });
});
```

---

## Test Coverage

### Measuring Coverage

**Using Hardhat**:
```bash
npm install --save-dev solidity-coverage
```

**hardhat.config.js**:
```javascript
require("solidity-coverage");

module.exports = {
    solidity: "0.8.0",
};
```

**Run coverage**:
```bash
npx hardhat coverage
```

### Coverage Report

```
-------------|----------|----------|----------|----------|----------------|
File         |  % Stmts | % Branch |  % Funcs |  % Lines |Uncovered Lines |
-------------|----------|----------|----------|----------|----------------|
 contracts/  |      100 |      100 |      100 |      100 |                |
  Token.sol  |      100 |      100 |      100 |      100 |                |
-------------|----------|----------|----------|----------|----------------|
All files    |      100 |      100 |      100 |      100 |                |
-------------|----------|----------|----------|----------|----------------|
```

### Coverage Goals

- ✅ **Statements**: >95%
- ✅ **Branches**: >90%
- ✅ **Functions**: 100%
- ✅ **Lines**: >95%

### What to Test

```javascript
describe("Comprehensive Coverage", function() {
    // ✅ Happy paths
    it("Should perform normal operations");
    
    // ✅ Edge cases
    it("Should handle boundary values");
    
    // ✅ Error cases
    it("Should revert on invalid inputs");
    
    // ✅ Access control
    it("Should enforce permissions");
    
    // ✅ State transitions
    it("Should update state correctly");
    
    // ✅ Events
    it("Should emit expected events");
    
    // ✅ Gas limits
    it("Should not exceed gas limits");
    
    // ✅ Reentrancy
    it("Should prevent reentrancy");
});
```

---

## Gas Optimization Testing

### Measuring Gas Usage

```javascript
describe("Gas Optimization", function() {
    it("Should measure gas for transfer", async function() {
        const tx = await token.transfer(addr1.address, 100);
        const receipt = await tx.wait();
        console.log("Gas used:", receipt.gasUsed.toString());
        
        // Assert gas is within acceptable range
        expect(receipt.gasUsed).to.be.lt(100000);
    });
    
    it("Should compare gas between implementations", async function() {
        // Test optimized version
        const tx1 = await tokenOptimized.batchTransfer([addr1.address], [100]);
        const receipt1 = await tx1.wait();
        
        // Test unoptimized version
        const tx2 = await tokenUnoptimized.batchTransfer([addr1.address], [100]);
        const receipt2 = await tx2.wait();
        
        expect(receipt1.gasUsed).to.be.lt(receipt2.gasUsed);
    });
});
```

### Gas Reporter

```bash
npm install --save-dev hardhat-gas-reporter
```

**hardhat.config.js**:
```javascript
require("hardhat-gas-reporter");

module.exports = {
    gasReporter: {
        enabled: true,
        currency: "USD",
        gasPrice: 21
    }
};
```

**Output**:
```
·--------------------------------|---------------------------|-------------|-----------------------------·
|      Solc version: 0.8.0       ·  Optimizer enabled: true  ·  Runs: 200  ·  Block limit: 30000000 gas  │
·································|···························|·············|······························
|  Methods                                                                                                │
··················|··············|·············|·············|·············|···············|··············
|  Contract       ·  Method      ·  Min        ·  Max        ·  Avg        ·  # calls      ·  usd (avg)  │
··················|··············|·············|·············|·············|···············|··············
|  Token          ·  transfer    ·      51823  ·      64723  ·      58273  ·          100  ·       1.22  │
··················|··············|·············|·············|·············|···············|··············
```

---

## Continuous Integration

### GitHub Actions

**.github/workflows/test.yml**:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Run coverage
        run: npm run coverage
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v2
        with:
          files: ./coverage/lcov.info
```

### Pre-commit Hooks

**Using Husky**:
```bash
npm install --save-dev husky
npx husky install
npx husky add .husky/pre-commit "npm test"
```

---

## Advanced Testing Techniques

### Fuzz Testing

**Using Foundry**:
```solidity
function testFuzz_Transfer(address to, uint256 amount) public {
    vm.assume(to != address(0));
    vm.assume(amount <= token.balanceOf(address(this)));
    
    token.transfer(to, amount);
    assertEq(token.balanceOf(to), amount);
}
```

### Invariant Testing

```solidity
contract InvariantTest is Test {
    Token token;
    
    function setUp() public {
        token = new Token();
    }
    
    function invariant_totalSupplyNeverChanges() public {
        assertEq(token.totalSupply(), 1000000);
    }
    
    function invariant_balancesSum() public {
        // Sum of all balances equals total supply
    }
}
```

### Snapshot Testing

```javascript
describe("Snapshot Testing", function() {
    it("Should match snapshot", async function() {
        await token.transfer(addr1.address, 100);
        
        const snapshotId = await ethers.provider.send("evm_snapshot");
        
        // Make changes
        await token.transfer(addr2.address, 50);
        
        // Revert to snapshot
        await ethers.provider.send("evm_revert", [snapshotId]);
        
        // State is restored
        expect(await token.balanceOf(addr2.address)).to.equal(0);
    });
});
```

---

## Best Practices

### ✅ Testing Checklist

- [ ] Test all public/external functions
- [ ] Test access control
- [ ] Test input validation
- [ ] Test edge cases (0, max values)
- [ ] Test state transitions
- [ ] Test events emission
- [ ] Test error messages
- [ ] Test gas consumption
- [ ] Test reentrancy protection
- [ ] Test integration with other contracts
- [ ] Achieve >95% code coverage
- [ ] Run tests on CI/CD
- [ ] Document test cases

### 📝 Writing Good Tests

1. **Descriptive names**: `it("Should revert when insufficient balance")`
2. **One assertion per test**: Focus on single behavior
3. **Arrange-Act-Assert**: Clear test structure
4. **Independent tests**: No dependencies between tests
5. **Fast execution**: Keep tests quick
6. **Deterministic**: Same results every time

---

## Common Testing Patterns

### Testing Modifiers

```javascript
it("Should apply modifier correctly", async function() {
    await expect(
        token.connect(addr1).restrictedFunction()
    ).to.be.revertedWith("Not authorized");
    
    await expect(
        token.connect(owner).restrictedFunction()
    ).to.not.be.reverted;
});
```

### Testing Payable Functions

```javascript
it("Should accept ETH payment", async function() {
    await token.deposit({ value: ethers.utils.parseEther("1") });
    expect(await ethers.provider.getBalance(token.address))
        .to.equal(ethers.utils.parseEther("1"));
});
```

### Testing Fallback/Receive

```javascript
it("Should trigger fallback", async function() {
    const tx = await owner.sendTransaction({
        to: token.address,
        value: ethers.utils.parseEther("1")
    });
    
    const receipt = await tx.wait();
    expect(receipt.events[0].event).to.equal("Received");
});
```

---

## Resources

### Documentation
- [Hardhat Testing](https://hardhat.org/tutorial/testing-contracts)
- [Foundry Book](https://book.getfoundry.sh/)
- [Chai Assertion Library](https://www.chaijs.com/)

### Tools
- [Hardhat](https://hardhat.org/)
- [Foundry](https://getfoundry.sh/)
- [Waffle](https://getwaffle.io/)
- [Solidity Coverage](https://github.com/sc-forks/solidity-coverage)

### Learning
- [Smart Contract Testing Best Practices](https://ethereum.org/en/developers/docs/smart-contracts/testing/)
- [Testing Smart Contracts](https://docs.openzeppelin.com/learn/deploying-and-interacting)

---

**🧪 Comprehensive testing is not optional - it's essential for secure smart contracts!**

**Next**: Continue to [Web3 Development](../05-web3-development/) →
