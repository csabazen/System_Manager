#!/bin/bash

DB_FILE="../systemctl_manager.db"

initialize_db() {
    sqlite3 $DB_FILE "CREATE TABLE IF NOT EXISTS activity_log (
                        id INTEGER PRIMARY KEY,
                        action TEXT,
                        service TEXT,
                        timestamp DATETIME);"
    sqlite3 $DB_FILE "CREATE TABLE IF NOT EXISTS machine_data (
                        id INTEGER PRIMARY KEY,
                        service_name TEXT,
                        service_status TEXT);"
}

log_activity() {
    local action=$1
    local service=$2
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    sqlite3 $DB_FILE "INSERT INTO activity_log (action, service, timestamp) VALUES ('$action', '$service', '$timestamp');"
}

show_menu() {
    echo " -------------------"
    echo "| Systemctl Manager |"
    echo " ------------------- "
    echo
    echo "1. List all available services"
    echo "2. List running services"
    echo "3. Start a service"
    echo "4. Stop a service"
    echo "5. Restart a service"
    echo "6. Enable a service"
    echo "7. Disable a service"
    echo "8. Check status of a service"
    echo "9. View all activity logs"
    echo "10. View activity logs for a specific service"
    echo "11. View all machine data"
    echo "12. Delete an activity log entry"
    echo "13. Delete a machine data entry"
    echo "14. Delete all activity log entries"
    echo "15. Delete all machine data entries"
    echo "16. Exit"
    echo 
    echo -n "Enter your choice (1-16): "
}

check_service_status() {
    read -p "Enter the service name: " service
    systemctl status $service
}

view_activity_logs_for_service() {
    read -p "Enter the service name: " service
    sqlite3 $DB_FILE "SELECT * FROM activity_log WHERE service = '$service';"
}

view_all_machine_data() {
    sqlite3 $DB_FILE "SELECT * FROM machine_data;"
}

delete_all_activity_logs() {
    sqlite3 $DB_FILE "DELETE FROM activity_log;"
    echo "All activity log entries have been deleted."
}

delete_all_machine_data() {
    sqlite3 $DB_FILE "DELETE FROM machine_data;"
    echo "All machine data entries have been deleted."
}

delete_activity_log_by_id() {
    read -p "Enter the ID of the activity log to delete: " log_id
    sqlite3 $DB_FILE "DELETE FROM activity_log WHERE id = $log_id;"
    echo "Deleted activity log with ID: $log_id"
}

delete_machine_data_by_service() {
    read -p "Enter the service name of the machine data to delete: " service_name
    sqlite3 $DB_FILE "DELETE FROM machine_data WHERE service_name = '$service_name';"
    echo "Deleted machine data for service: $service_name"
}

main() {
    initialize_db

    while true; do
        show_menu
        read choice
        case $choice in
            1) systemctl list-units --type=service ;;
            2) systemctl list-units --type=service --state=running ;;
            3)
                read -p "Enter the service name: " service
                systemctl start $service
                log_activity "start" $service
                ;;
            4)
                read -p "Enter the service name: " service
                systemctl stop $service
                log_activity "stop" $service
                ;;
            5)
                read -p "Enter the service name: " service
                systemctl restart $service
                log_activity "restart" $service
                ;;
            6)
                read -p "Enter the service name: " service
                systemctl enable $service
                log_activity "enable" $service
                ;;
            7)
                read -p "Enter the service name: " service
                systemctl disable $service
                log_activity "disable" $service
                ;;
            8) check_service_status ;;
            9) sqlite3 $DB_FILE "SELECT * FROM activity_log;" ;;
            10) view_activity_logs_for_service ;;
            11) view_all_machine_data ;;
            12) delete_activity_log_by_id ;;
            13) delete_machine_data_by_service ;;
            14) delete_all_activity_logs ;;
            15) delete_all_machine_data ;;
            16) break ;;
            *)  echo "Invalid choice. Please enter a number between 1 and 16." ;;
        esac
    done
}

main
