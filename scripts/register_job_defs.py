import json
import os
import os.path as op

import boto3

import ob_pipelines.apps

APPS_DIR = op.dirname(ob_pipelines.apps.__file__)

batch_client = boto3.client('batch')

for app in os.listdir(APPS_DIR):
    app_dir = op.join(APPS_DIR, app)
    if os.path.isdir(app_dir):
        for file in os.listdir(app_dir):
            if file.endswith('definition.json'):
                job_def_file = op.join(APPS_DIR, app, file)
                print(job_def_file)
                with open(job_def_file) as f:
                    job_def = json.load(f)
                response = batch_client.register_job_definition(
                    jobDefinitionName=job_def['jobDefinitionName'],
                    type=job_def['type'],
                    containerProperties=job_def['containerProperties']
                )
            else:
                continue
