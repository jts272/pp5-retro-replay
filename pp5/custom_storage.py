import os

from storages.backends.s3boto3 import S3Boto3Storage

if os.path.isfile("env.py"):
    import env  # noqa


class StaticStorage(S3Boto3Storage):
    bucket_name = os.getenv("AWS_S3_STORAGE_BUCKET_NAME")
    location = "static"


class MediaStorage(S3Boto3Storage):
    bucket_name = os.getenv("AWS_S3_STORAGE_BUCKET_NAME")
    location = "media"
