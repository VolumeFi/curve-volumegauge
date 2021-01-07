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

# tokenPrice: public(HashMap[address, HashMap[uint256, uint256]])
lastVolume: public(HashMap[address, uint256])
lastAmount: public(HashMap[address, uint256])
lastDate: public(HashMap[address, uint256])
currentVolume: public(HashMap[address, uint256])
currentAmount: public(HashMap[address, uint256])

PERIOD: constant(uint256) = 30
DENOMINATOR: constant(uint256) = 10 ** 10
SMOOTHING: constant(uint256) = 2
ALPHA: constant(uint256) = DENOMINATOR - SMOOTHING * DENOMINATOR / (PERIOD + DENOMINATOR)
DAY: constant(uint256) = 600
rewardAmount: public(uint256) # based on USD, decimals 8

gauges: public(HashMap[address, bool])
owner: public(address)

fee: public(uint256)


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

    date: uint256 = block.timestamp / DAY
    lastvolume: uint256 = self.lastVolume[_tokenx]
    lastamount: uint256 = self.lastAmount[_tokenx]
    currentvolume: uint256 = 0
    currentamount: uint256 = 0
    if self.lastDate[_tokenx] != date:
        self.lastVolume[_tokenx] = ALPHA * lastvolume + (DENOMINATOR - ALPHA) * self.currentVolume[_tokenx]
        self.lastAmount[_tokenx] = ALPHA * lastamount + (DENOMINATOR - ALPHA) * self.currentAmount[_tokenx]
        self.lastDate[_tokenx] = date
    else:
        currentvolume = self.currentVolume[_tokenx]
        currentamount = self.currentAmount[_tokenx]

    newvolume: uint256 = 0
    newamount: uint256 = 0
    currentvolume += _amountx * _pricex
    currentamount += _amountx
    self.currentVolume[_tokenx] = currentvolume
    self.currentAmount[_tokenx] = currentamount

    newvolume = ALPHA * lastvolume + (DENOMINATOR - ALPHA) * currentvolume
    newamount = ALPHA * lastamount + (DENOMINATOR - ALPHA) * currentamount
    # price_v_ema:uint256 = newvolume / newamount
    self.rewardAmount += (newvolume / newamount) * _amountx * self.fee / DENOMINATOR / 10 ** ERC20(_tokenx).decimals()

@external
def set_fee(_fee: uint256):
    assert self.owner == msg.sender
    self.fee = _fee
