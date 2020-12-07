# Volume Gauge

gov: public(address)

@internal
@pure
def approxSqrt(num:decimal) -> decimal:
    error:decimal = 0.0001
    guess:decimal = num
    diff:decimal = num
    j:int128 = 0
    for i in range(100):
        newGuess:decimal = guess - ((guess * guess - num) / (guess + guess))
        diff = newGuess - guess
        if diff < 0.0:
            diff = -diff
        guess = newGuess
        if diff <= error:
            j = i
            break
    return convert(j, decimal)

@external
def __init__():
    self.gov = msg.sender

# for test
@external
@view
def testSqrt(num:uint256) -> uint256:
    val:decimal = convert(num, decimal)
    val /= 10000000000.0
    result:decimal = self.approxSqrt(val)
    result *= 10000000000.0
    return convert(result, uint256)
