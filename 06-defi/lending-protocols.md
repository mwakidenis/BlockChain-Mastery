# Lending Protocols 🏦

Learn how decentralized lending and borrowing works in DeFi, with focus on major protocols like Aave and Compound.

## How DeFi Lending Works

### Basic Concept

1. **Suppliers** deposit assets and earn interest
2. **Borrowers** provide collateral and borrow assets
3. **Interest rates** determined algorithmically
4. **Liquidations** protect the protocol

## Key Protocols

### Aave

- **Largest** lending protocol
- **Flash loans** pioneer
- **Variable & stable** rates
- **Multiple assets** supported

### Compound

- **Algorithmic** interest rates
- **cTokens** represent deposits
- **COMP** governance token
- **Battle-tested** security

## Supplying Assets

### How It Works

```javascript
import { ethers } from 'ethers';

async function supplyToAave(asset, amount) {
    const lendingPool = new ethers.Contract(
        AAVE_LENDING_POOL,
        LENDING_POOL_ABI,
        signer
    );
    
    // Approve token
    await assetContract.approve(lendingPool.address, amount);
    
    // Supply
    await lendingPool.deposit(
        asset,
        amount,
        await signer.getAddress(),
        0  // referral code
    );
    
    console.log('Supplied', amount, 'to Aave');
}
```

### Interest Earning

- **APY calculated** from utilization
- **Compounding** automatically
- **aTokens** represent your deposit
- **Withdrawable** anytime

## Borrowing Assets

### Collateralization

Must provide collateral worth more than borrowed amount.

```javascript
async function borrowFromAave(asset, amount) {
    const lendingPool = new ethers.Contract(
        AAVE_LENDING_POOL,
        LENDING_POOL_ABI,
        signer
    );
    
    // Borrow (2 = variable rate)
    await lendingPool.borrow(
        asset,
        amount,
        2,  // interest rate mode
        0,  // referral code
        await signer.getAddress()
    );
    
    console.log('Borrowed', amount);
}
```

### Loan-to-Value (LTV)

**LTV Ratio** = Borrowed Amount / Collateral Value

**Example**:
- Collateral: 1 ETH ($2000)
- Max LTV: 75%
- Can borrow: $1500 worth of assets

### Health Factor

Indicates position safety:

```javascript
function calculateHealthFactor(collateral, borrowed, liquidationThreshold) {
    return (collateral * liquidationThreshold) / borrowed;
}

// Example
const healthFactor = calculateHealthFactor(
    2000,  // $2000 collateral
    1000,  // $1000 borrowed
    0.80   // 80% liquidation threshold
);

console.log('Health Factor:', healthFactor);
// 1.6 (safe if > 1.0)
```

**Status**:
- `> 1.0`: Safe
- `= 1.0`: At liquidation threshold
- `< 1.0`: Can be liquidated

## Interest Rates

### Variable Rate

Changes based on utilization:

```javascript
function calculateInterestRate(utilization) {
    const baseRate = 0.02;  // 2%
    const slope1 = 0.04;    // 4%
    const slope2 = 0.75;    // 75%
    const optimalUtilization = 0.80;  // 80%
    
    if (utilization < optimalUtilization) {
        return baseRate + (utilization / optimalUtilization) * slope1;
    } else {
        const excess = utilization - optimalUtilization;
        return baseRate + slope1 + (excess / (1 - optimalUtilization)) * slope2;
    }
}

// At 90% utilization
const rate = calculateInterestRate(0.90);
console.log('Borrow APY:', (rate * 100).toFixed(2) + '%');
```

### Stable Rate

Fixed rate (Aave only) for predictability.

## Liquidations

### When They Happen

When health factor < 1.0, liquidators can repay debt and claim collateral at a discount.

```javascript
async function liquidate(user, debtAsset, collateralAsset, debtToCover) {
    const lendingPool = new ethers.Contract(
        AAVE_LENDING_POOL,
        LENDING_POOL_ABI,
        signer
    );
    
    await lendingPool.liquidationCall(
        collateralAsset,
        debtAsset,
        user,
        debtToCover,
        false  // receiveAToken
    );
}
```

### Liquidation Bonus

Liquidators earn a bonus (typically 5-10%):

```
Debt to Repay: $1000
Collateral Value: $1000
Liquidation Bonus: 5%
Liquidator Receives: $1050 worth of collateral
Profit: $50
```

