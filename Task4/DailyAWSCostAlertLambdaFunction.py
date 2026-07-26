import boto3
from datetime import datetime, timezone

ce = boto3.client("ce")
sns = boto3.client("sns")


SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:360999005537:AWS-Cost-Alert-Topic"

# For testing use low value
#COST_THRESHOLD = 0.01

# For production example:
COST_THRESHOLD = 50


def lambda_handler(event, context):

    today = datetime.now(timezone.utc)

    start_date = today.replace(day=1).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    response = ce.get_cost_and_usage(
        TimePeriod={
            "Start": start_date,
            "End": end_date
        },
        Granularity="MONTHLY",
        Metrics=[
            "UnblendedCost"
        ]
    )

    amount = float(
        response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
    )

    print(f"Current AWS Cost: ${amount}")

    if amount > COST_THRESHOLD:

        message = (
            f"AWS Cost Alert!\n\n"
            f"Current Month-to-Date Cost: ${amount}\n"
            f"Threshold: ${COST_THRESHOLD}"
        )

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="AWS Cost Alert Notification",
            Message=message
        )

        print("Cost alert sent successfully.")

    else:
        print("Cost is below threshold.")

    return {
        "statusCode": 200,
        "currentCost": amount
    }