from google.cloud import storage


def download_file(
    bucket_name, source_blob_name,
    destination_file,
):
    """downloads file blob from bucket"""

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    print(dir(bucket))
    blob = bucket.blob(source_blob_name)
    return blob.download_as_string()
