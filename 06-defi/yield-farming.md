# Yield Farming 🌾

Learn how to earn passive income through yield farming, liquidity mining, and staking in DeFi protocols.

## What is Yield Farming?

**Yield Farming** (or Liquidity Mining) is the practice of providing liquidity or staking assets to earn rewards, typically in the form of additional tokens.

## Key Concepts

### Annual Percentage Yield (APY)

**APY** includes compounding, while **APR** does not.

```javascript
function calculateAPY(apr, compoundingPeriods) {
    return (Math.pow(1 + apr / compoundingPeriods, compoundingPeriods) - 1) * 100;
}

// 20% APR with daily compounding
const apy = calculateAPY(0.20, 365);
console.log('APY:', apy.toFixed(2) + '%');  // 22.13%
```

### Total Value Locked (TVL)

Total amount of assets deposited in a protocol.

```javascript
async function calculateTVL(poolAddress) {
    const pool = new ethers.Contract(poolAddress, POOL_ABI, provider);
    
    const token0Balance = await token0.balanceOf(poolAddress);
    const token1Balance = await token1.balanceOf(poolAddress);
    
    const token0Price = await getPrice(token0.address);
    const token1Price = await getPrice(token1.address);
    
    const tvl = 
        token0Balance * token0Price + 
        token1Balance * token1Price;
    
    return tvl;
}
```

## Yield Farming Strategies

### 1. Liquidity Provision

Provide liquidity to DEX pools and earn trading fees + rewards.

```javascript
async function provideLiquidity(tokenA, tokenB, amountA, amountB) {
    const router = new ethers.Contract(
        UNISWAP_ROUTER,
        ROUTER_ABI,
        signer
    );
    
    // Approve tokens
    await tokenAContract.approve(router.address, amountA);
    await tokenBContract.approve(router.address, amountB);
    
    // Add liquidity
    const tx = await router.addLiquidity(
        tokenA,
        tokenB,
        amountA,
        amountB,
        amountA * 0.95,  // min amount (5% slippage)
        amountB * 0.95,
        await signer.getAddress(),
        Date.now() + 1000 * 60 * 20  // 20 min deadline
    );
    
    await tx.wait();
    console.log('Liquidity added!');
}
```

### 2. Staking

Lock tokens to earn rewards.

```javascript
async function stakeTokens(stakingPool, amount) {
    const pool = new ethers.Contract(
        stakingPool,
        STAKING_ABI,
        signer
    );
    
    // Approve staking token
    await tokenContract.approve(pool.address, amount);
    
    // Stake
    await pool.stake(amount);
    
    console.log('Tokens staked!');
}

async function claimRewards(stakingPool) {
    const pool = new ethers.Contract(
        stakingPool,
        STAKING_ABI,
        signer
    );
    
    await pool.claimReward();
    console.log('Rewards claimed!');
}
```

### 3. Lending & Borrowing

Supply assets to lending protocols, borrow against them, and farm with borrowed assets.

**Strategy**:
1. Supply ETH to Aave
2. Borrow stablecoins
3. Provide stablecoin liquidity
4. Earn LP rewards > borrow cost

### 4. Auto-Compounding Vaults

Protocols like Yearn automatically reinvest yields.

```javascript
async function depositToVault(vaultAddress, amount) {
    const vault = new ethers.Contract(
        vaultAddress,
        VAULT_ABI,
        signer
    );
    
    await tokenContract.approve(vault.address, amount);
    await vault.deposit(amount);
    
    console.log('Deposited to vault');
}
```

## Calculating Returns

### Simple Yield Calculation

```javascript
function calculateYield(principal, apy, days) {
    const dailyRate = apy / 365 / 100;
    const finalAmount = principal * Math.pow(1 + dailyRate, days);
    const profit = finalAmount - principal;
    
    return {
        finalAmount,
        profit,
        roi: (profit / principal) * 100
    };
}

// Example: $1000 for 30 days at 50% APY
const result = calculateYield(1000, 50, 30);
console.log('Profit:', result.profit.toFixed(2));
console.log('ROI:', result.roi.toFixed(2) + '%');
```

