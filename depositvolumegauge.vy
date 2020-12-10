
# A "zap" to deposit/withdraw Curve contract without too many transactions
# (c) Curve.Fi, 2020
from vyper.interfaces import ERC20

# External Contracts
interface cERC20:
    def totalSupply() -> uint256: view
    def allowance(_owner: address, _spender: address) -> uint256: view
    def transfer(_to: address, _value: uint256) -> bool: nonpayable
    def transferFrom(_from: address, _to: address, _value: uint256) -> bool: nonpayable
    def approve(_spender: address, _value: uint256) -> bool: nonpayable
    def burn(_value: uint256): nonpayable
    def burnFrom(_to: address, _value: uint256): nonpayable
    def name() -> String[64]: view
    def symbol() -> String[32]: view
    def decimals() -> uint256: view
    def balanceOf(arg0: address) -> uint256: view
    def mint(mintAmount: uint256) -> uint256: nonpayable
    def redeem(redeemTokens: uint256) -> uint256: nonpayable
    def redeemUnderlying(redeemAmount: uint256) -> uint256: nonpayable
    def exchangeRateStored() -> uint256: view
    def exchangeRateCurrent() -> uint256: nonpayable
    def supplyRatePerBlock() -> uint256: view
    def accrualBlockNumber() -> uint256: view

# Tether transfer-only ABI
interface USDT:
    def transfer(_to: address, _value: uint256): nonpayable
    def transferFrom(_from: address, _to: address, _value: uint256): nonpayable
    def approve(_spender: address, _value: uint256) -> bool: nonpayable

interface Curve:
    def add_liquidity(amounts: uint256[N_COINS], min_mint_amount: uint256): nonpayable
    def remove_liquidity(_amount: uint256, min_amounts: uint256[N_COINS]): nonpayable
    def remove_liquidity_imbalance(amounts: uint256[N_COINS], max_burn_amount: uint256): nonpayable
    def balances(i: int128) -> uint256: view
    def A() -> uint256: view
    def fee() -> uint256: view
    def owner() -> address: view

interface Deposit:
    def add_liquidity(uamounts: uint256[N_COINS], min_mint_amount: uint256): nonpayable
    def remove_liquidity(_amount: uint256, min_uamounts: uint256[N_COINS]): nonpayable
    def remove_liquidity_imbalance(uamounts: uint256[N_COINS], max_burn_amount: uint256): nonpayable

N_COINS: constant(int128) = 2
TETHERED: constant(bool[N_COINS]) = [False, False]
USE_LENDING: constant(bool[N_COINS]) = [True, True]
ZERO256: constant(uint256) = 0  # This hack is really bad XXX
ZEROS: constant(uint256[N_COINS]) = [ZERO256, ZERO256]  # <- change
LENDING_PRECISION: constant(uint256) = 10 ** 18
PRECISION: constant(uint256) = 10 ** 18
PRECISION_MUL: constant(uint256[N_COINS]) = [1, 1000000000000]
FEE_DENOMINATOR: constant(uint256) = 10 ** 10
FEE_IMPRECISION: constant(uint256) = 25 * 10 ** 8  # % of the fee

coins: public(address[N_COINS])
underlying_coins: public(address[N_COINS])
curve: public(address)
token: public(address)
base: public(address)

struct TrackData:
    source_addr: address
    contract_addr: address
    time_stamp: uint256

trackData: HashMap[address, TrackData[1000000000000]]
trackDataSize: HashMap[address, uint256]

@internal
def track(source_:address, sender_:address, contract_:address):
    trackdatum:TrackData = TrackData({source_addr:source_, contract_addr:contract_, time_stamp:block.timestamp})
    self.trackData[sender_][self.trackDataSize[sender_]] = trackdatum
    self.trackDataSize[sender_] += 1

@internal
def _send_all(_addr: address, min_uamounts: uint256[N_COINS], one: int128):
    use_lending: bool[N_COINS] = USE_LENDING
    tethered: bool[N_COINS] = TETHERED

    for i in range(N_COINS):
        if (one < 0) or (i == one):
            if use_lending[i]:
                _coin: address = self.coins[i]
                _balance: uint256 = cERC20(_coin).balanceOf(self)
                if _balance == 0:  # Do nothing if there are 0 coins
                    continue
                ok: uint256 = cERC20(_coin).redeem(_balance)
                if ok > 0:
                    raise "Could not redeem coin"

            _ucoin: address = self.underlying_coins[i]
            _uamount: uint256 = ERC20(_ucoin).balanceOf(self)
            assert _uamount >= min_uamounts[i], "Not enough coins withdrawn"

            # Send only if we have something to send
            if _uamount >= 0:
                if tethered[i]:
                    USDT(_ucoin).transfer(_addr, _uamount)
                else:
                    ERC20(_ucoin).transfer(_addr, _uamount)

