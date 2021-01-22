# @version ^0.2.0

# VolumeGauge for ren

# External Contracts

interface ERC20:
    def balanceOf(arg0: address) -> uint256: view
    def approve(_spender: address, _value:uint256): nonpayable
    def decimals() -> uint256: view

interface SWAP:
    def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256): nonpayable

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
BASE: constant(address) = 0x93054188d876f558f4a66B2EF1d97d16eDf0895B
renBTC: constant(address) = 0xEB4C2781e4ebA804CE9a9803C67d0893436bB27D
WBTC: constant(address) = 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599
COINS: constant(address[N_COINS]) = [renBTC, WBTC]
# will use constant instead of storage
BTCETHAGGREGATOR: constant(address) = 0xdeb288F737066589598e9214E782fa5A8eD689e8
CRVETHAGGREGATOR: constant(address) = 0x8a12Be339B0cD1829b91Adc01977caa5E9ac121e


tracker: public(Tracker)
btcaggregator: public(address)
crvaggregator: public(address)


@external
def __init__(
    _tracker: address,
    _btcaggregator: address,
    _crvaggregator: address
):
    """
    @notice Contract constructor
    @param _tracker Address of volume gauge tracker contract
    @param _btcaggregator Address of aggregators to get ETH/USD
    @param _crvaggregator Address of aggregators to get CRV/ETH
    """
    coins: address[N_COINS] = COINS
    for i in range(N_COINS):
        ERC20(coins[i]).approve(BASE, MAX_UINT256)
    self.tracker = Tracker(_tracker)
    self.btcaggregator = _btcaggregator
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

    # pricex: uint256 = convert(Aggregator(BTCETHAGGREGATOR).latestAnswer(), uint256) * 10 ** 18 / convert(Aggregator(CRVETHAGGREGATOR).latestAnswer(), uint256)
    pricex: uint256 = convert(Aggregator(self.btcaggregator).latestAnswer(), uint256) * 10 ** 18 / convert(Aggregator(self.crvaggregator).latestAnswer(), uint256)

    self.tracker.track(tx.origin, coins[i], coins[j], pricex, dx, dy, msg.sender, BASE)
