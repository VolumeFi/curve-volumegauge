# @version ^0.2.0

# from vyper.interfaces import ERC20
interface ERC20:
    def decimals() -> uint256: view

struct TrackData:
    tokenx: address
    pricex: uint256
    amountx: uint256
    tokeny: address
    pricey: uint256
    amounty: uint256
    source_addr: address
    contract_addr: address
    time_stamp: uint256

trackData: public(HashMap[address, TrackData[1000000000000]])
trackDataSize: public(HashMap[address, uint256])

tokenPrice: public(HashMap[address, HashMap[uint256, uint256]])

rewardAmount: public(uint256) # based on USD, decimals 8

gauges: public(HashMap[address, bool])
owner: public(address)

fee: public(uint256)

FEE_DENOMINATOR: constant(uint256) = 10 ** 10

@external
def __init__():
    self.owner = msg.sender
    self.fee = 2 * 10 ** 6

@external
def addGauge(_gauge: address):
    assert self.owner == msg.sender
    self.gauges[_gauge] = True

@external
def track(_sender: address,
    _tokenx: address,
    _pricex: uint256,
    _amountx: uint256,
    _tokeny: address,
    _pricey: uint256,
    _amounty: uint256,
    _source_addr: address,
    _contract_addr: address):
    assert self.gauges[msg.sender] == True
    trackdatum:TrackData = TrackData({tokenx: _tokenx, pricex: _pricex, amountx: _amountx, tokeny: _tokeny, pricey: _pricey, amounty: _amounty, source_addr: _source_addr, contract_addr: _contract_addr, time_stamp: block.timestamp})
    self.trackData[_sender][self.trackDataSize[_sender]] = trackdatum
    self.trackDataSize[_sender] += 1
    date: uint256 = block.timestamp / 86400
    isum: uint256 = 0
    current_price: uint256 = self.tokenPrice[_tokenx][date]
    if current_price == 0:
        self.tokenPrice[_tokenx][date] = _pricex
        current_price = _pricex
    token_price: uint256 = 0
    temp_price: uint256 = 0
    for i in range(1, 6):
        temp_price = self.tokenPrice[_tokenx][date - 7 + i] * i
        if temp_price > 0:
            token_price += temp_price
            isum += i
    token_price = (token_price + current_price * 7) / (isum + 7)
    self.rewardAmount += token_price * _amountx * self.fee / FEE_DENOMINATOR / 10 ** ERC20(_tokenx).decimals()

@external
def set_fee(_fee: uint256):
    assert self.owner == msg.sender
    self.fee = _fee
