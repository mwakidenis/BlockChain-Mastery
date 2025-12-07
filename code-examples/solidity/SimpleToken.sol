// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title SimpleToken
 * @dev A basic ERC-20 token implementation for learning purposes
 * @notice This is an educational example - use OpenZeppelin for production!
 */
contract SimpleToken {
    // Token metadata
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    
    // Balances for each account
    mapping(address => uint256) public balanceOf;
    
    // Allowances: owner => spender => amount
    mapping(address => mapping(address => uint256)) public allowance;
    
    // Events as per ERC-20 standard
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    
    /**
     * @dev Constructor to initialize the token
     * @param _name Token name
     * @param _symbol Token symbol
     * @param _decimals Number of decimals
     * @param _initialSupply Initial token supply
     */
    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 _initialSupply
    ) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _initialSupply * 10 ** uint256(_decimals);
        balanceOf[msg.sender] = totalSupply;
        
        emit Transfer(address(0), msg.sender, totalSupply);
    }
    
    /**
     * @dev Transfer tokens to a specified address
     * @param _to The address to transfer to
     * @param _value The amount to be transferred
     * @return success True if the operation was successful
     */
    function transfer(address _to, uint256 _value) 
        public 
        returns (bool success) 
    {
        require(_to != address(0), "Cannot transfer to zero address");
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
    
    /**
     * @dev Approve the passed address to spend tokens on behalf of msg.sender
     * @param _spender The address which will spend the funds
     * @param _value The amount of tokens to be spent
     * @return success True if the operation was successful
     */
    function approve(address _spender, uint256 _value) 
        public 
        returns (bool success) 
    {
        require(_spender != address(0), "Cannot approve zero address");
        
        allowance[msg.sender][_spender] = _value;
        
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    
    /**
     * @dev Transfer tokens from one address to another
     * @param _from The address which you want to send tokens from
     * @param _to The address which you want to transfer to
     * @param _value The amount of tokens to be transferred
     * @return success True if the operation was successful
     */
    function transferFrom(address _from, address _to, uint256 _value) 
        public 
        returns (bool success) 
    {
        require(_to != address(0), "Cannot transfer to zero address");
        require(_value <= balanceOf[_from], "Insufficient balance");
        require(_value <= allowance[_from][msg.sender], "Allowance exceeded");
        
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        
        emit Transfer(_from, _to, _value);
        return true;
    }
}
