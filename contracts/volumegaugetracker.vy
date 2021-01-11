# @version ^0.2.0

# from vyper.interfaces import ERC20
interface ERC20:
    def decimals() -> uint256: view

struct TrackData:
    tokenx: address
    tokeny: address
    price: uint256
    amount: uint256
    source_addr: address
    contract_addr: address
    time_stamp: uint256

trackData: public(HashMap[address, TrackData[1000000000000]])
trackDataSize: public(HashMap[address, uint256])

# tokenPrice: public(HashMap[address, HashMap[uint256, uint256]])
lastVolume: public(HashMap[address, uint256])
lastAmount: public(HashMap[address, uint256])
lastDate: public(HashMap[address, uint256])
currentVolume: public(HashMap[address, uint256])
currentAmount: public(HashMap[address, uint256])

PERIOD: constant(uint256) = 30
DENOMINATOR: constant(uint256) = 10 ** 18
SMOOTHING: constant(uint256) = 2
ALPHA: constant(uint256) = DENOMINATOR - SMOOTHING * DENOMINATOR / (PERIOD + 1)
DAY: constant(uint256) = 86400 # 600 for test - 10 minutes
rewardAmount: public(uint256) # based on USD, decimals 8

gauges: public(HashMap[address, bool])
owner: public(address)

fee: public(uint256)


@external
def __init__():
    self.owner = msg.sender
    self.fee = 2 * 10 ** 14

@external
def addGauge(_gauge: address):
    assert self.owner == msg.sender
    self.gauges[_gauge] = True

@external
def track(_sender: address,
    _tokenx: address,
    _tokeny: address,
    _price: uint256,
    _amount: uint256,
    _source_addr: address,
    _contract_addr: address):
    assert self.gauges[msg.sender] == True
    trackdatum:TrackData = TrackData({tokenx: _tokenx, tokeny: _tokeny, price: _price, amount: _amount, source_addr: _source_addr, contract_addr: _contract_addr, time_stamp: block.timestamp})
    _length:uint256 = self.trackDataSize[_sender]
    self.trackData[_sender][_length] = trackdatum
    self.trackDataSize[_sender] = _length + 1

    date: uint256 = block.timestamp / DAY
    lastvolume: uint256 = self.lastVolume[_tokenx]
    lastamount: uint256 = self.lastAmount[_tokenx]
    currentvolume: uint256 = self.currentVolume[_tokenx]
    currentamount: uint256 = self.currentAmount[_tokenx]
    if self.lastDate[_tokenx] != date:
        lastvolume = (ALPHA * lastvolume + (DENOMINATOR - ALPHA) * currentvolume) / DENOMINATOR
        lastamount = (ALPHA * lastamount + (DENOMINATOR - ALPHA) * currentamount) / DENOMINATOR
        self.lastVolume[_tokenx] = lastvolume
        self.lastAmount[_tokenx] = lastamount
        currentvolume = 0
        currentamount = 0
        self.lastDate[_tokenx] = date

    currentvolume += _amount * _price
    currentamount += _amount
    self.currentVolume[_tokenx] = currentvolume
    self.currentAmount[_tokenx] = currentamount

    newvolume_num: uint256 = ALPHA * lastvolume + (DENOMINATOR - ALPHA) * currentvolume # Numerator
    newamount_num: uint256 = ALPHA * lastamount + (DENOMINATOR - ALPHA) * currentamount # Numerator
    price_v_ema:uint256 = newvolume_num / newamount_num
    self.rewardAmount += price_v_ema * _amount * self.fee / DENOMINATOR / 10 ** ERC20(_tokenx).decimals()

@external
def set_fee(_fee: uint256):
    assert self.owner == msg.sender
    self.fee = _fee
