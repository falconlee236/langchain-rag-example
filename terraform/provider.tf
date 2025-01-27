terraform {
    required_providers {
        google = {
            source = "hashicorp/google"
            version = "~> 5.6.0"
        }
    }
}

provider "google" {
    credentials = file("../credentials.json")
    project = var.project
    region = var.region
    zone = var.zone
}