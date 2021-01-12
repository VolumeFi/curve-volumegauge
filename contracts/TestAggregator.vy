# @version ^0.2.0

# Test Aggregator ETH/USD

baseAggregator: public(address)

interface Aggregator:
    def latestAnswer() -> int128: view

@external
def __init__(_baseAggregator: address):
    self.baseAggregator = _baseAggregator
# ETH/USD : 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
# BTC/ETH : 0xdeb288F737066589598e9214E782fa5A8eD689e8
# CRV/ETH : 0x8a12Be339B0cD1829b91Adc01977caa5E9ac121e

@external
@view
def latestAnswer() -> int128:
    random:int128 = convert(convert(keccak256(convert(block.number, bytes32)), uint256) % 201, int128)
    _latestAnswer:int128 = Aggregator(self.baseAggregator).latestAnswer() * (900 + random) / 1000
    return _latestAnswer