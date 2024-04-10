# ТЕСТОВЫЙ СКРИПТ.
# 1. ПОЛУЧЕНИЕ Данных с биржи Бинанс
# - Через неофициальную библиотеку Pyton Binance и его клиента.
# 2. Расчет индикаторов SMA и EMA
# 3. Отрисовка графиков с индикаторами
import numpy
from binance.client import Client
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
limit = 100
sma_length = 10
ema_length = 10
wma_length = 10
sma_color = 'yellow'
ema_color = 'red'
wma_color = 'green'

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
    df = df.set_index('Time')
    # Переводим столбец Time из Datatime в читаемый вид
    df.index = pd.to_datetime(df.index, unit='ms')
    # Изменяем тип данных на float, чтобы можно было вести рассчет алгоритмов
    df = df.astype(float)
    return df

# Получаем массив данных с бинанс
klines = fn_get_binance_klines(symbol = symbol, interval = interval, limit = limit)
# Вывод результатов запроса от Бинанс
print('Binance_klines: \n', klines)
# Создаем новые столбцы и добавлячем в него расчитываемые значения EMA
klines['SMA'] = ta.sma(klines['Close'], length = sma_length, offset=None)
klines['EMA'] = ta.ema(klines['Close'], length = ema_length, offset=None)
klines['WMA'] = ta.wma(klines['Close'], length = wma_length, offset=None)

# Удаляем все строки, где EMA200 == NaN (это первые 200 значений, на основании которых и расчитывается кривая)
drop_klines = klines.dropna()
# Меняемся значениями
drop_klines, klines = klines, drop_klines
# Печатаем весь DataFrame
print('EMA:\n', klines)

# ============ ГРАФИКА ==============
# Черная тема
plt.style.use('dark_background')

# Печать двух графиков с установкой разных сеток
fig = plt.figure(figsize = (18, 13))

#fig = plt.figure(dpi = 10)

ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

# ====== ФОРМИПУЕМ ПЕПРВЫЙ ГРАФИК
ax1.set_title('График 1: {title}'.format(title= symbol+ ' LINE style'), fontsize=10)
ax1.plot(klines['Close'], color = 'blue')
ax1.plot(klines['SMA'],linewidth= 1, color = sma_color, label= 'SMA '+ str(sma_length))
ax1.plot(klines['EMA'], linewidth= 1, color = ema_color, label= 'EMA '+ str(ema_length))
ax1.plot(klines['WMA'], linewidth= 1, color = wma_color, label= 'WMA '+ str(wma_length))

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

# =====  ФОРМИРОВАНИЕ ВТОРОГО ГРАФИКА
ax2.set_title('График 1: {title}'.format(title= symbol+ ' LOG style'), fontsize=10)
ax2.plot(klines['Close'], color = 'blue')
ax2.plot(klines['SMA'],linewidth= 1, color = sma_color, label= 'SMA '+ str(sma_length))
ax2.plot(klines['EMA'], linewidth= 1, color = ema_color, label= 'EMA '+ str(ema_length))
ax2.plot(klines['WMA'], linewidth= 1, color = wma_color, label= 'WMA '+ str(wma_length))

# Легенду выводим
ax2.legend()

# Устанавливаем размер шрифта меток на осях
ax2.tick_params(axis='y', labelsize=6)
ax2.tick_params(axis='x', labelsize=6)

# Установить цену деления по шкале Y = grid_price_step (USDT) :
#ax2.set_yticks(np.arange(0, max(klines['Close']), grid_price_step))

ax2.set_yscale('log')

# Сетку рисуем
ax2.grid(True,which="both",ls="--",c='gray')
#ax2.grid(True)

plt.show()


