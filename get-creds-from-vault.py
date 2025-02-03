import hvac  # HashiCorp Vault client library for Python
import getpass  # For securely getting user input (e.g., passwords)
import logging  # For logging messages
import warnings  # To handle warnings
import urllib3  # To manage HTTP connections
import os  # To interact with environment variables and file paths
import argparse  # For handling command-line arguments
import json  # To handle JSON data
import sys  # To interact with the Python runtime

# Function to initialize a Vault client
def get_vault_client():
    Vault_url = ""
    try:
        Account_name = os.environ["ACCOUNT_NAME"]
    except KeyError:
        logging.error("ACCOUNT_NAME is not defined in Environment Vars")
        raise

    try:
        Account_type = Account_name.split("-", 3)[2]
    except IndexError:
        logging.error("ACCOUNT_NAME is invalid")
        raise

    if Account_type == "prd":
        Vault_url = "https://vault.example.com/prod"
    elif Account_type == "dev":
        Vault_url = "https://vault.example.com/dev"
    else:
        logging.error("Unsupported ACCOUNT_TYPE")
        raise ValueError("Unsupported ACCOUNT_TYPE")

    client = hvac.Client(url=Vault_url)
    if not client.is_authenticated():
        logging.error("Failed to authenticate with Vault")
        raise Exception("Vault authentication failed")

    return client

# Function to retrieve a secret from Vault
def get_secret(client, secret_path):
    try:
        response = client.secrets.kv.read_secret_version(path=secret_path)
        return response["data"]["data"]
    except Exception as e:
        logging.error(f"Failed to retrieve secret: {e}")
        raise

# The main function encapsulates the execution logic
def main():
    logging.basicConfig(level=logging.INFO)

    # Suppress warnings about insecure HTTP connections
    warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Retrieve secrets from Vault")
    parser.add_argument("secret_path", help="Path to the secret in Vault")
    args = parser.parse_args()

    try:
        # Initialize Vault client
        client = get_vault_client()

        # Retrieve the secret
        secret = get_secret(client, args.secret_path)
        logging.info(f"Retrieved secret: {json.dumps(secret, indent=2)}")
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

# Entry point of the script
if __name__ == "__main__": #If this script is imported as a module in another project, the main() logic will not execute.
    main()
#The main() function handles parsing command-line arguments using argparse. example usage: python script.py secret/path/to/key