import boto3
region = 'us-east-1'
instances = ['i-0e7ef28df57c13e84']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.start_instances(InstanceIds=instances)
    print('started your instances: ' + str(instances))
    
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
        FunctionName='ssm-assignment2',
        InvocationType='Event',
    )