# ТЕСТОВЫЙ СКРИПТ.
# 1. ПОЛУЧЕНИЕ Данных с биржи Бинанс
# - Через неофициальную библиотеку Pyton Binance и его клиента.
# 2. Расчет индикатора EMA200
# Отрисовка ДВУМЯ способами

from binance.client import Client
import pandas as pd
import pandas_ta as ta
import numpy as np
import talib, requests
from time import sleep
from binance.exceptions import BinanceAPIException
import keys
import matplotlib.pyplot as plt

# ОПРЕДЕЛЯЕМ ПЕРЕМЕННЫЕ
background_color = '#bebebe'
symbol = 'BTCUSDT'
interval = '1d'
limit = 400
ema_length = 200

# ПОДКЛЮЧЕНИЕ К БИНАНСУ
client = Client(api_key=keys.api_key, api_secret=keys.api_secret)

# Функция (С ЗАЩИТОЙ) получения массива информации для свечей с биржи Бинанс.
# Возвращает таблицу, которую уже можно анализировать
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
# Создаем новый столбец и добавлячем в него расчитываемые значения EMA200
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
print('np.Trend:\n', Trend)

# Вариант 2. Расчитиваем разницу между соседними значениями прямо в DataFrame
klines.loc[:,['EMA_DIFF']] = klines['EMA'].diff()
print('df.EMA_DIFF:\n', klines['EMA_DIFF'])

# Печать двух графиков с установкой разных сеток
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax.set_title('График 1: {}'.format('XXX/USDT+EMA'), fontsize=10)
ax.plot(klines['Close'], color='blue')
ax.plot(klines['EMA'], color='#c0c0c0')
ax.grid(True)


# Устанавливаем размер шрифта меток на осях
ax.tick_params(axis='y', labelsize=8)
ax.tick_params(axis='x', labelsize=8)
ax.set_yticks(np.arange(0, max(klines['Close']), 125))

# Формирование второго графика
ax2.plot(Trend, color='orange')
#ax2.plot(klines['EMA_DIFF'], color='orange')

ax2.set_title('График 2: {}'.format('BNB/USDT+Производная(Разница соседних значений EMA)'), fontsize=10)
# Устанавливаем размер шрифта меток на осях
ax2.tick_params(axis='y', labelsize=8)
ax2.tick_params(axis='x', labelsize=8)
ax2.grid(True)
plt.show()




#
# Вариант 2. Печать двух графиков с установкой разных сеток
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax.set_title('График 1: {}'.format('BNB/USDT+EMA'), fontsize=10)

ax.plot(klines['Close'], color='blue')
ax.plot(klines['EMA'], color='orange')

ax.grid(True)

# Устанавливаем размер шрифта меток на осях
ax.tick_params(axis='y', labelsize=8)
ax.tick_params(axis='x', labelsize=8)
ax.set_yticks(np.arange(0, max(klines['Close']), 25))

ax2.plot(klines['Close'], color='blue')
ax2.plot(klines['EMA'], color='orange')
ax2.set_title('График 2: {}'.format('BNB/USDT+EMA'), fontsize=10)
# Устанавливаем размер шрифта меток на осях
ax2.tick_params(axis='y', labelsize=8)
ax2.tick_params(axis='x', labelsize=8)
# ШАГ по Y
ax2.set_yticks(np.arange(0, max(klines['Close']), 50))
# Заливаем зеленым- если график НАД графиком EMA200 и КРАСНЫМ, если график НАД EMA200
ax2.fill_between(klines.index, klines['EMA'], klines['Close'], where=klines['Close'] >= klines['EMA'], color='g')
ax2.fill_between(klines.index, klines['EMA'], klines['Close'], where=klines['Close'] <= klines['EMA'], color='r')
#ax2.grid(True)
plt.show()