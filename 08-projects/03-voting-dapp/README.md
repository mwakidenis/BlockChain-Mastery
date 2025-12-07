# Project 3: Decentralized Voting DApp 🗳️

Create a decentralized voting application where users can create polls and vote on proposals.

## 🎯 Learning Objectives

- Write and deploy smart contracts
- Build frontend with Web3 integration
- Implement voting mechanisms
- Handle blockchain state management
- Test smart contracts

## 📋 Requirements

### Smart Contract Features

1. **Poll Creation**
   - Create new polls
   - Set voting duration
   - Add options
   - Ownership control

2. **Voting**
   - Cast votes
   - One vote per address
   - Vote weight (optional)
   - Anonymous voting

3. **Results**
   - Real-time tallying
   - Winner determination
   - View all polls

### Frontend Features

- Connect wallet
- Create poll interface
- Vote on active polls
- View results
- Poll history

## 🛠️ Smart Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingDApp {
    struct Poll {
        string question;
        string[] options;
        uint256[] votes;
        uint256 endTime;
        address creator;
        mapping(address => bool) hasVoted;
    }
    
    mapping(uint256 => Poll) public polls;
    uint256 public pollCount;
    
    event PollCreated(uint256 indexed pollId, string question, address creator);
    event Voted(uint256 indexed pollId, uint256 optionIndex, address voter);
    
    function createPoll(
        string memory question,
        string[] memory options,
        uint256 duration
    ) public {
        uint256 pollId = pollCount++;
        Poll storage poll = polls[pollId];
        
        poll.question = question;
        poll.options = options;
        poll.votes = new uint256[](options.length);
        poll.endTime = block.timestamp + duration;
        poll.creator = msg.sender;
        
        emit PollCreated(pollId, question, msg.sender);
    }
    
    function vote(uint256 pollId, uint256 optionIndex) public {
        Poll storage poll = polls[pollId];
        
        require(block.timestamp < poll.endTime, "Poll ended");
        require(!poll.hasVoted[msg.sender], "Already voted");
        require(optionIndex < poll.options.length, "Invalid option");
        
        poll.hasVoted[msg.sender] = true;
        poll.votes[optionIndex]++;
        
        emit Voted(pollId, optionIndex, msg.sender);
    }
    
    function getResults(uint256 pollId) public view returns (uint256[] memory) {
        return polls[pollId].votes;
    }
}
```

## 📚 Frontend Integration

```javascript
import { ethers } from 'ethers';

async function createPoll(question, options, duration) {
    const contract = new ethers.Contract(
        CONTRACT_ADDRESS,
        ABI,
        signer
    );
    
    const tx = await contract.createPoll(question, options, duration);
    await tx.wait();
    
    console.log('Poll created!');
}

async function vote(pollId, optionIndex) {
    const tx = await contract.vote(pollId, optionIndex);
    await tx.wait();
    
    console.log('Vote cast!');
}
```

## ✅ Completion Checklist

- [ ] Write smart contract
- [ ] Deploy to testnet
- [ ] Build frontend
- [ ] Connect wallet
- [ ] Create poll feature
- [ ] Voting feature
- [ ] Results display
- [ ] Test thoroughly
