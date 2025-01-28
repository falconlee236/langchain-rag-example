variable "project" {
    description = "GCP project ID"
    type = string
    default = "optimap-438115"
}

variable "region" {
    description = "gcp region name"
    type = string
    default = "asia-northeast3"
}

variable "zone" {
    description = "gcp availability zone"
    type = string
    default = "asia-northeast3-a"
}

variable "pg_name" {
    description = "gcp cloud postgre sql name"
    type = string
    default = "postgresql-primary"
}

variable "pg_version" {
    description = "gcp cloud postgre sql database version"
    type = string
    default = "POSTGRES_12"
}

variable "pg_tier" {
    description = "gcp cloud postgre sql CPU tier"
    type = string
    default = "db-f1-micro"
}

variable "gcp_services" {
    description = "gcp service list"
    type = list(string)
    default = [ 
        "sqladmin.googleapis.com",
        "sql-component.googleapis.com",
        "servicenetworking.googleapis.com",
        "secretmanager.googleapis.com",
        "bigtable.googleapis.com",
        "bigtableadmin.googleapis.com",
        "bigtabletableadmin.googleapis.com",
        "pubsub.googleapis.com",
        "cloudfunctions.googleapis.com",
        "cloudbuild.googleapis.com",
        "eventarc.googleapis.com",
    ]
}