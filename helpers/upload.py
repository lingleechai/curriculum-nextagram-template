import boto3, botocore
import os
from flask import request
# from helpers.upload import s3

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.environ.get('S3ACCESSKEY'),
   aws_secret_access_key=os.environ.get('S3SECRETKEY')
)


def upload():
    file = request.files.get('image')
    s3.upload_fileobj(
        file,
        'linglee-nextagram',
        file.filename,
        ExtraArgs={
            "ACL": 'public-read',
            "ContentType": file.content_type
        }
    )
    # except Exception as e:
    #     # This is a catch all exception, edit this part to fit your needs.
    #     print("Something Happened: ", e)
    #     return e
