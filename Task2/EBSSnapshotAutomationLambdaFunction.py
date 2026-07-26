import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client("ec2")

VOLUME_ID = "vol-0035f7b3edf669a4f"

# For testing: 5 minutes
# Before final submission: change to 30 days
#RETENTION_PERIOD = timedelta(minutes=5)
RETENTION_PERIOD = timedelta(days=30)


def lambda_handler(event, context):

    # Create snapshot
    response = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description="Automated Lambda Backup"
    )

    snapshot_id = response["SnapshotId"]

    ec2.create_tags(
        Resources=[snapshot_id],
        Tags=[
            {
                "Key": "CreatedBy",
                "Value": "Lambda-Backup"
            }
        ]
    )

    print(f"Created Snapshot: {snapshot_id}")

    # Cleanup old snapshots
    snapshots = ec2.describe_snapshots(
        OwnerIds=["self"],
        Filters=[
            {
                "Name": "tag:CreatedBy",
                "Values": ["Lambda-Backup"]
            }
        ]
    )["Snapshots"]

    now = datetime.now(timezone.utc)

    deleted = []

    for snapshot in snapshots:

        age = now - snapshot["StartTime"]

        if age > RETENTION_PERIOD:

            ec2.delete_snapshot(
                SnapshotId=snapshot["SnapshotId"]
            )

            deleted.append(snapshot["SnapshotId"])

            print(f"Deleted Snapshot: {snapshot['SnapshotId']}")

    return {
        "statusCode": 200,
        "createdSnapshot": snapshot_id,
        "deletedSnapshots": deleted
    }