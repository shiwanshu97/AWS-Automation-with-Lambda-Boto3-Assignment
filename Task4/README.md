# Task 4 - Daily AWS Cost Alert Automation Using Lambda, Cost Explorer, SNS & EventBridge Scheduler

## Objective

The objective of this task is to create an automated AWS cost monitoring and alerting system.

The solution checks the current AWS month-to-date cost using the AWS Cost Explorer API and sends an email notification through Amazon SNS when the cost exceeds the configured threshold.

---

# AWS Services Used

- AWS Lambda
- AWS Cost Explorer
- Amazon SNS
- Amazon EventBridge Scheduler
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
EventBridge Scheduler
        |
        ↓
Lambda Function
DailyAWSCostAlert
        |
        ↓
AWS Cost Explorer API
        |
        ↓
Cost Threshold Validation
        |
        ↓
SNS Topic
AWS-Cost-Alert-Topic
        |
        ↓
Email Notification
```

---

# Resources Created

| Resource | Name |
|----------|------|
| SNS Topic | AWS-Cost-Alert-Topic |
| SNS Subscription | Email Subscription |
| IAM Role | LambdaCostAlertRole |
| IAM Inline Policy | CostAlertInlinePolicy |
| Lambda Function | DailyAWSCostAlert |
| EventBridge Scheduler | DailyAWSCostAlertSchedule |

---

# Step 1 - Create SNS Topic

Created SNS topic for sending AWS cost alert notifications.

Navigation:

```
AWS Console → SNS → Topics → Create Topic
```

Topic Type:

```
Standard
```

Created Topic:

```
AWS-Cost-Alert-Topic
```

Purpose:

- Receives cost alert messages from Lambda.
- Sends notifications to subscribed email addresses.

Screenshot:

![Task4-TopicCreation](Images/Task4-TopicCreation.png)

---

# Step 2 - Create SNS Email Subscription

Created email subscription for receiving cost alerts.

Navigation:

```
SNS → Topics → AWS-Cost-Alert-Topic → Create Subscription
```

Configuration:

| Setting | Value |
|---------|-------|
| Protocol | Email |
| Endpoint | Email Address |

SNS confirmation process:

1. Open email inbox.
2. Open AWS SNS confirmation email.
3. Click "Confirm subscription".

Subscription status changed:

```
Pending confirmation
```

to:

```
Confirmed
```

Screenshot:

![Task4-SubscriptionCreation](Images/Task4-SubscriptionCreation.png)

---

# Step 3 - Create IAM Role For Lambda

Created IAM role for Lambda execution.

Navigation:

```
IAM → Roles → Create Role
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
LambdaCostAlertRole
```

Purpose:

- Allows Lambda execution.
- Allows Lambda to create CloudWatch Logs.

---

# Step 4 - Create IAM Inline Policy

Created least privilege inline policy.

Policy Name:

```
CostAlertInlinePolicy
```

Policy JSON:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "arn:aws:sns:ap-south-1:360999005537:AWS-Cost-Alert-Topic"
    }
  ]
}
```

Permissions:

| Permission | Purpose |
|------------|---------|
| ce:GetCostAndUsage | Retrieves AWS cost data |
| sns:Publish | Sends alert messages through SNS |

This follows AWS least privilege security practices.

---

# Step 5 - Create Lambda Function

Created Lambda function:

```
DailyAWSCostAlert
```

Lambda Configuration:

| Setting | Value |
|---------|-------|
| Runtime | Python 3.12 |
| Architecture | x86_64 |
| Execution Role | LambdaCostAlertRole |

---

# Step 6 - Configure Lambda Code

Lambda function performs the following operations:

1. Gets current date.
2. Calculates month start date.
3. Calls AWS Cost Explorer API using Boto3.
4. Retrieves month-to-date AWS cost.
5. Compares cost with configured threshold.
6. Sends SNS notification when threshold is exceeded.

Configured testing threshold:

```
COST_THRESHOLD = 0.01
```

---

# Step 7 - Deploy Lambda Function

Lambda function deployment completed successfully.

Output:

```
Successfully updated the function "DailyAWSCostAlert".
```

---

# Step 8 - Create Lambda Test Event

Created Lambda test event.

Event Name:

```
CostAlertTest
```

Test JSON:

```json
{
  "test": "cost-alert"
}
```

Saved the test event successfully.

---

# Step 9 - Execute Lambda Test

Executed Lambda test.

Lambda successfully retrieved AWS cost data.

Output:

```
Current AWS Cost: $7.5732850983
```

Configured Threshold:

```
$0.01
```

Condition:

```
Current Cost > Threshold
```

Result:

```
Cost alert sent successfully.
```

Screenshot:

![Task4-CostAlertTest](Images/Task4-CostAlertTest.png)

---

# Step 10 - Verify CloudWatch Logs

Checked Lambda execution logs.

Navigation:

```
CloudWatch → Log Groups → Lambda Logs
```

