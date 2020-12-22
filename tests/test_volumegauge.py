#!/usr/bin/python3

import pytest

def test_exchange_cdai_to_cusdc(volumegauge, tracker, accounts):
    volumegauge.exchange(0, 1, 10000, 0, {'from': accounts[0]})
    track_data_size = tracker.trackDataSize(accounts[0])
    track_data = tracker.trackData(accounts[0], track_data_size - 1)
    print("tokenx : " + str(track_data[0]))
    print("pricex : " + str(track_data[1]))
    print("amountx : " + str(track_data[2]))
    print("tokeny : " + str(track_data[3]))
    print("pricey : " + str(track_data[4]))
    print("amounty : " + str(track_data[5]))
    print("source_addr : " + str(track_data[6]))
    print("contract_addr : " + str(track_data[7]))
    print("time_stamp : " + str(track_data[8]))

def test_exchange_cusdc_to_cdai(volumegauge, tracker, accounts):
    volumegauge.exchange(1, 0, 10000, 0, {'from': accounts[0]})
    track_data_size = tracker.trackDataSize(accounts[0])
    track_data = tracker.trackData(accounts[0], track_data_size - 1)
    print("tokenx : " + str(track_data[0]))
    print("pricex : " + str(track_data[1]))
    print("amountx : " + str(track_data[2]))
    print("tokeny : " + str(track_data[3]))
    print("pricey : " + str(track_data[4]))
    print("amounty : " + str(track_data[5]))
    print("source_addr : " + str(track_data[6]))
    print("contract_addr : " + str(track_data[7]))
    print("time_stamp : " + str(track_data[8]))

def test_exchange_underlying_dai_to_usdc(volumegauge, tracker, accounts):
    volumegauge.exchange_underlying(0, 1, 10000, 0, {'from': accounts[0]})
    track_data_size = tracker.trackDataSize(accounts[0])
    track_data = tracker.trackData(accounts[0], track_data_size - 1)
    print("tokenx : " + str(track_data[0]))
    print("pricex : " + str(track_data[1]))
    print("amountx : " + str(track_data[2]))
    print("tokeny : " + str(track_data[3]))
    print("pricey : " + str(track_data[4]))
    print("amounty : " + str(track_data[5]))
    print("source_addr : " + str(track_data[6]))
    print("contract_addr : " + str(track_data[7]))
    print("time_stamp : " + str(track_data[8]))

def test_exchange_underlying_usdc_to_dai(volumegauge, tracker, accounts):
    volumegauge.exchange_underlying(1, 0, 10000, 0, {'from': accounts[0]})
    track_data_size = tracker.trackDataSize(accounts[0])
    track_data = tracker.trackData(accounts[0], track_data_size - 1)
    print("tokenx : " + str(track_data[0]))
    print("pricex : " + str(track_data[1]))
    print("amountx : " + str(track_data[2]))
    print("tokeny : " + str(track_data[3]))
    print("pricey : " + str(track_data[4]))
    print("amounty : " + str(track_data[5]))
    print("source_addr : " + str(track_data[6]))
    print("contract_addr : " + str(track_data[7]))
    print("time_stamp : " + str(track_data[8]))
