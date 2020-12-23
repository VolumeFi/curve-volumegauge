# @version ^0.2.0
# (c) Curve.Fi, 2020

# External Contracts
interface cERC20:
    def transfer(_to: address, _value: uint256) -> bool: nonpayable
    def transferFrom(_from: address, _to: address, _value: uint256) -> bool: nonpayable
    def balanceOf(arg0: address) -> uint256: view
    def approve(_spender: address, _value:uint256): nonpayable
    def exchangeRateStored() -> uint256: view

# from vyper.interfaces import ERC20
interface ERC20:
    def transfer(_to: address, _value: uint256) -> bool: nonpayable
    def transferFrom(_from: address, _to: address, _value: uint256) -> bool: nonpayable
    def balanceOf(arg0: address) -> uint256: view
    def approve(_spender: address, _value:uint256): nonpayable
    def decimals() -> uint256: view

# Tether transfer-only ABI
interface USDT:
    def balanceOf(_to: address) -> uint256: view
    def transfer(_to: address, _value: uint256): nonpayable
    def transferFrom(_from: address, _to: address, _value: uint256): nonpayable
    def approve(_spender: address, _value:uint256): nonpayable

interface SWAP:
    def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256): nonpayable
    def exchange_underlying(i: int128, j: int128, dx: uint256, min_dy: uint256): nonpayable

interface Tracker:
    def track(_sender: address, _tokenx: address, _pricex: uint256, _amountx: uint256, _tokeny: address, _pricey: uint256, _amounty: uint256, _source_addr: address, _contract_addr: address): nonpayable

interface Aggregator:
    def latestAnswer() -> int128: view

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
base: public(address)
tracker: public(Tracker)
aggregators: public(address[N_COINS])
ethaggregator: public(address)
@external
def __init__(_coins: address[N_COINS], _underlying_coins: address[N_COINS],_aggregators: address[N_COINS], _ethaggregator: address, _base: address, _tracker: address):
    """
    _coins: Addresses of ERC20 conracts of coins (c-tokens) involved
    _underlying_coins: Addresses of plain coins (ERC20)
    """
    for i in range(N_COINS):
        assert _coins[i] != ZERO_ADDRESS
        assert _underlying_coins[i] != ZERO_ADDRESS
    self.aggregators = _aggregators
    self.ethaggregator = _ethaggregator
    self.coins = _coins
    self.underlying_coins = _underlying_coins
    self.base = _base
    self.tracker = Tracker(_tracker)

##### mainnet #####
# base
# 0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56
#
# coins
# 0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643 cDAI
# 0x39AA39c021dfbaE8faC545936693aC917d5E7563 cUSDC
#
# underlying coins
# 0x6B175474E89094C44Da98b954EedeAC495271d0F DAI
# 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 USDC
#
# aggregators
# 0x773616E4d11A78F511299002da57A0a94577F1f4 DAI / ETH
# 0x986b5E1e1755e3C2440e960477f25201B0a8bbD4 USDC / ETH
#
# ethaggregator
# 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419 ETH / USD
#
#
##### rinkeby #####
# base
# 0xA319E978505b19b5E145436Cc040c12E70e1840b
#
# coins
# 0x6D7F0754FFeb405d23C51CE938289d4835bE3b14 cDAI
# 0x5B281A6DdA0B271e91ae35DE655Ad301C976edb1 cUSDC
#
# underlying coins
# 0x5592EC0cfb4dbc12D3aB100b257153436a1f0FEa DAI
# 0x4DBCdF9B62e891a7cec5A2568C3F4FAF9E8Abe2b USDC
#
# aggregators
# 0x74825DbC8BF76CC4e9494d0ecB210f676Efa001D DAI / ETH
# 0xdCA36F27cbC4E38aE16C4E9f99D39b42337F6dcf USDC / ETH
#
# ethaggregator
# 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e ETH / USD

