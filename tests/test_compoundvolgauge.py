#!/usr/bin/python3

import pytest

PERIOD = 30
DENOMINATOR = 10 ** 18
SMOOTHING = 2
ALPHA = DENOMINATOR - SMOOTHING * DENOMINATOR / (PERIOD + 1)

def test_exchange_cdai_to_cusdc(_compoundvolgauge, cDAI, tracker, accounts):
    for i in range(5):
        last_reward_amount = tracker.rewardAmount()
        _compoundvolgauge.exchange(0, 1, 20 * 10 ** 8, 0, {'from': accounts[0]})
        track_data_size = tracker.trackDataSize(accounts[0])
        track_data = tracker.trackData(accounts[0], track_data_size - 1)
        current_reward_amount = tracker.rewardAmount()
        last_volume = tracker.lastVolume(cDAI)
        last_amount = tracker.lastAmount(cDAI)
        current_volume = tracker.currentVolume(cDAI)
        current_amount = tracker.currentAmount(cDAI)
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("token_x : " + track_data[0])
        print("token_y : " + track_data[1])
        print("price : " + str(track_data[2]) + " (" + str(float(track_data[2]) / DENOMINATOR) + " CRV)")
        print("amount : " + str(track_data[3]) + " (" + str(float(track_data[3]) / 10 ** cDAI.decimals()) + " tokens)")
        print("source_addr : " + track_data[4])
        print("contract_addr : " + track_data[5])
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")
        print("time_stamp : " + str(track_data[6]))

def test_exchange_cusdc_to_cdai(_compoundvolgauge, cUSDC, tracker, accounts):
    for i in range(5):
        last_reward_amount = tracker.rewardAmount()
        _compoundvolgauge.exchange(1, 0, 20 * 10 ** 8, 0, {'from': accounts[0]})
        track_data_size = tracker.trackDataSize(accounts[0])
        track_data = tracker.trackData(accounts[0], track_data_size - 1)
        current_reward_amount = tracker.rewardAmount()
        last_volume = tracker.lastVolume(cUSDC)
        last_amount = tracker.lastAmount(cUSDC)
        current_volume = tracker.currentVolume(cUSDC)
        current_amount = tracker.currentAmount(cUSDC)
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("token_x : " + track_data[0])
        print("token_y : " + track_data[1])
        print("price : " + str(track_data[2]) + " (" + str(float(track_data[2]) / DENOMINATOR) + " CRV)")
        print("amount : " + str(track_data[3]) + " (" + str(float(track_data[3]) / 10 ** cUSDC.decimals()) + " tokens)")
        print("source_addr : " + track_data[4])
        print("contract_addr : " + track_data[5])
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")
        print("time_stamp : " + str(track_data[6]))
    
def test_exchange_underlying_dai_to_usdc(_compoundvolgauge, DAI, tracker, accounts):
    for i in range(5):
        last_reward_amount = tracker.rewardAmount()
        _compoundvolgauge.exchange_underlying(0, 1, 10 ** 18, 0, {'from': accounts[0]})
        track_data_size = tracker.trackDataSize(accounts[0])
        track_data = tracker.trackData(accounts[0], track_data_size - 1)
        current_reward_amount = tracker.rewardAmount()
        last_volume = tracker.lastVolume(DAI)
        last_amount = tracker.lastAmount(DAI)
        current_volume = tracker.currentVolume(DAI)
        current_amount = tracker.currentAmount(DAI)
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("token_x : " + track_data[0])
        print("token_y : " + track_data[1])
        print("price : " + str(track_data[2]) + " (" + str(float(track_data[2]) / DENOMINATOR) + " CRV)")
        print("amount : " + str(track_data[3]) + " (" + str(float(track_data[3]) / 10 ** DAI.decimals()) + " tokens)")
        print("source_addr : " + track_data[4])
        print("contract_addr : " + track_data[5])
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")
        print("time_stamp : " + str(track_data[6]))

def test_exchange_underlying_usdc_to_dai(_compoundvolgauge, USDC, tracker, accounts):
    for i in range(5):
        last_reward_amount = tracker.rewardAmount()
        _compoundvolgauge.exchange_underlying(1, 0, 10 ** 6, 0, {'from': accounts[0]})
        track_data_size = tracker.trackDataSize(accounts[0])
        track_data = tracker.trackData(accounts[0], track_data_size - 1)
        current_reward_amount = tracker.rewardAmount()
        last_volume = tracker.lastVolume(USDC)
        last_amount = tracker.lastAmount(USDC)
        current_volume = tracker.currentVolume(USDC)
        current_amount = tracker.currentAmount(USDC)
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("token_x : " + track_data[0])
        print("token_y : " + track_data[1])
        print("price : " + str(track_data[2]) + " (" + str(float(track_data[2]) / DENOMINATOR) + " CRV)")
        print("amount : " + str(track_data[3]) + " (" + str(float(track_data[3]) / 10 ** USDC.decimals()) + " tokens)")
        print("source_addr : " + track_data[4])
        print("contract_addr : " + track_data[5])
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")
        print("time_stamp : " + str(track_data[6]))
