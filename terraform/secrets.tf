resource "google_secret_manager_secret" "secret-basic" {
    secret_id = "pg_password"

    replication {
        auto {}
    }

    depends_on = [ time_sleep.wait_60_seconds ]
}

resource "random_string" "root_password" {
    length = 10
    override_special = "%*()-_=+[]{}?"
}

resource "google_secret_manager_secret_version" "secret-version-basic" {
    secret = google_secret_manager_secret.secret-basic.id
    secret_data = random_string.root_password.result

    depends_on = [ google_secret_manager_secret.secret-basic ]
}