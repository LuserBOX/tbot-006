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

# ПЕЧАТЬ ГРАФИКА МЕТОДОМ mplfinance

# ФОРМИРОВАНИЕ СТИЛЯ.
#  ВАРИАНТ1
mc = mpf.make_marketcolors(up='blue',down='red',edge='inherit',wick='black',volume='in',ohlc='i')
s = mpf.make_mpf_style(marketcolors=mc)

# ВАРИАНТ 2- СУПЕР!!!!!
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

mpf.plot(klines, type='line', title=symbol ,  ylabel='Price', volume=True, style=s, mav=[720,200],tight_layout=True ,figratio=(200,100))
#                                                                                       EMA 50 200
mpf.plot(klines, type='candle', title=symbol ,  ylabel='Price', volume=True, style=binance_dark, mav=[720,200],tight_layout=True ,figratio=(200,100))

# Вывод результатов запроса от Бинанс
print('Binance_klines: \n', klines)







# Создаем новые столбцы и добавлячем в него расчитываемые значения EMA

klines['EMA'] = ta.ema(klines['Close'], length = ema_length, offset=None)


# Удаляем все строки, где EMA200 == NaN (это первые 200 значений, на основании которых и расчитывается кривая)
drop_klines = klines.dropna()
# Меняемся значениями
drop_klines, klines = klines, drop_klines
# Печатаем весь DataFrame
print('EMA:\n', klines)

# Вариант 1
# Расчитываем производную от EMA
Trend = np.diff(klines['EMA'])

T = numpy.gradient(klines['EMA'])
print('np.Trend:\n', Trend)
print('np.Trend_1 :\n', T)


# Вариант 2. Расчитиваем разницу между соседними значениями прямо в DataFrame
# ПРАВИЛЬНОЕ РЕШЕНИЕ, Так ак остаются валидными ДАТЫ!!!
klines.loc[:,['EMA_DIFF']] = klines['EMA'].diff()

# Определяем разницу между значениями в процентах
klines.loc[:,['EMA_PCT']] = klines['EMA'].pct_change ()



print('df.EMA_DIFF:\n', klines['EMA_DIFF'])


# Черная тема
plt.style.use('dark_background')

# Печать двух графиков с установкой разных сеток
fig = plt.figure(figsize = (18, 13))

#fig = plt.figure(dpi = 10)

ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)


# ====== ФОПМИПУЕМ ПЕПРВЫЙ ГРАФИК
ax1.set_title('График 1: {title}'.format(title= symbol+ ' LOG style'), fontsize=10)
ax1.plot(klines['Close'], color = price_color)
ax1.plot(klines['EMA'], linewidth= 1, color = ema_color, label= 'EMA '+ str(ema_length))


# Легенду выводим
ax1.legend()

# Устанавливаем размер шрифта меток на осях
ax1.tick_params(axis='y', labelsize=6)
ax1.tick_params(axis='x', labelsize=6)

# Установить цену деления по шкале Y = grid_price_step (USDT) :
ax1.set_yticks(np.arange(grid_y_start, max(klines['Close']), grid_price_step))

# Сетку рисуем
#ax1.grid(True)
ax1.grid(True,which="both",ls="--",c='gray')

# Шкала Y- логарифмическая
ax1.set_yscale('log')


# =====  ФОРМИРОВАНИЕ ВТОРОГО ГРАФИКА
ax2.plot(klines['EMA_DIFF'], color='orange')
ax2.plot(klines['EMA_PCT']*100, color='red')

#ax3.plot(T, color='blue')
#ax3.plot(Trend, color='orange')
#ax2.plot(klines['EMA_DIFF'], color='orange')

# Ели линия выше 0- тренд возрастающий.
ax2.set_title('График 2: Линия индекса тренда (производная) {title}'.format(title= symbol), fontsize=10)
# Устанавливаем размер шрифта меток на осях
ax2.tick_params(axis='y', labelsize=8)
ax2.tick_params(axis='x', labelsize=8)
ax2.grid(True)

# УСТАНАВЛИВАТЬ ПОСДЕДНИМ !!! По оси Y - логарифмическая шкала
#ax3.set_yscale('log')
ax2.set_yscale('symlog', linthresh=1)

# Сетку рисуем
#ax1.grid(True)
ax2.grid(True,which="both",ls="--",c='gray')

plt.show()


