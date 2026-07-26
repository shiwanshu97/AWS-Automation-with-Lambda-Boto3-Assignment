import boto3
from datetime import datetime

ec2 = boto3.client('ec2')


def lambda_handler(event, context):

    print("Received event:")
    print(event)

    detail = event.get("detail")

    if not detail:
        print("No detail found in event")
        return {
            "statusCode": 400,
            "body": "Invalid event format"
        }

    # Extract instance ID
    instance_id = (
        detail["responseElements"]
        ["instancesSet"]
        ["items"][0]
        ["instanceId"]
    )

    # Extract IAM user
    user_identity = detail["userIdentity"]

    owner = user_identity.get(
        "userName",
        user_identity.get("arn", "Unknown").split("/")[-1]
    )

    launch_date = datetime.utcnow().strftime("%Y-%m-%d")

    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {
                "Key": "Owner",
                "Value": owner
            },
            {
                "Key": "LaunchDate",
                "Value": launch_date
            }
        ]
    )

    print("Tagged instance:", instance_id)
    print("Owner:", owner)

    return {
        "statusCode": 200,
        "body": "Tagging completed"
    }