### Factoring in Impermanent Loss

```javascript
function calculateNetReturn(
    lpRewards,
    tradingFees,
    impermanentLoss,
    gasCosts
) {
    const totalEarnings = lpRewards + tradingFees;
    const netProfit = totalEarnings - impermanentLoss - gasCosts;
    
    return netProfit;
}

// Example
const netReturn = calculateNetReturn(
    500,   // $500 LP rewards
    200,   // $200 trading fees
    150,   // $150 impermanent loss
    50     // $50 gas costs
);
console.log('Net profit:', netReturn);  // $500
```

## Risk Management

### Risks in Yield Farming

1. **Smart Contract Risk** 🐛
   - Protocol bugs
   - Hacks and exploits
   
2. **Impermanent Loss** 📉
   - Price divergence in LP pairs
   
3. **Rug Pulls** 🏃
   - Malicious projects
   
4. **Liquidation Risk** ⚠️
   - When using leverage
   
5. **Token Price Risk** 💸
   - Reward token dumps

### Risk Mitigation

```javascript
class YieldFarmingStrategy {
    assessRisk(protocol) {
        const riskScore = {
            auditScore: this.checkAudits(protocol),
            tvlScore: this.checkTVL(protocol),
            timeScore: this.checkAge(protocol),
            teamScore: this.checkTeam(protocol)
        };
        
        const totalScore = Object.values(riskScore)
            .reduce((a, b) => a + b) / 4;
        
        return {
            score: totalScore,
            recommendation: totalScore > 7 ? 'Low Risk' : 
                          totalScore > 4 ? 'Medium Risk' : 'High Risk'
        };
    }
    
    checkAudits(protocol) {
        // Check for security audits
        const audits = protocol.audits || [];
        return audits.length >= 2 ? 10 : audits.length * 5;
    }
    
    checkTVL(protocol) {
        // Higher TVL = more trust
        const tvl = protocol.tvl;
        if (tvl > 1000000000) return 10;  // $1B+
        if (tvl > 100000000) return 7;    // $100M+
        if (tvl > 10000000) return 5;     // $10M+
        return 2;
    }
    
    checkAge(protocol) {
        // Older = more battle-tested
        const ageMonths = protocol.ageInMonths;
        if (ageMonths > 12) return 10;
        if (ageMonths > 6) return 7;
        if (ageMonths > 3) return 4;
        return 1;
    }
}
```

## Popular Yield Farming Protocols

### DeFi Blue Chips

| Protocol | Type | Average APY | Risk |
|----------|------|-------------|------|
| **Curve** | Stablecoin DEX | 5-20% | Low |
| **Aave** | Lending | 3-15% | Low |
| **Uniswap V3** | DEX | 10-50% | Medium |
| **Yearn** | Vault | 5-30% | Low |
| **Convex** | Curve Booster | 10-40% | Medium |

### Newer Protocols

Higher risk, potentially higher rewards:
- Newer DEXs on L2s
- New lending protocols
- Algorithmic stablecoins
- GameFi protocols

## Advanced Strategies

### 1. Leverage Yield Farming

Borrow to increase position size:

```
Capital: $1000
Borrow: $3000 (with collateral)
Total Farm: $4000
APY: 50%
Annual Yield: $2000
Borrow Cost: 10% on $3000 = $300
Net Profit: $1700 (170% on capital)
```

**Risks**: Liquidation if collateral drops

### 2. Yield Aggregation

Use multiple strategies simultaneously:

```javascript
class YieldAggregator {
    async optimizeYield(capital) {
        const strategies = [
            { protocol: 'Curve', apy: 15, risk: 2 },
            { protocol: 'Aave', apy: 10, risk: 1 },
            { protocol: 'Convex', apy: 25, risk: 4 }
        ];
        
        // Allocate based on risk-adjusted returns
        const allocation = this.allocateCapital(capital, strategies);
        
        for (const alloc of allocation) {
            await this.deposit(alloc.protocol, alloc.amount);
        }
    }
    
    allocateCapital(capital, strategies) {
        // Example: Equal weight
        const perStrategy = capital / strategies.length;
        
        return strategies.map(s => ({
            protocol: s.protocol,
            amount: perStrategy
        }));
    }
}
```