@external
@nonreentrant('lock')
def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256):
    tethered: bool[N_COINS] = TETHERED
    use_lending: bool[N_COINS] = USE_LENDING
    _coins: address[N_COINS] = self.coins
    _base:address =  self.base

    if tethered[i] and not use_lending[i]:
        USDT(_coins[i]).transferFrom(msg.sender, self, dx)
        USDT(_coins[i]).approve(_base, dx)
    else:
        cERC20(_coins[i]).transferFrom(msg.sender, self, dx)
        cERC20(_coins[i]).approve(_base, dx)

    SWAP(_base).exchange(i, j, dx, min_dy)

    dy: uint256 = 0
    if tethered[j] and not use_lending[j]:
        dy = USDT(_coins[j]).balanceOf(self)
        USDT(_coins[j]).transfer(msg.sender, dy)
    else:
        dy = cERC20(_coins[j]).balanceOf(self)
        cERC20(_coins[j]).transfer(msg.sender, dy)

    pricex: uint256 = convert(Aggregator(self.aggregators[i]).latestAnswer(), uint256)
    pricey: uint256 = convert(Aggregator(self.aggregators[j]).latestAnswer(), uint256)
    priceeth: uint256 = convert(Aggregator(self.ethaggregator).latestAnswer(), uint256) # decimals : 8
    pricex = pricex * priceeth / (10 ** 18) # USD price per token
    pricey = pricey * priceeth / (10 ** 18) # USD price per token

    exchangeratex: uint256 = cERC20(_coins[i]).exchangeRateStored() / (10 ** ERC20(self.underlying_coins[i]).decimals())
    exchangeratey: uint256 = cERC20(_coins[j]).exchangeRateStored() / (10 ** ERC20(self.underlying_coins[j]).decimals())
    pricex = pricex * exchangeratex / 10 ** 10 # ExchangeRate decimals : 10
    pricey = pricey * exchangeratey / 10 ** 10 # ExchangeRate decimals : 10
    self.tracker.track(tx.origin, _coins[i], pricex, dx, _coins[j], pricey, dy, msg.sender, _base)

    log TokenExchange(msg.sender, i, dx, j, dy)

@external
@nonreentrant('lock')
def exchange_underlying(i: int128, j: int128, dx: uint256, min_dy: uint256):
    use_lending: bool[N_COINS] = USE_LENDING
    tethered: bool[N_COINS] = TETHERED
    _underlying_coins: address[N_COINS] = self.underlying_coins
    _base: address = self.base
    ok: uint256 = 0
    if tethered[i]:
        USDT(_underlying_coins[i]).transferFrom(msg.sender, self, dx)
        USDT(_underlying_coins[i]).approve(_base, dx)
    else:
        ERC20(_underlying_coins[i]).transferFrom(msg.sender, self, dx)
        ERC20(_underlying_coins[i]).approve(_base, dx)

    SWAP(_base).exchange_underlying(i, j, dx, min_dy)

    dy: uint256 = 0

    if tethered[j]:
        dy = USDT(_underlying_coins[j]).balanceOf(self)
        USDT(_underlying_coins[j]).transfer(msg.sender, dy)
    else:
        dy = ERC20(_underlying_coins[j]).balanceOf(self)
        ERC20(_underlying_coins[j]).transfer(msg.sender, dy)

    pricex: uint256 = convert(Aggregator(self.aggregators[i]).latestAnswer(), uint256)
    pricey: uint256 = convert(Aggregator(self.aggregators[j]).latestAnswer(), uint256)
    priceeth: uint256 = convert(Aggregator(self.ethaggregator).latestAnswer(), uint256)
    pricex = pricex * priceeth / (10 ** 18)
    pricey = pricey * priceeth / (10 ** 18)
    self.tracker.track(tx.origin, _underlying_coins[i], pricex, dx, _underlying_coins[j], pricey, dy, msg.sender, _base)
    log TokenExchangeUnderlying(msg.sender, i, dx, j, dy)
