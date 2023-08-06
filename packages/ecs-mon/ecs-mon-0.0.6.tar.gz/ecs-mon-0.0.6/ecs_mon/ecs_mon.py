import boto3
import json
import argparse
import os
import sys

from prettytable import PrettyTable


def get_aws_client(aws_svc_name, profile_name = None ):
    """return aws client according to service name"""
    session = boto3.session.Session(profile_name=profile_name)
    client = session.client(aws_svc_name)
    return client


def get_svc_tasks_list(cluster_n, svc_n, profile_name = None):
    """return a list of running tasks a service"""
    tasks_list = []
    client = get_aws_client("ecs", profile_name=profile_name)
    response = client.list_tasks(
    cluster=cluster_n,
    serviceName=svc_n
    )
    for i in response['taskArns']:
        tasks_list.append(i.split("/", 1)[-1])
    return tasks_list


def get_tsk_def_img_tag(tsk, profile_name = None):
    """return container image tag from a task definition"""
    img_tag = None
    client = get_aws_client("ecs", profile_name=profile_name)
    response = client.describe_task_definition(
    taskDefinition=tsk
    )
    for i in response['taskDefinition']['containerDefinitions']:
        img_tag = i['image'].split(":", 1)[-1]
    return img_tag


def display_svc_tsk(task_list, profile_name = None):
    """Display svc's tasks table"""
    client = get_aws_client("ecs", profile_name=profile_name)
    response = client.describe_tasks(
    cluster='linux-int',
    tasks=task_list
    )
    tsk_table = PrettyTable(['Task ID', 'Task Definition', 
                            'Status', 'Image Tag'])
    index=0
    for i in response['tasks']:
        img_tag = get_tsk_def_img_tag(i['taskDefinitionArn'], profile_name)
        tsk_table.add_row([task_list[index],
                            i['taskDefinitionArn'].split("/", 1)[-1],
                            i['lastStatus'], img_tag]
                        )
        index+=1
    print(tsk_table)

def get_svc_alb_tg_arn(cluster_n, svc_n, profile_name = None):
    """return alb target group that links to a svc"""
    client = get_aws_client("ecs", profile_name=profile_name)
    response = client.describe_services(
    cluster=cluster_n,
    services=[svc_n]
    )
    if not response['services']:
        print("Cannot find ECS service: {}".format(svc_n))
        sys.exit(1)
    try:
        return response['services'][0]['loadBalancers'][0]['targetGroupArn']
    except IndexError as error:
        print("This service does not connect to a load balanacer.")
        print(error)
        sys.exit(1)

def get_svc_alb_healthccheck_info(tg_arn, profile_name = None):
    """return alb arn, healthpath, and protocol"""
    client = get_aws_client("elbv2", profile_name=profile_name)
    response = client.describe_target_groups(
    TargetGroupArns=[tg_arn]
    )
    response2 = client.describe_load_balancers(
        LoadBalancerArns=[
            response['TargetGroups'][0]['LoadBalancerArns'][0]
        ]
    )
    return {
    "LoadBalancerArns": response['TargetGroups'][0]['LoadBalancerArns'][0],
    "HealthCheckProtocol": response['TargetGroups'][0]['HealthCheckProtocol'],
    "HealthCheckPath": response['TargetGroups'][0]['HealthCheckPath'],
    "DNSName": response2['LoadBalancers'][0]['DNSName']
    }
    

def list_svc(cluster_n, profile_name = None):
    """list all services from a cluster"""
    client = get_aws_client("ecs", profile_name=profile_name)
    try:
        response = client.list_services(
        cluster=cluster_n,
        maxResults=100
        )
        if response['serviceArns']:
            print
            for svc in response['serviceArns']:
                print(svc.split("/", 1)[-1])
        else:
            print("The provided ECS cluster does not have ECS services.")
    except Exception as error:
        print("Cannot find ECS services from the provided ECS cluster")
        print(error)


def get_aws_account_id(profile_name = None):
    """print aws account"""
    client = get_aws_client("sts", profile_name=profile_name)
    account_id = client.get_caller_identity()["Account"]
    print("account_id: {}".format(account_id))


def parse_args():
    """esmon's options"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', required=False, default=None,
                        help='The AWS profile to run this request under.' )
    parser.add_argument('--svc',
                        help='ecs svc name')
    parser.add_argument('--cluster', required=True,
                        help='ecs cluster name')
    parser.add_argument('--alb', action='store_true',
                        help='ecs service with alb ')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if not args.profile:
      if 'AWS_PROFILE' in os.environ:
        args.profile=os.environ['AWS_PROFILE']
        print("aws profile: {}".format(args.profile))
      else:
        print("Please provide an AWS profile or set AWS_PROFILE env")
        sys.exit(1)
    get_aws_account_id(profile_name=args.profile)
    print("cluster name: {}".format(args.cluster))
    if args.svc:
        print("service name: {}".format(args.svc))        
        if args.alb:
            svc_tg_arn = get_svc_alb_tg_arn(args.cluster,args.svc,
                                    profile_name=args.profile)
            alb_info = get_svc_alb_healthccheck_info(svc_tg_arn,
                                            profile_name=args.profile)
            print("service url: {}://{}{}".format(alb_info['HealthCheckProtocol'].lower(),
                                alb_info['DNSName'],
                                alb_info['HealthCheckPath']))
        tasks = get_svc_tasks_list(args.cluster, args.svc,
                                    profile_name=args.profile)
        display_svc_tsk(tasks, profile_name=args.profile)
    else:
        list_svc(args.cluster, profile_name=args.profile)

if __name__ == "__main__":
    main()
