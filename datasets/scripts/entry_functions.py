from datetime import datetime

def string_to_date(string):
    new_date = datetime.strptime(string, '%Y-%m-%d')
    
    return new_date

def date_to_string(date):
    new_string = str(date)[:10]
    
    return new_string

def dict_convert(old_d):
    keys_values = old_d.items()
    new_d = {date_to_string(key): round(value, 2) for key,value in keys_values}
    
    return new_d