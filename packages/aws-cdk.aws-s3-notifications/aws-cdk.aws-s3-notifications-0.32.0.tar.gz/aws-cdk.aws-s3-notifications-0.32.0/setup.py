import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-s3-notifications",
    "version": "0.32.0",
    "description": "Bucket Notifications API for AWS S3",
    "url": "https://github.com/awslabs/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "project_urls": {
        "Source": "https://github.com/awslabs/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.aws_s3_notifications",
        "aws_cdk.aws_s3_notifications._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_s3_notifications._jsii": [
            "aws-s3-notifications@0.32.0.jsii.tgz"
        ],
        "aws_cdk.aws_s3_notifications": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.11.0",
        "publication>=0.0.3",
        "aws-cdk.cdk~=0.32.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
