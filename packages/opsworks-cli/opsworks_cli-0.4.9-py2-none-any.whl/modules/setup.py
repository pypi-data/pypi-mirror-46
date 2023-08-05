#!/usr/bin/env python
# Copyright 2018 Chathuranga Abeyrathna. All Rights Reserved.
# AWS OpsWorks deployment cli

# execute setup

import sys
import getopt
import boto3
import time
from common_functions import setup_usage
from common_functions import get_names
from common_functions import get_status


def setup():
    try:
        opts, args = getopt.getopt(sys.argv[2:], 'r:s:l:i:h', [
            'region=', 'stack=', 'layer=', 'help'
        ])
    except getopt.GetoptError:
        setup_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            setup_usage()
        elif opt in ('-r', '--region'):
            region = arg
        elif opt in ('-s', '--stack'):
            stack = arg
        elif opt in ('-l', '--layer'):
            layer = arg
        else:
            setup_usage()

    get_names(stack, layer, region, "setup")
    # initiate boto3 client
    client = boto3.client('opsworks', region_name=region)
    # calling deployment to specified stack layer
    run_setup = client.create_deployment(
        StackId=stack,
        LayerIds=[
            layer,
        ],
        Command={
            'Name': 'setup'
        },
        Comment='automated setup job'
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

    deploymentId = run_setup['DeploymentId']
    # sending describe command to get status"""  """
    get_status(deploymentId, region, instances)
