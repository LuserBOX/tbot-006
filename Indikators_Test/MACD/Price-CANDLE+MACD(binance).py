# ТЕСТОВЫЙ СКРИПТ.
# 1. ПОЛУЧЕНИЕ Данных с биржи Бинанс
# - Через неофициальную библиотеку Pyton Binance и его клиента.
# https://www.youtube.com/watch?v=hl6p89NqWAM
# 2. Расчет индикаторов SMA и EMA
# 3. Отрисовка графиков с индикаторами


import numpy
from binance.client import Client
import mplfinance as mpf
import pandas as pd
import pandas_ta as ta
import numpy as np
import talib, requests
from time import sleep
from binance.exceptions import BinanceAPIException
import keys
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FixedLocator

# ОПРЕДЕЛЯЕМ ПЕРЕМЕННЫЕ
background_color = '#bebebe'
symbol = 'LTCUSDT'
interval = '1d'
grid_y_start = 60
grid_price_step = 5
limit = 900

price_color = 'green'
ema_length = 10
ema_color = 'red'
# ==================== ФОРМИРОВАНИЕ СТИЛЯ ВЫВОДА ГРАФИКА ==============
# ВАРИАНТ- СУПЕР!!!!!
binance_dark = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "#3dc985", "down": "#ef4f60"},
        "edge": {"up": "#3dc985", "down": "#ef4f60"},
        "wick": {"up": "#3dc985", "down": "#ef4f60"},
        "ohlc": {"up": "green", "down": "red"},
        "volume": {"up": "#247252", "down": "#82333f"},
        "vcedge": {"up": "green", "down": "red"},
        "vcdopcod": False,
        "alpha": 1,
    },
    "mavcolors": ("#ad7739", "#a63ab2", "#62b8ba"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": True,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#474d56",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "binance-dark",
}
#
# ФОРМИРОВАНИЕ ОБЫЧНОГО СТИЛЯ.
#  ВАРИАНТ1
mc = mpf.make_marketcolors(up='blue',down='red',edge='inherit',wick='black',volume='in',ohlc='i')
s = mpf.make_mpf_style(marketcolors=mc)
# ==================================================================
# ПОДКЛЮЧЕНИЕ К БИНАНСУ
client = Client(api_key=keys.api_key, api_secret=keys.api_secret)

# Функция (С ЗАЩИТОЙ) получения массива информации для свечей с биржи Бинанс.
# Возвращает таблицу (Dataframe), которую уже можно анализировать
def fn_get_binance_klines(symbol, interval, limit):
    try:
        df = pd.DataFrame(client.get_historical_klines(symbol = symbol, interval = interval, limit = limit))
    except BinanceAPIException as e:
        print(e)
        sleep(60)
        df = pd.DataFrame(client.get_historical_klines(symbol = symbol, interval = interval, limit = limit))

    # Оставляем первые 6 столбцов
    df = df.iloc[:, :6]

    # Переименуем столбцы по значению в них
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']

    # В таблице нам не нужен первый столбец- нумерация. Убираем его. Индескируем по столбцу Time
    df = df.set_index('Time').shift(-1)[:-1]

    # Переводим столбец Time из Datatime в читаемый вид
    df.index = pd.to_datetime(df.index, unit='ms')

    # Изменяем тип данных на float, чтобы можно было вести рассчет алгоритмов
    df = df.astype(float)

    return df

# Получаем массив данных с бинанс
klines = fn_get_binance_klines(symbol = symbol, interval = interval, limit = limit)

# Вывод результатов запроса от Бинанс
print('Binance_klines: \n', klines)

# РАСЧЕТ MACD
#klines["macd"], klines["macd_signal"], klines["macd_hist"] = ta.macd(klines['Close'])
macd = klines.ta.macd(close='Close', fast=12, slow=26, signal=9, append=True)

print(macd)

# ПЕЧАТЬ ГРАФИКА МЕТОДОМ mplfinance

# Вариант простого оформления
mpf.plot(klines, type='line', title=symbol ,  ylabel='Price', volume=True, style=s, mav=[720,200],tight_layout=True ,figratio=(200,100))
# Вариант стиля под Binance                                                                       EMA 720 200
mpf.plot(klines, type='candle', title=symbol ,  ylabel='Price', volume=True, style=binance_dark, mav=[720,200],tight_layout=True ,figratio=(200,100))

# Формирование графика с MACD
# macd panel
#colors = ['g' if v >= 0 else 'r' for v in klines["macd_hist"]]
macd_plot = mpf.make_addplot(macd["MACD_12_26_9"], panel=1, color='fuchsia', title="MACD")
macd_hist_plot = mpf.make_addplot(macd["MACDh_12_26_9"], type='bar', panel=1, color='g') # color='dimgray'
macd_signal_plot = mpf.make_addplot(macd["MACDs_12_26_9"], panel=1, color='b')

macd_plot = mpf.make_addplot(macd["MACD_12_26_9"], panel=1, color='fuchsia', title="MACD")
macd_hist_plot = mpf.make_addplot(macd["MACDh_12_26_9"], type='bar', panel=1, color='g')
macd_signal_plot = mpf.make_addplot(macd["MACDs_12_26_9"], panel=1, color='b')

plots = [macd_plot, macd_signal_plot, macd_hist_plot]


mpf.plot(klines, type='candle', style=binance_dark, addplot=plots)
# ==================================================================
# Печать двух графиков с установкой разных сеток
fig = plt.figure(figsize = (12, 6))

ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

ax.set_title('График 1: {}'.format('XXX/USDT+EMA'), fontsize=10)
ax.plot(klines['Close'], color = 'blue')

ax.grid(True)
# Enabling both grids:

# Устанавливаем размер шрифта меток на осях
ax.tick_params(axis='y', labelsize=6)
ax.tick_params(axis='x', labelsize=6)

ax.set_yticks(np.arange(0, max(klines['Close']), 25))

# Формирование второго графика

#ax2.plot(klines['EMA_DIFF'], color='orange')
ax2.plot(klines['MACD_12_26_9'], color='r', label='MACD')
ax2.plot(klines['MACDh_12_26_9'], color='g', label='MACDh')
ax2.plot(klines['MACDs_12_26_9'], color='w', label='MACDs')
ax2.set_title('График 2: {}'.format('BNB/USDT+Производная(Разница соседних значений EMA)'), fontsize=10)
# Устанавливаем размер шрифта меток на осях
ax2.tick_params(axis='y', labelsize=8)
ax2.tick_params(axis='x', labelsize=8)
ax2.grid(True)


plt.show()
