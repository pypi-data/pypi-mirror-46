import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def get_secret(secret_name, region_name=None):
    """
    Gets the secret from AWS Secrets Manager
    :param secret_name: The name of the secret
    :param region_name: The reigion name where the secret resides
    :return: The value of the secret
    """
    if region_name is None:
        region_name = "eu-west-2"
    endpoint_url = "https://secretsmanager.%s.amazonaws.com" % region_name

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        endpoint_url=endpoint_url
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        return
    except NoCredentialsError:
        # Used for pipelines as the credentials won't be configured
        return None
    else:
        # Decrypted secret using the associated KMS CMK
        # Depending on whether the secret was a string or binary, one of
        # these fields will be populated
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = get_secret_value_response['SecretBinary']
    return secret
