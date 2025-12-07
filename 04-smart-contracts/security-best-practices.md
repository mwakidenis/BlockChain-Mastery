# Smart Contract Security Best Practices 🔒

Smart contract security is paramount as vulnerabilities can lead to significant financial losses. This guide covers essential security practices, common vulnerabilities, and how to protect your contracts.

## 📋 Table of Contents

1. [Common Vulnerabilities](#common-vulnerabilities)
2. [Security Patterns](#security-patterns)
3. [Security Checklist](#security-checklist)
4. [Audit Process](#audit-process)
5. [Security Tools](#security-tools)

---

## Common Vulnerabilities

### 1. Reentrancy Attacks 🔄

**What it is**: When a function makes an external call to an untrusted contract before resolving its own state.

**Vulnerable Code**:
```solidity
// ❌ VULNERABLE
function withdraw() public {
    uint256 amount = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] = 0;
}
```

**Secure Code**:
```solidity
// ✅ SECURE - Checks-Effects-Interactions Pattern
function withdraw() public {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0;  // Update state BEFORE external call
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
}

// Or use ReentrancyGuard
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract Safe is ReentrancyGuard {
    function withdraw() public nonReentrant {
        uint256 amount = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
        balances[msg.sender] = 0;
    }
}
```

### 2. Integer Overflow/Underflow ➕➖

**Note**: Solidity 0.8.0+ has built-in overflow checking. For older versions, use SafeMath.

**Vulnerable Code (Solidity < 0.8.0)**:
```solidity
// ❌ VULNERABLE (pre-0.8.0)
function add(uint256 a, uint256 b) public pure returns (uint256) {
    return a + b;  // Can overflow
}
```

**Secure Code**:
```solidity
// ✅ SECURE (Solidity 0.8.0+)
pragma solidity ^0.8.0;

function add(uint256 a, uint256 b) public pure returns (uint256) {
    return a + b;  // Automatic overflow protection
}

// For explicit unchecked math (when needed):
function uncheckedAdd(uint256 a, uint256 b) public pure returns (uint256) {
    unchecked {
        return a + b;  // Skip overflow check (gas savings)
    }
}
```

### 3. Access Control Issues 🚫

**Vulnerable Code**:
```solidity
// ❌ VULNERABLE - Missing access control
function setPrice(uint256 _price) public {
    price = _price;  // Anyone can change price!
}
```

**Secure Code**:
```solidity
// ✅ SECURE
import "@openzeppelin/contracts/access/Ownable.sol";

contract Secure is Ownable {
    uint256 public price;
    
    function setPrice(uint256 _price) public onlyOwner {
        price = _price;
    }
}

// Or custom modifier
address public admin;

modifier onlyAdmin() {
    require(msg.sender == admin, "Not admin");
    _;
}

function setPrice(uint256 _price) public onlyAdmin {
    price = _price;
}
```

### 4. Front-Running 🏃

**What it is**: Attackers see pending transactions and submit their own with higher gas to execute first.

**Mitigation**:
```solidity
// ✅ Commit-Reveal Pattern
mapping(address => bytes32) public commits;

function commit(bytes32 _hash) public {
    commits[msg.sender] = _hash;
}

function reveal(uint256 _value, bytes32 _secret) public {
    bytes32 hash = keccak256(abi.encodePacked(_value, _secret));
    require(hash == commits[msg.sender], "Invalid reveal");
    // Process the value
}

// ✅ Use minimum/maximum bounds
function trade(uint256 minAmount) public {
    uint256 amount = calculateAmount();
    require(amount >= minAmount, "Slippage too high");
    // Execute trade
}
```

### 5. Unchecked External Calls 📞

**Vulnerable Code**:
```solidity
// ❌ VULNERABLE - Ignored return value
function sendPayment(address recipient, uint256 amount) public {
    recipient.call{value: amount}("");  // Return value ignored!
}
```

**Secure Code**:
```solidity
// ✅ SECURE - Check return value
function sendPayment(address recipient, uint256 amount) public {
    (bool success, ) = recipient.call{value: amount}("");
    require(success, "Transfer failed");
}

// Or use transfer (throws on failure, but limited to 2300 gas)
function sendPayment(address payable recipient, uint256 amount) public {
    recipient.transfer(amount);
}
```

### 6. Timestamp Dependence ⏰

**Vulnerable Code**:
```solidity
// ❌ VULNERABLE - Miners can manipulate timestamp
function generateRandom() public view returns (uint256) {
    return uint256(keccak256(abi.encodePacked(block.timestamp)));
}
```

**Secure Code**:
```solidity
// ✅ BETTER - Use block.number or Chainlink VRF
function generateRandom() public view returns (uint256) {
    return uint256(keccak256(abi.encodePacked(block.number)));
}

// ✅ BEST - Use Chainlink VRF for true randomness
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract RandomNumber is VRFConsumerBase {
    // Implement Chainlink VRF
}
```

### 7. Delegatecall Injection 🎭

**Vulnerable Code**:
```solidity
// ❌ VULNERABLE - User controls delegatecall target
function execute(address target, bytes memory data) public {
    target.delegatecall(data);  // Can change contract storage!
}
```

**Secure Code**:
```solidity
// ✅ SECURE - Whitelist allowed contracts
mapping(address => bool) public allowedContracts;

function execute(address target, bytes memory data) public onlyOwner {
    require(allowedContracts[target], "Contract not allowed");
    (bool success, ) = target.delegatecall(data);
    require(success);
}
```

### 8. Denial of Service (DoS) 🚫

**Vulnerable Code**:
```solidity
// ❌ VULNERABLE - Loop over user array
address[] public users;

function distributeRewards() public {
    for (uint256 i = 0; i < users.length; i++) {
        users[i].call{value: rewards[users[i]]}("");  // Can run out of gas!
    }
}
```

**Secure Code**:
```solidity
// ✅ SECURE - Pull over push pattern
mapping(address => uint256) public rewards;

function claimReward() public {
    uint256 amount = rewards[msg.sender];
    rewards[msg.sender] = 0;
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
}
```

---

## Security Patterns

### 1. Checks-Effects-Interactions Pattern

**Always follow this order**:
```solidity
function withdraw(uint256 amount) public {
    // 1. CHECKS
    require(balances[msg.sender] >= amount, "Insufficient balance");
    require(amount > 0, "Invalid amount");
    
    // 2. EFFECTS (update state)
    balances[msg.sender] -= amount;
    
    // 3. INTERACTIONS (external calls)
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

### 2. Pull Over Push Pattern

**Avoid pushing payments** to multiple addresses:
```solidity
// ✅ Users pull their funds
mapping(address => uint256) public pendingWithdrawals;

function allowWithdrawal(address user, uint256 amount) internal {
    pendingWithdrawals[user] += amount;
}

function withdraw() public {
    uint256 amount = pendingWithdrawals[msg.sender];
    pendingWithdrawals[msg.sender] = 0;
    payable(msg.sender).transfer(amount);
}
```

### 3. Rate Limiting ⏱️

```solidity
mapping(address => uint256) public lastAction;
uint256 public constant COOLDOWN = 1 hours;

modifier rateLimit() {
    require(
        block.timestamp >= lastAction[msg.sender] + COOLDOWN,
        "Action on cooldown"
    );
    lastAction[msg.sender] = block.timestamp;
    _;
}

function sensitiveAction() public rateLimit {
    // Function logic
}
```

### 4. Emergency Stop (Circuit Breaker) 🔴

```solidity
import "@openzeppelin/contracts/security/Pausable.sol";

contract MyContract is Pausable, Ownable {
    function deposit() public whenNotPaused {
        // Normal functionality
    }
    
    function emergencyStop() public onlyOwner {
        _pause();
    }
    
    function resume() public onlyOwner {
        _unpause();
    }
}
```

### 5. Safe Math (Pre-0.8.0)

```solidity
// For Solidity < 0.8.0, use SafeMath
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract LegacyContract {
    using SafeMath for uint256;
    
    function add(uint256 a, uint256 b) public pure returns (uint256) {
        return a.add(b);  // Safe addition
    }
}
```

---

## Security Checklist

### Pre-Development ✅

- [ ] Define clear contract specifications
- [ ] Plan upgrade strategy (if needed)
- [ ] Review similar contracts for common patterns
- [ ] Identify potential attack vectors
- [ ] Consider economic attack scenarios

### Development ✅

- [ ] Use latest stable Solidity version
- [ ] Follow style guide and best practices
- [ ] Use established libraries (OpenZeppelin)
- [ ] Implement proper access control
- [ ] Add comprehensive NatSpec comments
- [ ] Use events for important state changes
- [ ] Validate all inputs
- [ ] Handle errors gracefully

### Testing ✅

- [ ] Write comprehensive unit tests
- [ ] Test edge cases and failure scenarios
- [ ] Achieve high test coverage (>95%)
- [ ] Test with different user roles
- [ ] Perform integration testing
- [ ] Test on testnets
- [ ] Conduct gas optimization

### Security Review ✅

- [ ] Run static analysis tools (Slither, Mythril)
- [ ] Perform manual code review
- [ ] Check for common vulnerabilities
- [ ] Verify access control mechanisms
- [ ] Review external dependencies
- [ ] Get professional audit (for mainnet)
- [ ] Implement bug bounty program

### Deployment ✅

- [ ] Deploy to testnet first
- [ ] Verify contract source code
- [ ] Test all functions on testnet
- [ ] Prepare emergency response plan
- [ ] Monitor contract after deployment
- [ ] Have upgrade mechanism ready
- [ ] Document deployment process

---

## Audit Process

### 1. Internal Audit 🔍

**Before external audit**:
```bash
# Static analysis
slither .
mythril analyze contracts/*.sol

# Test coverage
npm run coverage

# Gas optimization
npm run test:gas
```

### 2. External Audit 🏢

**Professional audit firms**:
- **ConsenSys Diligence** - Comprehensive audits
- **Trail of Bits** - Security research
- **OpenZeppelin** - Smart contract security
- **CertiK** - Blockchain security
- **Quantstamp** - Automated + manual review

**Audit Process**:
1. Submit code and documentation
2. Auditors perform review (2-4 weeks)
3. Receive preliminary report
4. Fix identified issues
5. Re-audit critical fixes
6. Receive final report
7. Publish audit publicly

### 3. Bug Bounty Programs 💰

**Incentivize security researchers**:
```solidity
// Example bug bounty tiers
// Critical: $50,000 - $100,000
// High: $10,000 - $50,000
// Medium: $2,000 - $10,000
// Low: $500 - $2,000
```

**Popular platforms**:
- **Immunefi** - Largest crypto bug bounty
- **HackerOne** - General bug bounties
- **Code4rena** - Competitive audits

---

## Security Tools

### Static Analysis Tools 🔍

**1. Slither**
```bash
pip install slither-analyzer
slither .

# Custom checks
slither . --detect reentrancy-eth,uninitialized-state
```

**2. Mythril**
```bash
pip install mythril
myth analyze contracts/MyContract.sol
```

**3. Securify**
```bash
# Online tool
# https://securify.chainsecurity.com/
```

### Testing Frameworks 🧪

**Hardhat with Waffle**:
```javascript
const { expect } = require("chai");

describe("Security Tests", function() {
    it("should prevent reentrancy", async function() {
        // Test reentrancy protection
    });
    
    it("should enforce access control", async function() {
        await expect(
            contract.connect(attacker).adminFunction()
        ).to.be.revertedWith("Not authorized");
    });
});
```

### Fuzzing Tools 🎲

**Echidna**:
```solidity
// Test invariants with Echidna
contract TestMyContract {
    function echidna_balance_never_negative() public returns (bool) {
        return balance[msg.sender] >= 0;
    }
}
```

### Formal Verification ✓

**Certora Prover**:
```javascript
// Specify properties to verify
rule balanceDoesNotDecrease {
    uint256 balanceBefore = balance[user];
    method f;
    env e;
    f(e);
    uint256 balanceAfter = balance[user];
    assert balanceAfter >= balanceBefore;
}
```

### Monitoring Tools 📊

**Tenderly**:
- Real-time monitoring
- Transaction simulation
- Alert system
- Debugger

**OpenZeppelin Defender**:
- Automated operations
- Transaction monitoring
- Security alerts
- Access control

---

## Best Practices Summary

### ✅ DO's

1. **Use established libraries** (OpenZeppelin)
2. **Follow Checks-Effects-Interactions pattern**
3. **Implement access control**
4. **Validate all inputs**
5. **Emit events for important actions**
6. **Test extensively**
7. **Get professional audits**
8. **Monitor post-deployment**
9. **Plan for upgrades**
10. **Document everything**

### ❌ DON'Ts

1. **Don't roll your own crypto**
2. **Don't ignore return values**
3. **Don't use tx.origin for authentication**
4. **Don't rely on block.timestamp for critical logic**
5. **Don't ignore compiler warnings**
6. **Don't deploy without testing**
7. **Don't hardcode addresses**
8. **Don't expose admin functions**
9. **Don't skip audits for production**
10. **Don't assume users act rationally**

---

## Real-World Exploits Case Studies

### The DAO Hack (2016) 💸

**Loss**: $60 million
**Vulnerability**: Reentrancy
**Lesson**: Always update state before external calls

### Parity Multi-Sig Hack (2017) 🔐

**Loss**: $30 million
**Vulnerability**: Unprotected initialization
**Lesson**: Protect initialization functions

### Poly Network Hack (2021) 🌉

**Loss**: $600 million (returned)
**Vulnerability**: Access control
**Lesson**: Validate privileges across systems

---

## Resources

### Documentation
- [Ethereum Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [SWC Registry](https://swcregistry.io/) - Smart Contract Weakness Classification
- [OpenZeppelin Security Docs](https://docs.openzeppelin.com/contracts/security)

### Tools
- [Slither](https://github.com/crytic/slither)
- [Mythril](https://github.com/ConsenSys/mythril)
- [Echidna](https://github.com/crytic/echidna)
- [Manticore](https://github.com/trailofbits/manticore)

### Learning
- [Ethernaut](https://ethernaut.openzeppelin.com/) - Security challenges
- [Damn Vulnerable DeFi](https://www.damnvulnerabledefi.xyz/)
- [Capture The Ether](https://capturetheether.com/)

---

**🔒 Security is not optional in smart contract development. Always prioritize security over features!**

**Next**: [Testing Contracts](testing-contracts.md) →
