import redis
import json

rds = redis.StrictRedis(host='127.0.0.1', port = 6379, db = 3)

with open('stocks.json', 'r') as file:
	stocks = json.load(file)

for i in stocks:
    rds.set(i, json.dumps(stocks[i]))