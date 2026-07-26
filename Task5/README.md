# Task 5 - Restore an EC2 Instance from the Latest EBS Snapshot Using AWS Lambda

## Objective

The objective of this task is to automate EC2 disaster recovery by restoring an EC2 instance from the latest available EBS snapshot using AWS Lambda.

The Lambda function automatically:

- Finds the latest EBS snapshot.
- Creates an Amazon Machine Image (AMI) from the snapshot.
- Launches a new EC2 instance using the generated AMI.
- Applies tags to the restored instance.
- Prints the newly created EC2 Instance ID.
- Logs the complete restoration process in Amazon CloudWatch Logs.

---

# AWS Services Used

- AWS Lambda
- Amazon EC2
- Amazon EBS Snapshots
- Amazon Machine Image (AMI)
- AWS IAM
- Amazon CloudWatch Logs
- Python 3.12
- Boto3 SDK

---

# AWS Region

```
Region: ap-south-1
Region Name: Asia Pacific (Mumbai)
```

---

# Architecture Flow

```
Existing EBS Snapshot
        |
        ↓
AWS Lambda
EC2InstanceRestore
        |
        ↓
Find Latest Snapshot
        |
        ↓
Register AMI
        |
        ↓
Wait For AMI Availability
        |
        ↓
Launch EC2 Instance
        |
        ↓
Apply Tags
        |
        ↓
CloudWatch Logs
```

---

# Resources Used

| Resource | Name |
|----------|------|
| Lambda Function | EC2InstanceRestore |
| IAM Role | LambdaRestoreEC2Role |
| IAM Inline Policy | EC2RestoreInlinePolicy |
| EBS Snapshot | snap-0889efac8c751b177 |
| Volume | vol-0035f7b3edf669a4f |
| Instance Type | t3.micro |

---

# Prerequisite

Before implementing this solution:

- At least one completed EBS snapshot must exist.
- Snapshot must belong to the EC2 root volume.
- Snapshot creation must be completed successfully.

Verified Snapshot:

```
Snapshot ID:

snap-0889efac8c751b177


State:

Completed


Volume:

vol-0035f7b3edf669a4f
```

---

# Step 1 - Create IAM Role

Created IAM role for Lambda execution.

Navigation:

```
AWS Console

↓

IAM

↓

Roles

↓

Create Role
```

Trusted Entity:

```
AWS Service
```

Use Case:

```
Lambda
```

Attached Managed Policy:

```
AWSLambdaBasicExecutionRole
```

Role Name:

```
LambdaRestoreEC2Role
```

Description:

```
IAM role for Lambda to restore an EC2 instance from the latest EBS snapshot.
```

Purpose:

- Allows Lambda to execute.
- Allows Lambda to write logs into CloudWatch Logs.

---

# Step 2 - Create Inline IAM Policy

Created least privilege inline policy.

Policy Name:

```
EC2RestoreInlinePolicy
```

Policy JSON:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EC2RestorePermissions",
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeSnapshots",
        "ec2:RegisterImage",
        "ec2:RunInstances",
        "ec2:DescribeImages",
        "ec2:CreateTags"
      ],
      "Resource": "*"
    }
  ]
}
```

Permissions Granted:

| Permission | Purpose |
|------------|---------|
| ec2:DescribeSnapshots | Finds available EBS snapshots |
| ec2:RegisterImage | Creates AMI from snapshot |
| ec2:RunInstances | Launches restored EC2 instance |
| ec2:DescribeImages | Checks AMI availability |
| ec2:CreateTags | Adds tags to resources |

---

# Step 3 - Create Lambda Function

Created Lambda function:

```
EC2InstanceRestore
```

Lambda Configuration:

| Setting | Value |
|---------|-------|
| Runtime | Python 3.12 |
| Architecture | x86_64 |
| Execution Role | LambdaRestoreEC2Role |

---

# Step 4 - Configure Lambda Code

Lambda code was configured using Python Boto3 SDK.

Configuration Values:

```
Volume ID

vol-0035f7b3edf669a4f
```

```
Subnet ID

subnet-015e347a7499948ba
```

```
Security Group

sg-0f005f9a0d5357925
```

Lambda performs the following operations:

1. Connects to Amazon EC2 using Boto3.
2. Retrieves snapshots for the specified volume.
3. Sorts snapshots using StartTime.
4. Selects the latest snapshot.
5. Creates an AMI from the snapshot.
6. Waits until AMI becomes available.
7. Launches a new EC2 instance.
8. Applies resource tags.
9. Prints Snapshot ID, AMI ID, and Instance ID.
10. Stores execution logs in CloudWatch.

---

# Step 5 - Deploy Lambda Function

Clicked:

```
Deploy
```

Deployment Result:

```
Successfully updated the function "EC2InstanceRestore".
```

---

# Step 6 - Create Lambda Test Event

Created Lambda test event.

Event Name:

```
RestoreEC2Test
```

Event JSON:

```json
{}
```

Saved the test event successfully.

---

# Step 7 - Execute Lambda Test

Executed Lambda function.

Execution workflow:

```
Find Latest Snapshot
        |
        ↓
