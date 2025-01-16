import hvac  # HashiCorp Vault client library for Python
import getpass  # For securely getting user input (e.g., passwords)
import logging  # For logging messages
import warnings  # To handle warnings
import urllib3  # To manage HTTP connections
import os  # To interact with environment variables and file paths
import argparse  # For handling command-line arguments
import json  # To handle JSON data
import sys  # To interact with the Python runtime
#Developed a Python script to retrieve credentials from Vault:
def get_vault_client():   #The function initializes an empty string for Vault_url, which will later store the URL of the Vault server.
    import hvac
    Vault_url = ""

    try:
        Account_name = os.environ["ACCOUNT_NAME"] #Retrieve the ACCOUNT_NAME environment variable
    except KeyError: #If the environment variable isn't set, it raises an exception and prints an error message.
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
