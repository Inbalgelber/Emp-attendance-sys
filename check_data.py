import re
import datetime

from datetime import date
from datetime import timedelta
import time
from DB import *

class Check_emp_data:

    def check_empty(variable):
        return False if variable == "" else True

    def check_ID(ID):
        if ID.isdigit() is True and len(ID) == 6:
            return True
        else:
            return False

    def check_id_in_list(ID):
        db = DB("emp_file.csv")
        emp_data = db.read_from_file()
        for i in emp_data:
            if ID in i:
                return True
        return False

    def check_name(name):
        if name.isalpha() and 2 <= len(name) <= 12:
            return True
        else:
            return False

    def check_year(year):
        for i in year:
            if i.isalpha():
                return False
            else:
                today = datetime.date.today()
                y_now = int(today.year)
                age_is_years = y_now - int(year)
                return True if 18 <= age_is_years <= 75 else False

    def check_month(month):
        for i in month:
            if i.isalpha():
                return False
            else:
                return True if 1 <= int(month) <= 12 else False

    def check_day(day):
        for i in day:
            if i.isalpha():
                return False
            else:
                return True if 1 <= int(day) <= 31 else False

    def check_number(number):
        return False if re.match(r'\d{6,12}', str(number)) is None else True



