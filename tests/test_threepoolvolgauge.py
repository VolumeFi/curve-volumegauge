#!/usr/bin/python3

import pytest

PERIOD = 30
DENOMINATOR = 10 ** 18
SMOOTHING = 2
ALPHA = DENOMINATOR - SMOOTHING * DENOMINATOR / (PERIOD + 1)

def test_exchange_dai_to_usdc(_threepoolvolgauge, threepool, DAI, tracker, accounts):
    last_reward_amount = tracker.rewardAmount()
    tx = _threepoolvolgauge.exchange(0, 1, 10 ** 18, 0, {'from': accounts[0]})
    vgas = tx.gas_used
    print("VGaugeGas : " + str(vgas) + " Unit")
    tx = threepool.exchange(0, 1, 10 ** 18, 0, {'from': accounts[0]})
    print("OriginGas : " + str(tx.gas_used) + " Unit")
    print("IncreasedGas : " + str(vgas - tx.gas_used) + " Unit")
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

def test_exchange_usdc_to_dai(_threepoolvolgauge, threepool, USDC, tracker, accounts):
    last_reward_amount = tracker.rewardAmount()
    tx = _threepoolvolgauge.exchange(1, 0, 10 ** 6, 0, {'from': accounts[0]})
    vgas = tx.gas_used
    print("VGaugeGas : " + str(vgas) + " Unit")
    tx = threepool.exchange(1, 0, 10 ** 6, 0, {'from': accounts[0]})
    print("OriginGas : " + str(tx.gas_used) + " Unit")
    print("IncreasedGas : " + str(vgas - tx.gas_used) + " Unit")
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

def test_exchange_dai_to_usdt(_threepoolvolgauge, threepool, DAI, tracker, accounts):
    last_reward_amount = tracker.rewardAmount()
    tx = _threepoolvolgauge.exchange(0, 2, 10 ** 18, 0, {'from': accounts[0]})
    vgas = tx.gas_used
    print("VGaugeGas : " + str(vgas) + " Unit")
    tx = threepool.exchange(0, 2, 10 ** 18, 0, {'from': accounts[0]})
    print("OriginGas : " + str(tx.gas_used) + " Unit")
    print("IncreasedGas : " + str(vgas - tx.gas_used) + " Unit")
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

def test_exchange_usdt_to_dai(_threepoolvolgauge, threepool, USDT, tracker, accounts):
    last_reward_amount = tracker.rewardAmount()
    tx = _threepoolvolgauge.exchange(2, 0, 10 ** 6, 0, {'from': accounts[0]})
    vgas = tx.gas_used
    print("VGaugeGas : " + str(vgas) + " Unit")
    tx = threepool.exchange(2, 0, 10 ** 6, 0, {'from': accounts[0]})
    print("OriginGas : " + str(tx.gas_used) + " Unit")
    print("IncreasedGas : " + str(vgas - tx.gas_used) + " Unit")
    track_data_size = tracker.trackDataSize(accounts[0])
    track_data = tracker.trackData(accounts[0], track_data_size - 1)
    current_reward_amount = tracker.rewardAmount()
    last_volume = tracker.lastVolume(USDT)
    last_amount = tracker.lastAmount(USDT)
    current_volume = tracker.currentVolume(USDT)
    current_amount = tracker.currentAmount(USDT)
    newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
    newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
    price_v_ema = newvolume / newamount
    print("token_x : " + track_data[0])
    print("token_y : " + track_data[1])
    print("price : " + str(track_data[2]) + " (" + str(float(track_data[2]) / DENOMINATOR) + " CRV)")
    print("amount : " + str(track_data[3]) + " (" + str(float(track_data[3]) / 10 ** USDT.decimals()) + " tokens)")
    print("source_addr : " + track_data[4])
    print("contract_addr : " + track_data[5])
    print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
    print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
    print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")
    print("time_stamp : " + str(track_data[6]))

def test_exchange_usdc_to_usdt(_threepoolvolgauge, threepool, USDC, tracker, accounts):
    last_reward_amount = tracker.rewardAmount()
    tx = _threepoolvolgauge.exchange(1, 2, 10 ** 6, 0, {'from': accounts[0]})
    vgas = tx.gas_used
    print("VGaugeGas : " + str(vgas) + " Unit")
    tx = threepool.exchange(1, 2, 10 ** 6, 0, {'from': accounts[0]})
    print("OriginGas : " + str(tx.gas_used) + " Unit")
    print("IncreasedGas : " + str(vgas - tx.gas_used) + " Unit")
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

def test_exchange_usdt_to_usdc(_threepoolvolgauge, threepool, USDT, tracker, accounts):
    last_reward_amount = tracker.rewardAmount()
    tx = _threepoolvolgauge.exchange(2, 1, 10 ** 6, 0, {'from': accounts[0]})
    vgas = tx.gas_used
    print("VGaugeGas : " + str(vgas) + " Unit")
    tx = threepool.exchange(2, 1, 10 ** 6, 0, {'from': accounts[0]})
    print("OriginGas : " + str(tx.gas_used) + " Unit")
    print("IncreasedGas : " + str(vgas - tx.gas_used) + " Unit")
    track_data_size = tracker.trackDataSize(accounts[0])
    track_data = tracker.trackData(accounts[0], track_data_size - 1)
    current_reward_amount = tracker.rewardAmount()
    last_volume = tracker.lastVolume(USDT)
    last_amount = tracker.lastAmount(USDT)
    current_volume = tracker.currentVolume(USDT)
    current_amount = tracker.currentAmount(USDT)
    newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
    newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
    price_v_ema = newvolume / newamount
    print("token_x : " + track_data[0])
    print("token_y : " + track_data[1])
    print("price : " + str(track_data[2]) + " (" + str(float(track_data[2]) / DENOMINATOR) + " CRV)")
    print("amount : " + str(track_data[3]) + " (" + str(float(track_data[3]) / 10 ** USDT.decimals()) + " tokens)")
    print("source_addr : " + track_data[4])
    print("contract_addr : " + track_data[5])
    print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
    print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
    print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")
    print("time_stamp : " + str(track_data[6]))