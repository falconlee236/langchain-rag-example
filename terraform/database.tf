resource "google_sql_user" "user" {
    name = "root"
    instance = google_sql_database_instance.primary.name
    password = google_secret_manager_secret_version.secret-version-basic.secret_data
    depends_on = [ google_secret_manager_secret_version.secret-version-basic ]
}

resource "google_sql_database" "db" {
    name = google_sql_user.user.name
    instance = google_sql_database_instance.primary.name
    depends_on = [ google_sql_user.user ]
}

resource "google_sql_database_instance" "primary" {
    name                = var.pg_name
    database_version    = var.pg_version
    region              = var.region
    deletion_protection = false

    settings {
        tier      = var.pg_tier
        disk_autoresize = true
        disk_autoresize_limit = 30
        disk_size = 10
        disk_type = "PD_SSD"
        
        ip_configuration {
            ipv4_enabled = true

            authorized_networks {
                name  = "all_networks"
                value = "0.0.0.0/0"
            }
        }

        insights_config {
            query_insights_enabled = true
        }
    }

    depends_on = [ time_sleep.wait_60_seconds ]
}


# install pgvector extension to postgresql  null_resource
resource "null_resource" "setup_pgvector" {
    depends_on = [google_sql_database.db]

    provisioner "local-exec" {
        command = <<-EOT
        PGPASSWORD=${google_sql_user.user.password} psql \
        -h ${google_sql_database_instance.primary.public_ip_address} \
        -U ${google_sql_user.user.name} \
        -d ${google_sql_database.db.name} \
        -c 'CREATE EXTENSION IF NOT EXISTS vector;'
        EOT
    }
}