## Flash Loans

Borrow without collateral, repay in same transaction.

```solidity
contract FlashLoanExample {
    function executeFlashLoan(address asset, uint256 amount) external {
        address[] memory assets = new address[](1);
        assets[0] = asset;
        
        uint256[] memory amounts = new uint256[](1);
        amounts[0] = amount;
        
        uint256[] memory modes = new uint256[](1);
        modes[0] = 0;  // no debt
        
        ILendingPool(AAVE_LENDING_POOL).flashLoan(
            address(this),
            assets,
            amounts,
            modes,
            address(this),
            "",
            0
        );
    }
    
    function executeOperation(
        address[] memory assets,
        uint256[] memory amounts,
        uint256[] memory premiums,
        address initiator,
        bytes memory params
    ) external returns (bool) {
        // Use borrowed funds
        // ... perform arbitrage, liquidations, etc.
        
        // Approve repayment
        for (uint i = 0; i < assets.length; i++) {
            uint amountOwed = amounts[i] + premiums[i];
            IERC20(assets[i]).approve(address(AAVE_LENDING_POOL), amountOwed);
        }
        
        return true;
    }
}
```

## Risks

### Protocol Risks

- 🐛 Smart contract bugs
- 🏃 Oracle manipulation
- 💸 Bad debt accumulation
- 👥 Governance attacks

### User Risks

- 📉 Liquidation risk
- 💹 Variable rate volatility
- ⛓️ Network congestion
- 🔑 Key management

## Best Practices

### For Suppliers

1. ✅ Diversify across protocols
2. ✅ Monitor APYs
3. ✅ Consider insurance (Nexus Mutual)
4. ✅ Understand risks

### For Borrowers

1. ✅ Maintain high health factor (>2.0)
2. ✅ Monitor liquidation threshold
3. ✅ Use price alerts
4. ✅ Keep repayment buffer
5. ✅ Understand interest rate models

## Complete Example

```javascript
class LendingProtocol {
    constructor(provider, lendingPoolAddress) {
        this.provider = provider;
        this.lendingPool = new ethers.Contract(
            lendingPoolAddress,
            LENDING_POOL_ABI,
            provider
        );
    }
    
    async getUserAccountData(user) {
        const data = await this.lendingPool.getUserAccountData(user);
        
        return {
            totalCollateralETH: ethers.utils.formatEther(data.totalCollateralETH),
            totalDebtETH: ethers.utils.formatEther(data.totalDebtETH),
            availableBorrowsETH: ethers.utils.formatEther(data.availableBorrowsETH),
            currentLiquidationThreshold: data.currentLiquidationThreshold / 100,
            ltv: data.ltv / 100,
            healthFactor: ethers.utils.formatEther(data.healthFactor)
        };
    }
    
    async supply(asset, amount) {
        const signer = this.provider.getSigner();
        const assetContract = new ethers.Contract(asset, ERC20_ABI, signer);
        
        await assetContract.approve(this.lendingPool.address, amount);
        
        await this.lendingPool.connect(signer).deposit(
            asset,
            amount,
            await signer.getAddress(),
            0
        );
    }
    
    async borrow(asset, amount, rateMode = 2) {
        const signer = this.provider.getSigner();
        
        await this.lendingPool.connect(signer).borrow(
            asset,
            amount,
            rateMode,
            0,
            await signer.getAddress()
        );
    }
    
    async repay(asset, amount, rateMode = 2) {
        const signer = this.provider.getSigner();
        const assetContract = new ethers.Contract(asset, ERC20_ABI, signer);
        
        await assetContract.approve(this.lendingPool.address, amount);
        
        await this.lendingPool.connect(signer).repay(
            asset,
            amount,
            rateMode,
            await signer.getAddress()
        );
    }
    
    async withdraw(asset, amount) {
        const signer = this.provider.getSigner();
        
        await this.lendingPool.connect(signer).withdraw(
            asset,
            amount,
            await signer.getAddress()
        );
    }
}
```

## Resources

- [Aave Documentation](https://docs.aave.com/)
- [Compound Documentation](https://compound.finance/docs)
- [DeFi Llama](https://defillama.com/) - Protocol TVL

**Next**: [Yield Farming](yield-farming.md) →
