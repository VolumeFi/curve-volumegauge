
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

interface Curve:
    def add_liquidity(amounts: uint256[N_COINS], min_mint_amount: uint256): nonpayable
    def remove_liquidity(_amount: uint256, min_amounts: uint256[N_COINS]): nonpayable
    def remove_liquidity_imbalance(amounts: uint256[N_COINS], max_burn_amount: uint256): nonpayable
    def balances(i: int128) -> uint256: view
    def A() -> uint256: view
    def fee() -> uint256: view
    def owner() -> address: view

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

@external
def __init__(_coins: address[N_COINS], _underlying_coins: address[N_COINS],
             _curve: address, _token: address, _base: address):
    self.coins = _coins
    self.underlying_coins = _underlying_coins
    self.curve = _curve
    self.token = _token
    self.base = _base

@external
@nonreentrant('lock')
def add_liquidity(uamounts: uint256[N_COINS], min_mint_amount: uint256):
    # can't use array for concat function, so must input separately
    raw_call(self.base, concat(method_id("add_liquidity(uint256[2],uint256)"), convert(uamounts[0], bytes32), convert(uamounts[1], bytes32), convert(min_mint_amount, bytes32)), is_delegate_call=True)

@external
@nonreentrant('lock')
def remove_liquidity(_amount: uint256, min_uamounts: uint256[N_COINS]):
    raw_call(self.base, concat(method_id("remove_liquidity(uint256,uint256[2])"), convert(_amount, bytes32), convert(min_uamounts[0], bytes32), convert(min_uamounts[1], bytes32)), is_delegate_call=True)

@external
@nonreentrant('lock')
def remove_liquidity_imbalance(uamounts: uint256[N_COINS], max_burn_amount: uint256):
    raw_call(self.base, concat(method_id("remove_liquidity_imbalance(uint256[2],uint256)"), convert(uamounts[0], bytes32), convert(uamounts[1], bytes32), convert(max_burn_amount, bytes32)), is_delegate_call=True)

@external
@view
def calc_withdraw_one_coin(_token_amount: uint256, i: int128) -> uint256:
    return convert(raw_call(self.base, concat(method_id("calc_withdraw_one_coin(uint256,int128)"), convert(_token_amount, bytes32), convert(i, bytes32)), max_outsize=32, is_static_call=True), uint256)

@external
@nonreentrant('lock')
def remove_liquidity_one_coin(_token_amount: uint256, i: int128, min_uamount: uint256, donate_dust: bool = False):
    raw_call(self.base, concat(method_id("remove_liquidity_one_coin(uint256,int128,uint256,bool)"), convert(_token_amount, bytes32), convert(1, bytes32), convert(min_uamount, bytes32), convert(donate_dust, bytes32)), is_delegate_call=True)

@external
@nonreentrant('lock')
def withdraw_donated_dust():
    raw_call(self.base, method_id("withdraw_donated_dust()"), is_delegate_call=True)
