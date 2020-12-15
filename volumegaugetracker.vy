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
