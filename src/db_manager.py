#!/usr/bin/env python

import sqlite3
import datetime

conn = sqlite3.connect('../systemctl_manager.db')
c = conn.cursor()

def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS activity_log (
                 id INTEGER PRIMARY KEY,
                 action TEXT,
                 service TEXT,
                 timestamp DATETIME)''')

    c.execute('''CREATE TABLE IF NOT EXISTS machine_data (
                 id INTEGER PRIMARY KEY,
                 service_name TEXT,
                 service_status TEXT)''')

def log_activity(action, service):
    timestamp = datetime.datetime.now()
    c.execute("INSERT INTO activity_log (action, service, timestamp) VALUES (?, ?, ?)",
              (action, service, timestamp))
    conn.commit()


def update_machine_data(service_name, service_status):
    c.execute("REPLACE INTO machine_data (service_name, service_status) VALUES (?, ?)",
              (service_name, service_status))
    conn.commit()

create_tables()


def format_timestamp(timestamp_str):
    timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def query_all_activity_logs():
    c.execute("SELECT * FROM activity_log")
    rows = c.fetchall()
    if rows:
        for row in rows:
            formatted_timestamp = format_timestamp(row[3])
            print(f"ID: {row[0]}, Action: {row[1]}, Service: {row[2]}, Timestamp: {formatted_timestamp}")
    else:
        print("No activity logs found.")

def query_activity_logs_by_service(service_name):
    c.execute("SELECT * FROM activity_log WHERE service = ?", (service_name,))
    rows = c.fetchall()
    if rows:
        for row in rows:
            formatted_timestamp = format_timestamp(row[3])
            print(f"ID: {row[0]}, Action: {row[1]}, Service: {row[2]}, Timestamp: {formatted_timestamp}")
    else:
        print(f"No activity logs found for service: {service_name}")

def query_all_machine_data():
    c.execute("SELECT * FROM machine_data")
    rows = c.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Service Name: {row[1]}, Service Status: {row[2]}")
    else:
        print("No machine data found.")

def delete_activity_log_by_id(log_id):
    try:
        log_id = int(log_id)
        c.execute("DELETE FROM activity_log WHERE id = ?", (log_id,))
        conn.commit()
        print(f"Deleted activity log with ID: {log_id}")
    except ValueError:
        print("Invalid ID. Please enter a numeric value.")

def delete_machine_data_by_service(service_name):
    c.execute("DELETE FROM machine_data WHERE service_name = ?", (service_name,))
    conn.commit()
    print(f"Deleted machine data for service: {service_name}")

def delete_activity_logs():
    c.execute("DROP TABLE activity_log")
    conn.commit()
    print(f"Deleted all activity log")

def delete_all_machine_data():
    c.execute("DROP TABLE machine_data")
    conn.commit()
    print(f"Deleted all machine data")
