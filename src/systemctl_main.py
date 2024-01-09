#!/usr/bin/env python

import subprocess
import sqlite3
import datetime

from db_manager import (log_activity, update_machine_data,
                        query_all_activity_logs, query_activity_logs_by_service,
                        query_all_machine_data, delete_activity_log_by_id,
                        delete_machine_data_by_service,delete_activity_logs,delete_all_machine_data)

def list_all_services():
    print("Available services:")
    subprocess.run(['systemctl', 'list-units', '--type=service'])

def list_running_services():
    print("Running services:")
    subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running'])

def get_service_status(service_name):
    result = subprocess.run(['systemctl', 'is-active', service_name], stdout=subprocess.PIPE)
    status = result.stdout.decode('utf-8').strip()
    return status

def execute_systemctl_command(action, service):
    if action in ['start', 'stop', 'restart', 'enable', 'disable', 'status']:
        print(f"Executing '{action}' on service: {service}")
        subprocess.run(['systemctl', action, service])
        log_activity(action, service)
        new_status = get_service_status(service)
        update_machine_data(service, new_status)
    else:
        print("Invalid action.")

def systemctl_commands():
    while True:
        print(" \n -----------------")
        print("|Systemctl Manager| ")
        print(" -----------------")
        print("Choose an action:")
        print("0. List all available services")
        print("1. List running services")
        print("2. Start a service")
        print("3. Stop a service")
        print("4. Restart a service")
        print("5. Enable a service")
        print("6. Disable a service")
        print("7. Check status of a service")
        print("8. View all activity logs")
        print("9. View activity logs for a specific service")
        print("10. View all machine data")
        print("11. Delete an activity log entry")
        print("12. Delete a machine data entry")
        print("13. Delete all activity log entry")
        print("14. Delete all machine data entry")
        print("15. Exit")

        choice = input("Enter your choice (0-15): ")
        print("\n")

        if choice == '0':
            list_all_services()
        elif choice == '1':
            list_running_services()
        elif choice in ['2', '3', '4', '5', '6', '7']:
            service = input("Enter the service name: ")
            action_map = {
                '2': 'start',
                '3': 'stop',
                '4': 'restart',
                '5': 'enable',
                '6': 'disable',
                '7': 'status'
            }
            action = action_map.get(choice)
            if action:
                execute_systemctl_command(action, service)
            else:
                print("Invalid choice. Please enter a number between 0 and 15.")
        elif choice == '8':
            query_all_activity_logs()
        elif choice == '9':
            service = input("Enter the service name for which you want to see the logs: ")
            query_activity_logs_by_service(service)
        elif choice == '10':
            query_all_machine_data()
        elif choice == '11':
            log_id = input("Enter the ID of the activity log to delete: ")
            delete_activity_log_by_id(log_id)
        elif choice == '12':
            service_name = input("Enter the service name of the machine data to delete: ")
            delete_machine_data_by_service(service_name)
        elif choice == '13':
            delete_activity_logs()
        elif choice == '14':
            delete_all_machine_data()
        elif choice == '15':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 15.")

systemctl_commands()
