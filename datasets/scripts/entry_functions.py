from datetime import datetime

def string_to_date(string):
    new_date = datetime.strptime(string, '%Y-%m-%d')
    
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