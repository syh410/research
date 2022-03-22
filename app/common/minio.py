from minio import Minio
from datetime import timedelta
from os.path import basename
import os


MINIO_HOST = os.getenv('MINIO_HOST', "192.168.66.247:9000")
ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', "root")
SECRET_KEY = os.getenv('MINIO_SECRET_KEY', "root123456")
MINIO_BUCKET = os.getenv('MINIO_BUCKET', "pjicloud")
MINIO_SECURE = os.getenv('MINIO_SECURE', 'False').lower() in ['true', '1', 'yes', 'y', 't', 'on']


def upload_file(filepath):
    client = Minio(
        MINIO_HOST,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=MINIO_SECURE,
    )

    found = client.bucket_exists(MINIO_BUCKET)
    if not found:
        client.make_bucket(MINIO_BUCKET)

    client.fput_object(
        MINIO_BUCKET, basename(filepath), filepath,
    )

    return client.presigned_get_object(MINIO_BUCKET, basename(filepath), expires=timedelta(hours=1))