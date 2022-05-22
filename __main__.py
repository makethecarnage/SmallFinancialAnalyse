import tinkoff.invest as tinvest
from pandas import DataFrame
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

token = 't.og8jYwK7ryJy3Ns1EGYcPvOBOFpONQbnNdlOL75ZgJMtXwFWqZXAqD5YEuXJPLKMgF6wAG8ycLhBlClXZg-Ncg'

def get_ticker():
    ticker = input()
    return ticker

def get_info(ticker):
    try:
        stocks = DataFrame(
            client.instruments.shares(instrument_status=tinvest.InstrumentStatus.INSTRUMENT_STATUS_ALL).instruments,
            columns=['name', 'figi', 'ticker']
        )
        comp_info = stocks[stocks['ticker'] == ticker]
        return comp_info
    except (TypeError, IndexError):
        print('Тикера не существует, или он был введен неправильно.')

def get_candle(figi):
    candles = client.market_data.get_candles(
        figi=figi,
        from_=datetime.utcnow()-timedelta(days=6),
        to=datetime.utcnow(),
        interval=tinvest.CandleInterval.CANDLE_INTERVAL_HOUR
    )

    df = DataFrame([{
        'time': c.time,
        'volume': c.volume,
        'open': money(c.open),
        'close': money(c.close),
        'high': money(c.high),
        'low': money(c.low),
    } for c in candles.candles])
    return df

def money(value):
    return value.units + value.nano / 1e9

def graph(df, name):
    plt.title='График компании ' + name
    df.plot(x='time', y='close')
    plt.show()


if __name__ == "__main__":
    with tinvest.Client(token) as client:
        ticker = get_ticker()
        comp_info = get_info(ticker)
        df = get_candle(comp_info['figi'].iloc[0])
        graph(df, comp_info['name'].iloc[0])
