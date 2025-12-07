# DEX & AMM Mechanics (Uniswap) 🔄

Learn how Decentralized Exchanges (DEX) and Automated Market Makers (AMM) work, with a focus on Uniswap, the leading DEX protocol.

## What is an AMM?

An **Automated Market Maker (AMM)** is a type of decentralized exchange that uses algorithmic "money robots" (smart contracts) to provide liquidity instead of traditional order books.

### Key Differences

| Feature | Traditional Exchange | AMM |
|---------|---------------------|-----|
| **Order Book** | Yes | No |
| **Market Makers** | Humans/Firms | Smart Contracts |
| **Liquidity** | Provided by traders | Liquidity pools |
| **Price Discovery** | Order matching | Mathematical formula |
| **Slippage** | Varies | Predictable |

## How Uniswap Works

### Constant Product Formula

Uniswap uses the **constant product formula**: `x * y = k`

- `x` = Amount of token A in pool
- `y` = Amount of token B in pool
- `k` = Constant (product must remain constant)

**Example**:
```
Pool: 10 ETH × 20,000 USDC = 200,000 (k)

If you buy 1 ETH:
- ETH decreases: 10 - 1 = 9 ETH
- USDC must increase: 200,000 / 9 = 22,222 USDC
- You pay: 22,222 - 20,000 = 2,222 USDC for 1 ETH
- New state: 9 ETH × 22,222 USDC = 200,000 (k)
```

### Liquidity Pools

Liquidity pools are smart contracts containing two tokens in equal value.

```solidity
// Simplified Uniswap V2 Pool
contract UniswapPair {
    address public token0;
    address public token1;
    uint112 private reserve0;
    uint112 private reserve1;
    
    uint public totalSupply;
    mapping(address => uint) public balanceOf;
    
    function addLiquidity(uint amount0, uint amount1) external {
        // Transfer tokens from user
        IERC20(token0).transferFrom(msg.sender, address(this), amount0);
        IERC20(token1).transferFrom(msg.sender, address(this), amount1);
        
        // Mint LP tokens
        uint liquidity;
        if (totalSupply == 0) {
            liquidity = sqrt(amount0 * amount1);
        } else {
            liquidity = min(
                amount0 * totalSupply / reserve0,
                amount1 * totalSupply / reserve1
            );
        }
        
        balanceOf[msg.sender] += liquidity;
        totalSupply += liquidity;
        
        // Update reserves
        reserve0 += amount0;
        reserve1 += amount1;
    }
    
    function swap(uint amountIn, address tokenIn) external {
        require(tokenIn == token0 || tokenIn == token1);
        
        bool isToken0 = tokenIn == token0;
        (uint reserveIn, uint reserveOut) = isToken0 
            ? (reserve0, reserve1) 
            : (reserve1, reserve0);
        
        // Calculate output amount
        uint amountInWithFee = amountIn * 997;
        uint amountOut = (amountInWithFee * reserveOut) / 
                        (reserveIn * 1000 + amountInWithFee);
        
        // Transfer tokens
        if (isToken0) {
            IERC20(token0).transferFrom(msg.sender, address(this), amountIn);
            IERC20(token1).transfer(msg.sender, amountOut);
        } else {
            IERC20(token1).transferFrom(msg.sender, address(this), amountIn);
            IERC20(token0).transfer(msg.sender, amountOut);
        }
        
        // Update reserves
        // ... (simplified)
    }
}
```

## Adding Liquidity

### How It Works

1. **Deposit equal value** of both tokens
2. **Receive LP tokens** representing your share
3. **Earn fees** from trades (0.3% per trade)

### Example

```javascript
import { ethers } from 'ethers';

async function addLiquidity(token0, token1, amount0, amount1) {
    const router = new ethers.Contract(
        UNISWAP_ROUTER_ADDRESS,
        ROUTER_ABI,
        signer
    );
    
    // Approve tokens
    await token0Contract.approve(router.address, amount0);
    await token1Contract.approve(router.address, amount1);
    
    // Add liquidity
    const tx = await router.addLiquidity(
        token0,
        token1,
        amount0,
        amount1,
        amount0Min, // Minimum amount (slippage protection)
        amount1Min, // Minimum amount (slippage protection)
        recipient,
        deadline
    );
    
    await tx.wait();
    console.log('Liquidity added!');
}
```

## Swapping Tokens

### How Swaps Work

1. User sends input token
2. AMM calculates output using formula
3. Output token sent to user
4. 0.3% fee goes to liquidity providers

### Example

