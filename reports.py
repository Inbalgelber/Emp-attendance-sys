from datetime import datetime
from DB import *
import datetime
from datetime import date


class Reports:
    def __init__(self, source_data, report_file_name, headers):
        self.source_data = source_data
        self.headers = headers
        self.report_file_name = report_file_name

    def prepare_emp_report(self):
        db1 = DB(self.source_data)
        emp_data = db1.read_from_file()
        data_for_report = sorted(emp_data)
        for i in data_for_report:
            #i.insert(3,Reports.calculate_age(i[4], i[5], i[6]))
            # כרגע בגלל שהקובץ עם נתוני עובדים לא נכונים מחזיק הודעת שגיאה שהערכים של חודש ויום לא נכונים...
            del (i[6])
            del (i[5])
            del (i[4])
        db2 = DB(self.report_file_name)
        db2.write_to_file(self.headers, data_for_report)

    def calculate_age(self, year, month, day):
        birth_day = datetime.date(int(year), int(month), int(day))
        today = datetime.date.today()
        age = (today - birth_day).days / 365
        return "{:.2f}".format(age)

    def prepare_date_parameters(self, from_month, from_year, until_month, until_year):
        until_month_manipulation = 0
        until_year_manipulation = 0
        if 1 <= int(until_month) < 12:
            until_month_manipulation = int(until_month) + 1
            until_year_manipulation = int(until_year)
        if int(until_month) == 12:
            until_month_manipulation = 1
            until_year_manipulation = int(until_year) + 1

        start = datetime.datetime.strptime("%s-%s" %(from_month, from_year),"%m-%Y")
        end = datetime.datetime.strptime("%s-%s" %(until_month_manipulation,until_year_manipulation),"%m-%Y")
        parameters = {"Start": start, "End": end}
        return parameters

    def prepare_time_parameters(self, from_hour, from_min):
        time_parameter = datetime.datetime.strptime("%s:%s" % (from_hour, from_min), "%H:%M")
        return time_parameter

    def get_attendance_log_from_file(self):
        db2 = DB(self.source_data)
        attendance_log = db2.read_from_file()
        for record in attendance_log:
            if record != []:
                record[1] = datetime.datetime.strptime(record[1], "%Y-%m-%d %H:%M:%S.%f")
        return attendance_log

    def prepare_report_by_emp(self, attendance_log, date_parameters, ID):
        data_for_report = []
        counter = 0
        filter_ID = [item for item in attendance_log if item[0] == ID]

        filter_start = [item for item in filter_ID if item[1] >= date_parameters["Start"]]
        filter_end = [item for item in filter_start if item[1] < date_parameters["End"]]
        sorted_dates = sorted(filter_end, key=lambda x: x[1])

        while counter < (len(sorted_dates) - 1):
            date = sorted_dates[counter][1].date()
            start = self.get_strtime(sorted_dates[counter][1])
            if sorted_dates[counter][1].date() == sorted_dates[counter + 1][1].date() and\
                    sorted_dates[counter][2] == "Enter" and sorted_dates[counter + 1][2] == "Exit":
                end = self.get_strtime(sorted_dates[counter + 1][1])
                duration = str(sorted_dates[counter + 1][1] - sorted_dates[counter][1])[:-10]
                data_for_report.append([ID, date, start, end, duration])
                counter += 2
            elif sorted_dates[counter][2] == "Exit":
                end = self.get_strtime(sorted_dates[counter][1])
                data_for_report.append([ID, date, "", end, ""])
                counter += 1
            else:
                data_for_report.append([ID, date, start, "", ""])
                counter += 1

        db = DB(self.report_file_name)
        db.write_to_file(self.headers, data_for_report)

    def prepare_laters_report(self, attendance_log, date_parameters, time_parameter):
        data_for_report = []
        filter_enter = [item for item in attendance_log if item[2] == "Enter"]
        filter_enter_time = [item for item in filter_enter if item[1] >= time_parameter]
        filter_start = [item for item in filter_enter_time if item[1] >= date_parameters["Start"]]
        filter_end = [item for item in filter_start if item[1] < date_parameters["End"]]
        sorted_emp = sorted(filter_end, key=lambda x: x[0])

        for i in sorted_emp:
            date = (i[1]).date()
            time = (i[1]).time()
            time_to_report = "%s:%s" % (time.hour, time.minute)
            data_for_report.append([i[0], date, time_to_report])

        db = DB(self.report_file_name)
        db.write_to_file(self.headers, data_for_report)

    def get_strtime(self, data):
        t1 = data.time()
        return "%s:%s" %(t1.hour, t1.minute)



