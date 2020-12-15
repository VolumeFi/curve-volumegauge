# (c) Curve.Fi, 2020

# External Contracts
interface cERC20:
    def transfer(_to: address, _value: uint256) -> bool: nonpayable
    def transferFrom(_from: address, _to: address, _value: uint256) -> bool: nonpayable
    def balanceOf(arg0: address) -> uint256: view

from vyper.interfaces import ERC20

# Tether transfer-only ABI
interface USDT:
    def balanceOf(_to: address) -> uint256: view
    def transfer(_to: address, _value: uint256): nonpayable
    def transferFrom(_from: address, _to: address, _value: uint256): nonpayable

interface SWAP:
    def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256): nonpayable
    def exchange_underlying(i: int128, j: int128, dx: uint256, min_dy: uint256): nonpayable

# This can (and needs to) be changed at compile time
N_COINS: constant(int128) = 2  # <- change
USE_LENDING: constant(bool[N_COINS]) = [True, True]
TETHERED: constant(bool[N_COINS]) = [False, False]

# Events
event TokenExchange:
    buyer: indexed(address)
    sold_id: int128
    tokens_sold: uint256
    bought_id: int128
    tokens_bought: uint256

event TokenExchangeUnderlying:
    buyer: indexed(address)
    sold_id: int128
    tokens_sold: uint256
    bought_id: int128
    tokens_bought: uint256


coins: public(address[N_COINS])
underlying_coins: public(address[N_COINS])

A: public(uint256)  # 2 x amplification coefficient
fee: public(uint256)  # fee * 1e10
admin_fee: public(uint256)  # admin_fee * 1e10
base: public(address)

@external
def __init__(_coins: address[N_COINS], _underlying_coins: address[N_COINS], _base: address):
    """
    _coins: Addresses of ERC20 conracts of coins (c-tokens) involved
    _underlying_coins: Addresses of plain coins (ERC20)
    """
    for i in range(N_COINS):
        assert _coins[i] != ZERO_ADDRESS
        assert _underlying_coins[i] != ZERO_ADDRESS
    self.coins = _coins
    self.underlying_coins = _underlying_coins
    self.base = _base


@external
@nonreentrant('lock')
def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256):
    tethered: bool[N_COINS] = TETHERED
    use_lending: bool[N_COINS] = USE_LENDING

    if tethered[i] and not use_lending[i]:
        USDT(self.coins[i]).transferFrom(msg.sender, self, dx)
    else:
        cERC20(self.coins[i]).transferFrom(msg.sender, self, dx)

    SWAP(self.base).exchange(i, j, dx, min_dy)

    dy: uint256 = 0
    if tethered[j] and not use_lending[j]:
        dy = USDT(self.coins[j]).balanceOf(self)
        USDT(self.coins[j]).transfer(msg.sender, dy)
    else:
        dy = cERC20(self.coins[j]).balanceOf(self)
        cERC20(self.coins[j]).transfer(msg.sender, dy)
        
    log TokenExchange(msg.sender, i, dx, j, dy)

@external
@nonreentrant('lock')
def exchange_underlying(i: int128, j: int128, dx: uint256, min_dy: uint256):
    use_lending: bool[N_COINS] = USE_LENDING
    tethered: bool[N_COINS] = TETHERED

    ok: uint256 = 0
    if tethered[i]:
        USDT(self.underlying_coins[i]).transferFrom(msg.sender, self, dx)
    else:
        ERC20(self.underlying_coins[i]).transferFrom(msg.sender, self, dx)
    
    SWAP(self.base).exchange_underlying(i, j, dx, min_dy)

    dy: uint256 = 0

    if tethered[j]:
        dy = USDT(self.underlying_coins[j]).balanceOf(self)
        USDT(self.underlying_coins[j]).transfer(msg.sender, dy)
    else:
        dy = ERC20(self.underlying_coins[j]).balanceOf(self)
        ERC20(self.underlying_coins[j]).transfer(msg.sender, dy)

    log TokenExchangeUnderlying(msg.sender, i, dx, j, dy)
