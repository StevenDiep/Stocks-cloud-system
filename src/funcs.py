import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

def string_to_date(string):
    new_date = datetime.datetime.strptime(string, '%Y-%m-%d')
    
    return new_date

def string_to_date_arr(date_arr):
    new_arr = [string_to_date(element) for element in date_arr]
    return new_arr

def date_to_string(date):
    new_string = str(date)[:10]
    
    return new_string

def dict_convert(old_d):
    keys_values = old_d.items()
    new_d = {date_to_string(key): round(value, 2) for key,value in keys_values}
    
    return new_d

#Given a date and a time period, returns a new date a period before the given date
#Periods are in 1d, 7d, 1m, 3m, 6m, 1y, 5y
#old_date is a datetime and period is a string
def get_past_date(old_date, period):
    accepted_periods = ['1d', '7d', '1m', '3m', '6m', '1y', '5y']
    
    if period not in accepted_periods:
        raise Exception("period needs to be in accepted period list: ['1d', '7d', '1m', '3m', '6m', '1y', '5y']")
        
    period_num = int(period[0])
    
    if 'd' in period:
        new_date = old_date - relativedelta(days=period_num)
    elif 'm' in period:
        new_date = old_date - relativedelta(months=period_num)
    elif 'y' in period:
        new_date = old_date - relativedelta(years=period_num) + \
            relativedelta(days = 1)
    
    return new_date

def get_new_arrays(dates, values, period):
    if period == '5y':
        return dates,values
    
    min_date = get_past_date(dates[-1], period)
    index = 0
    for date in dates:
        if date <= min_date:
            index += 1;
        else:
            break
    
    
    return list(dates)[index:], list(values)[index:]
    
    
#Returns the percent difference of a stock given the ticker dict and period str
def get_stock_diff(ticker, period):
    dates = list(ticker.keys())
    current_date = dates[-1]
    current_value = ticker[current_date]
    
    current_date = datetime.datetime.strptime(current_date, "%Y-%m-%d")
    past_date = date_to_string(get_past_date(current_date, period))
    past_value = ticker[past_date]
    
    diff = current_value/past_value
    
    if diff > 1:
        diff = diff - 1
        return "The stock has increased by " + format(diff, ".2%")
    else:
        diff = (1 - diff)
        return "The stock has decreased by " + format(diff, ".2%")
    
def convert_values_to_diff(values):
    first_value = list(values)[0]
    new_values = ((np.array(list(values))-first_value)/first_value) * 100
    return new_values
    

def validate(date_string):
    try:
        datetime.date.fromisoformat(date_string)
        return date_string
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")














