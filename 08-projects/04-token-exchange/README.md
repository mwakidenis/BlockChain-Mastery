# Project 4: Token Exchange (DEX) 🔄

Build a decentralized exchange where users can swap ERC-20 tokens using an automated market maker (AMM).

## 🎯 Learning Objectives

- Implement AMM logic
- Create liquidity pools
- Handle token swaps
- Calculate prices
- Manage liquidity providers

## 📋 Features

### Core Functionality

1. **Liquidity Pools**
   - Add liquidity
   - Remove liquidity
   - LP token minting

2. **Token Swaps**
   - Swap token A for token B
   - Price calculation
   - Slippage protection

3. **Price Discovery**
   - Constant product formula
   - Real-time pricing

## 🛠️ Smart Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleAMM {
    address public token0;
    address public token1;
    uint256 public reserve0;
    uint256 public reserve1;
    
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    
    function addLiquidity(uint256 amount0, uint256 amount1) external {
        IERC20(token0).transferFrom(msg.sender, address(this), amount0);
        IERC20(token1).transferFrom(msg.sender, address(this), amount1);
        
        uint256 liquidity;
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
        
        reserve0 += amount0;
        reserve1 += amount1;
    }
    
    function swap(address tokenIn, uint256 amountIn) external {
        require(tokenIn == token0 || tokenIn == token1, "Invalid token");
        
        bool isToken0 = tokenIn == token0;
        (uint256 reserveIn, uint256 reserveOut) = isToken0 
            ? (reserve0, reserve1) 
            : (reserve1, reserve0);
        
        uint256 amountInWithFee = amountIn * 997;
        uint256 amountOut = (amountInWithFee * reserveOut) / 
                            (reserveIn * 1000 + amountInWithFee);
        
        IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn);
        IERC20(isToken0 ? token1 : token0).transfer(msg.sender, amountOut);
        
        if (isToken0) {
            reserve0 += amountIn;
            reserve1 -= amountOut;
        } else {
            reserve1 += amountIn;
            reserve0 -= amountOut;
        }
    }
}
```

## ✅ Completion Checklist

- [ ] Write AMM contract
- [ ] Deploy tokens
- [ ] Deploy DEX
- [ ] Add liquidity feature
- [ ] Swap functionality
- [ ] Price display
- [ ] Test on testnet
