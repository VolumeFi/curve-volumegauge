# Volume Gauge

struct TrackingData:
    pool:address
    source:address
    timestmp:uint256


gov: public(address)


@internal
@pure
def approxSqrt(num: decimal) -> decimal:
    error: decimal = 0.0001
    guess: decimal = num
    diff: decimal = num
    j: int128 = 0
    for i in range(100):
        newGuess: decimal = guess - ((guess * guess - num) / (guess + guess))
        diff = newGuess - guess
        if diff < 0.0:
            diff = - diff
        guess = newGuess
        if diff <= error:
            break
    return guess

@internal
@pure
def approxLogarithm(num: decimal) -> decimal:
    if num == 1.0:
        return 0.0
    n: decimal = 1000.0
    val: decimal = num
    error: decimal = (val - 1.0) * 0.0001
    times: decimal = 1.0
    for i in range(100):
        if (val <= 2.0):
            break
        times += 1.0
        val /= 2.0
    underlying: decimal = - 1.0
    result: decimal = 0.0
    for i in range(100000):
        underlying *= - (val - 1.0)
        guess: decimal = underlying / convert(i, decimal)
        result += guess
        if (guess < error):
            break
    return result * times

@external
def __init__():
    self.gov = msg.sender

# for test
@external
@view
def testLog(num:uint256) -> uint256:
    val:decimal = convert(num, decimal)
    val /= 10000000000.0
    result:decimal = self.approxLogarithm(val)
    result *= 10000000000.0
    return convert(result, uint256)
