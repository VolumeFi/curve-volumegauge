# @version ^0.2.0

# VolumeGauge for compound

# External Contracts
interface cERC20:
    def exchangeRateStored() -> uint256: view

interface ERC20:
    def balanceOf(arg0: address) -> uint256: view
    def approve(_spender: address, _value:uint256): nonpayable
    def decimals() -> uint256: view

interface SWAP:
    def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256): nonpayable
    def exchange_underlying(i: int128, j: int128, dx: uint256, min_dy: uint256): nonpayable

interface Tracker:
    def track(_sender: address,
        _tokenx: address,
        _tokeny: address,
        _price: uint256,
        _amount: uint256,
        _source_addr: address,
        _contract_addr: address): nonpayable

interface Aggregator:
    def latestAnswer() -> int128: view

# This can (and needs to) be changed at compile time
N_COINS: constant(int128) = 2  # <- change

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
usdaggregator: public(address)
crvaggregator: public(address)

@external
def __init__(
    _coins: address[N_COINS],
    _underlying_coins: address[N_COINS],
    _usdaggregator: address,
    _crvaggregator: address,
    _base: address,
    _tracker: address
):
    """
    @notice Contract constructor
    @param _coins Addresses of ERC20 conracts of coins (c-tokens) involved
    @param _underlying_coins Addresses of plain coins (ERC20)
    @param _usdaggregator Address of aggregators to get ETH/USD
    @param _crvaggregator Address of aggregators to get CRV/ETH
    @param _base Address of base swap contract
    @param _tracker Address of volume gauge tracker contract
    """
    for i in range(N_COINS):
        assert _coins[i] != ZERO_ADDRESS
        assert _underlying_coins[i] != ZERO_ADDRESS
        ERC20(_coins[i]).approve(_base, MAX_UINT256)
        ERC20(_underlying_coins[i]).approve(_base, MAX_UINT256)
    self.usdaggregator = _usdaggregator
    self.crvaggregator = _crvaggregator
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
# 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419 ETH / USD
# 0x8a12Be339B0cD1829b91Adc01977caa5E9ac121e CRV / ETH

@external
@nonreentrant('lock')
def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256):
    _coins: address[N_COINS] = self.coins
    _underlying_coins: address[N_COINS] = self.underlying_coins
    _base:address =  self.base
    _usdaggregator: address= self.usdaggregator
    _crvaggregator: address= self.crvaggregator

    # "safeTransferFrom" which works for ERC20s which return bool or not
    _response: Bytes[32] = raw_call(
        _coins[i],
        concat(
            method_id("transferFrom(address,address,uint256)"),
            convert(msg.sender, bytes32),
            convert(self, bytes32),
            convert(dx, bytes32),
        ),
        max_outsize=32
    )  # dev: failed transfer
    if len(_response) > 0:
        assert convert(_response, bool)  # dev: failed transfer

    SWAP(_base).exchange(i, j, dx, min_dy)

    dy: uint256 = 0
    dy = ERC20(_coins[j]).balanceOf(self)

    # "safeTransfer" which works for ERC20s which return bool or not
    _response = raw_call(
        _coins[j],
        concat(
            method_id("transfer(address,uint256)"),
            convert(msg.sender, bytes32),
            convert(dy, bytes32),
        ),
        max_outsize=32
    )  # dev: failed transfer
    if len(_response) > 0:
        assert convert(_response, bool)  # dev: failed transfer

    pricex: uint256 = 10 ** 26 / convert(Aggregator(_usdaggregator).latestAnswer(), uint256) # 10 ** 18 ETH price of 1 USD
    pricecrv: uint256 = 10 ** 36 / convert(Aggregator(_crvaggregator).latestAnswer(), uint256) # decimals : CRV price of 1 USD

    pricex = pricex * pricecrv / (10 ** 18) # CRV Price of USD Token

    exchangeratex: uint256 = cERC20(_coins[i]).exchangeRateStored() / (10 ** ERC20(_underlying_coins[i]).decimals())
    exchangeratey: uint256 = cERC20(_coins[j]).exchangeRateStored() / (10 ** ERC20(_underlying_coins[j]).decimals())
    pricex = pricex * exchangeratex / 10 ** 10 # ExchangeRate decimals : 10
    self.tracker.track(tx.origin, _coins[i], _coins[j], pricex, dx, msg.sender, _base)

    log TokenExchange(msg.sender, i, dx, j, dy)

@external
@nonreentrant('lock')
def exchange_underlying(i: int128, j: int128, dx: uint256, min_dy: uint256):
    _underlying_coins: address[N_COINS] = self.underlying_coins
    _base: address = self.base
    _usdaggregator: address= self.usdaggregator
    _crvaggregator: address= self.crvaggregator

    # "safeTransferFrom" which works for ERC20s which return bool or not
    _response: Bytes[32] = raw_call(
        _underlying_coins[i],
        concat(
            method_id("transferFrom(address,address,uint256)"),
            convert(msg.sender, bytes32),
            convert(self, bytes32),
            convert(dx, bytes32),
        ),
        max_outsize=32
    )  # dev: failed transfer
    if len(_response) > 0:
        assert convert(_response, bool)  # dev: failed transfer

    SWAP(_base).exchange_underlying(i, j, dx, min_dy)

    dy: uint256 = ERC20(_underlying_coins[j]).balanceOf(self)

    # "safeTransfer" which works for ERC20s which return bool or not
    _response = raw_call(
        _underlying_coins[j],
        concat(
            method_id("transfer(address,uint256)"),
            convert(msg.sender, bytes32),
            convert(dy, bytes32),
        ),
        max_outsize=32
    )  # dev: failed transfer
    if len(_response) > 0:
        assert convert(_response, bool)  # dev: failed transfer

    pricex: uint256 = 10 ** 26 / convert(Aggregator(_usdaggregator).latestAnswer(), uint256) # 10 ** 18 ETH price of 1 USD
    pricecrv: uint256 = 10 ** 36 / convert(Aggregator(_crvaggregator).latestAnswer(), uint256) # decimals : CRV price of 1 USD

    pricex = pricex * pricecrv / (10 ** 18) # CRV Price of Token
    
    self.tracker.track(tx.origin, _underlying_coins[i], _underlying_coins[j], pricex, dx, msg.sender, _base)

    log TokenExchangeUnderlying(msg.sender, i, dx, j, dy)

@external
def approveAllToBase():
    _base: address = self.base
    _coins: address[N_COINS] = self.coins
    _underlying_coins: address[N_COINS] = self.underlying_coins
    for i in range(N_COINS):
        ERC20(_coins[i]).approve(_base, MAX_UINT256)
        ERC20(_underlying_coins[i]).approve(_base, MAX_UINT256)