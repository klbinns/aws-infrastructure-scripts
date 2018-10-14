#!/usr/bin/env python
"""
S3 bucket and object ACL audit script

This python script crawls all accessible S3 buckets and objects,
and if there is an access control open to the public, prints out the access
control for that bucket/object to a distict file (not STDOUT)

This report is meant to bring focus to poor S3 policies
and help us identify where we are leaking potentially sensitive data.

You will need to supply AWS_ACCESS_KEY and AWS_SECRET_ACCESS_KEY.

Usage: s3-bucket-audit.py [bucket_names...]

Reqirements: boto3 (AWS Python SDK - use pip to install)

Tested on Python 2.7 but I don't see why Python 3 would not work either.

If no arguments are supplied, it will crawl all visible buckets that the access keys can see.
An array of 1 or more bucket names can be supplied if you only want to
run the report against a subset of buckets.

"""
import sys
import boto3

AWS_ACCESS_KEY = ''
AWS_SECRET_ACCESS_KEY = ''

S3 = boto3.resource(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

def check_S3_buckets(bucket_list = []):
    buckets = get_bucket_objects(bucket_list)

    for bucket in buckets:
        output_file = open(bucket.name + ".txt", "w")

        try:
            check_bucket_grants(output_file, bucket)
            check_bucket_object_grants(output_file, bucket)
        except RuntimeError:
            print "Error with " + bucket.name

        output_file.close()
        print "Bucket " + bucket.name + " processed."

def get_bucket_objects(bucket_list):
    buckets = []
    if not bucket_list:
        buckets = S3.buckets.all()
    else:
        for bucket_str in bucket_list:
            buckets.append(S3.Bucket(bucket_str))

    return buckets

def check_bucket_grants(output_file, bucket):
    rights = process_grants(bucket.Acl())
    print_info(output_file, 'Bucket', rights)

def check_bucket_object_grants(output_file, bucket):
    for bucket_object in bucket.objects.all():
        acl = S3.ObjectAcl(bucket.name, bucket_object.key)
        rights = process_grants(acl)

        print "Processing " + bucket_object.key
        print_info(output_file, bucket_object.key, rights)

def process_grants(acl):
    rights = []
    for grant in acl.grants:
        #http://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
        if grant['Grantee']['Type'].lower() == 'group' \
            and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
            rights.append(grant['Permission'])

    return rights

def print_info(output_file, name, rights):
    if rights:
        output_file.write(name + ": " + ", ".join(rights) + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_S3_buckets(sys.argv[1:])
    else:
        check_S3_buckets()
