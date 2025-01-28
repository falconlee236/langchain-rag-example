# https://cloud.google.com/functions/docs/tutorials/terraform-pubsub?hl=ko
# https://cloud.google.com/functions/docs/writing?hl=ko#directory-structure
resource "google_pubsub_topic" "default" {
    name = "functions2-topic"

    depends_on = [ time_sleep.wait_60_seconds ]
}