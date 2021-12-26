#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Directs when to run different scripts based on AWS dynamoDB values.

import boto3
import os
from subprocess import call
from dotenv import load_dotenv

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_NAME = os.path.basename(BASE_PATH)
ENV_FILE_PATH = os.path.join(os.path.dirname(BASE_PATH), '.env')
REMOVE_SCRIPT = os.path.join(BASE_PATH, 'triggerRemove.sh')
SYNC_SCRIPT = os.path.join(BASE_PATH, 'triggerSynchronization.sh')
load_dotenv(dotenv_path=ENV_FILE_PATH)


def main():
    resource = boto3.resource('dynamodb', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                              aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), region_name=os.getenv('AWS_REGION'))

    table = resource.Table(os.getenv('DYNAMODB_TABLE_NAME'))
    item = table.get_item(Key={'cam': BASE_NAME})['Item']
    if item['deleteRequired'] is True:
        call([REMOVE_SCRIPT])
        item['deleteRequired'] = False
        table.put_item(Item=item)
        call([SYNC_SCRIPT])
    else:
        call([SYNC_SCRIPT])


if __name__ == '__main__':
    main()
