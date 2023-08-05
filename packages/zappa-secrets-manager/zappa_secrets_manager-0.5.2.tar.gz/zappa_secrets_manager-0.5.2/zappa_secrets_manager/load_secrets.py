import json
import os

from dotenv import load_dotenv

from .get_secrets import get_secret


def load_secrets(PROJECT_NAME,
                 ENV_PATH,
                 EXTRA_ENVS_TO_SET=None,
                 ENV_FILE_NAME='development.env',
                 REGION_NAME=None):
    """
    Loads the secrets in PROJECT_NAME/STAGE into the local environment or
    loads the contents of ENV_PATH/development.env.
    :param PROJECT_NAME: The name of the project part of the key to lookup
                         on AWS Secrets Manager
    :param ENV_PATH:  The path to the local environment file
    :param EXTRA_ENVS_TO_SET: A list of tuples detailing extra environment
                              variables to set
    :param ENV_FILE_NAME: The name of the local environment file
    :param REGION_NAME: The region name
    :return:
    """
    STAGE = os.environ.get('STAGE', None)
    if EXTRA_ENVS_TO_SET is None:
        EXTRA_ENVS_TO_SET = []
    ENV_PATH = os.path.join(ENV_PATH, ENV_FILE_NAME)
    env_file_exists = \
        os.path.exists(ENV_PATH)
    if STAGE is not None and not env_file_exists:
        """
        As we only deploy via zappa, the STAGE environment variable will be there
        so we can check for the existence of that to determine if we are on a
        server or not.  Never go into here if the local env file exists
        """

        envs_to_set = [
            ('API_KEYS', '{PROJECT_NAME}/{STAGE}'.format(
                PROJECT_NAME=PROJECT_NAME,
                STAGE=STAGE)),
        ]
        for extra_envs in EXTRA_ENVS_TO_SET:
            envs_to_set.append(
                (extra_envs[0].format(STAGE=STAGE,
                                      PROJECT_NAME=PROJECT_NAME),
                 extra_envs[1].format(STAGE=STAGE,
                                      PROJECT_NAME=PROJECT_NAME))
            )

        for env_name, secret_name in envs_to_set:
            loaded_secret = get_secret(secret_name,
                                       region_name=REGION_NAME)
            if loaded_secret is not None:
                json_loaded = json.loads(loaded_secret)
                if 'password' in json_loaded:
                    secret = json_loaded['password']
                    os.environ[env_name] = secret
                else:
                    for api_name, secret in json_loaded.items():
                        os.environ[api_name] = secret
    elif env_file_exists:
        """
        We don't deploy the development.env - use that for handling
        development specific settings (local API keys etc)
        """
        load_dotenv(ENV_PATH)
    else:
        raise RuntimeError('Running application and "{0}" '
                           'was not found.  If running on a server ensure '
                           'that the "STAGE" environment variable is '
                           'set'.format(ENV_PATH))
