import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-ecs",
    "version": "0.32.0",
    "description": "The CDK Construct Library for AWS::ECS",
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
        "aws_cdk.aws_ecs",
        "aws_cdk.aws_ecs._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_ecs._jsii": [
            "aws-ecs@0.32.0.jsii.tgz"
        ],
        "aws_cdk.aws_ecs": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.11.0",
        "publication>=0.0.3",
        "aws-cdk.assets-docker~=0.32.0",
        "aws-cdk.aws-applicationautoscaling~=0.32.0",
        "aws-cdk.aws-autoscaling~=0.32.0",
        "aws-cdk.aws-certificatemanager~=0.32.0",
        "aws-cdk.aws-cloudformation~=0.32.0",
        "aws-cdk.aws-cloudwatch~=0.32.0",
        "aws-cdk.aws-ec2~=0.32.0",
        "aws-cdk.aws-ecr~=0.32.0",
        "aws-cdk.aws-elasticloadbalancing~=0.32.0",
        "aws-cdk.aws-elasticloadbalancingv2~=0.32.0",
        "aws-cdk.aws-iam~=0.32.0",
        "aws-cdk.aws-lambda~=0.32.0",
        "aws-cdk.aws-logs~=0.32.0",
        "aws-cdk.aws-route53~=0.32.0",
        "aws-cdk.aws-route53-targets~=0.32.0",
        "aws-cdk.aws-secretsmanager~=0.32.0",
        "aws-cdk.aws-servicediscovery~=0.32.0",
        "aws-cdk.aws-sns~=0.32.0",
        "aws-cdk.aws-sqs~=0.32.0",
        "aws-cdk.cdk~=0.32.0",
        "aws-cdk.cx-api~=0.32.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
