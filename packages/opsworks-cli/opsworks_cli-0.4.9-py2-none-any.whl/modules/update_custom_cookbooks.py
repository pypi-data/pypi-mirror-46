#!/usr/bin/env python
# Copyright 2018 Chathuranga Abeyrathna. All Rights Reserved.
# AWS OpsWorks deployment cli

# update custom cookbooks

import sys
import getopt
import boto3
import time
from common_functions import update_custom_cookbooks_usage
from common_functions import get_names
from common_functions import get_status


def update_custom_cookbooks():
    try:
        opts, args = getopt.getopt(sys.argv[2:], 'r:s:l:i:h', [
            'region=', 'stack=', 'layer=', 'help'
        ])
    except getopt.GetoptError:
        update_custom_cookbooks_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            update_custom_cookbooks_usage()
        elif opt in ('-r', '--region'):
            region = arg
        elif opt in ('-s', '--stack'):
            stack = arg
        elif opt in ('-l', '--layer'):
            layer = arg
        else:
            update_custom_cookbooks_usage()

    get_names(stack, layer, region, "update_custom_cookbooks")
    # initiate boto3 client
    client = boto3.client('opsworks', region_name=region)
    # calling deployment to specified stack layer
    run_update_custom_cookbooks = client.create_deployment(
        StackId=stack,
        LayerIds=[
            layer,
        ],
        Command={
            'Name': 'update_custom_cookbooks'
        },
        Comment='automated update_custom_cookbooks job'
    )
    
    # calling aws api to get the instances within the layer
    get_intance_count = client.describe_instances(
        LayerId=layer
    )
    all_instance_IDs = []
    for instanceid in get_intance_count['Instances']:
        ec2id = instanceid['Ec2InstanceId']
        all_instance_IDs.append(ec2id)
    instances = len(all_instance_IDs)

    deploymentId = run_update_custom_cookbooks['DeploymentId']
    # sending describe command to get status"""  """
    get_status(deploymentId, region, instances)
