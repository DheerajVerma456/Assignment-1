import csv
from datetime import datetime, timedelta

def time_duration_to_hours(time_duration):
    # Parse the time duration in HH:MM format and convert to float
    hours, minutes = map(int, time_duration.split(':'))
    return hours + minutes / 60

def analyze_employee_data(file_path):
    # Dictionary to store employee information
    employees = {}

    # Read CSV file and populate the employees dictionary
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            name = row['Employee Name']
            position_id = row['Position ID']
            status = row['Position Status']

            # Check if 'Time In' and 'Time Out' values are not empty
            if row['Time'] and row['Time Out']:
                time_in = datetime.strptime(row['Time'], '%m/%d/%Y %I:%M %p')
                time_out = datetime.strptime(row['Time Out'], '%m/%d/%Y %I:%M %p')

                # Convert time duration to float
                timecard_hours = time_duration_to_hours(row['Timecard Hours (as Time)'])
                
                if name not in employees:
                    employees[name] = {'positions': set(), 'shifts': []}
                
                employees[name]['positions'].add((position_id, status))
                employees[name]['shifts'].append({'time_in': time_in, 'time_out': time_out, 'timecard_hours': timecard_hours})

    # Analyze and print employee information
    for name, info in employees.items():
        shifts = info['shifts']

        # Check for employees who worked for 7 consecutive days
        consecutive_days = 0
        for i in range(len(shifts) - 1):
            if (shifts[i + 1]['time_in'] - shifts[i]['time_in']).days == 1:
                consecutive_days += 1
                if consecutive_days == 6:  # 7 consecutive days including the current one
                    print(f"{name} has worked for 7 consecutive days.")

            else:
                consecutive_days = 0

        # Check for employees with less than 10 hours between shifts but greater than 1 hour
        for i in range(len(shifts) - 1):
            time_between_shifts = shifts[i + 1]['time_in'] - (shifts[i]['time_out'] + timedelta(hours=1))
            if 1 < time_between_shifts.total_seconds() / 3600 < 10:
                print(f"{name} has less than 10 hours between shifts but greater than 1 hour.")

        # Check for employees who worked for more than 14 hours in a single shift
        for shift in shifts:
            if shift['timecard_hours'] > 14:
                print(f"{name} has worked for more than 14 hours in a single shift.")

# Assuming the input file is named 'assignment.csv'
file_path = 'assignment.csv'
analyze_employee_data(file_path)
