# MEV & Flash Loans 💎

Learn about Maximal Extractable Value (MEV) and Flash Loans - advanced DeFi concepts for arbitrage and complex transactions.

## What is MEV?

**MEV (Maximal Extractable Value)** is profit that can be extracted by reordering, including, or excluding transactions in a block.

### Common MEV Strategies

1. **Arbitrage**: Price differences across DEXs
2. **Liquidations**: Liquidating undercollateralized positions
3. **Sandwich Attacks**: Front-run + back-run user trades
4. **Front-running**: Execute before user transaction

## Flash Loans

**Flash Loans** allow borrowing any amount without collateral, as long as it's repaid in the same transaction.

### How They Work

```
1. Borrow 1000 ETH (no collateral)
2. Use ETH for arbitrage/liquidation
3. Repay 1000 ETH + 0.09% fee
4. Keep profit
```

If repayment fails, entire transaction reverts!

## Flash Loan Providers

| Protocol | Fee | Max Amount |
|----------|-----|------------|
| **Aave** | 0.09% | Unlimited |
| **dYdX** | 0% | Pool liquidity |
| **Uniswap V2** | 0.3% | Pool liquidity |
| **Balancer** | Varies | Pool liquidity |

## Aave Flash Loan

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@aave/core-v3/contracts/flashloan/base/FlashLoanSimpleReceiverBase.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract FlashLoanArbitrage is FlashLoanSimpleReceiverBase {
    address private immutable owner;
    
    constructor(address _addressProvider) 
        FlashLoanSimpleReceiverBase(IPoolAddressesProvider(_addressProvider)) 
    {
        owner = msg.sender;
    }
    
    function executeFlashLoan(
        address asset,
        uint256 amount
    ) external {
        address receiverAddress = address(this);
        bytes memory params = "";
        uint16 referralCode = 0;
        
        POOL.flashLoanSimple(
            receiverAddress,
            asset,
            amount,
            params,
            referralCode
        );
    }
    
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        // Use borrowed funds for arbitrage
        uint256 profit = performArbitrage(asset, amount);
        
        // Calculate total owed (borrowed + fee)
        uint256 totalDebt = amount + premium;
        
        // Must have profit > fee
        require(profit > premium, "No profit");
        
        // Approve repayment
        IERC20(asset).approve(address(POOL), totalDebt);
        
        // Transfer profit to owner
        IERC20(asset).transfer(owner, profit - premium);
        
        return true;
    }
    
    function performArbitrage(address asset, uint256 amount) 
        internal 
        returns (uint256 profit) 
    {
        // 1. Buy low on DEX A
        uint256 bought = buyOnDexA(asset, amount);
        
        // 2. Sell high on DEX B
        uint256 sold = sellOnDexB(asset, bought);
        
        // 3. Calculate profit
        profit = sold > amount ? sold - amount : 0;
    }
    
    function buyOnDexA(address asset, uint256 amount) internal returns (uint256) {
        // Implementation
    }
    
    function sellOnDexB(address asset, uint256 amount) internal returns (uint256) {
        // Implementation
    }
}
```

## dYdX Flash Loan

```solidity
import "@dydxprotocol/solo/contracts/protocol/interfaces/ISoloMargin.sol";

