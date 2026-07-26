import boto3
from datetime import datetime

ec2 = boto3.client("ec2")


def lambda_handler(event, context):

    # Get Instance ID from EventBridge event
    instance_id = event["detail"]["instance-id"]

    # Current date
    launch_date = datetime.utcnow().strftime("%Y-%m-%d")

    # Create tags
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {
                "Key": "LaunchDate",
                "Value": launch_date
            },
            {
                "Key": "Environment",
                "Value": "Development"
            }
        ]
    )

    print(f"Successfully tagged instance: {instance_id}")

    return {
        "statusCode": 200,
        "instanceId": instance_id
    }