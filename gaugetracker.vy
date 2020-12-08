# Volume Gauge Tracker

gov: public(address)


@external
def __init__():
    self.gov = msg.sender

@external
def trackContract(addr:address, user:address)