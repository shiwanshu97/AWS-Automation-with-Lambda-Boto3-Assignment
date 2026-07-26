import boto3
from datetime import datetime

ec2 = boto3.client('ec2')


def lambda_handler(event, context):

    print("Event received:")
    print(event)

    # Extract instance ID from CloudTrail event
    instance_id = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']

    # Extract IAM username
    user_identity = event['detail']['userIdentity']

    if 'userName' in user_identity:
        owner = user_identity['userName']
    else:
        owner = user_identity.get('arn', 'Unknown').split('/')[-1]

    # Current date
    launch_date = datetime.now().strftime("%Y-%m-%d")

    # Add tags to EC2 instance
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {
                'Key': 'Owner',
                'Value': owner
            },
            {
                'Key': 'LaunchDate',
                'Value': launch_date
            }
        ]
    )

    print(f"Successfully tagged instance {instance_id}")
    print(f"Owner: {owner}")
    print(f"LaunchDate: {launch_date}")

    return {
        'statusCode': 200,
        'body': 'EC2 tagging completed successfully'
    }