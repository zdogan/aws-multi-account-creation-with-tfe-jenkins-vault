import boto3
from botocore.exceptions import ClientError
import sys
import argparse
import logging
# 
#python retrieve_default_sg.py --account_id 123456789012
#The script will validate and log whether the default security group exists in the account.
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ec2_client(account_id):
    """
    Assumes a role in the given AWS account and returns an EC2 client.
    
    Parameters:
    account_id (str): AWS Account ID
    
    Returns:
    boto3.client: EC2 client
    """
    try:
        assume_role_client = boto3.client('sts')
        core_account_arn = f'arn:aws:iam::{account_id}:role/VAULT-AWSADMIN'
        
        assume_role_object = assume_role_client.assume_role(
            RoleArn=core_account_arn,
            RoleSessionName="AdminRoleSession",
            DurationSeconds=900
        )
        
        credentials = assume_role_object['Credentials']
        ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        return ec2_client
    except ClientError as e:
        logger.error(f"Failed to assume role: {e}")
        sys.exit(1)

def get_default_sg(account_id):
    """
    Retrieves and validates the default Security Group in the given AWS account.
    
    Parameters:
    account_id (str): AWS Account ID
    
    Returns:
    None
    """
    try:
        ec2_client = get_ec2_client(account_id)
        response = ec2_client.describe_security_groups(
            Filters=[{'Name': 'group-name', 'Values': ['default']}]
        )
        
        security_groups = response.get('SecurityGroups', [])
        
        if not security_groups:
            logger.warning("Default SG: Fail! No default security group found.")
        else:
            for sg in security_groups:
                if sg.get('GroupName') == 'default':
                    logger.info("Default SG: Pass!")
                    return
            logger.warning("Default SG: Fail!")
    
    except ClientError as e:
        logger.error(f"Error retrieving security groups: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main(argv):
    """
    Main function to parse arguments and invoke default SG retrieval.
    """
    parser = argparse.ArgumentParser(description="Find default Security Group by name")
    parser.add_argument('-f', '--account_id', required=True, help="AWS Account ID")
    
    args = parser.parse_args()
    get_default_sg(args.account_id)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
