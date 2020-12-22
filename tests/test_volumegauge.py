#!/usr/bin/python3

import pytest


def test_exchange_cdai_to_cusdc(swap_volumegauge, accounts):
    swap_volumegauge.exchange(0, 1, 10000, 0, {'from': accounts[0]})
    pass

def test_exchange_cusdc_to_cdai(swap_volumegauge, accounts):
    swap_volumegauge.exchange(1, 0, 10000, 0, {'from': accounts[0]})
    pass

def test_exchange_underlying_dai_to_usdc(swap_volumegauge, accounts):
    swap_volumegauge.exchange_underlying(0, 1, 10000, 0, {'from': accounts[0]})
    pass

def test_exchange_underlying_usdc_to_dai(swap_volumegauge, accounts):
    swap_volumegauge.exchange_underlying(1, 0, 10000, 0, {'from': accounts[0]})
    pass