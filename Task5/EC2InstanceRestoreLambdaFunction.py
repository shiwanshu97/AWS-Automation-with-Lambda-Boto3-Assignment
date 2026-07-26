import boto3
import time

ec2 = boto3.client("ec2")

# Replace with your EBS Volume ID
VOLUME_ID = "vol-0035f7b3edf669a4f"

# Replace with your Subnet ID
SUBNET_ID = "subnet-015e347a7499948ba"

# Replace with your Security Group ID
SECURITY_GROUP_ID = "sg-0f005f9a0d5357925"


def lambda_handler(event, context):

    # Get all snapshots for the volume
    snapshots = ec2.describe_snapshots(
        OwnerIds=["self"],
        Filters=[
            {
                "Name": "volume-id",
                "Values": [VOLUME_ID]
            }
        ]
    )["Snapshots"]

    if not snapshots:
        raise Exception("No snapshots found for the specified volume.")

    # Find the latest snapshot
    latest_snapshot = sorted(
        snapshots,
        key=lambda x: x["StartTime"],
        reverse=True
    )[0]

    snapshot_id = latest_snapshot["SnapshotId"]

    print(f"Latest Snapshot: {snapshot_id}")

    # Register AMI from snapshot
    image = ec2.register_image(
        Name=f"RestoreAMI-{int(time.time())}",
        RootDeviceName="/dev/xvda",
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/xvda",
                "Ebs": {
                    "SnapshotId": snapshot_id,
                    "DeleteOnTermination": True,
                    "VolumeType": "gp3"
                }
            }
        ],
        VirtualizationType="hvm",
        Architecture="x86_64"
    )

    image_id = image["ImageId"]

    print(f"AMI Created: {image_id}")

    # Wait until the AMI is available
    print("Waiting for AMI to become available...")

    waiter = ec2.get_waiter("image_available")
    waiter.wait(ImageIds=[image_id])

    print("AMI is now available.")

    # Launch EC2 instance
    response = ec2.run_instances(
        ImageId=image_id,
        InstanceType="t3.micro",
        MinCount=1,
        MaxCount=1,
        SubnetId=SUBNET_ID,
        SecurityGroupIds=[SECURITY_GROUP_ID],
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "Restored-Instance"
                    },
                    {
                        "Key": "RestoredFrom",
                        "Value": snapshot_id
                    }
                ]
            }
        ]
    )

    instance_id = response["Instances"][0]["InstanceId"]

    print(f"New Instance Created: {instance_id}")

    return {
        "statusCode": 200,
        "SnapshotId": snapshot_id,
        "AMIId": image_id,
        "InstanceId": instance_id
    }