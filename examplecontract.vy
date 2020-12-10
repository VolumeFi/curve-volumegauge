# NUM: constant(int128) = 2
# addresses: public(address[2])
# worked: public(bool)
# base: public(address)
struct TrackData:
    val: uint256
    time_stamp: uint256

trackData: HashMap[address, TrackData[1000000000]]
trackDataSize: HashMap[address, uint256]
# @external
# def __init__(base_: address):
    # self.base = base_

# @internal
# def work(worked_:bool):
#     self.worked = worked_

# @external
# def changeAddresses(addresses_: address[NUM]):
#     self.addresses = addresses_

# @external
# def changeAddresses(addresses_: address[NUM]): # NUM in string is not work. This is an error.
#    raw_call(self.base, concat(method_id("changeAddresses(address[NUM])"), convert(addresses_[0], bytes32), convert(addresses_[1], bytes32)), is_delegate_call=True)

# @external
# def proofWork():
#     self.work(True)

# @external
# def proofWork():
    # raw_call(self.base, method_id("proofWork()"), is_delegate_call=True)

@external
def addval(val_:uint256):
    trackdatum:TrackData = TrackData({val:val_, time_stamp:block.timestamp})
    self.trackData[msg.sender][self.trackDataSize[msg.sender]] = trackdatum
    self.trackDataSize[msg.sender] += 1
