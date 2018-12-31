import requests
import time
from datetime import datetime
import pandas as pd
import winsound

trading_costs = .0025  # GEM/GDAX trading costs
ETH_m_fees_USD = 0.5  # $ Ethereum transmission costs
wire_fee_USD = 35  # Wire fees
errors = []

# Public exchange API urls:
gem_url = 'https://api.gemini.com/v1/pubticker/ethusd'
gdax_url = 'https://api.gdax.com/products/ETH-USD/ticker'
krk_url_usdt = 'https://api.kraken.com/0/public/Ticker?pair=USDTZUSD'
krk_url = 'https://api.kraken.com/0/public/Ticker?pair=ETHUSD'
pol_url = 'https://poloniex.com/public?command=returnTicker'
btx_url = 'https://bittrex.com/api/v1.1/public/getticker?market=USDT-ETH'

ex_df = pd.DataFrame()


# the main loop
while True:
    time.sleep(1)  # a delay to prevent exchange from blocking requests
    t_date = datetime.now()

    # Gemini Data:
    try:
        r = requests.get(gem_url)
        json_gem = r.json()
        price_gem = float(json_gem['last'])
        vol_gem = float(json_gem['volume']['USD'])
    except ValueError:
        print('ValueError Gemini Exchange')
        errors.append('ValueError Gemini Exchange')
        pass
    except KeyError:
        print('KeyError Gemini Exchange')
        errors.append('KeyError Gemini Exchange')
        pass

    # Gdax Data:
    try:
        g = requests.get(gdax_url)  # USD/ETH price data
        json_gdax = g.json()
        price_gdax = float(json_gdax['price'])
        vol_gdax = float(json_gdax['volume'])
    except ValueError:
        print('ValueError Gdax Exchange')
        errors.append('ValueError Gdax Exchange')
        pass
    except KeyError:
        print('KeyError Gdax Exchange')
        errors.append('KeyError Gdax Exchange')
        pass

    # Kraken Data:
    try:
        krk = requests.get(krk_url_usdt)  # USDT/USD price data
        json_krk = krk.json()
        price_krk_usdt = float(json_krk['result']['USDTZUSD']['c'][0])
    except ValueError:
        print('ValueError Kraken Exchange -USDT')
        errors.append('ValueError Kraken Exchange -USDT')
        pass
    except KeyError:
        print('KeyError Kraken Exchange -USDT')
        errors.append('KeyError Kraken Exchange -USDT')
        pass

    try:
        krk1 = requests.get(krk_url)  # USD/ETH price data
        json_krk1 = krk1.json()
        price_krk = float(json_krk1['result']['XETHZUSD']['c'][0])
    except ValueError:
        print('ValueError Kraken Exchange -ETH')
        errors.append('ValueError Kraken Exchange -ETH')
        pass
    except KeyError:
        print('KeyError Kraken Exchange -ETH')
        errors.append('KeyError Kraken Exchange -ETH')
        pass

    # Poloniex Data:
    try:
        px = requests.get(pol_url)
        json_px = px.json()
        price_px = float(json_px['USDT_ETH']['last']) * price_krk_usdt  # USDT/ETH price data
        vol_px = float(json_px['USDT_ETH']['baseVolume'])

    except ValueError:
        print('ValueError Poloniex Exchange')
        errors.append('ValueError Poloniex Exchange')
        pass
    except KeyError:
        print('KeyError Poloniex Exchange')
        errors.append('KeyError Poloniex Exchange')
        pass

    # Bittrex Data:
    try:
        btx = requests.get(btx_url)  # USD/ETH price data
        json_btx = btx.json()
        price_btx = float(json_btx['result']['Last']) * price_krk_usdt
        # vol_btx = float(json_px['USDT_ETH']['baseVolume'])
    except ValueError:
        print('ValueError Bittrex Exchange')
        errors.append('ValueError Bittrex Exchange')
        pass
    except KeyError:
        print('KeyError Bittrex Exchange')
        errors.append('KeyError Bittrex Exchange')
        pass

    # ETH arbitrage GDAX-GEM:
    inv = 10000 #hypothetical investment
    qty = (inv * (1 - (trading_costs))) / price_gem
    tx_costs_USD = (inv + (price_gdax * qty)) * trading_costs
    pct_tr_costs = (tx_costs_USD + wire_fee_USD) / inv * 100

    delta_inv = (price_gdax - price_gem) * qty

    delta_T_USD = delta_inv - tx_costs_USD - wire_fee_USD
    delta_T_pc = ((price_gdax / price_gem - 1) * 100) - pct_tr_costs

    # Aggregated ETH Price Data with min and max
    ETH_prices = {'Gdax': price_gdax, 'Poloniex': price_px, 'Bittrex': price_btx, 'Gemini': price_gem, 'Kraken': price_krk}

    # Dictionary of min/max prices
    ETH_max_exchange = {max(ETH_prices, key=ETH_prices.get): max(ETH_prices.values())}
    ETH_min_exchange = {min(ETH_prices, key=ETH_prices.get): min(ETH_prices.values())}

    # Get min/max values from dictionary, save as a list, convert to float.
    ETH_maxp = float(str([ETH_max_exchange.values()]).strip('[dict_values([ ])]'))
    ETH_minp = float(str([ETH_min_exchange.values()]).strip('[dict_values([ ])]'))

    raw_delta = ETH_maxp - ETH_minp
    raw_delta_pc = (raw_delta / ETH_minp) * 100

    # Screen Output:
    print("1.__________________________________")  # Print a line to prettify output
    for k, v in ETH_prices.items():
        print(k + ': ', '{:,.2f}'.format(v))

    print("2.__________________________________")  # Print a line to prettify output
    for k, v in ETH_min_exchange.items():  # Print our the exchange info with min price
        print('Min ' + k + ': ' + '{:,.2f}'.format(v))

    for k, v in ETH_max_exchange.items():  # Print our the exchange info with max price
        print('Max ' + k + ': ' + '{:,.2f}'.format(v))

    print("3.__________________________________")  # Print a line to prettify output
    print('Max-Min$: ' + '{:,.2f}'.format(raw_delta))
    print('Max-Min%: ' + '{:,.2f}'.format(raw_delta_pc) + '%' + '\n')

    print("4.__________________________________")  # Print a line to prettify output
    print('10K Delta$: ' + '$' + '{:,.2f}'.format(delta_T_USD))
    print('10K Delta%: ' + '{:,.2f}'.format(delta_T_pc) + '%' + '\n')

    # Sound Alert if price deviates by more than 2.5%
    if delta_T_pc > 2.5 or delta_T_pc < -2.5:
        fname = "soundfilepath"
        winsound.PlaySound(fname, winsound.SND_FILENAME)
        print('Buy at Gemini:' + '$' + '{:,.2f}'.format(price_gem))
        print('Sell at Gdax:' + '$' + '{:,.2f}'.format(price_gdax) + '\n')
        
    # Exchange Data Aggregation:
    s_data = {'Date': t_date, '10K_GDAX_GEM_delta%': delta_T_pc, '10K_GDAX_GEM_delta$': delta_T_USD, 'Min_max_delta$': raw_delta, 'Min_max_delta%': raw_delta_pc, 'wire_fee_USD': wire_fee_USD, 'total trading_costs%': trading_costs * 2, 'MaxExchange': ETH_maxp, 'MinExchange': ETH_minp, 'Errors': errors[:]}

    data_pool = {**ETH_prices, **s_data}  # pool the data into one dictionary

    ex_df = ex_df.append(data_pool, ignore_index=True)  # append data to pandas dataframe
    filepath = 'pricefilepath'

    # Save the pool output to csv file:
    filename = filepath + 'ETH_Prices_' + time.strftime("%Y-%m-%d-%H") + '.csv'
    ex_df.to_csv(filename)
    errors.clear()
