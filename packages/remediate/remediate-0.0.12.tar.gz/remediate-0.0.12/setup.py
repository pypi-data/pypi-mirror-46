from setuptools import setup, find_packages

setup(
    name="remediate",
    version="0.0.12",
    packages=['remediate','remediate/runbook'],
    include_package_data=True,
    install_requires=['boto3'],
    python_requires='~=3.7',
    license='MIT',
    author='cloudcraeft',
    author_email='cloudcraeft@outloook.com',
    url='https://github.com/cloudcraeft/remediate',
    description='integrate previously written remediation code',
)
