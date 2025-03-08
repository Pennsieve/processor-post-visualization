#!/usr/bin/env python3.9

import os
from boto3 import client as boto3_client

print("start of processing")

def start_task():  
    ecs_client = boto3_client("ecs",  os.environ['REGION'])
    response = ecs_client.run_task(
        cluster = os.environ['CLUSTER_NAME'],
        launchType = 'FARGATE',
        taskDefinition=os.environ['VIZ_TASK_DEFINITION_NAME'],
        count = 1,
        platformVersion='LATEST',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': os.environ['SUBNET_IDS'].split(","),
                'assignPublicIp': 'ENABLED',
                'securityGroups': [os.environ['VIZ_SECURITY_GROUP_ID']]
                }   
        },
        overrides={
            'containerOverrides': [
                {
                    'name': os.environ['VIZ_CONTAINER_NAME'],
                },
            ],
    })

    task_arn = response['tasks'][0]['taskArn']
    container_task_arn = response['tasks'][0]['containers'][0]['taskArn']

    return task_arn, container_task_arn

task_arn, container_task_arn = start_task()
print(task_arn)
print(container_task_arn)


print("end of processing")