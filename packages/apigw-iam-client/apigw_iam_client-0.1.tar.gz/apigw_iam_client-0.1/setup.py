
from setuptools import setup
import os

description = ""
if os.path.exists('readme.md'):
    description = open('readme.md', 'r').read()

setup(
    name='apigw_iam_client',
    version='0.1',
    description="AWS API Gateway Client Lib for IAM Authorized APIs",
    long_description=description,
    long_description_content_type='text/markdown',
    url="https://github.com/kapilt/apigw-iam-client",
    author="Kapil Thangavelu",
    author_email="kapil.foss@gmail.com",
    license="Apache-2.0",
    py_modules=["apigw_iam_client"],
    install_requires=['boto3', 'requests', 'six'])
