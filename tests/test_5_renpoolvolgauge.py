#!/usr/bin/python3

import pytest

PERIOD = 30
DENOMINATOR = 10 ** 18
SMOOTHING = 2
ALPHA = DENOMINATOR - SMOOTHING * DENOMINATOR / (PERIOD + 1)

def test_exchange_renbtc_to_wbtc(_renvolgauge, renpool, renBTC, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _renvolgauge.exchange(0, 1, 5 * 10 ** 5, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = renpool.exchange(0, 1, 5 * 10 ** 5, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(renBTC)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(renBTC)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_wbtc_to_renbtc(_renvolgauge, renpool, WBTC, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _renvolgauge.exchange(1, 0, 5 * 10 ** 5, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = renpool.exchange(1, 0, 5 * 10 ** 5, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(WBTC)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(WBTC)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")
