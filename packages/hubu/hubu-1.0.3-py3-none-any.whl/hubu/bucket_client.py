import boto3
import logging
import os
from botocore.client import ClientError


class BucketClient:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

        options = {}

        if 'ENDPOINT_URL' in os.environ:
            options['endpoint_url'] = os.environ.get('ENDPOINT_URL')

        if 'AWS_ACCESS_KEY_ID' in os.environ:
            options['aws_access_key_id'] = os.environ.get('AWS_ACCESS_KEY_ID')

        if 'AWS_SECRET_ACCESS_KEY' in os.environ:
            options['aws_secret_access_key'] = os.environ.get('AWS_SECRET_ACCESS_KEY')

        if 'BUCKET_NAME' in os.environ:
            self.bucket_name = os.environ.get('BUCKET_NAME')
        else:
            raise Exception('BUCKET_NAME is not defined!')

        self.__s3 = boto3.client('s3', **options)

        if not self.__bucket_exists():
            raise Exception("Bucket check failed")

    def __bucket_exists(self):
        try:
            self.__s3.head_bucket(Bucket=self.bucket_name)
            self.log.info('Bucket exists')
            return True
        except ClientError:
            self.log.error('Bucket does not exist')
            return False
        except Exception as e:
            self.log.error('Something went wrong', e)
            return False

    def delete_object(self, path):
        self.log.info(f'Delete file: {path}')
        self.__s3.delete_object(Bucket=self.bucket_name, Key=path)

    def put_object(self, body, path):
        self.__s3.put_object(Bucket=self.bucket_name,
                             Key=path,
                             Body=body)

    def upload_fileobj(self, body, path, callback=None):
        self.__s3.upload_fileobj(Bucket=self.bucket_name,
                                 Key=path,
                                 Fileobj=body,
                                 Callback=callback)

    def file_size(self, path):
        """Return key's size, or zero if does not exist"""
        try:
            response = self.__s3.head_object(Bucket=self.bucket_name,
                                             Key=path)
            return response['ContentLength']
        except:
            return 0
