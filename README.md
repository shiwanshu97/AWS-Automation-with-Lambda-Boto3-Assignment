# AWS Automation with Lambda & Boto3

## Project Overview

This project demonstrates real-world AWS automation solutions using **AWS Lambda, Python 3.12, Boto3 SDK, Amazon EventBridge, IAM, CloudWatch Logs, SNS, EC2, S3, EBS Snapshots, and AWS Cost Explorer**.

The objective of this project is to automate common DevOps and Cloud Operations tasks including:

- S3 object lifecycle cleanup
- EBS backup automation
- EC2 instance auto-tagging
- AWS cost monitoring and alerting
- EC2 disaster recovery restoration
- S3 security auditing

These solutions follow AWS best practices:

- Least privilege IAM permissions
- Event-driven architecture
- Serverless automation
- CloudWatch monitoring
- Automated notifications
- Resource tracking

---

# Assignment Requirements Covered

This project satisfies the AWS Lambda & Boto3 automation assignment requirements:

✅ Python 3.12 Lambda Runtime  
✅ AWS Boto3 SDK Implementation  
✅ IAM Least Privilege Policies  
✅ EventBridge Scheduling  
✅ CloudWatch Logging  
✅ SNS Email Notifications  
✅ End-to-End Testing  
✅ Documentation with Screenshots  
✅ GitHub Code Submission  

---

# AWS Architecture Overview

```
                         AWS Cloud

                             |
                             |
                    Amazon EventBridge
                             |
                             |
              +--------------+--------------+
              |              |              |
              ↓              ↓              ↓


        Backup Tasks    Cost Monitoring   Security Audit


              |              |              |

              ↓              ↓              ↓


          AWS Lambda Functions (Python 3.12)

                             |

                             ↓


                       Boto3 SDK

                             |

        +--------------------+--------------------+

        |                    |                    |

        ↓                    ↓                    ↓


       EC2                 S3                  AWS Cost
       EBS                 IAM                 Explorer


        |                    |                    |

        ↓                    ↓                    ↓


                 CloudWatch Logs


                             |

                             ↓


                   SNS Email Alerts
```

---

# Project Workflow

```
AWS Event / Scheduler

          |

          ↓

Amazon EventBridge

          |

          ↓

AWS Lambda Function

          |

          ↓

Python Boto3 SDK

          |

          ↓

AWS Service API

          |

          ↓

CloudWatch Logs

          |

          ↓

SNS Notification (If Required)
```

---

# AWS Services Used

| AWS Service | Purpose |
|-------------|---------|
| AWS Lambda | Executes automation code |
| Python 3.12 | Lambda runtime |
| Boto3 SDK | AWS API interaction |
| IAM | Secure permission management |
| Amazon EventBridge | Scheduling and event triggers |
| Amazon EC2 | Compute automation |
| Amazon EBS | Snapshot backup and restore |
| Amazon S3 | Storage automation and security |
| AWS Cost Explorer | Cost monitoring |
| Amazon SNS | Email notifications |
| Amazon CloudWatch | Logging and monitoring |

---

# Region Used

```
Region:

ap-south-1

Region Name:

Asia Pacific (Mumbai)
```

---

# Repository Structure

```
AWS_Automation_With_Lambda_Boto3

│
├── README.md
│
├── Task1-S3-Bucket-Cleanup
│   |
│   ├── lambda_function.py
│   ├── Images
│   └── README.md
│
├── Task2-EBS-Snapshot-Automation
│   |
│   ├── lambda_function.py
│   ├── Images
│   └── README.md
│
├── Task3-EC2-AutoTagging
│   |
│   ├── lambda_function.py
│   ├── Images
│   └── README.md
│
├── Task4-AWS-Cost-Alert
│   |
│   ├── lambda_function.py
│   ├── Images
│   └── README.md
│
├── Task5-EC2-Restore-Automation
│   |
│   ├── lambda_function.py
│   ├── Images
│   └── README.md
│
└── Task6-S3-Public-Access-Audit
    |
    ├── lambda_function.py
    ├── Images
    └── README.md
```

