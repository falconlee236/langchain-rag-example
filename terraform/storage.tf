resource "random_id" "bucket_prefix" {
    byte_length = 8
}

resource "google_storage_bucket" "default" {
    name = "${random_id.bucket_prefix.hex}-gcf-source" # Every bucket name must be globally unique
    location = var.region
    uniform_bucket_level_access = true
    force_destroy = true
    depends_on = [ time_sleep.wait_60_seconds ]
}

resource "null_resource" "archive_trigger" {
    triggers = {
        main_py_hash = md5(file("../function-source/main.py"))
    }
}

resource "archive_file" "default" {
    type        = "zip"
    output_path = "../function-source.zip" # tmp의 function-source로 압축
    source_dir  = "../function-source/" # 로컬의 이 디렉토리를
    depends_on = [ null_resource.archive_trigger ]
}

resource "google_storage_bucket_object" "default" {
    name   = "function-source.zip"
    bucket = google_storage_bucket.default.name
    source = resource.archive_file.default.output_path # Path to the zipped function source code
}
