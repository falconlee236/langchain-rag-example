resource "google_storage_bucket" "bucket" {
    name     = "vertex-ai-index-test"
    location = var.region
    uniform_bucket_level_access = true
}

# The sample data comes from the following link:
# https://cloud.google.com/vertex-ai/docs/matching-engine/filtering#specify-namespaces-tokens
resource "google_storage_bucket_object" "data" {
    name   = "contents/data.json"
    bucket = google_storage_bucket.bucket.name
    content = <<EOF
    {"id": "42", "embedding": [0.5, 1.0], "restricts": [{"namespace": "class", "allow": ["cat", "pet"]},{"namespace": "category", "allow": ["feline"]}]}
    {"id": "43", "embedding": [0.6, 1.0], "restricts": [{"namespace": "class", "allow": ["dog", "pet"]},{"namespace": "category", "allow": ["canine"]}]}
    EOF
}

resource "google_vertex_ai_index" "index" {
    labels = {
        foo = "bar"
    }
    region   = var.region
    display_name = "test-index"
    description = "index for test"
    metadata {
        contents_delta_uri = "gs://${google_storage_bucket.bucket.name}/contents"
        config {
            dimensions = 2
            approximate_neighbors_count = 150
            shard_size = "SHARD_SIZE_SMALL"
            distance_measure_type = "DOT_PRODUCT_DISTANCE"
            algorithm_config {
                tree_ah_config {
                    leaf_node_embedding_count = 500
                    leaf_nodes_to_search_percent = 7
                }
            }
        }
    }
    index_update_method = "BATCH_UPDATE"
}