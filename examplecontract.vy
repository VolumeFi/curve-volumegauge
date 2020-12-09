NUM: constant(int128) = 2
addresses: public(address[2])
base: public(address)

@external
def __init__(base_: address):
    self.base = base_

# @external
# def changeAddresses(addresses_: address[NUM]):
#     self.addresses = addresses_

@external
def changeAddresses(addresses_: address[NUM]): # NUM in string is not work. This is an error.
   raw_call(self.base, concat(method_id("changeAddresses(address[NUM])"), convert(addresses_[0], bytes32), convert(addresses_[1], bytes32)), is_delegate_call=True)