Create AMI
        |
        ↓
Wait For AMI Availability
        |
        ↓
Launch New EC2 Instance
        |
        ↓
Apply Tags
        |
        ↓
Return Instance ID
```

Screenshot:

![Task5-Test-Log](Images/Task5-Test-Log.png)

---

# Step 8 - Verify CloudWatch Logs

Checked Lambda execution logs.

Navigation:

```
CloudWatch

↓

Log Groups

↓

Lambda Log Group
```

Verified output:

```
Latest Snapshot:

snap-0889efac8c751b177


AMI Created:

ami-0de1000cf4105d83b


Waiting for AMI to become available...


AMI is now available.


New Instance Created:

i-0fd4977f216f6a860
```

Screenshot:

![Task5-Cloudwatch-Log](Images/Task5-Cloudwatch-Log.png)

---

# Step 9 - Verify Created AMI

Verified generated AMI.

Navigation:

```
EC2

↓

AMIs
```

Result:

```
AMI created successfully from the latest EBS snapshot.
```

Purpose:

- AMI acts as the bootable image for the restored EC2 instance.

Screenshot:

![Task5-Snapshot-Image](Images/Task5-Snapshot-Image.png)

---

# Step 10 - Verify Restored EC2 Instance

Verified restored EC2 instance.

Navigation:

```
EC2

↓

Instances
```

Instance Name:

```
Restored-Instance
```

Instance Type:

```
t3.micro
```

Tags Applied:

```
Name

Restored-Instance
```

```
RestoredFrom

snap-0889efac8c751b177
```

Instance Status:

```
Running
```

Screenshot:

![Task5-Restored-Instance](Images/Task5-Restored-Instance.png)

---

# Lambda Workflow

```
Lambda Trigger
        |
        ↓
Describe Snapshots
        |
        ↓
Sort Snapshots By StartTime
        |
        ↓
Select Latest Snapshot
        |
        ↓
Register AMI
        |
        ↓
Wait Until AMI Available
        |
        ↓
Launch t3.micro EC2 Instance
        |
        ↓
Create Tags
        |
        ↓
Return Instance ID
```

---

# Testing Result

Latest Snapshot:

```
snap-0889efac8c751b177
```

Generated AMI:

```
ami-0de1000cf4105d83b
```

Restored EC2 Instance:

```
i-0fd4977f216f6a860
```

Result:

```
Successfully restored a new EC2 instance from the latest EBS snapshot.
```

---

# Screenshots

## Lambda Test Output

![Task5-Test-Log](Images/Task5-Test-Log.png)

---

## CloudWatch Logs

![Task5-Cloudwatch-Log](Images/Task5-Cloudwatch-Log.png)

---

## AMI Created From Snapshot

![Task5-Snapshot-Image](Images/Task5-Snapshot-Image.png)

---

## Restored EC2 Instance

![Task5-Restored-Instance](Images/Task5-Restored-Instance.png)

---

# Production Improvements

Future improvements:

- Add automatic backup scheduling using AWS Backup.
- Store snapshot IDs dynamically instead of hardcoding.
- Add Multi-AZ disaster recovery strategy.
- Add SNS notifications after restore completion.
- Use AWS Systems Manager Parameter Store for configuration values.
- Implement automated rollback handling.
- Add CloudTrail monitoring for restore activities.

---

# Assignment Checklist

| Requirement | Status |
|------------|--------|
| Verified Existing EBS Snapshot | ✅ Completed |
| IAM Role Created | ✅ Completed |
| AWSLambdaBasicExecutionRole Attached | ✅ Completed |
| Inline IAM Policy Created | ✅ Completed |
| EC2 Restore Permissions Granted | ✅ Completed |
| Lambda Function Created | ✅ Completed |
| Python Boto3 Code Added | ✅ Completed |
| Latest Snapshot Retrieved | ✅ Completed |
| AMI Created | ✅ Completed |
| AMI Availability Verified | ✅ Completed |
| New EC2 Instance Launched | ✅ Completed |
| Resource Tags Applied | ✅ Completed |
| CloudWatch Logs Verified | ✅ Completed |
| Restored Instance Verified | ✅ Completed |
| Disaster Recovery Automation Completed | ✅ Completed |

---

# Result

Successfully implemented an automated EC2 disaster recovery solution using:

- AWS Lambda
- Amazon EC2
- EBS Snapshots
- Amazon Machine Images
- Python 3.12
- Boto3
- IAM
- CloudWatch Logs

The Lambda function automatically identifies the latest EBS snapshot, creates an AMI, launches a new EC2 instance, applies required tags, and records the complete restoration workflow in Amazon CloudWatch Logs.

This solution improves:

- Disaster recovery automation
- Backup restoration process
- Infrastructure recovery speed
- Operational reliability
