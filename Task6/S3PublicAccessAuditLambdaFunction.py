import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
sns = boto3.client("sns")

# Replace with your SNS Topic ARN
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:360999005537:S3PublicAccessAlertTopic"


def is_bucket_public(bucket_name):
    """
    Returns True if:
    - Block Public Access is disabled
    - Bucket policy allows public access
    - Bucket ACL grants public access
    """

    public = False
    reasons = []

    # Check Block Public Access
    try:
        response = s3.get_public_access_block(Bucket=bucket_name)

        config = response["PublicAccessBlockConfiguration"]

        if not all(config.values()):
            public = True
            reasons.append("Block Public Access is disabled")

    except ClientError:
        public = True
        reasons.append("No Block Public Access configuration found")

    # Check Bucket Policy Status
    try:
        policy = s3.get_bucket_policy_status(Bucket=bucket_name)

        if policy["PolicyStatus"]["IsPublic"]:
            public = True
            reasons.append("Bucket policy allows public access")

    except ClientError:
        pass

    # Check Bucket ACL
    try:
        acl = s3.get_bucket_acl(Bucket=bucket_name)

        for grant in acl["Grants"]:

            grantee = grant.get("Grantee", {})

            if (
                grantee.get("Type") == "Group"
                and "AllUsers" in grantee.get("URI", "")
            ):
                public = True
                reasons.append("Bucket ACL allows public access")
                break

    except ClientError:
        pass

    return public, reasons


def lambda_handler(event, context):

    buckets = s3.list_buckets()["Buckets"]

    public_buckets = []

    for bucket in buckets:

        bucket_name = bucket["Name"]

        public, reasons = is_bucket_public(bucket_name)

        if public:

            public_buckets.append(
                f"Bucket: {bucket_name}\nReason: {', '.join(reasons)}"
            )

    if public_buckets:

        message = "Public S3 Bucket(s) Detected\n\n"
        message += "\n\n".join(public_buckets)

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="S3 Public Access Alert",
            Message=message
        )

        print("SNS Alert Sent")
        print(message)

    else:

        print("No public S3 buckets found.")

    return {
        "statusCode": 200,
        "publicBuckets": public_buckets
    }