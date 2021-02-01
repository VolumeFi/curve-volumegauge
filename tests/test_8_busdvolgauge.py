#!/usr/bin/python3

import pytest

PERIOD = 30
DENOMINATOR = 10 ** 18
SMOOTHING = 2
ALPHA = DENOMINATOR - SMOOTHING * DENOMINATOR / (PERIOD + 1)

def test_exchange_ydai_to_yusdc(_busdvolgauge, busdpool, yDAI_BUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange(0, 1, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange(0, 1, 50 * 10 ** 18, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(yDAI_BUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(yDAI_BUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_yusdc_to_ydai(_busdvolgauge, busdpool, yUSDC_BUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange(1, 0, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange(1, 0, 50 * 10 ** 6, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(yUSDC_BUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(yUSDC_BUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_ydai_to_yusdt(_busdvolgauge, busdpool, yDAI_BUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange(0, 2, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange(0, 2, 50 * 10 ** 18, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(yDAI_BUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(yDAI_BUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_yusdt_to_ydai(_busdvolgauge, busdpool, yUSDT_BUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange(2, 0, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange(2, 0, 50 * 10 ** 6, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(yUSDT_BUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(yUSDT_BUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_ydai_to_ybusd(_busdvolgauge, busdpool, yDAI_BUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange(0, 3, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange(0, 3, 50 * 10 ** 18, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(yDAI_BUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(yDAI_BUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_ybusd_to_ydai(_busdvolgauge, busdpool, yBUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange(3, 0, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange(3, 0, 50 * 10 ** 18, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(yBUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(yBUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_yusdc_to_yusdt(_busdvolgauge, busdpool, yUSDC_BUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange(1, 2, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange(1, 2, 50 * 10 ** 6, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(yUSDC_BUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(yUSDC_BUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_yusdt_to_yusdc(_busdvolgauge, busdpool, yUSDT_BUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange(2, 1, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange(2, 1, 50 * 10 ** 6, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(yUSDT_BUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(yUSDT_BUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_yusdc_to_ybusd(_busdvolgauge, busdpool, yUSDC_BUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange(1, 3, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange(1, 3, 50 * 10 ** 6, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(yUSDC_BUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(yUSDC_BUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_ybusd_to_yusdc(_busdvolgauge, busdpool, yBUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange(3, 1, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange(3, 1, 50 * 10 ** 18, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(yBUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(yBUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_yusdt_to_ybusd(_busdvolgauge, busdpool, yUSDT_BUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange(2, 3, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange(2, 3, 50 * 10 ** 6, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(yUSDT_BUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(yUSDT_BUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_ybusd_to_yusdt(_busdvolgauge, busdpool, yBUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange(3, 2, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange(3, 2, 50 * 10 ** 18, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(yBUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(yBUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_underlying_dai_to_usdc(_busdvolgauge, busdpool, DAI, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange_underlying(0, 1, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange_underlying(0, 1, 50 * 10 ** 18, 0, {'from': accounts[0]})
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

def test_exchange_underlying_usdc_to_dai(_busdvolgauge, busdpool, USDC, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange_underlying(1, 0, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange_underlying(1, 0, 50 * 10 ** 6, 0, {'from': accounts[0]})
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

def test_exchange_underlying_dai_to_usdt(_busdvolgauge, busdpool, DAI, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange_underlying(0, 2, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange_underlying(0, 2, 50 * 10 ** 18, 0, {'from': accounts[0]})
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

def test_exchange_underlying_usdt_to_dai(_busdvolgauge, busdpool, USDT, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange_underlying(2, 0, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange_underlying(2, 0, 50 * 10 ** 6, 0, {'from': accounts[0]})
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

def test_exchange_underlying_dai_to_busd(_busdvolgauge, busdpool, DAI, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange_underlying(0, 3, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange_underlying(0, 3, 50 * 10 ** 18, 0, {'from': accounts[0]})
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

def test_exchange_underlying_busd_to_dai(_busdvolgauge, busdpool, BUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange_underlying(3, 0, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange_underlying(3, 0, 50 * 10 ** 18, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(BUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(BUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_underlying_usdc_to_usdt(_busdvolgauge, busdpool, USDC, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange_underlying(1, 2, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange_underlying(1, 2, 50 * 10 ** 6, 0, {'from': accounts[0]})
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

def test_exchange_underlying_usdt_to_usdc(_busdvolgauge, busdpool, USDT, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange_underlying(2, 1, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange_underlying(2, 1, 50 * 10 ** 6, 0, {'from': accounts[0]})
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

def test_exchange_underlying_usdc_to_busd(_busdvolgauge, busdpool, USDC, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange_underlying(1, 3, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange_underlying(1, 3, 50 * 10 ** 6, 0, {'from': accounts[0]})
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

def test_exchange_underlying_busd_to_usdc(_busdvolgauge, busdpool, BUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange_underlying(3, 1, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange_underlying(3, 1, 50 * 10 ** 18, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(BUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(BUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")

def test_exchange_underlying_usdt_to_busd(_busdvolgauge, busdpool, USDC, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange_underlying(1, 3, 50 * 10 ** 6, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange_underlying(1, 3, 50 * 10 ** 6, 0, {'from': accounts[0]})
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

def test_exchange_underlying_busd_to_usdt(_busdvolgauge, busdpool, BUSD, tracker, accounts):
    for i in range(5):
        print("Attemp #" + str(i + 1) + " .....")
        last_reward_amount = tracker.rewardAmount()
        tx = _busdvolgauge.exchange_underlying(3, 1, 50 * 10 ** 18, 0, {'from': accounts[0]})
        vgas = tx.gas_used
        print("VGaugeGas : " + str(vgas) + " Unit")
        tx = busdpool.exchange_underlying(3, 1, 50 * 10 ** 18, 0, {'from': accounts[0]})
        print("OriginGas : " + str(tx.gas_used) + " Unit")
        print("ConsumedGasByVolumeGauge : " + str(vgas - tx.gas_used) + " Unit")
        current_reward_amount = tracker.rewardAmount()
        lastvolumedata = tracker.lastVolumeData(BUSD)
        last_volume = lastvolumedata[0]
        last_amount = lastvolumedata[1]
        currentvolumedata = tracker.currentVolumeData(BUSD)
        current_volume = currentvolumedata[0]
        current_amount = currentvolumedata[1]
        newvolume = ALPHA * last_volume + (DENOMINATOR - ALPHA) * current_volume
        newamount = ALPHA * last_amount + (DENOMINATOR - ALPHA) * current_amount
        price_v_ema = newvolume / newamount
        print("price_by_volume_EMA* : " + str(price_v_ema / DENOMINATOR) + " CRV")
        print("reward_amount : " + str(current_reward_amount) + " (" + str(current_reward_amount / DENOMINATOR) + " CRV)")
        print("increased_reward_amount_in_CRV : " + str(float(current_reward_amount - last_reward_amount) / DENOMINATOR) + " CRV")
