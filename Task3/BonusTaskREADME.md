# AWS EC2 Auto Tagging Using CloudTrail, EventBridge and Lambda

## Bonus Task Objective

Automatically tag newly launched EC2 instances for:

- Resource tracking
- Ownership identification
- Cost allocation

The solution extracts the IAM user who launched the EC2 instance using AWS CloudTrail and automatically adds:

- `Owner`
- `LaunchDate`

tags to the EC2 instance.

---

# Architecture

```
IAM User
    |
    | Launch EC2 Instance
    |
    v
AWS CloudTrail
    |
    | Captures RunInstances API Event
    |
    v
Amazon EventBridge Rule
    |
    | Triggers Lambda Function
    |
    v
AWS Lambda
    |
    | Extracts:
    | - Instance ID
    | - IAM Username
    |
    v
EC2 CreateTags API
    |
    v
EC2 Instance
    |
    | Automatic Tags:
    | - Owner
    | - LaunchDate
```

---

# AWS Services Used

| Service | Purpose |
|---|---|
| AWS CloudTrail | Captures EC2 API events |
| Amazon EventBridge | Detects EC2 RunInstances events |
| AWS Lambda | Executes automatic tagging logic |
| IAM Role | Provides Lambda permissions |
| Amazon EC2 | Receives automatic tags |

---

# Step 1: CloudTrail Creation

Created CloudTrail trail:

```
Trail Name:
ec2-auto-tagging-trail
```

Region:

```
Asia Pacific (Mumbai)
ap-south-1
```

Configuration:

- Management Events Enabled
- Read Events Enabled
- Write Events Enabled

CloudTrail records EC2 API activity such as:

```
RunInstances
```

Screenshot:

![CloudTrail Creation](image/BonusTask-CloudTrail-Creation.png)

---

# Step 2: CloudTrail Logging Creation

Verified CloudTrail logging status.

Trail:

```
ec2-auto-tagging-trail
```

Status:

```
Logging Enabled
```

CloudTrail continuously records AWS API actions.

Screenshot:

![CloudTrail Logging Creation](image/BonusTask-CloudTrail-Logging-Creation.png)

---

# Step 3: IAM Role Creation For Lambda

Created IAM Role:

```
EC2-AutoTag-Lambda-Role
```

Trusted Entity:

```
AWS Lambda
```

Permissions:

```
ec2:DescribeInstances
ec2:CreateTags
```

This role allows Lambda to:

- Read EC2 instance information
- Create EC2 tags automatically

---

# Step 4: Lambda Function Creation

Created Lambda Function:

```
EC2-AutoTag-Function
```

Runtime:

```
Python 3.12
```

Lambda receives CloudTrail events from EventBridge.

---

## Lambda Function Code

```python
import boto3
from datetime import datetime

ec2 = boto3.client('ec2')


def lambda_handler(event, context):

    print("Received event:")
    print(event)

    detail = event.get("detail")

    if not detail:
        return {
            "statusCode": 400,
            "body": "Invalid event format"
        }


    instance_id = (
        detail["responseElements"]
        ["instancesSet"]
        ["items"][0]
        ["instanceId"]
    )


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


    print("Tagged Instance:", instance_id)
    print("Owner:", owner)


    return {
        "statusCode": 200,
        "body": "Tagging completed"
    }
```

---

# Step 5: EventBridge Rule Creation

Created EventBridge rule:

```
Rule Name:
EC2-RunInstances-AutoTag-Rule
```

Purpose:

Detect EC2 instance launch events from CloudTrail.

Event Pattern:

```json
{
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "detail": {
    "eventSource": [
      "ec2.amazonaws.com"
    ],
    "eventName": [
      "RunInstances"
    ]
  }
}
```

Target:

```
Lambda Function:

EC2-AutoTag-Function
```

Screenshot:

![EventBridge Creation](image/BonusTask-EventBridge-Creation.png)

---

# Step 6: Lambda Permission For EventBridge

Added Lambda resource-based permission.

Principal:

```
events.amazonaws.com
```

Action:

```
lambda:InvokeFunction
```

Source:

```
EC2-RunInstances-AutoTag-Rule
```

This allows EventBridge to trigger Lambda.

---

# Step 7: Testing The Automation

Created a new EC2 instance:

```
Name:
AutoTag-Bonus-Test
```

Instance launch event:

```
RunInstances
```

Flow:

```
EC2 Launch
    |
    v
CloudTrail Event
    |
    v
EventBridge Rule
    |
    v
Lambda Execution
    |
    v
EC2 Tags Added
```

Screenshot:

![Test Logging Creation](image/BonusTask-Test-Logging-Creation.png)

---

# Step 8: EC2 Instance Created With Automatic Tags

After launching the EC2 instance, Lambda automatically added tags.

Instance:

```
AutoTag-Bonus-Test
```

Automatically created tags:

| Key | Value |
|---|---|
| Owner | IAM User |
| LaunchDate | Current Date |
| Name | AutoTag-Bonus-Test |

Screenshot:

![Instance Created With Tags](image/BonusTask-InstanceCreatedWithTag-Creation.png)

---

# Final Verification

| Task | Status |
|---|---|
| CloudTrail Created | ✅ Completed |
| CloudTrail Logging Enabled | ✅ Completed |
| IAM Role Created | ✅ Completed |
| Lambda Function Created | ✅ Completed |
| EventBridge Rule Created | ✅ Completed |
| Lambda Permission Added | ✅ Completed |
| EC2 Launch Event Captured | ✅ Completed |
| Owner Tag Added Automatically | ✅ Completed |
| LaunchDate Tag Added Automatically | ✅ Completed |

---

# Conclusion

The EC2 Auto Tagging automation was successfully implemented using:

- AWS CloudTrail
- Amazon EventBridge
- AWS Lambda
- IAM Permissions
- Amazon EC2 Tags

The system automatically identifies the IAM user who launches an EC2 instance and applies ownership and launch date tags without manual intervention.

This solution can be used for:

- Cloud cost allocation
- Resource ownership tracking
- Compliance auditing
- Enterprise cloud governance
