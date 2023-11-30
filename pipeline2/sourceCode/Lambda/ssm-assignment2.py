import time
import json
import boto3

def lambda_handler(event, context):
    client = boto3.client("ec2")
    ssm = boto3.client("ssm")

    instance_id = "i-0e7ef28df57c13e84"
    max_retries = 10
    retry_interval = 10  

    for i in range(max_retries):
        describe_instance = client.describe_instances(InstanceIds=[instance_id])

        if describe_instance['Reservations'][0]['Instances'][0]['State']['Name'] == "running":
            response = ssm.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={
                    "commands": ["/bin/bash", "/home/ubuntu/run.sh"]
                }
            )

            command_id = response["Command"]["CommandId"]
            time.sleep(10)  

            output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
            print(output)

            return {"statusCode": 200, "body": json.dumps("Code is running")}

        time.sleep(retry_interval)

    print("Instance did not reach 'running' state after multiple retries.")
    return {"statusCode": 500, "body": json.dumps("Instance startup failed.")}