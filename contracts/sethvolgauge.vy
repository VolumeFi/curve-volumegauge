# @version ^0.2.0

# VolumeGauge for seth

# External Contracts

interface ERC20:
    def balanceOf(arg0: address) -> uint256: view
    def approve(_spender: address, _value:uint256): nonpayable

interface SWAP:
    def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256) -> uint256: payable

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
BASE: constant(address) = 0xc5424B857f758E906013F3555Dad202e4bdB4567
ETH: constant(address) = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
sETH: constant(address) = 0x5e74C9036fb86BD7eCdcb084a0673EFc32eA31cb
COINS: constant(address[N_COINS]) = [ETH, sETH]
# will use constant instead of storage
CRVETHAGGREGATOR: constant(address) = 0x8a12Be339B0cD1829b91Adc01977caa5E9ac121e


tracker: public(Tracker)
crvaggregator: public(address)


@external
def __init__(
    _tracker: address,
    _crvaggregator: address
):
    """
    @notice Contract constructor
    @param _tracker Address of volume gauge tracker contract
    @param _crvaggregator Address of aggregators to get CRV/ETH
    """
    ERC20(sETH).approve(BASE, MAX_UINT256)
    self.tracker = Tracker(_tracker)
    self.crvaggregator = _crvaggregator

@external
@payable
def __default__():
    assert True

@payable
@external
@nonreentrant('lock')
def exchange(i: int128, j: int128, dx: uint256, min_dy: uint256) -> uint256:
    # "safeTransferFrom" which works for ERC20s which return bool or not
    coins: address[N_COINS] = COINS

    if coins[i] == ETH:
        assert msg.value == dx
    else:
        assert msg.value == 0
        _response: Bytes[32] = raw_call(
            coins[i],
            concat(
                method_id("transferFrom(address,address,uint256)"),
                convert(msg.sender, bytes32),
                convert(self, bytes32),
                convert(dx, bytes32),
            ),
            max_outsize=32,
        )  # dev: failed transfer
        if len(_response) > 0:
            assert convert(_response, bool)

    dy: uint256 = SWAP(BASE).exchange(i, j, dx, min_dy, value=msg.value)

    if coins[j] == ETH:
        # dy = self.balance
        send(msg.sender, dy)
    else:
        # dy = ERC20(coins[j]).balanceOf(self)
        _response: Bytes[32] = raw_call(
            coins[j],
            concat(
                method_id("transfer(address,uint256)"),
                convert(msg.sender, bytes32),
                convert(dy, bytes32),
            ),
            max_outsize=32,
        )  # dev: failed transfer
        if len(_response) > 0:
            assert convert(_response, bool)

    # pricex: uint256 = 10 ** 36 / convert(Aggregator(CRVETHAGGREGATOR).latestAnswer(), uint256)
    pricex: uint256 = 10 ** 36 / convert(Aggregator(self.crvaggregator).latestAnswer(), uint256)

    self.tracker.track(tx.origin, coins[i], coins[j], pricex, dx, dy, msg.sender, BASE)

    return dy
