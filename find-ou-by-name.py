import boto3 #interact programmatically with AWS services, such as EC2, S3, DynamoDB, Lambda, and many more
import time
#This code is designed to interact with AWS Organizations and related AWS services to determine and fetch details about Organizational Units (OUs) in an AWS account hierarchy
def mgmt_ou_type(mgmt_name_type, region_nm):
    """
    Determines the management type name based on input.

    Params:
        mgmt_name_type: The type of management (e.g., 'mgmt', 'identity', 'core').
        region_nm: The region name.

    Return Type:
        str

    Returns:
        The management type name or an error message if invalid.
    """
    if mgmt_name_type == 'mgmt':
        mgmt_type_name = 'logging'
    elif mgmt_name_type == 'identity':
        mgmt_type_name = 'identity'
    elif mgmt_name_type == 'core':
        mgmt_type_name = 'core-services'
    else:
        mgmt_type_name = "wrong mgmt_type_name"
        print("Mgmt type name is wrong")
    return mgmt_type_name


def ou_name(ou_name, region_name, mgmt_type, root_ou_id):
    """
    Fetches details about an Organizational Unit (OU).

    Params:
        ou_name: The name of the organizational unit.
        region_name: The AWS region name.
        mgmt_type: The type of management.
        root_ou_id: The ID of the root OU.

    Return Type:
        dict

    Returns:
        A JSON object containing the details of the OU.
    """
    # Assume the role for the master account
    client = boto3.client('sts')

    # Define the role ARN
    role_arn = 'arn:aws:iam::66867786876:role/VAUL-AWSADMIN'

    try:
        # Assume the role
        assume_role_object = client.assume_role(
            RoleArn=role_arn,
            RoleSessionName='OUFetcherSession',
            DurationSeconds=900
        )

        credentials = assume_role_object['Credentials']

        # Create an EC2 client using the assumed role credentials
        ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

        # Fetch the child OUs
        org_client = boto3.client('organizations')
        response = org_client.list_organizational_units_for_parent(
            ParentId=root_ou_id
        )
        time.sleep(3)

        children = response['OrganizationalUnits']
        return {"orgid": children}
    except Exception as e:
        print(f"Error fetching OU details: {e}")
        return {"error": str(e)}
