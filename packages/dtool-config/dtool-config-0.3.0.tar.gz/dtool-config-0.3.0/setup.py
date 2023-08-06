from setuptools import setup

url = "https://github.com/jic-dtool/dtool-config"
version = "0.3.0"
readme = open('README.rst').read()

setup(
    name="dtool-config",
    packages=["dtool_config"],
    version=version,
    description="Plugin to make configuration of dtool easier",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@jic.ac.uk",
    url=url,
    install_requires=[
        "dtoolcore>=3.9.0",
        "click",
    ],
    entry_points={
        "dtool.cli": [
            "config=dtool_config.cli:config",
        ],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
