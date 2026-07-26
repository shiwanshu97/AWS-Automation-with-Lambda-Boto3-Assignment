# Task 6 - Audit S3 Buckets for Public Access and Notify Using AWS Lambda

## Objective

The objective of this task is to automatically audit all Amazon S3 buckets, identify buckets that are publicly accessible, and send an email notification using Amazon SNS whenever a public bucket is detected.

Since Amazon S3 enables **Block Public Access** by default for new buckets, the Lambda function verifies:

- Block Public Access configuration
- Bucket Policy Status
- Bucket ACL permissions

If any bucket is found to be publicly accessible or has Block Public Access disabled, an SNS email alert is sent.

---

# AWS Services Used

- Amazon S3
- AWS Lambda
- Amazon SNS
- Amazon EventBridge Scheduler
- AWS IAM
- Amazon CloudWatch Logs
- Python 3.12
- Boto3 SDK

---

# AWS Region

```
Region : ap-south-1
Region Name : Asia Pacific (Mumbai)
```

---

# Architecture Flow

```
Amazon EventBridge Scheduler
            |
            ↓
AWS Lambda
S3PublicAccessAudit
            |
            ↓
List All S3 Buckets
            |
            ↓
Check Block Public Access
            |
            ↓
Check Bucket Policy Status
            |
            ↓
Check Bucket ACL
            |
            ↓
Public Bucket Found?
        |             |
       Yes            No
        |             |
        ↓             ↓
 Publish SNS       Exit
 Email Alert
        |
        ↓
CloudWatch Logs
```

---

# AWS Resources Used

| Resource | Name |
|----------|------|
| SNS Topic | S3PublicAccessAlertTopic |
| Lambda Function | S3PublicAccessAudit |
| IAM Role | LambdaS3AuditRole |
| IAM Inline Policy | S3PublicAuditInlinePolicy |
| Runtime | Python 3.12 |

---

# Step 1 - Create SNS Topic

Created SNS topic for sending S3 public access alerts.

Navigation:

```
AWS Console

↓

Amazon SNS

↓

Topics

↓

Create Topic
```

Topic Type:

```
Standard
```

Topic Name:

```
S3PublicAccessAlertTopic
```

Display Name:

```
S3 Public Access Alert
```

Purpose:

- Receives public S3 bucket alerts from Lambda.
- Sends email notifications to subscribed users.

Screenshot:

![Task6-Topic-Creation-Image](Images/Task6-Topic-Creation-Image.png)

---

# Step 2 - Create Email Subscription

Created SNS email subscription.

Navigation:

```
SNS

↓

Topics

↓

S3PublicAccessAlertTopic

↓

Create Subscription
```

Configuration:

| Setting | Value |
|---------|-------|
| Protocol | Email |
| Endpoint | Email Address |

Confirmation Process:

1. Open email inbox.
2. Open AWS SNS confirmation email.
3. Click "Confirm Subscription".

Subscription Status:

```
Confirmed
```

Purpose:

- Allows SNS to deliver email alerts.

Screenshot:

![Task6-Subscription-Creation](Images/Task6-Subscription-Creation.png)

---

# Step 3 - Create IAM Role

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
LambdaS3AuditRole
```

Description:

```
IAM role for Lambda to audit S3 buckets and publish SNS alerts.
```

Purpose:

- Allows Lambda execution.
- Allows Lambda to create CloudWatch Logs.

---

# Step 4 - Create Inline IAM Policy

Created least privilege IAM policy.

Policy Name:

```
S3PublicAuditInlinePolicy
```

Policy JSON:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3AuditPermissions",
      "Effect": "Allow",
      "Action": [
        "s3:ListAllMyBuckets",
        "s3:GetBucketPublicAccessBlock",
        "s3:GetBucketPolicyStatus",
        "s3:GetBucketAcl"
      ],
      "Resource": "*"
    },
    {
      "Sid": "SNSPublishPermission",
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "*"
    }
  ]
}
```

Permissions Granted:

| Permission | Purpose |
|------------|---------|
| s3:ListAllMyBuckets | Lists all S3 buckets |
| s3:GetBucketPublicAccessBlock | Checks Block Public Access configuration |
| s3:GetBucketPolicyStatus | Checks bucket policy public access |
| s3:GetBucketAcl | Checks ACL permissions |
| sns:Publish | Sends SNS notifications |

---

# Step 5 - Create Lambda Function

Created Lambda function:

```
S3PublicAccessAudit
```

Configuration:

| Setting | Value |
|---------|-------|
| Runtime | Python 3.12 |
| Architecture | x86_64 |
| Execution Role | LambdaS3AuditRole |

---

# Step 6 - Configure Lambda Function Code

Lambda function was configured using Python Boto3.

SNS Topic ARN:

```
arn:aws:sns:ap-south-1:360999005537:S3PublicAccessAlertTopic
```

Lambda performs:

1. Connects to Amazon S3.
2. Lists all S3 buckets.
3. Checks Block Public Access settings.
4. Checks Bucket Policy Status.
5. Checks Bucket ACL permissions.
6. Detects publicly accessible buckets.
7. Publishes SNS alert.
8. Writes logs into CloudWatch.

---

# Step 7 - Deploy Lambda Function

Clicked:

```
Deploy
```

Deployment Result:

```
Successfully updated the function "S3PublicAccessAudit".
```

---

# Step 8 - Create Test S3 Bucket

Created test bucket.

Navigation:

```
AWS Console

↓

Amazon S3

↓

Create Bucket
```

Bucket Name:

```
s3-public-audit-test-bucket
```

Region:

```
Asia Pacific (Mumbai)
```

Object Ownership:

```
ACLs Disabled
```

Purpose:

- Creates a test environment to validate public access detection.

Screenshot:

