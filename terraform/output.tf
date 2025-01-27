output "instance_primary_ip_address" {
    value = google_sql_database_instance.primary.ip_address
}