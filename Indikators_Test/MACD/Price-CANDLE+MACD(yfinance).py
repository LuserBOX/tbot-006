import yfinance as yf
import mplfinance as mpf
import talib as ta

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

ticker_name = 'KAS-USD'
yticker = yf.Ticker("KAS-USD")
data = yticker.history(period="1y") # max, 1y, 3mo
# trim volume to avoid exponential form
data['Volume'] = data['Volume'] / 1000
# macd
data["macd"], data["macd_signal"], data["macd_hist"] = ta.MACD(data['Close'])
# macd panel
colors = ['g' if v >= 0 else 'r' for v in data["macd_hist"]]
macd_plot = mpf.make_addplot(data["macd"], panel=1, color='fuchsia', title="MACD")
macd_hist_plot = mpf.make_addplot(data["macd_hist"], type='bar', panel=1, color=colors) # color='dimgray'
macd_signal_plot = mpf.make_addplot(data["macd_signal"], panel=1, color='b')
# plot
plots = [macd_plot, macd_signal_plot, macd_hist_plot]
mpf.plot(data, type='candle', style=binance_dark, mav=(50,100,200), addplot=plots, title=f"\n{ticker_name}", yscale='log', volume=True, volume_panel=2, ylabel='', ylabel_lower='')
mpf.plot(data, type='candle', style='yahoo', mav=(50,100,200), addplot=plots, title=f"\n{ticker_name}", yscale='log', volume=True, volume_panel=2, ylabel='', ylabel_lower='')
