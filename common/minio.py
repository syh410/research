from minio import Minio
from datetime import timedelta
from os.path import basename


MINIO_HOST = ""
ACCESS_KEY = "root"
SECRET_KEY = "root123456"
MINIO_BUCKET = "pjicloud"


def upload_file(filepath):
    client = Minio(
        MINIO_HOST,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=True,
    )

    found = client.bucket_exists(MINIO_BUCKET)
    if not found:
        client.make_bucket(MINIO_BUCKET)

    client.fput_object(
        MINIO_BUCKET, basename(filepath), filepath,
    )

    return client.presigned_get_object(MINIO_BUCKET, basename(filepath), expires=timedelta(hours=1))