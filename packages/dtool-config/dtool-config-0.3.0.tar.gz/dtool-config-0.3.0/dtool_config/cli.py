"""dtool_config.cli module."""

import click

import dtoolcore.utils

import dtool_config.utils


CONFIG_PATH = dtoolcore.utils.DEFAULT_CONFIG_PATH


@click.group()
def config():
    """Configure dtool settings."""


@config.group()
def user():
    """Configure user settings."""


@user.command()
@click.argument("username", nargs=-1, required=False)
def name(username):
    """Display / set / update the user name."""
    if not username:
        click.secho(dtool_config.utils.get_username(CONFIG_PATH))
    else:
        username_str = " ".join(username)
        click.secho(dtool_config.utils.set_username(CONFIG_PATH, username_str))


@user.command()
@click.argument("email_address", required=False)
def email(email_address):
    """Display / set / update the user email."""
    if not email_address:
        click.secho(dtool_config.utils.get_user_email(CONFIG_PATH))
    else:
        click.secho(dtool_config.utils.set_user_email(
            CONFIG_PATH,
            email_address
        ))


@config.command()
@click.argument(
    "readme_template_file",
    required=False,
    type=click.Path(exists=True, dir_okay=False)
)
def readme_template(readme_template_file):
    """Display / set / update the readme template file."""
    if not readme_template_file:
        click.secho(dtool_config.utils.get_readme_template_fpath(
            CONFIG_PATH,
        ))
    else:
        click.secho(dtool_config.utils.set_readme_template_fpath(
            CONFIG_PATH,
            readme_template_file
        ))


@config.group()
def ecs():
    """Configure ECS S3 object storage."""


@ecs.command()
@click.argument("bucket_name")
@click.argument("url", required=False)
def endpoint(bucket_name, url):
    """Display / set / update the ECS endpoint URL."""
    if not url:
        click.secho(
            dtool_config.utils.get_ecs_endpoint(CONFIG_PATH, bucket_name)
        )
    else:
        click.secho(
            dtool_config.utils.set_ecs_endpoint(CONFIG_PATH, bucket_name, url)
        )


@ecs.command()
@click.argument("bucket_name")
@click.argument("ecs_access_key_id", required=False)
def access_key_id(bucket_name, ecs_access_key_id):
    """Display / set / update the ECS access key id (username)."""
    if not ecs_access_key_id:
        click.secho(
            dtool_config.utils.get_ecs_access_key_id(CONFIG_PATH, bucket_name)
        )
    else:
        click.secho(dtool_config.utils.set_ecs_access_key_id(
            CONFIG_PATH,
            bucket_name,
            ecs_access_key_id
        ))


@ecs.command()
@click.argument("bucket_name")
@click.argument("ecs_secret_access_key", required=False)
def secret_access_key(bucket_name, ecs_secret_access_key):
    """Display / set / update the ECS secret access key."""
    if not ecs_secret_access_key:
        click.secho(dtool_config.utils.get_ecs_secret_access_key(
                CONFIG_PATH,
                bucket_name
            )
        )
    else:
        click.secho(dtool_config.utils.set_ecs_secret_access_key(
            CONFIG_PATH,
            bucket_name,
            ecs_secret_access_key
        ))


@config.command()
@click.argument(
    "cache_directory_path",
    required=False,
    type=click.Path(exists=True, file_okay=False)
)
def cache(cache_directory_path):
    """Display / set / update the dtool cache directory."""
    if not cache_directory_path:
        click.secho(dtool_config.utils.get_cache(
            CONFIG_PATH,
        ))
    else:
        click.secho(dtool_config.utils.set_cache(
            CONFIG_PATH,
            cache_directory_path
        ))


@config.group()
def azure():
    """Configure Azure Storage."""


@azure.command()  # NOQA
@click.argument("container")
def get(container):
    """Print the secret access key of the specified Azure storage container."""
    click.secho(dtool_config.utils.get_azure_secret_access_key(
        CONFIG_PATH,
        container,
    ))


@azure.command()  # NOQA
@click.argument("container")
@click.argument("azure_secret_access_key")
def set(container, azure_secret_access_key):
    """Set/update the access key for the specified Azure storage container."""
    click.secho(dtool_config.utils.set_azure_secret_access_key(
        CONFIG_PATH,
        container,
        azure_secret_access_key
    ))


@azure.command()  # NOQA
def ls():
    """List all Azure storage containers."""
    for container in dtool_config.utils.list_azure_containers(CONFIG_PATH):
        click.secho(container)