Verified output:

```
Current AWS Cost: $7.5732850983

Cost alert sent successfully.
```

Screenshot:

![Task4-CostAlertTest-CloudwatchLog](Images/Task4-CostAlertTest-CloudwatchLog.png)

---

# Step 11 - Create EventBridge Scheduler

Created EventBridge Scheduler for daily cost monitoring.

Navigation:

```
AWS Console → EventBridge → Scheduler → Create Schedule
```

---

# Step 12 - Configure Scheduler Details

Schedule Name:

```
DailyAWSCostAlertSchedule
```

Description:

```
Runs daily AWS cost check and sends SNS alert
```

Schedule Group:

```
default
```

---

# Step 13 - Configure Schedule Pattern

Schedule Type:

```
Recurring Schedule
```

Time Zone:

```
(UTC+05:30) Asia/Calcutta
```

Schedule Pattern:

```
Rate-based schedule
```

Rate:

```
1 day
```

Expression:

```
rate(1 days)
```

Flexible Time Window:

```
Off
```

---

# Step 14 - Select Lambda Target

Target Type:

```
AWS Lambda
```

Selected Function:

```
DailyAWSCostAlert
```

Payload:

```
None
```

---

# Step 15 - Configure Scheduler Permissions

Created execution role:

```
Amazon_EventBridge_Scheduler_LAMBDA_xxxxx
```

Purpose:

Allows EventBridge Scheduler to invoke Lambda.

---

# Step 16 - Create Scheduler

Scheduler created successfully.

Configuration:

| Setting | Value |
|---------|-------|
| Schedule Name | DailyAWSCostAlertSchedule |
| Status | Enabled |
| Target | DailyAWSCostAlert Lambda |
| Schedule | rate(1 days) |

Screenshot:

![Task4-CreatedScheduler](Images/Task4-CreatedScheduler.png)

---

# Step 17 - Verify Email Notification

SNS successfully delivered email notification.

Email Subject:

```
AWS Cost Alert Notification
```

Email Content:

```
AWS Cost Alert!

Current Month-to-Date Cost: $7.5732850983

Threshold: $0.01
```

Screenshot:

![Task4-EmailReceived](Images/Task4-EmailReceived.png)

---

# Complete Workflow

```
EventBridge Scheduler
        |
        ↓
DailyAWSCostAlert Lambda
        |
        ↓
AWS Cost Explorer API
        |
        ↓
Cost Threshold Validation
        |
        ↓
SNS Publish
        |
        ↓
Email Alert
```

---

# Testing Result

Test Cost:

```
$7.5732850983
```

Threshold:

```
$0.01
```

Result:

```
SNS Email Alert Sent Successfully
```

---

# Screenshots

## SNS Topic Creation

![Task4-TopicCreation](Images/Task4-TopicCreation.png)

## SNS Subscription Creation

![Task4-SubscriptionCreation](Images/Task4-SubscriptionCreation.png)

## Lambda Cost Alert Test

![Task4-CostAlertTest](Images/Task4-CostAlertTest.png)

## CloudWatch Logs

![Task4-CostAlertTest-CloudwatchLog](Images/Task4-CostAlertTest-CloudwatchLog.png)

## EventBridge Scheduler

![Task4-CreatedScheduler](Images/Task4-CreatedScheduler.png)

## Email Notification

![Task4-EmailReceived](Images/Task4-EmailReceived.png)

---

# Production Improvements

Future improvements:

- Store threshold values in AWS Systems Manager Parameter Store.
- Use AWS Budgets for advanced cost control.
- Send alerts to Slack or Microsoft Teams.
- Store monthly reports in Amazon S3.
- Add multiple cost thresholds.
- Create organization-level cost monitoring.

---

# Assignment Completion Checklist

| Requirement | Status |
|------------|--------|
| SNS Topic Created | ✅ Completed |
| SNS Email Subscription Created | ✅ Completed |
| IAM Role Created | ✅ Completed |
| IAM Inline Policy Created | ✅ Completed |
| Lambda Function Created | ✅ Completed |
| Cost Explorer API Integrated | ✅ Completed |
| SNS Notification Implemented | ✅ Completed |
| Lambda Testing Completed | ✅ Completed |
| CloudWatch Logs Verified | ✅ Completed |
| EventBridge Scheduler Created | ✅ Completed |
| Daily Cost Automation Completed | ✅ Completed |
| Email Alert Verified | ✅ Completed |
| Documentation Completed | ✅ Completed |

---

# Result

Successfully implemented an automated AWS Cost Alert system using:

- AWS Lambda
- AWS Cost Explorer API
- Amazon SNS
- Amazon EventBridge Scheduler
- IAM
- Amazon CloudWatch Logs

The system automatically checks AWS spending every day and sends email notifications whenever the configured cost threshold is exceeded.

This solution improves:

- AWS cost visibility
- Budget monitoring
- Automated notifications
- Cloud financial management
