# @version ^0.2.0

# Test Aggregator ETH/USD

baseAggregator: public(address)
nonce_num: public(uint256)

interface Aggregator:
    def lastestAnswer() -> uint256: view

@external
def __init__(_baseAggregator: address):
    self.baseAggregator = _baseAggregator
    self.nonce_num = 0
# ETH/USD : 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
# BTC/ETH : 0xdeb288F737066589598e9214E782fa5A8eD689e8
# CRV/ETH : 0x8a12Be339B0cD1829b91Adc01977caa5E9ac121e

@external
def lastestAnswer() -> uint256:
    random:uint256 = convert(keccak256(convert(block.number + self.nonce_num, bytes32)), uint256) % 201
    self.nonce_num += 1
    _lastestAnswer:uint256 = Aggregator(self.baseAggregator).lastestAnswer() * (900 + random) / 1000
    return _lastestAnswer