import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client("s3")

# Replace with your bucket name
BUCKET_NAME = "shiwanshu-cleanup-assignment"

# For testing: use 5 minutes
# Before final submission: change this to 30 days
#AGE_THRESHOLD = timedelta(minutes=5)
AGE_THRESHOLD = timedelta(days=30)


def lambda_handler(event, context):
    now = datetime.now(timezone.utc)

    paginator = s3.get_paginator("list_objects_v2")

    deleted_objects = []

    for page in paginator.paginate(Bucket=BUCKET_NAME):

        if "Contents" not in page:
            continue

        for obj in page["Contents"]:

            key = obj["Key"]
            last_modified = obj["LastModified"]

            age = now - last_modified

            if age > AGE_THRESHOLD:
                s3.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=key
                )

                deleted_objects.append(key)
                print(f"Deleted: {key}")

    if not deleted_objects:
        print("No old objects found.")

    return {
        "statusCode": 200,
        "deletedObjects": deleted_objects
    }