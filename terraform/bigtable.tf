resource "google_bigtable_instance" "instance" {
    # project 없으면 자동으로 provider에 있는 내용 사용
    name = "tf-instance"
    deletion_protection = false
    labels = {
        my-label = "prod-label"
    }
    cluster {
        cluster_id = "tf-instance-cluster"
        num_nodes = 1
        storage_type = "SSD"
    }
}

resource "google_bigtable_table" "table" {
    name = "tf-table"
    instance_name = google_bigtable_instance.instance.name
}