@external
def __init__(_coins: address[N_COINS], _underlying_coins: address[N_COINS], _curve: address, _token: address, _base: address):
    self.coins = _coins
    self.underlying_coins = _underlying_coins
    self.curve = _curve
    self.token = _token
    self.base = _base

@external
@nonreentrant('lock')
def add_liquidity(uamounts: uint256[N_COINS], min_mint_amount: uint256):
    self.track(msg.sender, tx.origin, self)
    use_lending: bool[N_COINS] = USE_LENDING
    tethered: bool[N_COINS] = TETHERED
    amounts: uint256[N_COINS] = ZEROS

    for i in range(N_COINS):
        uamount: uint256 = uamounts[i]

        if uamount > 0:
            # Transfer the underlying coin from owner
            if tethered[i]:
                USDT(self.underlying_coins[i]).transferFrom(msg.sender, self, uamount)
                USDT(self.underlying_coins[i]).approve(self.base, uamount)
            else:
                ERC20(self.underlying_coins[i]).transferFrom(msg.sender, self, uamount)
                ERC20(self.underlying_coins[i]).approve(self.base, uamount)

    Deposit(self.base).add_liquidity(uamounts, min_mint_amount)

    tokens: uint256 = ERC20(self.token).balanceOf(self)
    ERC20(self.token).transfer(msg.sender, tokens)


@external
@nonreentrant('lock')
def remove_liquidity(_amount: uint256, min_uamounts: uint256[N_COINS]):
    self.track(msg.sender, tx.origin, self)
    zeros: uint256[N_COINS] = ZEROS

    ERC20(self.token).transferFrom(msg.sender, self, _amount)
    ERC20(self.token).approve(self.base, _amount)
    Deposit(self.base).remove_liquidity(_amount, zeros)

    self._send_all(msg.sender, min_uamounts, -1)

@external
@nonreentrant('lock')
def remove_liquidity_imbalance(uamounts: uint256[N_COINS], max_burn_amount: uint256):
    """
    Get max_burn_amount in, remove requested liquidity and transfer back what is left
    """
    self.track(msg.sender, tx.origin, self)

    _token: address = self.token

    # Transfrer max tokens in
    _tokens: uint256 = ERC20(_token).balanceOf(msg.sender)
    if _tokens > max_burn_amount:
        _tokens = max_burn_amount
    ERC20(_token).transferFrom(msg.sender, self, _tokens)
    ERC20(_token).approve(self.base, _tokens)

    Deposit(self.base).remove_liquidity_imbalance(uamounts, max_burn_amount)

    # Transfer unused tokens back
    _tokens = ERC20(_token).balanceOf(self)
    ERC20(_token).transfer(msg.sender, _tokens)

    # Unwrap and transfer all the coins we've got
    self._send_all(msg.sender, ZEROS, -1)

@external
@view
def calc_withdraw_one_coin(_token_amount: uint256, i: int128) -> uint256:
    return convert(raw_call(self.base, concat(method_id("calc_withdraw_one_coin(uint256,int128)"), convert(_token_amount, bytes32), convert(i, bytes32)), max_outsize=32, is_static_call=True), uint256)

@external
@nonreentrant('lock')
def remove_liquidity_one_coin(_token_amount: uint256, i: int128, min_uamount: uint256, donate_dust: bool = False):
    self.track(msg.sender, tx.origin, self)
    raw_call(self.base, concat(method_id("remove_liquidity_one_coin(uint256,int128,uint256,bool)"), convert(_token_amount, bytes32), convert(1, bytes32), convert(min_uamount, bytes32), convert(donate_dust, bytes32)), is_delegate_call=True)

@external
@nonreentrant('lock')
def withdraw_donated_dust():
    raw_call(self.base, method_id("withdraw_donated_dust()"), is_delegate_call=True)
