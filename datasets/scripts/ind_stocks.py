import yfinance as yf

aapl = yf.Ticker("^GSPC")

hist = aapl.history(period="5y")
data = hist["Close"]

AAPL = data.to_dict()

print(AAPL)
