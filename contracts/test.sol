// SPDX-License-Identifier: MIT

pragma solidity ^0.7.0;

interface ERC20 {
    function balanceOf(address) external returns(uint256);
    function transferFrom(address, address, uint256) external;
    function transfer(address, uint256) external;
    function approve(address, uint256) external;
}

interface Gauge {
    function exchange(int128, int128, uint256, uint256) external;
    function exchange_underlying(int128, int128, uint256, uint256) external;
}

interface Swap {
    function add_liquidity(uint256[2] memory, uint256) external;
}

contract Test {

    ERC20 public token1;
    ERC20 public token2;
    ERC20 public ctoken1;
    ERC20 public ctoken2;
    ERC20 public ptoken;
    Gauge public gauge;
    Swap public swap;
    address public owner;

    constructor (address _gauge) {
        owner = msg.sender;
        token1 = ERC20(0x5592EC0cfb4dbc12D3aB100b257153436a1f0FEa);
        token2 = ERC20(0x4DBCdF9B62e891a7cec5A2568C3F4FAF9E8Abe2b);
        ctoken1 = ERC20(0x6D7F0754FFeb405d23C51CE938289d4835bE3b14);
        ctoken2 = ERC20(0x5B281A6DdA0B271e91ae35DE655Ad301C976edb1);
        ptoken = ERC20(0xb50FfA66bdF880B15635cd417218D46109Fb7060);
        gauge = Gauge(_gauge);
        swap = Swap(0xA319E978505b19b5E145436Cc040c12E70e1840b);
    }

    function test_underlying_token(int128 i, int128 j, uint256 dx, uint256 min_dy) external {
        token1.approve(address(gauge), uint256(-1));
        token2.approve(address(gauge), uint256(-1));
        gauge.exchange_underlying(i, j, dx, min_dy);
        payback();
    }

    function test_compound_token(int128 i, int128 j, uint256 dx, uint256 min_dy) external {
        ctoken1.approve(address(gauge), uint256(-1));
        ctoken2.approve(address(gauge), uint256(-1));
        gauge.exchange(i, j, dx, min_dy);
        payback();
    }

    function deposit(uint256 amount1, uint256 amount2) external {
        ctoken1.approve(address(swap), uint256(-1));
        ctoken2.approve(address(swap), uint256(-1));
        uint256[2] memory amounts = [amount1, amount2];
        swap.add_liquidity(amounts, 0);
        payback();
    }

    function payback() public {
        uint256 amount = token1.balanceOf(address(this));
        if (amount > 0)
            token1.transfer(owner, amount);
        amount = token2.balanceOf(address(this));
        if (amount > 0)
            token2.transfer(owner, amount);
        amount = ctoken1.balanceOf(address(this));
        if (amount > 0)
            ctoken1.transfer(owner, amount);
        amount = ctoken2.balanceOf(address(this));
        if (amount > 0)
            ctoken2.transfer(owner, amount);
        amount = ptoken.balanceOf(address(this));
        if (amount > 0)
            ptoken.transfer(owner, amount);
    }
}
