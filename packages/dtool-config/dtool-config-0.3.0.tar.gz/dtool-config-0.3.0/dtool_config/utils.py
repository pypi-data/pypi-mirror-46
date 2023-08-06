"""Helper functions for getting and setting config values."""

import os

from dtoolcore.utils import (
    _get_config_dict_from_file,
    get_config_value_from_file,
    write_config_value_to_file,
)

USERNAME_KEY = "DTOOL_USER_FULL_NAME"
USER_EMAIL_KEY = "DTOOL_USER_EMAIL"

README_TEMPLATE_KEY = "DTOOL_README_TEMPLATE_FPATH"

CACHE_DIRECTORY_KEY = "DTOOL_CACHE_DIRECTORY"

ECS_ENDPOINT_KEY_PREFIX = "DTOOL_ECS_ENDPOINT_"
ECS_ACCESS_KEY_ID_KEY_PREFIX = "DTOOL_ECS_ACCESS_KEY_ID_"
ECS_SECRET_ACCESS_KEY_KEY_PREFIX = "DTOOL_ECS_SECRET_ACCESS_KEY_"

AZURE_KEY_PREFIX = "DTOOL_AZURE_ACCOUNT_KEY_"


def get_username(config_fpath):
    """Return the user name.

    :param config_fpath: path to the dtool config file
    :returns: the user name or an empty string
    """
    return get_config_value_from_file(USERNAME_KEY, config_fpath, "")


def set_username(config_fpath, username):
    """Write the user name to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param username: user name
    """
    return write_config_value_to_file(USERNAME_KEY, username, config_fpath)


def get_user_email(config_fpath):
    """Return the user email.

    :param config_fpath: path to the dtool config file
    :returns: the user email or an empty string
    """
    return get_config_value_from_file(USER_EMAIL_KEY, config_fpath, "")


def set_user_email(config_fpath, email):
    """Write the user email to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param email: user email
    """
    return write_config_value_to_file(USER_EMAIL_KEY, email, config_fpath)


def get_readme_template_fpath(config_fpath):
    """Return the readme template path.

    :param config_fpath: path to the dtool config file
    :returns: path to the readme template file
    """
    return get_config_value_from_file(README_TEMPLATE_KEY, config_fpath, "")


def set_readme_template_fpath(config_fpath, readme_template_fpath):
    """Write the user email to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param readme_template_fpath: path to the readme template file
    """
    return write_config_value_to_file(
        README_TEMPLATE_KEY,
        readme_template_fpath,
        config_fpath
    )


def get_ecs_endpoint(config_fpath, bucket_name):
    """Return the ECS endpoint URL.

    :param config_fpath: path to the dtool config file
    :param bucket_name: name of the bucket in a ECS namespace
    :returns: the ECS endpoint URL or an empty string
    """
    key = ECS_ENDPOINT_KEY_PREFIX + bucket_name
    return get_config_value_from_file(key, config_fpath, "")


def set_ecs_endpoint(config_fpath, bucket_name, ecs_endpoint):
    """Write the ECS endpoint URL to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param bucket_name: name of the bucket in a ECS namespace
    :param ecs_endpoint: ECS endpoint URL
    """
    key = ECS_ENDPOINT_KEY_PREFIX + bucket_name
    return write_config_value_to_file(
        key,
        ecs_endpoint,
        config_fpath
    )


def get_ecs_access_key_id(config_fpath, bucket_name):
    """Return the ECS access key id.

    :param config_fpath: path to the dtool config file
    :param bucket_name: name of the bucket in a ECS namespace
    :returns: the ECS access key id or an empty string
    """
    key = ECS_ACCESS_KEY_ID_KEY_PREFIX + bucket_name
    return get_config_value_from_file(key, config_fpath, "")


def set_ecs_access_key_id(config_fpath, bucket_name, ecs_access_key_id):
    """Write the ECS access key id to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param bucket_name: name of the bucket in a ECS namespace
    :param ecs_access_key_id: ECS access key id
    """
    key = ECS_ACCESS_KEY_ID_KEY_PREFIX + bucket_name
    return write_config_value_to_file(
        key,
        ecs_access_key_id,
        config_fpath
    )


def get_ecs_secret_access_key(config_fpath, bucket_name):
    """Return the ECS secret access key.

    :param config_fpath: path to the dtool config file
    :param bucket_name: name of the bucket in a ECS namespace
    :returns: the ECS secret access key or an empty string
    """
    key = ECS_SECRET_ACCESS_KEY_KEY_PREFIX + bucket_name
    return get_config_value_from_file(
        key,
        config_fpath,
        ""
    )


def set_ecs_secret_access_key(
    config_fpath,
    bucket_name,
    ecs_secret_access_key
):
    """Write the ECS access key id to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param bucket_name: name of the bucket in a ECS namespace
    :param ecs_secret_access_key: ECS secret access key
    """
    key = ECS_SECRET_ACCESS_KEY_KEY_PREFIX + bucket_name
    return write_config_value_to_file(
        key,
        ecs_secret_access_key,
        config_fpath
    )


def get_cache(config_fpath):
    """Return the cache directory specified in the dtool config file.

    :param config_fpath: path to the dtool config file
    :returns: the path to the dtool cache directory
    """

    return get_config_value_from_file(
        CACHE_DIRECTORY_KEY,
        config_fpath,
        ""
    )


def set_cache(config_fpath, cache_dir):
    """Write the cache directory to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param cache_dir: the path to the dtool cache direcotory
    """
    cache_dir = os.path.abspath(cache_dir)
    return write_config_value_to_file(
        CACHE_DIRECTORY_KEY,
        cache_dir,
        config_fpath
    )


def get_azure_secret_access_key(config_fpath, container):
    """Return the Azure storage container secret access key.

    :param config_fpath: path to the dtool config file
    :param container: azure storage container name
    :returns: the Azure container secret access key or an empty string
    """
    key = AZURE_KEY_PREFIX + container
    return get_config_value_from_file(key, config_fpath, "")


def set_azure_secret_access_key(config_fpath, container, az_secret_access_key):
    """Write the ECS access key id to the dtool config file.

    :param config_fpath: path to the dtool config file
    :param container: azure storage container name
    :param az_secret_access_key: azure secret access key for the container
    """
    key = AZURE_KEY_PREFIX + container
    return write_config_value_to_file(key, az_secret_access_key, config_fpath)


def list_azure_containers(config_fpath):
    """List the azure storage containers in the config file.

    :param config_fpath: path to the dtool config file
    :returns: the list of azure storage container names
    """
    config_content = _get_config_dict_from_file(config_fpath)
    az_container_names = []
    for key in config_content.keys():
        if key.startswith(AZURE_KEY_PREFIX):
            name = key[len(AZURE_KEY_PREFIX):]
            az_container_names.append(name)
    return sorted(az_container_names)
