# Task 3.
import csv

try:
    with open("../csv/employees.csv", "r") as file:
        reader = csv.reader(file)
        employees_list = []
        for row in reader:
            employees_list.append(row)
except Exception as e:
    print(e)

employees_names_list = [first_name + " " + last_name for _, first_name, last_name, _ in employees_list[1:]]
print(employees_names_list)

employees_names_list_with_e = [name for name in employees_names_list if "e" in name]
print(employees_names_list_with_e)
