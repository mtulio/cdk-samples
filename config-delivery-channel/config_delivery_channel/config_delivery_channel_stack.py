from aws_cdk import (
    core,
    aws_iam as _iam,
    aws_s3 as _s3,
    aws_config as _config,
)
from aws_cdk.aws_config import (
    CfnConfigurationRecorder,
    CfnDeliveryChannel
)
import boto3

class ConfigDeliveryChannelStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ## Config
        #- Create bucket
        #- Create IAM role
        #- Setup Recorder
        #- Setup Delivery Channel: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_config/CfnDeliveryChannel.html

        cliSts = boto3.client('sts')
        caller = cliSts.get_caller_identity()

        roleConfig = _iam.CfnRole(self, "CustomAWSConfigService",
                               role_name="CustomAWSConfigService",
                               assume_role_policy_document={
                                    "Version": "2012-10-17",
                                    "Statement": [
                                        {
                                        "Effect": "Allow",
                                        "Principal": {
                                            "Service": "config.amazonaws.com"
                                        },
                                        "Action": "sts:AssumeRole"
                                        }
                                    ]
                                    },
                                managed_policy_arns=[
                                    "arn:aws:iam::aws:policy/service-role/AWSConfigRole",
                                    "arn:aws:iam::aws:policy/AmazonS3FullAccess"
                                ])

        bname = "aws-config-custom-{}".format(caller['Account'])
        bucketConfig = _s3.CfnBucket(self, bname, bucket_name=bname)
        bucketConfig.apply_removal_policy(apply_to_update_replace_policy=False)

        rec = _config.CfnConfigurationRecorder(self, "ConfigRec", name="ConfigRec",
                role_arn=roleConfig.attr_arn,
                recording_group=CfnConfigurationRecorder.RecordingGroupProperty(
                    all_supported=True, include_global_resource_types=True        
                ))
        rec.add_depends_on(roleConfig)

        cfgDC = _config.CfnDeliveryChannel(self, 'aws-config',
            s3_bucket_name=bname, 
            config_snapshot_delivery_properties=CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty(
                delivery_frequency="Twelve_Hours"),
            name='aws-config')
        cfgDC.add_depends_on(bucketConfig)
