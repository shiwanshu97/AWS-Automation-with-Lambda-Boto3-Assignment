# Task 3 - Auto-Tagging EC2 Instances on Launch

## Objective

The objective of this task is to automatically tag newly launched EC2 instances using **AWS Lambda, Boto3, and Amazon EventBridge**.

Whenever an EC2 instance changes its state to **running**, an EventBridge rule triggers a Lambda function that automatically adds tags to the instance.

The Lambda function adds:

- `LaunchDate`
- `Environment`

tags for resource tracking, ownership, and cost management.

---

# AWS Services Used

- Amazon EC2
- AWS Lambda
- AWS IAM
- Amazon EventBridge
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

# Resources Created

| Resource | Name |
|----------|------|
| IAM Role | LambdaEC2AutoTagRole |
| IAM Inline Policy | EC2AutoTagInlinePolicy |
| Lambda Function | EC2AutoTagging |
| EventBridge Rule | EC2AutoTagRule |
| Test EC2 Instance | AutoTag-Test-Instance |

---

# Architecture Flow

```
EC2 Instance Launch
        |
        ↓
EC2 State Change Event
        |
        ↓
Amazon EventBridge Rule
        |
        ↓
AWS Lambda Function
        |
        ↓
Boto3 EC2 CreateTags API
        |
        ↓
Tags Added Successfully
```

---

# Implementation Steps

## Step 1 - Create IAM Role

Created IAM role for Lambda execution.

Role Name:

```
LambdaEC2AutoTagRole
```

Trusted Entity:

```
AWS Lambda
```

Attached Managed Policy:

```
AWSLambdaBasicExecutionRole
```

Purpose:

- Allows Lambda to execute.
- Allows Lambda to send logs to Amazon CloudWatch Logs.

---

# Step 2 - Create Least Privilege IAM Policy

Created inline IAM policy:

```
EC2AutoTagInlinePolicy
```

Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EC2TaggingPermissions",
      "Effect": "Allow",
      "Action": [
        "ec2:CreateTags",
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

Permissions:

| Permission | Purpose |
|------------|---------|
| ec2:CreateTags | Creates tags on EC2 instances |
| ec2:DescribeInstances | Retrieves EC2 instance details |

This follows AWS least privilege security practices.

---

# Step 3 - Create Lambda Function

Created Lambda function:

```
EC2AutoTagging
```

Lambda Configuration:

| Setting | Value |
|---------|-------|
| Runtime | Python 3.12 |
| Architecture | x86_64 |
| Execution Role | LambdaEC2AutoTagRole |

---

# Step 4 - Lambda Function Logic

The Lambda function performs:

1. Receives EC2 instance state change event from EventBridge.
2. Extracts EC2 instance ID.
3. Generates current date.
4. Creates tags using Boto3 EC2 API.
5. Logs execution details in CloudWatch.

Tags Created:

```
LaunchDate = YYYY-MM-DD

Environment = Development
```

---

# Step 5 - Lambda Deployment

Lambda deployment completed successfully.

Output:

```
Successfully updated the function "EC2AutoTagging".
```

---

# Step 6 - Create EventBridge Rule

Created EventBridge rule:

```
EC2AutoTagRule
```

Configuration:

| Setting | Value |
|---------|-------|
| Event Bus | default |
| Status | Enabled |

---

# Step 7 - Configure Event Pattern

EventBridge pattern:

```json
{
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "EC2 Instance State-change Notification"
  ],
  "detail": {
    "state": [
      "running"
    ]
  }
}
```

This rule triggers Lambda whenever an EC2 instance enters the running state.

---

# Step 8 - Configure Lambda Target

Configured Lambda function as EventBridge target.

Target:

```
EC2AutoTagging
```

Invocation Role:

```
Amazon_EventBridge_Invoke_Lambda_1470225984
```

This allows EventBridge to invoke Lambda.

---

# Step 9 - Testing Automation

Created test EC2 instance.

Instance Name:

```
AutoTag-Test-Instance
```

Instance Type:

```
t3.micro
```

Testing Flow:

```
EC2 Instance Launch
        |
        ↓
EC2 State Change Event
        |
        ↓
Amazon EventBridge Rule
        |
        ↓
Lambda Function
        |
        ↓
EC2 CreateTags API
        |
        ↓
Tags Added Successfully
```

---

# Step 10 - Verification

Verified EC2 instance tags after the instance entered running state.

Automatically added tags:

| Key | Value |
|-----|-------|
| LaunchDate | 2026-07-24 |
| Environment | Development |

---

# CloudWatch Logs Verification

Checked Lambda execution logs in Amazon CloudWatch.

Successful output:

```
Successfully tagged instance: i-0ba91d34bd2259093
```

This confirms:

- EventBridge successfully triggered Lambda.
- Lambda received EC2 event.
- Boto3 successfully created EC2 tags.

---

# Screenshots

## 1. EC2 AutoTag Test Instance

The EC2 instance displays automatically created tags:

- LaunchDate
- Environment

![Task3-Autotag-Test-Instance](Images/Task3-Autotag-Test-Instance.png)

---

## 2. CloudWatch Logs

Lambda execution logs showing successful EC2 tagging.

![Task3-Cloudwatch-Log](Images/Task3-Cloudwatch-Log.png)

---

# Project Structure

```
Task3-EC2-AutoTagging/
│
├── lambda_function.py
│
├── Images/
│   ├── Task3-Autotag-Test-Instance.png
│   └── Task3-Cloudwatch-Log.png
│
└── README.md
```

---

# Production Considerations

In production environments, this solution can be enhanced by:

- Extracting EC2 owner information using AWS CloudTrail.
- Adding automatic Owner tags.
- Applying team and application-based tagging.
- Integrating with AWS Organizations Tag Policies.
- Adding AWS Config compliance monitoring.

---

# Assignment Requirements Covered

| Requirement | Status |
|------------|--------|
| Python 3.12 Lambda Runtime | ✅ Completed |
| IAM Least Privilege Policy | ✅ Completed |
| EC2 CreateTags Automation | ✅ Completed |
| Boto3 Implementation | ✅ Completed |
| EventBridge Rule | ✅ Completed |
| Automatic EC2 Tagging | ✅ Completed |
| CloudWatch Logging | ✅ Completed |
| Testing Completed | ✅ Completed |
| Documentation Completed | ✅ Completed |
| Screenshots Included | ✅ Completed |

---

# Result

Successfully implemented an automated EC2 instance tagging solution using:

- AWS Lambda
- Python 3.12
- Boto3
- Amazon EventBridge
- IAM
- Amazon CloudWatch Logs

Whenever a new EC2 instance enters the **running** state, Lambda automatically applies:

```
LaunchDate
Environment
```

tags and records execution details in CloudWatch Logs.

This solution improves:

- Resource tracking
- Cost management
- Environment identification
- Operational automation