```javascript
async function swapTokens(amountIn, tokenIn, tokenOut) {
    const router = new ethers.Contract(
        UNISWAP_ROUTER_ADDRESS,
        ROUTER_ABI,
        signer
    );
    
    // Approve token
    await tokenInContract.approve(router.address, amountIn);
    
    // Get expected output
    const amounts = await router.getAmountsOut(amountIn, [tokenIn, tokenOut]);
    const amountOutMin = amounts[1].mul(95).div(100); // 5% slippage
    
    // Swap
    const tx = await router.swapExactTokensForTokens(
        amountIn,
        amountOutMin,
        [tokenIn, tokenOut],
        recipient,
        deadline
    );
    
    await tx.wait();
    console.log('Swap completed!');
}
```

## Impermanent Loss

### What Is It?

**Impermanent Loss** occurs when the price of tokens in a pool changes compared to when you deposited them.

### Example

**Initial State**:
- Deposit: 1 ETH + 2000 USDC (ETH = $2000)
- Total value: $4000
- Pool share: 1%

**Price Changes** (ETH doubles to $4000):
- Pool rebalances: 0.707 ETH + 2828 USDC
- Your share: 0.00707 ETH + 28.28 USDC
- Value: $2828 + $28.28 = $2856.28

**If You Held**:
- 1 ETH + 2000 USDC = $4000 + $2000 = $6000

**Impermanent Loss**: $6000 - $2856.28 = $3143.72 (but you earned trading fees!)

### Calculating Impermanent Loss

```javascript
function calculateImpermanentLoss(priceRatio) {
    // priceRatio = currentPrice / initialPrice
    const loss = 2 * Math.sqrt(priceRatio) / (1 + priceRatio) - 1;
    return loss * 100; // percentage
}

// Examples
console.log(calculateImpermanentLoss(1.25)); // 1.25x: -0.6%
console.log(calculateImpermanentLoss(1.50)); // 1.5x:  -2.0%
console.log(calculateImpermanentLoss(2.00)); // 2x:    -5.7%
console.log(calculateImpermanentLoss(4.00)); // 4x:    -20.0%
```

### Mitigating Impermanent Loss

1. **Provide liquidity to stable pairs** (USDC/DAI)
2. **Choose correlated assets** (ETH/WBTC)
3. **Consider trading fee income**
4. **Use impermanent loss insurance** (some protocols)

## Slippage

### What Is It?

**Slippage** is the difference between expected and executed price due to price movement during transaction.

### Types

1. **Price Slippage**: Market moves while transaction pending
2. **Liquidity Slippage**: Not enough liquidity for large trades

### Calculating Slippage

```javascript
function calculatePriceImpact(amountIn, reserveIn, reserveOut) {
    // Get expected output
    const amountInWithFee = amountIn * 0.997;
    const amountOut = (amountInWithFee * reserveOut) / (reserveIn + amountInWithFee);
    
    // Calculate price impact
    const executionPrice = amountIn / amountOut;
    const midPrice = reserveIn / reserveOut;
    const priceImpact = (executionPrice / midPrice - 1) * 100;
    
    return {
        amountOut,
        priceImpact: priceImpact.toFixed(2) + '%'
    };
}

// Example
const result = calculatePriceImpact(
    100,      // Buying 100 tokens
    10000,    // Reserve in
    20000     // Reserve out
);
console.log('Amount out:', result.amountOut);
console.log('Price impact:', result.priceImpact);
```

### Setting Slippage Tolerance

```javascript
async function swapWithSlippage(amountIn, path, slippageTolerance = 0.5) {
    // Get expected amounts
    const amounts = await router.getAmountsOut(amountIn, path);
    const expectedOut = amounts[amounts.length - 1];
    
    // Calculate minimum with slippage
    const slippageMultiplier = 1 - (slippageTolerance / 100);
    const amountOutMin = expectedOut.mul(
        Math.floor(slippageMultiplier * 10000)
    ).div(10000);
    
    // Execute swap
    await router.swapExactTokensForTokens(
        amountIn,
        amountOutMin,
        path,
        recipient,
        deadline
    );
}
```

## Fees

### Trading Fees

- **Uniswap V2**: 0.3% per trade (all to LPs)
- **Uniswap V3**: 0.05%, 0.3%, or 1% (based on pool tier)
- **SushiSwap**: 0.3% (0.25% to LPs, 0.05% to treasury)

### Fee APR Calculation

```javascript
function calculateFeeAPR(dailyVolume, totalLiquidity, feePercent = 0.3) {
    const dailyFees = dailyVolume * (feePercent / 100);
    const dailyReturn = dailyFees / totalLiquidity;
    const annualReturn = dailyReturn * 365;
    
    return annualReturn * 100; // percentage
}

// Example
const apr = calculateFeeAPR(
    1000000,  // $1M daily volume
    5000000,  // $5M liquidity
    0.3
);
console.log('Fee APR:', apr.toFixed(2) + '%');
```

## Uniswap V3 Improvements

### Concentrated Liquidity

Provide liquidity in specific price ranges for higher capital efficiency.

