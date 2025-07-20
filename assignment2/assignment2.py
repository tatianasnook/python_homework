import traceback
import csv
import os
import custom_module
from datetime import datetime

# Task 2.
def read_employees():
    employees_dict = {}
    rows_list = []

    try:
        with open("../csv/employees.csv", "r") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    employees_dict["fields"] = row
                else:
                    rows_list.append(row)
            employees_dict["rows"] = rows_list
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(
                f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print("An exception occurred.")
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")

    return employees_dict

employees = read_employees()


# Task 3.
def column_index(column_name):
    return employees["fields"].index(column_name)

employee_id_column = column_index("employee_id")


# Task 4.
def first_name(row_number):
    column_index_for_row = column_index("first_name")
    return employees["rows"][row_number][column_index_for_row]


# Task 5.
def employee_find(employee_id):

    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    
    matches = list(filter(employee_match, employees["rows"]))
    return matches


# Task 6.
def employee_find_2(employee_id):
    matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id, employees["rows"]))
    return matches


# Task 7.
def sort_by_last_name():
    last_name_index = column_index("last_name")
    employees["rows"].sort(key=lambda row : row[last_name_index])
    return employees["rows"]

print(sort_by_last_name())


#Task 8.
def employee_dict(row):
    current_employee_dict = {}

    for i in range(1, len(row)):
        current_employee_dict[employees["fields"][i]] = row[i]

    return current_employee_dict

print(employee_dict(['3', 'Lauren', 'Martinez', '+250 8878764159']))


#Task 9.
def all_employees_dict():
    company_employees_dict = {}
    rows_list = employees["rows"]

    for i, value in enumerate(rows_list):
        company_employees_dict[rows_list[i][0]] = employee_dict(value)

    return company_employees_dict

print(all_employees_dict())


#Task 10.
def get_this_value():
    return os.environ.get("THISVALUE")


#Task 11.
def set_that_secret(new_secret):
    return custom_module.set_secret(new_secret)

set_that_secret("Open!")
print(custom_module.secret)


#Task 12.
def process_minutes_file(file_name):
    minutes = {}
    rows = []

    try:
        with open(f"../csv/{file_name}", "r") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    minutes["fields"] = row
                else:
                    rows.append(tuple(row))
            minutes["rows"] = rows
            return minutes
    except Exception as e:
        print(e)

def read_minutes():
    minutes1 = process_minutes_file("minutes1.csv")
    minutes2 = process_minutes_file("minutes2.csv")
    return minutes1, minutes2

minutes1, minutes2 = read_minutes()
print(minutes1)
print(minutes2)


#TASK 13.
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    return set1.union(set2)

minutes_set = create_minutes_set()


#Task 14.
def create_minutes_list():
    minutes_list = list(minutes_set)
    minutes_list = list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_list))
    return minutes_list

minutes_list = create_minutes_list()
print(minutes_list)


#Task 15.
def write_sorted_list():
    sorted_minutes_list = sorted(minutes_list, key=lambda x: x[1])
    converted_list = list(map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), sorted_minutes_list))

    try:
        with open("../csv/minutes.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(minutes1["fields"])
            for row in converted_list:
                writer.writerow(row)

    except Exception as e:
        print(e)

    return converted_list

write_sorted_list()
