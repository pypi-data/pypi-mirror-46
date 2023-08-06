import boto3
from importlib import import_module


class AWS:
    def __init__(self, access_key_id, secret_access_key, region_name):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_name = region_name

    def run(self, runbook_id, incident, region_name=None):
        session = boto3.Session(self.access_key_id, self.secret_access_key, region_name=region_name)
        try:
            runbook = import_module('runbook.' + runbook_id)
        except Exception as e:
            raise Exception(f'Cannot import/find runbook for {runbook_id} ({incident}). Error: {str(e)}')
        runbook.remediate(session, incident, None)


if __name__ == '__main__':
    import os
    import sys
    incident = {}
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', '')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    aws_default_region = os.environ.get('AWS_DEFAULT_REGION', '')
    if not aws_access_key_id or not aws_secret_access_key or not aws_default_region:
        print("Empty environ var")
        sys.exit(1)

    AWS(aws_access_key_id, aws_secret_access_key, aws_default_region).run('AWS-RDS-010', incident)
