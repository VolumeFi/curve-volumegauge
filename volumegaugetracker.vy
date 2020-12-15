struct TrackData:
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
def track(source_:address, sender_:address, contract_:address):
    assert self.gauges[msg.sender] == True
    trackdatum:TrackData = TrackData({source_addr:source_, contract_addr:contract_, time_stamp:block.timestamp})
    self.trackData[sender_][self.trackDataSize[sender_]] = trackdatum
    self.trackDataSize[sender_] += 1