---

# Assignment Tasks Overview

| Task | Objective | AWS Services |
|------|-----------|--------------|
| Task 1 | Delete S3 objects older than 30 days | S3, Lambda, Boto3 |
| Task 2 | Automate EBS snapshot creation and cleanup | EC2, EBS, Lambda |
| Task 3 | Automatically tag EC2 instances | EC2, EventBridge, Lambda |
| Task 4 | AWS daily cost alert system | Cost Explorer, SNS, Lambda |
| Task 5 | Restore EC2 instance from snapshot | EBS, AMI, EC2, Lambda |
| Task 6 | Audit S3 public access | S3, SNS, Lambda |

---

# Task 1 - Automated S3 Bucket Cleanup

## Objective

Automatically delete stale objects from Amazon S3 buckets.

## Workflow

```
EventBridge Scheduler

        ↓

Lambda Function

        ↓

List S3 Objects

        ↓

Check LastModified Date

        ↓

Delete Objects Older Than 30 Days

        ↓

CloudWatch Logs
```

## Permissions Used

```
s3:ListBucket

s3:DeleteObject
```

## Production Note

For simple object expiration, S3 Lifecycle Rules are preferred.

Lambda is useful when deletion requires:

- Custom conditions
- File naming logic
- Cross-service actions

---

# Task 2 - Automated EBS Snapshot Creation and Cleanup

## Objective

Automate EBS volume backups and snapshot retention.

## Workflow

```
EventBridge Scheduler

        ↓

Lambda

        ↓

Create EBS Snapshot

        ↓

Apply Tags

        ↓

Delete Old Snapshots

        ↓

CloudWatch Logs
```

## Permissions Used

```
ec2:CreateSnapshot

ec2:DescribeSnapshots

ec2:DeleteSnapshot

ec2:CreateTags
```

## Production Note

AWS Data Lifecycle Manager is recommended for standard backup schedules.

Lambda is useful for:

- Custom retention rules
- Notifications
- Cross-account backups

---

# Task 3 - EC2 Auto Tagging

## Objective

Automatically tag newly launched EC2 instances.

## Architecture

```
EC2 Instance Launch

        ↓

EC2 State Change Event

        ↓

EventBridge Rule

        ↓

Lambda Function

        ↓

EC2 CreateTags API

        ↓

Tags Applied
```

## Tags Created

```
LaunchDate = YYYY-MM-DD

Environment = Development
```

## Permissions Used

```
ec2:CreateTags

ec2:DescribeInstances
```

---

# Task 4 - AWS Cost Alert Automation

## Objective

Monitor AWS spending and send alerts when cost exceeds threshold.

## Architecture

```
EventBridge Scheduler

        ↓

Lambda Function

        ↓

AWS Cost Explorer API

        ↓

Compare Cost

        ↓

SNS Topic

        ↓

Email Notification
```

## Permissions Used

```
ce:GetCostAndUsage

sns:Publish
```

## Production Note

AWS Budgets is the managed solution.

Lambda provides additional customization:

- Service based cost analysis
- Slack/Teams notifications
- Custom alert logic

---

# Task 5 - EC2 Disaster Recovery Automation

## Objective

Restore an EC2 instance automatically from the latest EBS snapshot.

## Workflow

```
EBS Snapshot

        ↓

Lambda

        ↓

Find Latest Snapshot

        ↓

Create AMI

        ↓

Launch EC2 Instance

        ↓

Apply Tags

        ↓

CloudWatch Logs
```

## Permissions Used

```
ec2:DescribeSnapshots

ec2:RegisterImage

ec2:RunInstances

ec2:DescribeImages

ec2:CreateTags
```

---

# Task 6 - S3 Public Access Audit

## Objective

Detect publicly accessible S3 buckets and notify administrators.

## Workflow

