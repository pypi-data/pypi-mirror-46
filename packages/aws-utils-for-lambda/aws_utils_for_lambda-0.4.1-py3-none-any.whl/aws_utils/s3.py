import boto3
import traceback
from boto3.exceptions import S3UploadFailedError


def upload_file(file, bucket, file_name):
    exception = None
    session = boto3.session.Session()
    s3 = session.resource('s3')
    try:
        s3.meta.client.upload_file(file, bucket, file_name)
    except Exception as e:
        print(e)
        exception = e
    finally:
        return Return(exception=exception).json()


def get_file_content(bucket, file_path):
    data = None
    exception = None
    session = boto3.session.Session()
    s3 = session.resource('s3')
    try:
        response = s3.meta.client.get_object(Bucket=bucket, Key=file_path)
        data = response.get('Body').read().decode('utf-8')
    except Exception as e:
        print(e)
        exception = e
    finally:
        return Return(data=data, exception=exception).json()


class Return:
    def __init__(self, data=None, exception=None, *args, **kwargs):
        self.success = False if exception else True
        self.data = data
        self.error = type(exception).__name__ if exception else None
        self.error_message = str(exception) if exception else None
        self.traceback = traceback.format_tb(exception.__traceback__) if exception else None

    def json(self):
        return self.__dict__
