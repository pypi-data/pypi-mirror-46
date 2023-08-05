#!/usr/bin/env python
# Copyright 2018 Chathuranga Abeyrathna. All Rights Reserved.
# AWS OpsWorks deployment cli

# common help

import sys
import getopt
import boto3
import time
from prettytable import PrettyTable
from colour import print_success
from colour import print_warning
from colour import print_err
from colour import print_muted


def usage():
    print 'usage: aws-opsworks [options] <command> <subcommand> [<subcommand> ...] [parameters]\n'
    print 'To see help text, you can run: \n' + \
          sys.argv[0] + ' --help \n' + \
          sys.argv[0] + ' [options] --help \n'
    print 'available options:\n - execute-recipes\n - update-custom-cookbooks\n - setup\n - deploy\n'
    exit(0)


def execute_recipes_usage():
    print 'usage: \n' + \
        sys.argv[1] + ' --region [region] --stack [opsworks_stack_id] --layer [opsworks_layer_id] --cookbook [cookbook] --custom-json [custom-json]'
    exit(0)


def deploy_usage():
    print 'usage: \n' + \
        sys.argv[1] + ' --region [region] --stack [opsworks_stack_id] --layer [opsworks_layer_id] '
    exit(0)


def update_custom_cookbooks_usage():
    print 'usage: \n' + \
        sys.argv[1] + ' --region [region] --stack [opsworks_stack_id] --layer [opsworks_layer_id]\n'
    exit(0)


def setup_usage():
    print 'usage: \n' + \
        sys.argv[1] + ' --region [region] --stack [opsworks_stack_id] --layer [opsworks_layer_id]'
    exit(0)


def summary(success_count, skipped_count, failed_count):
    table = PrettyTable()
    table.field_names = ["Success", "Skipped", "Failed"]
    table.add_row([str(success_count), str(skipped_count), str(failed_count)])
    print(table.get_string(title="Summary"))


def get_status(deploymentId, region, instances):
    client = boto3.client('opsworks', region_name=region)
    describe_deployment = client.describe_commands(
        DeploymentId=deploymentId
    )

    try:
        success_count = 0
        skipped_count = 0
        failed_count = 0
        fail_skip_count = 0
        print "Deployment started..."
        time.sleep(2)
        while not (success_count == int(instances) or failed_count == int(instances)):
            print "Deployment not completed yet..waiting 10 seconds before send request back to aws..."
            time.sleep(10)
            describe_deployment = client.describe_commands(
                DeploymentId=deploymentId)
            success_count = str(describe_deployment).count("successful")
            skipped_count = str(describe_deployment).count("skipped")
            failed_count = str(describe_deployment).count("failed")
            fail_skip_count = int(skipped_count) + int(failed_count)
            if int(success_count) + int(skipped_count) == int(instances):
                success_count = int(instances)
            elif int(skipped_count) == int(instances):
                skipped_count = int(instances)
            elif int(failed_count) == int(instances):
                failed_count = int(instances)
            elif int(skipped_count) + int(failed_count) == int(instances):
                fail_skip_count = int(instances)
            elif int(success_count) + int(failed_count) == int(instances):
                success_fail_count = int(instances)
        if success_count == int(instances):
            print_success("\nDeployment completed...")
            summary(success_count, skipped_count, failed_count)
            print "\nCheck the deployment logs...\n"
            for logs in describe_deployment['Commands']:
                print logs['LogUrl']
        elif skipped_count == int(instances):
            print_warning("\nDeployment skipped...")
            summary(success_count, skipped_count, failed_count)
            print "\nCheck the deployment logs...\n"
            for logs in describe_deployment['Commands']:
                print logs['LogUrl']
        elif failed_count == int(instances):
            print_err("\nDeployment failed...")
            summary(success_count, skipped_count, failed_count)
            print "\nCheck the deployment logs...\n"
            for logs in describe_deployment['Commands']:
                print logs['LogUrl']
        elif fail_skip_count == int(instances):
            print_muted("\nDeployment failed and some of them skipped...")
            summary(success_count, skipped_count, failed_count)
            print "\nCheck the deployment logs...\n"
            for logs in describe_deployment['Commands']:
                print logs['LogUrl']
        elif success_fail_count == int(instances):
            print_warning(
                "\nDeployment success on some instances and some are got failed...")
            summary(success_count, skipped_count, failed_count)
            print "\nCheck the deployment logs...\n"
            for logs in describe_deployment['Commands']:
                print logs['LogUrl']
    except Exception, e:
        print e


def get_names(stack, layer, region, name):
    client = boto3.client('opsworks', region_name=region)
    stack_details = client.describe_stacks(
        StackIds=[
            stack,
        ]
    )
    stack_name = stack_details['Stacks'][0]['Name']
    if layer is not None:
        layer_details = client.describe_layers(
            LayerIds=[
                layer,
            ]
        )
        layer_name = layer_details['Layers'][0]['Name']
    else:
        layer_name = "None"
    print "\nRunning " + str(name) + " for, " + \
        "\n stack id: " + str(stack) + " | stack name: " + str(stack_name) + \
        "\n layer id: " + str(layer) + " | layer name: " + \
        str(layer_name) + "\n"


def version():
    print '0.4.9'
    exit(0)