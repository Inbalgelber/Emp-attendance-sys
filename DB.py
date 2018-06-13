import csv
import datetime


class DB:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_from_file(self):
        data_from_reader = []
        with open (self.file_name, "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data_from_reader.append(row)
            return data_from_reader

    def add_to_file(self, data):
        with open(self.file_name, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def del_from_file(self, value_to_del):
        data = self.read_from_file()
        with open (self.file_name, "w", newline='') as f:
            writer = csv.writer(f)
            for row in data:
                if value_to_del not in row:
                    writer.writerow(row)

    def write_to_file(self, headers, data):
        with open(self.file_name, "w", newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(headers)
            for i in data:
                csv_writer.writerow(i)