![Task6-Test_Bucket](Images/Task6-Test_Bucket.png)

---

# Step 9 - Make Bucket Public For Testing

Disabled Block Public Access.

Navigation:

```
S3

↓

Bucket

↓

Permissions
```

Disabled:

```
Block All Public Access
```

Confirmed:

```
confirm
```

Attached public bucket policy.

Purpose:

- Simulates a publicly accessible S3 bucket.

---

# Step 10 - Test Lambda Function

Created Lambda test event.

Navigation:

```
Lambda

↓

S3PublicAccessAudit

↓

Test
```

Event Name:

```
S3AuditTest
```

Test JSON:

```json
{}
```

Testing Workflow:

```
List All Buckets
        |
        ↓
Check Block Public Access
        |
        ↓
Check Bucket Policy Status
        |
        ↓
Check Bucket ACL
        |
        ↓
Public Bucket Found
        |
        ↓
SNS Notification Sent
        |
        ↓
CloudWatch Logs Updated
```

Screenshot:

![Task6-Test-Log](Images/Task6-Test-Log.png)

---

# Step 11 - Verify CloudWatch Logs

Checked Lambda execution logs.

Navigation:

```
CloudWatch

↓

Log Groups

↓

Lambda Log Group
```

Verified Output:

```
SNS Alert Sent

Public S3 Bucket(s) Detected

Bucket:
s3-public-audit-test-bucket

Reason:
Block Public Access is disabled,
Bucket policy allows public access
```

Screenshot:

![Task6-Cloudwatch-Log](Images/Task6-Cloudwatch-Log.png)

---

# Step 12 - Verify Email Notification

Verified SNS email delivery.

Email contains:

- Bucket Name
- Public Access Reason
- Detection Details

Screenshot:

![Task6-Email-Alert](Images/Task6-Email-Alert.png)

---

# Step 13 - Re-Secure Bucket

Restored security configuration after testing.

Removed:

```
Public Bucket Policy
```

Enabled:

```
Block Public Access
```

(All four options)

Purpose:

- Ensures bucket is secure after testing.

---

# Step 14 - Configure EventBridge Scheduler

Created daily automation schedule.

Navigation:

```
AWS Console

↓

Amazon EventBridge Scheduler

↓

Create Schedule
```

Configuration:

Schedule Name:

```
S3PublicAccessAuditSchedule
```

Schedule Type:

```
Rate Based
```

Expression:

```
rate(1 day)
```

Target:

```
AWS Lambda
```

Lambda Function:

```
S3PublicAccessAudit
```

Purpose:

- Automatically audits S3 buckets every day.

---

# Lambda Workflow

```
Start

 ↓

List All S3 Buckets

 ↓

Check Block Public Access

 ↓

Check Bucket Policy Status

 ↓

Check Bucket ACL

 ↓

Public Bucket Found?

       |

       ├── No → Finish

       |

       Yes

       |

       ↓

Publish SNS Alert

       |

       ↓

Write CloudWatch Logs

       |

       ↓

Finish
```

---

# Testing Result

Detected Public Bucket:

```
s3-public-audit-test-bucket
```

Reason:

```
Block Public Access Disabled

Bucket Policy Allows Public Access
```

SNS Alert:

```
Successfully Sent
```

CloudWatch Logs:

```
Successfully Generated
```

Result:

```
Successfully detected publicly accessible S3 buckets and notified the administrator using Amazon SNS.
```

---

# Screenshots

## SNS Topic Creation

![Task6-Topic-Creation-Image](Images/Task6-Topic-Creation-Image.png)

---

## SNS Subscription

![Task6-Subscription-Creation](Images/Task6-Subscription-Creation.png)

---

## Test Bucket

![Task6-Test_Bucket](Images/Task6-Test_Bucket.png)

---

## Lambda Test Output

![Task6-Test-Log](Images/Task6-Test-Log.png)

---

## CloudWatch Logs

![Task6-Cloudwatch-Log](Images/Task6-Cloudwatch-Log.png)

---

## Email Alert

![Task6-Email-Alert](Images/Task6-Email-Alert.png)

---

# Assignment Checklist

| Requirement | Status |
|------------|--------|
| SNS Topic Created | ✅ Completed |
| Email Subscription Created | ✅ Completed |
| SNS Subscription Confirmed | ✅ Completed |
| IAM Role Created | ✅ Completed |
| AWSLambdaBasicExecutionRole Attached | ✅ Completed |
| Inline IAM Policy Created | ✅ Completed |
| S3 Audit Permissions Granted | ✅ Completed |
| SNS Publish Permission Granted | ✅ Completed |
| Lambda Function Created | ✅ Completed |
| Python Boto3 Code Added | ✅ Completed |
| SNS Topic ARN Configured | ✅ Completed |
| Lambda Deployment Completed | ✅ Completed |
| Test S3 Bucket Created | ✅ Completed |
| Public Access Testing Completed | ✅ Completed |
| CloudWatch Logs Verified | ✅ Completed |
| SNS Email Alert Verified | ✅ Completed |
| Bucket Security Restored | ✅ Completed |
| EventBridge Scheduler Configured | ✅ Completed |

---

# Result

Successfully implemented an automated Amazon S3 public access auditing solution using:

- AWS Lambda
- Amazon S3
- Amazon SNS
- Amazon EventBridge Scheduler
- IAM
- Amazon CloudWatch Logs
- Python 3.12
- Boto3 SDK

The Lambda function automatically audits all S3 buckets, checks Block Public Access settings, Bucket Policy Status, and ACL permissions, detects publicly accessible buckets, sends email notifications through SNS, and records audit results in CloudWatch Logs.

The solution improves:

- S3 security monitoring
- Compliance visibility
- Automated threat detection
- Cloud security operations