```
EventBridge Scheduler

        ↓

Lambda Function

        ↓

List S3 Buckets

        ↓

Check Public Access

        ↓

Public Bucket Found

        ↓

SNS Email Alert

        ↓

CloudWatch Logs
```

## Security Checks

Lambda verifies:

```
✓ Block Public Access

✓ Bucket Policy Status

✓ Bucket ACL Permissions
```

## Permissions Used

```
s3:ListAllMyBuckets

s3:GetBucketPublicAccessBlock

s3:GetBucketPolicyStatus

s3:GetBucketAcl

sns:Publish
```

---

# IAM Security Implementation

Each Lambda function uses a dedicated IAM role.

Example:

```
Lambda Function

        ↓

IAM Execution Role

        ↓

Least Privilege Inline Policy

        ↓

Required AWS Permissions Only
```

Security practices followed:

✅ No AdministratorAccess policy  
✅ No FullAccess managed policies  
✅ Resource specific permissions where possible  
✅ CloudWatch logging enabled  

---

# Monitoring and Logging

All Lambda functions generate CloudWatch Logs.

Logs include:

- Execution status
- Created resource IDs
- Deleted resources
- Error messages
- Automation results

Example:

```
Snapshot Created:

snap-xxxxxxxx


Instance Created:

i-xxxxxxxx


SNS Alert Sent Successfully
```

---

# EventBridge Automation

EventBridge is used for:

- Daily cost monitoring
- Daily S3 security audits
- Weekly EBS backups
- EC2 event based tagging

Example:

```
EventBridge

      ↓

Lambda Trigger

      ↓

Automation Execution
```

---

# Testing Performed

Each automation was tested using:

## Lambda Test Invocation

```
AWS Console

↓

Lambda

↓

Test
```

## Verification

Checked:

- Lambda output
- CloudWatch Logs
- AWS Console Resources
- SNS Email Notifications

---

# Screenshots Included

Each task folder contains screenshots of:

✅ IAM Role  
✅ Lambda Configuration  
✅ Test Execution Output  
✅ CloudWatch Logs  
✅ Final Result  

---

# AWS Cost Management

During testing:

- EC2 instances were terminated after validation.
- Temporary S3 buckets were deleted.
- Snapshots were removed after testing.
- Unused Elastic IP addresses were released.
- Cost Explorer API calls were minimized.

Recommended:

Create AWS Budget Alert before testing.

Example:

```
AWS Budget:

$1 Alert Threshold
```

---

# Production Improvements

## Security

- AWS Config Rules
- AWS Security Hub
- CloudTrail Integration
- Secrets Manager

## Monitoring

- CloudWatch Dashboards
- CloudWatch Alarms
- Slack / Teams Notifications

## Deployment

- AWS CDK
- Terraform
- CI/CD Pipeline

## Cost Optimization

- AWS Budgets
- Cost Anomaly Detection
- Automated Reporting

---

# Final Completion Checklist

| Requirement | Status |
|------------|--------|
| Python Lambda Functions | ✅ Completed |
| Boto3 Integration | ✅ Completed |
| IAM Least Privilege | ✅ Completed |
| EventBridge Automation | ✅ Completed |
| CloudWatch Logging | ✅ Completed |
| SNS Notifications | ✅ Completed |
| EC2 Automation | ✅ Completed |
| S3 Automation | ✅ Completed |
| Cost Monitoring | ✅ Completed |
| Disaster Recovery | ✅ Completed |
| Documentation | ✅ Completed |

---

# Final Result

Successfully implemented a complete AWS automation framework using:

- AWS Lambda
- Python Boto3
- Amazon EventBridge
- Amazon EC2
- Amazon S3
- Amazon EBS
- AWS Cost Explorer
- Amazon SNS
- IAM
- CloudWatch Logs

The project demonstrates practical DevOps automation patterns including:

- Serverless automation
- Backup and recovery
- Cost governance
- Security auditing
- Infrastructure management
- Event-driven architecture

This solution reduces manual AWS administration and improves reliability, security, and operational efficiency.
