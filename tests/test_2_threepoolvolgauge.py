#!/usr/bin/python3

import pytest

PERIOD = 30
DENOMINATOR = 10 ** 18
SMOOTHING = 2
ALPHA = DENOMINATOR - SMOOTHING * DENOMINATOR / (PERIOD + 1)

def test_exchange_dai_to_usdc(_threepoolvolgauge, threepool, DAI, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _threepoolvolgauge.exchange(0, 1, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = threepool.exchange(0, 1, 50 * 10 ** 18, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(DAI)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(DAI)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_usdc_to_dai(_threepoolvolgauge, threepool, USDC, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _threepoolvolgauge.exchange(1, 0, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = threepool.exchange(1, 0, 50 * 10 ** 6, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(USDC)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(USDC)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_dai_to_usdt(_threepoolvolgauge, threepool, DAI, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _threepoolvolgauge.exchange(0, 2, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = threepool.exchange(0, 2, 50 * 10 ** 18, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(DAI)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(DAI)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_usdt_to_dai(_threepoolvolgauge, threepool, USDT, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _threepoolvolgauge.exchange(2, 0, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = threepool.exchange(2, 0, 50 * 10 ** 6, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(USDT)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(USDT)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_usdc_to_usdt(_threepoolvolgauge, threepool, USDC, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _threepoolvolgauge.exchange(1, 2, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = threepool.exchange(1, 2, 50 * 10 ** 6, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(USDC)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(USDC)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_usdt_to_usdc(_threepoolvolgauge, threepool, USDT, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _threepoolvolgauge.exchange(2, 1, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = threepool.exchange(2, 1, 50 * 10 ** 6, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(USDT)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(USDT)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")