### 3. Auto-Compounding

Automatically reinvest rewards:

```javascript
async function autoCompound(farmAddress, interval = 86400) {
    const farm = new ethers.Contract(
        farmAddress,
        FARM_ABI,
        signer
    );
    
    setInterval(async () => {
        try {
            // Claim rewards
            const tx1 = await farm.claimReward();
            await tx1.wait();
            
            // Check reward balance
            const rewardBalance = await rewardToken.balanceOf(
                await signer.getAddress()
            );
            
            if (rewardBalance > minAmount) {
                // Sell half rewards for pairing token
                await swapTokens(rewardToken, pairToken, rewardBalance / 2);
                
                // Add liquidity
                await addLiquidity(rewardToken, pairToken);
                
                // Restake LP tokens
                const lpBalance = await lpToken.balanceOf(
                    await signer.getAddress()
                );
                await farm.stake(lpBalance);
                
                console.log('Compounded successfully');
            }
        } catch (error) {
            console.error('Compound failed:', error);
        }
    }, interval * 1000);
}
```

## Tax Considerations

### Taxable Events

- ✅ Claiming rewards
- ✅ Swapping tokens
- ✅ Harvesting and compounding
- ✅ Withdrawing liquidity

### Record Keeping

```javascript
class YieldTracker {
    constructor() {
        this.transactions = [];
    }
    
    recordDeposit(protocol, asset, amount, timestamp) {
        this.transactions.push({
            type: 'deposit',
            protocol,
            asset,
            amount,
            timestamp,
            txHash: '0x...'
        });
    }
    
    recordWithdrawal(protocol, asset, amount, timestamp) {
        this.transactions.push({
            type: 'withdrawal',
            protocol,
            asset,
            amount,
            timestamp,
            txHash: '0x...'
        });
    }
    
    recordReward(protocol, rewardAsset, amount, timestamp) {
        this.transactions.push({
            type: 'reward',
            protocol,
            asset: rewardAsset,
            amount,
            timestamp,
            txHash: '0x...'
        });
    }
    
    exportTaxReport() {
        // Generate CSV for tax software
        return this.transactions.map(tx => ({
            date: new Date(tx.timestamp).toLocaleDateString(),
            type: tx.type,
            asset: tx.asset,
            amount: tx.amount,
            protocol: tx.protocol
        }));
    }
}
```

## Tools & Resources

### Yield Aggregators
- **Yearn Finance** - Auto-compound vaults
- **Beefy Finance** - Multi-chain yield optimizer
- **Harvest Finance** - Automated farming

### Analytics
- **DeFi Llama** - TVL and APY tracking
- **APY.vision** - Impermanent loss calculator
- **DeBank** - Portfolio tracking
- **Zapper** - DeFi dashboard

### Calculators
- Impermanent loss calculators
- APY vs APR converters
- Gas cost estimators
- ROI calculators

## Best Practices

1. ✅ **Start small** - Test with small amounts
2. ✅ **Diversify** - Don't put all capital in one farm
3. ✅ **Research** - Check audits and team
4. ✅ **Calculate costs** - Factor in gas and fees
5. ✅ **Monitor** - Track positions daily
6. ✅ **Take profits** - Don't be greedy
7. ✅ **Consider taxes** - Keep good records
8. ✅ **Stay informed** - Join communities

## Resources

- [DeFi Pulse](https://defipulse.com/)
- [Yield farming tutorials](https://www.youtube.com/results?search_query=yield+farming+tutorial)
- [CoinGecko Yield Farming](https://www.coingecko.com/en/yield-farming)

**Next**: Continue to [NFTs](../07-nfts/) →