```javascript
// Uniswap V3 position
const position = {
    tokenA: 'ETH',
    tokenB: 'USDC',
    tickLower: 1800,  // Lower price bound
    tickUpper: 2200,  // Upper price bound
    liquidity: amount
};

// Only earns fees when price is in range [1800, 2200]
```

### Multiple Fee Tiers

- **0.05%**: Stable pairs (USDC/DAI)
- **0.30%**: Most pairs (ETH/USDC)
- **1.00%**: Exotic pairs

### Range Orders

Act as limit orders by providing liquidity at a specific price.

## Flash Swaps

Borrow tokens, use them, and repay in same transaction.

```solidity
contract FlashSwap {
    function executeFlashSwap(
        address token,
        uint amount
    ) external {
        // Borrow tokens from Uniswap
        IUniswapV2Pair(pair).swap(
            amount,
            0,
            address(this),
            abi.encode(token, amount)
        );
    }
    
    // Callback function
    function uniswapV2Call(
        address sender,
        uint amount0,
        uint amount1,
        bytes calldata data
    ) external {
        // Use borrowed tokens
        // ...perform arbitrage or other operations
        
        // Calculate repayment (amount + 0.3% fee)
        uint repayAmount = amount0 * 1003 / 1000;
        
        // Repay the flash loan
        IERC20(token0).transfer(msg.sender, repayAmount);
    }
}
```

## Price Oracles

Use Uniswap as a price oracle (V2 TWAP - Time Weighted Average Price).

```solidity
contract PriceOracle {
    address public pair;
    uint public price0CumulativeLast;
    uint public price1CumulativeLast;
    uint32 public blockTimestampLast;
    
    function update() external {
        (
            uint price0Cumulative,
            uint price1Cumulative,
            uint32 blockTimestamp
        ) = UniswapV2OracleLibrary.currentCumulativePrices(pair);
        
        uint32 timeElapsed = blockTimestamp - blockTimestampLast;
        require(timeElapsed >= PERIOD, 'Period not elapsed');
        
        // Calculate average price
        price0Average = (price0Cumulative - price0CumulativeLast) / timeElapsed;
        price1Average = (price1Cumulative - price1CumulativeLast) / timeElapsed;
        
        price0CumulativeLast = price0Cumulative;
        price1CumulativeLast = price1Cumulative;
        blockTimestampLast = blockTimestamp;
    }
}
```

## Best Practices

### For Liquidity Providers

1. ✅ Understand impermanent loss
2. ✅ Choose appropriate pairs
3. ✅ Monitor your positions
4. ✅ Consider V3 range positions
5. ✅ Factor in gas costs

### For Traders

1. ✅ Set appropriate slippage
2. ✅ Check price impact
3. ✅ Use limit orders for large trades
4. ✅ Monitor gas prices
5. ✅ Verify token addresses

### For Developers

1. ✅ Use official SDK
2. ✅ Handle edge cases
3. ✅ Implement price checks
4. ✅ Test on testnets
5. ✅ Monitor for front-running

## Code Examples

### Complete Swap Implementation

```javascript
import { ethers } from 'ethers';
import { UNISWAP_ROUTER_ABI, ERC20_ABI } from './abis';

class UniswapTrader {
    constructor(provider, routerAddress) {
        this.provider = provider;
        this.router = new ethers.Contract(
            routerAddress,
            UNISWAP_ROUTER_ABI,
            provider
        );
    }
    
    async getPrice(tokenIn, tokenOut, amountIn) {
        const amounts = await this.router.getAmountsOut(
            amountIn,
            [tokenIn, tokenOut]
        );
        return amounts[1];
    }
    
    async swap(tokenIn, tokenOut, amountIn, slippage = 0.5) {
        const signer = this.provider.getSigner();
        const tokenContract = new ethers.Contract(tokenIn, ERC20_ABI, signer);
        
        // Approve
        await tokenContract.approve(this.router.address, amountIn);
        
        // Get minimum output
        const amounts = await this.router.getAmountsOut(
            amountIn,
            [tokenIn, tokenOut]
        );
        const amountOutMin = amounts[1].mul(100 - slippage).div(100);
        
        // Swap
        const deadline = Math.floor(Date.now() / 1000) + 60 * 20; // 20 minutes
        
        const tx = await this.router.swapExactTokensForTokens(
            amountIn,
            amountOutMin,
            [tokenIn, tokenOut],
            await signer.getAddress(),
            deadline
        );
        
        return await tx.wait();
    }
}
```

## Resources

- [Uniswap Documentation](https://docs.uniswap.org/)
- [Uniswap V3 Whitepaper](https://uniswap.org/whitepaper-v3.pdf)
- [AMM Simulator](https://www.desmos.com/calculator/hqpmzgezxf)

**Next**: [Lending Protocols](lending-protocols.md) →
