from setuptools import setup

from onepanel.constants import *

setup(
    name="onepanel",
    version=CLI_VERSION,
    packages=['onepanel', 'onepanel.commands', 'onepanel.onepanel_types', 'onepanel.models',
              'onepanel.utilities', 'onepanel.utilities.s3', 'onepanel.utilities.gcp_cs',
              'onepanel.git_hooks', 'onepanel.sdk'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    install_requires=[
        'configparser',
        'PyYAML<=3.13,>=3.10',
        'prettytable',
        'requests',
        'click>=7',
        'PTable',
        'configobj',
        'websocket-client',
        'humanize',
        'botocore>=1.12.0,<1.13.0'
        'awscli>=1.16.0,<1.17.0',
        'boto3>=1.9.0,<1.10.0',
        'watchdog',
        'iso8601',
        'future',
        'psutil',
        'nvidia-ml-py3',
        'google-cloud-storage'
    ],
    setup_requires=[
        # Need this here to ensure the right version of click is installed on the users machine.
        # Otherwise, they might get the "hidden" error.
        'click>=7',
        'awscli>=1.16.0,<1.17.0'
    ],
    entry_points='''
        [console_scripts]
        onepanel=onepanel.cli:main
    ''',
)
