# Ethereum InterExchange Arbitrage Tracker

This is a simple python script aimed to identify ETH/USD and ETH/USDT arbitrage opportunities between five cryptocurrecy exchanges. The script monitors ETH spot prices between exchanges and alerts the user with a sound every time the price gap is more than 2.5%.

The script also collects price data. The collected data is saved in a .csv file on your computer for further analysis/charting. Example of a .csv files can be found in this directory. The data is collected/checked with 1 second resolution.

List of supported exchanges:
1. GDAX (now Coinbase Pro)
2. Gemini
3. Poloniex
4. Bittrex
5. Kraken

The arbitrage strategy involves buying ETH on one exchange, transferring the asset to another exchange and selling it at a premium. Experience shows that at the time of high market distress, prices may diverge significantly between exchanges. Some of this divergence can be explained by temporary blocks exchanges put in place on outgoing ETH transfers. 

This strategy is not risk-free. It takes 12-15 minutes to transfer ETH between exchanges. During this [transfer] time the arbitrage opportunity may dissappear.   

### Prerequisites

1. python3.6.8
2. python editor (e.g. sublime text 3)

### Installing

Copy and paste the raw data file from this file onto your editor.

## Running the tests

Don't forget to replace file path placeholders [on lines 163, 174] with specific paths in your machine/system.


### MIT License

Copyright (c) 2019 Umed Saidov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
