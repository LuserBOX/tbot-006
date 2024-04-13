# Запрашивает с TradingView показатели от тех нидикторов с рекомендациями на продажу и покупку-
# ПОКАЗАТЕЛИ ЛЖИВЫЕ !!!!!!!
from tradingview_ta import TA_Handler, Interval, Exchange
from pprint import pprint

# Проверяем на покупку следующие токены. Формируем список элементов

token_b = ['BTCUSDT','LTCUSDT','XMRUSDT']
# Проверяем на продажу следующие токены

token_s = ['KASUSDT','BNBUSDT','ADAUSDT']

# Опрациваем в цикде инфу по всем элементам  списска токенов на покупку
print('===== КАНДИДАТЫ НА ПОКУПКУ ==== \n')
for i in token_b:
    print(i)
    handler = TA_Handler(
        symbol="LTCUSDT",
        screener="crypto",
        exchange="binance",
        interval=Interval.INTERVAL_1_DAY,
        # proxies={'http': 'http://example.com:8080'} # Uncomment to enable proxy (replace the URL).
    )
    print(handler.get_analysis().summary)

print('\n===== КАНДИДАТЫ НА ПРОДАЖУ ==== \n')

for i in token_s:
    print(i)
    handler = TA_Handler(
        symbol="LTCUSDT",
        screener="crypto",
        exchange="binance",
        interval=Interval.INTERVAL_1_DAY,
        # proxies={'http': 'http://example.com:8080'} # Uncomment to enable proxy (replace the URL).
    )
    print(handler.get_analysis().summary)



# Вывод на печать всех индикаторов с показателями.
#pprint(handler.get_analysis().indicators)