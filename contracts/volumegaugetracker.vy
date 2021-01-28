# @version ^0.2.0

# from vyper.interfaces import ERC20
interface ERC20:
    def decimals() -> uint256: view


struct LastVolumeData:
    volume: uint256
    amount: uint256
    date: uint256

struct CurrentVolumeData:
    volume: uint256
    amount: uint256


PERIOD: constant(uint256) = 30
DENOMINATOR: constant(uint256) = 10 ** 18
SMOOTHING: constant(uint256) = 2
ALPHA: constant(uint256) = DENOMINATOR - SMOOTHING * DENOMINATOR / (PERIOD + 1)
DAY: constant(uint256) = 60 # 60 for test - 1 minute # 86400 for real
FEE: constant(uint256) = 2 * 10 ** 14
ETH: constant(address) = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE


event ExchangeTrack:
    sender: indexed(address)
    sold_token: address
    bought_token: address
    price: uint256
    sold_amount: uint256
    bought_amount: uint256
    source_addr: indexed(address)
    contract_addr: indexed(address)


lastVolumeData: public(HashMap[address, LastVolumeData])
currentVolumeData: public(HashMap[address, CurrentVolumeData])

rewardAmount: public(uint256) # based on USD, decimals 8

gauges: public(HashMap[address, bool])
owner: public(address)


@external
def __init__():
    self.owner = msg.sender

@external
def addGauge(_gauge: address):
    assert self.owner == msg.sender
    self.gauges[_gauge] = True

@external
def track(_sender: address,
    _tokenx: address,
    _tokeny: address,
    _pricex: uint256,
    _amountx: uint256,
    _amounty: uint256,
    _source_addr: address,
    _contract_addr: address):
    assert self.gauges[msg.sender] == True

    date: uint256 = block.timestamp / DAY
    lastvolumedata: LastVolumeData = self.lastVolumeData[_tokenx]
    currentvolumedata: CurrentVolumeData = self.currentVolumeData[_tokenx]

    if lastvolumedata.date < date:
        lastvolumedata.volume = (ALPHA * lastvolumedata.volume + (DENOMINATOR - ALPHA) * currentvolumedata.volume) / DENOMINATOR
        lastvolumedata.amount = (ALPHA * lastvolumedata.amount + (DENOMINATOR - ALPHA) * currentvolumedata.amount) / DENOMINATOR
        lastvolumedata.date = date
        self.lastVolumeData[_tokenx] = lastvolumedata
        currentvolumedata.volume = 0
        currentvolumedata.amount = 0

    currentvolumedata.volume += _amountx * _pricex
    currentvolumedata.amount += _amountx
    self.currentVolumeData[_tokenx] = currentvolumedata

    newvolume_num: uint256 = ALPHA * lastvolumedata.volume + (DENOMINATOR - ALPHA) * currentvolumedata.volume # Numerator
    newamount_num: uint256 = ALPHA * lastvolumedata.amount + (DENOMINATOR - ALPHA) * currentvolumedata.amount # Numerator
    price_v_ema:uint256 = newvolume_num / newamount_num
    decimals: uint256 = 18
    if (_tokenx != ETH):
        decimals = ERC20(_tokenx).decimals()
    self.rewardAmount += price_v_ema * _amountx * FEE / DENOMINATOR / 10 ** decimals

    log ExchangeTrack(_sender, _tokenx, _tokeny, _pricex, _amountx, _amounty, _source_addr, _contract_addr)
