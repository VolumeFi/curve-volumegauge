# @version ^0.2.0

# VolumeGauge for usdn

# External Contracts

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
        _pricex: uint256,
        _amountx: uint256,
        _amounty: uint256,
        _source_addr: address,
        _contract_addr: address): nonpayable

interface Aggregator:
    def latestAnswer() -> int128: view


# This can (and needs to) be changed at compile time
N_COINS: constant(int128) = 2  # <- change
MAX_COIN: constant(int128) = N_COINS - 1
BASE_POOL_COINS: constant(int128) = 3
BASE: constant(address) = 0x0f9cb53Ebe405d49A0bbdBD291A65Ff571bC83e1
USDN: constant(address) = 0x674C6Ad92Fd080e4004b2312b45f796a192D27a0
CRV3: constant(address) = 0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490
DAI: constant(address) = 0x6B175474E89094C44Da98b954EedeAC495271d0F
USDC: constant(address) = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
USDT: constant(address) = 0xdAC17F958D2ee523a2206206994597C13D831ec7
COINS: constant(address[N_COINS]) = [USDN, CRV3]
BASE_COINS: constant(address[BASE_POOL_COINS]) = [DAI, USDC, USDT]
ETHUSDAGGREGATOR: constant(address) = 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
CRVETHAGGREGATOR: constant(address) = 0x8a12Be339B0cD1829b91Adc01977caa5E9ac121e


tracker: public(Tracker)
usdaggregator: public(address)
crvaggregator: public(address)


@external
def __init__(_tracker: address, _usdaggregator: address, _crvaggregator: address):
    """
    @notice Contract constructor
    @param _tracker Address of volume gauge tracker contract
    @param _usdaggregator Address of aggregators to get ETH/USD
    @param _crvaggregator Address of aggregators to get CRV/ETH
    """
    coins: address[N_COINS] = COINS
    base_coins: address[BASE_POOL_COINS] = BASE_COINS
    for i in range(N_COINS):
        ERC20(coins[i]).approve(BASE, MAX_UINT256)
    for i in range(BASE_POOL_COINS):
        ERC20(base_coins[i]).approve(BASE, MAX_UINT256)
    self.tracker = Tracker(_tracker)
    self.usdaggregator = _usdaggregator
    self.crvaggregator = _crvaggregator

@external
@nonreentrant('lock')
def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256):
    coins: address[N_COINS] = COINS

    # "safeTransferFrom" which works for ERC20s which return bool or not
    _response: Bytes[32] = raw_call(
        coins[i],
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

    SWAP(BASE).exchange(i, j, dx, min_dy)

    dy: uint256 = 0
    dy = ERC20(coins[j]).balanceOf(self)

    # "safeTransfer" which works for ERC20s which return bool or not
    _response = raw_call(
        coins[j],
        concat(
            method_id("transfer(address,uint256)"),
            convert(msg.sender, bytes32),
            convert(dy, bytes32),
        ),
        max_outsize=32
    )  # dev: failed transfer
    if len(_response) > 0:
        assert convert(_response, bool)  # dev: failed transfer

    # pricex:uint256 = 10 ** 44 / convert(Aggregator(ETHUSDAGGREGATOR).latestAnswer(), uint256) / convert(Aggregator(CRVETHAGGREGATOR).latestAnswer(), uint256) # 18(CRV/ETH) + 8(ETH/USD) + 18 = 44
    pricex:uint256 = 10 ** 44 / convert(Aggregator(self.usdaggregator).latestAnswer(), uint256) / convert(Aggregator(self.crvaggregator).latestAnswer(), uint256) # 18(CRV/ETH) + 8(ETH/USD) + 18 = 44

    # pricex = pricex * yERC20(coins[i]).getPricePerFullShare() / 10 ** 18 # ExchangeRate decimals : 18

    self.tracker.track(tx.origin, coins[i], coins[j], pricex, dx, dy, msg.sender, BASE)

@external
@nonreentrant('lock')
def exchange_underlying(i: int128, j: int128, dx: uint256, min_dy: uint256):
    coins: address[N_COINS] = COINS
    base_coins: address[BASE_POOL_COINS] = BASE_COINS
    # Use base_i or base_j if they are >= 0
    base_i: int128 = i - MAX_COIN
    base_j: int128 = j - MAX_COIN

    # Addresses for input and output coins
    input_coin: address = ZERO_ADDRESS
    if base_i < 0:
        input_coin = coins[i]
    else:
        input_coin = base_coins[base_i]

    output_coin: address = ZERO_ADDRESS
    if base_j < 0:
        output_coin = coins[j]
    else:
        output_coin = base_coins[base_j]

    # "safeTransferFrom" which works for ERC20s which return bool or not
    _response: Bytes[32] = raw_call(
        input_coin,
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

    SWAP(BASE).exchange_underlying(i, j, dx, min_dy)

    dy: uint256 = ERC20(output_coin).balanceOf(self)

    # "safeTransfer" which works for ERC20s which return bool or not
    _response = raw_call(
        output_coin,
        concat(
            method_id("transfer(address,uint256)"),
            convert(msg.sender, bytes32),
            convert(dy, bytes32),
        ),
        max_outsize=32
    )  # dev: failed transfer
    if len(_response) > 0:
        assert convert(_response, bool)  # dev: failed transfer

    # pricex:uint256 = 10 ** 44 / convert(Aggregator(ETHUSDAGGREGATOR).latestAnswer(), uint256) / convert(Aggregator(CRVETHAGGREGATOR).latestAnswer(), uint256) # 18(CRV/ETH) + 8(ETH/USD) + 18 = 44
    pricex:uint256 = 10 ** 44 / convert(Aggregator(self.usdaggregator).latestAnswer(), uint256) / convert(Aggregator(self.crvaggregator).latestAnswer(), uint256) # 18(CRV/ETH) + 8(ETH/USD) + 18 = 44
    
    self.tracker.track(tx.origin, input_coin, output_coin, pricex, dx, dy, msg.sender, BASE)
