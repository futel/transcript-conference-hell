# We don't have real packages.
#import sys
#sys.path.append('../src')

import boto3
#import util

# S3 bucket which holds the trancripts.
bucket = 'transcript-conference-hell'
s3 = boto3.client('s3')

# Get everything in the bucket and dump it in the local directory.
for key in s3.list_objects(Bucket=bucket)['Contents']:
    print(key['Key'])
    s3.download_file(bucket, key['Key'], key['Key'])