contract DydxFlashLoan {
    ISoloMargin public soloMargin;
    
    function initiateFlashLoan(
        address token,
        uint256 amount
    ) external {
        // Prepare actions
        Actions.ActionArgs[] memory operations = new Actions.ActionArgs[](3);
        
        // Withdraw
        operations[0] = Actions.ActionArgs({
            actionType: Actions.ActionType.Withdraw,
            accountId: 0,
            amount: Types.AssetAmount({
                sign: false,
                denomination: Types.AssetDenomination.Wei,
                ref: Types.AssetReference.Delta,
                value: amount
            }),
            primaryMarketId: getMarketId(token),
            secondaryMarketId: 0,
            otherAddress: address(this),
            otherAccountId: 0,
            data: ""
        });
        
        // Call custom logic
        operations[1] = Actions.ActionArgs({
            actionType: Actions.ActionType.Call,
            accountId: 0,
            amount: Types.AssetAmount({
                sign: false,
                denomination: Types.AssetDenomination.Wei,
                ref: Types.AssetReference.Delta,
                value: 0
            }),
            primaryMarketId: 0,
            secondaryMarketId: 0,
            otherAddress: address(this),
            otherAccountId: 0,
            data: abi.encode(token, amount)
        });
        
        // Deposit (repay)
        operations[2] = Actions.ActionArgs({
            actionType: Actions.ActionType.Deposit,
            accountId: 0,
            amount: Types.AssetAmount({
                sign: true,
                denomination: Types.AssetDenomination.Wei,
                ref: Types.AssetReference.Delta,
                value: amount + 2 // +2 wei profit required
            }),
            primaryMarketId: getMarketId(token),
            secondaryMarketId: 0,
            otherAddress: address(this),
            otherAccountId: 0,
            data: ""
        });
        
        // Execute
        soloMargin.operate(accountInfos, operations);
    }
    
    function callFunction(
        address sender,
        Account.Info memory accountInfo,
        bytes memory data
    ) external {
        (address token, uint256 amount) = abi.decode(data, (address, uint256));
        
        // Custom logic with borrowed funds
        performArbitrage(token, amount);
    }
}
```

## Arbitrage Bot Example

```javascript
import { ethers } from 'ethers';

class ArbitrageBot {
    constructor(provider, flashLoanContract) {
        this.provider = provider;
        this.flashLoan = flashLoanContract;
    }
    
    async findArbitrage() {
        const tokens = ['WETH', 'USDC', 'DAI'];
        
        for (const token of tokens) {
            const opportunity = await this.checkOpportunity(token);
            
            if (opportunity.profitable) {
                console.log('Arbitrage opportunity found!');
                await this.executeArbitrage(opportunity);
            }
        }
    }
    
    async checkOpportunity(token) {
        // Get prices from different DEXs
        const priceUniswap = await this.getPrice('uniswap', token);
        const priceSushiswap = await this.getPrice('sushiswap', token);
        
        const priceDiff = Math.abs(priceUniswap - priceSushiswap);
        const profitPercent = (priceDiff / priceUniswap) * 100;
        
        // Account for fees: 0.3% swap + 0.09% flash loan
        const breakEven = 0.39;
        const profitable = profitPercent > breakEven;
        
        return {
            token,
            buyDex: priceUniswap < priceSushiswap ? 'uniswap' : 'sushiswap',
            sellDex: priceUniswap < priceSushiswap ? 'sushiswap' : 'uniswap',
            profitPercent,
            profitable
        };
    }
    
    async executeArbitrage(opportunity) {
        const amount = ethers.utils.parseEther("100");
        
        try {
            const tx = await this.flashLoan.executeFlashLoan(
                opportunity.token,
                amount
            );
            
            await tx.wait();
            console.log('Arbitrage executed successfully!');
        } catch (error) {
            console.error('Arbitrage failed:', error);
        }
    }
    
    async getPrice(dex, token) {
        // Implementation to fetch price from DEX
    }
}

// Run bot
const bot = new ArbitrageBot(provider, flashLoanContract);
setInterval(() => bot.findArbitrage(), 5000); // Check every 5 seconds
```

## Liquidation Bot

```javascript
class LiquidationBot {
    async findLiquidations() {
        const lendingProtocol = new ethers.Contract(
            AAVE_ADDRESS,
            LENDING_POOL_ABI,
            provider
        );
        
        // Get all users with active positions
        const users = await this.getActiveUsers();
        
        for (const user of users) {
            const data = await lendingProtocol.getUserAccountData(user);
            const healthFactor = data.healthFactor;
            
            // Health factor < 1 = liquidatable
            if (healthFactor.lt(ethers.utils.parseEther("1"))) {
                console.log('Liquidatable position found:', user);
                await this.liquidate(user, data);
            }
        }
    }
    
