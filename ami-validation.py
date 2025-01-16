# Retrieve the account_id from AWS
import boto3
from botocore.exceptions import ClientError
import sys
import argparse
import json
import logging
#Automated the provisioning of Vault access and secret keys for target AWS accounts using Python scripts:
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ec2_client(account_id, version):
    """
    Retrieves the EC2 client after assuming a role and validates the AMI.
    
    Parameters:
    account_id (str): AWS Account ID
    version (str): AMI version to validate

    Returns:
    None
    """
    default_ami_name = "SEV-ENCRYPTED-RHEL-"
    default_ami_version = default_ami_name + version
    
    try:
        # Assume role in the specified account
        assume_role_client = boto3.client('sts')
        core_account_arn = f'arn:aws:iam::{account_id}:role/VAULT-AWSADMIN'
        assume_role_object = assume_role_client.assume_role(
            RoleArn=core_account_arn,
            RoleSessionName="AdminRoleSession",
            DurationSeconds=900
        )
        
        # Extract credentials from the assumed role
        credentials = assume_role_object['Credentials']
        ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        
        # Retrieve AMI images matching the filter
        ami_images = ec2_client.describe_images(Filters=[{'Name': 'name', 'Values': ['ENCRYPTED-RHEL*']}])
        images = ami_images.get('Images', [])
        
        # Check if any AMI matches the required version
        for image in images:
            ami_name = image.get('Name', '')
            if ami_name.startswith(default_ami_version):
                logger.info("Validate AMI: Pass")
                return
        logger.warning("Validate AMI: Fail")
    
    except ClientError as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

def main(argv):
    """
    Main function to parse arguments and invoke the EC2 client function.
    """
    parser = argparse.ArgumentParser(description='Find and validate an AMI')
    parser.add_argument('-f', '--account_id', required=True, help='AWS Account ID')
    parser.add_argument('-v', '--version', required=True, help='AMI version to validate')
    
    args = parser.parse_args()
    get_ec2_client(args.account_id, args.version)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
