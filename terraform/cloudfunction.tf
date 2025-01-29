resource "google_cloudfunctions2_function" "default" {
    name        = "function"
    location    = var.region
    description = "a new function"

    build_config {
        runtime     = "python312"
        entry_point = "my_cloudevent_function" # Set the entry point
        environment_variables = {
            BUILD_CONFIG_TEST = "build_test"
        }
        source {
            storage_source { # build 한 함수가 저장되는 부분
                bucket = google_storage_bucket.default.name
                object = google_storage_bucket_object.default.name
            }
        }
    }

    service_config {
        max_instance_count = 3
        min_instance_count = 1
        available_cpu = "1" # https://cloud.google.com/functions/docs/configuring/memory?hl=ko
        available_memory   = "2Gi"
        timeout_seconds    = 60
        environment_variables = {
            SERVICE_CONFIG_TEST = "config_test"
        }
        ingress_settings               = "ALLOW_INTERNAL_ONLY"
        all_traffic_on_latest_revision = true
    }

    event_trigger {
        trigger_region = var.region
        event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
        pubsub_topic   = google_pubsub_topic.default.id
        retry_policy   = "RETRY_POLICY_RETRY"
    }

    depends_on = [ time_sleep.wait_60_seconds ]
}