    async liquidate(user, accountData) {
        // Calculate max liquidation
        const debtToCover = accountData.totalDebt.div(2); // Max 50%
        
        // Use flash loan to liquidate
        const tx = await this.flashLoan.executeLiquidation(
            user,
            accountData.collateralAsset,
            accountData.debtAsset,
            debtToCover
        );
        
        await tx.wait();
        console.log('Liquidation successful!');
    }
}
```

## MEV Protection

### For Users

1. **Use Private RPCs**: Flashbots Protect
2. **Set Slippage Tolerance**: Limit sandwich attacks
3. **Split Large Trades**: Reduce price impact
4. **Use Limit Orders**: Avoid slippage

### Flashbots Protect

```javascript
import { FlashbotsBundleProvider } from '@flashbots/ethers-provider-bundle';

async function sendPrivateTransaction(tx) {
    const flashbotsProvider = await FlashbotsBundleProvider.create(
        provider,
        authSigner,
        'https://relay.flashbots.net'
    );
    
    const signedBundle = await flashbotsProvider.signBundle([
        { signer: signer, transaction: tx }
    ]);
    
    const simulation = await flashbotsProvider.simulate(
        signedBundle,
        await provider.getBlockNumber()
    );
    
    if ('error' in simulation) {
        console.error('Simulation error:', simulation.error);
        return;
    }
    
    const bundleSubmission = await flashbotsProvider.sendBundle(
        signedBundle,
        await provider.getBlockNumber() + 1
    );
    
    console.log('Bundle submitted');
}
```

## Sandwich Attack (Educational)

```solidity
// DO NOT USE FOR MALICIOUS PURPOSES - Educational only
contract SandwichBot {
    function sandwich(
        address victim,
        address tokenIn,
        address tokenOut,
        uint256 victimAmount
    ) external {
        // 1. Front-run: Buy before victim
        uint256 bought = buyTokens(tokenIn, tokenOut, calculateFrontrunAmount(victimAmount));
        
        // 2. Victim's transaction executes (higher price)
        // This happens automatically
        
        // 3. Back-run: Sell after victim
        uint256 profit = sellTokens(tokenOut, tokenIn, bought);
        
        require(profit > calculateFrontrunAmount(victimAmount), "No profit");
    }
}
```

## Flash Loan Attack Patterns

### Price Oracle Manipulation

```solidity
// Attack: Manipulate spot price oracle
contract OracleAttack {
    function attack(address pool, address lendingProtocol) external {
        // 1. Flash loan large amount
        uint256 amount = 1000000 ether;
        
        // 2. Swap to manipulate pool price
        swapToManipulatePrice(pool, amount);
        
        // 3. Borrow against manipulated price
        borrowAgainstManipulatedPrice(lendingProtocol);
        
        // 4. Swap back
        swapBack(pool);
        
        // 5. Repay flash loan + profit
    }
}
```

**Prevention**: Use time-weighted average price (TWAP) oracles

## Best Practices

### For Flash Loan Developers

1. ✅ **Test Thoroughly**: Testnet first
2. ✅ **Calculate Fees**: Account for all costs
3. ✅ **Handle Failures**: Proper error handling
4. ✅ **Gas Optimization**: Every wei counts
5. ✅ **Slippage Protection**: Set min amounts

### For Protocol Developers

1. ✅ **Use TWAP Oracles**: Resist manipulation
2. ✅ **Reentrancy Guards**: Protect callbacks
3. ✅ **Flash Loan Detection**: Track flash loans
4. ✅ **Rate Limiting**: Limit borrows
5. ✅ **Multi-block Logic**: Spread over blocks

## Resources

- [Flashbots](https://www.flashbots.net/)
- [MEV Explore](https://explore.flashbots.net/)
- [Aave Flash Loan Docs](https://docs.aave.com/developers/guides/flash-loans)

---

**⚠️ Warning**: MEV and flash loans involve significant technical and financial risk. This content is for educational purposes only. Always test thoroughly and understand the risks before deploying.

**Next**: Review all created content →
