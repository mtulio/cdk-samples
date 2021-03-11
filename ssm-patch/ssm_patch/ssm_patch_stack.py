from aws_cdk import core
from aws_cdk import (
    aws_ssm as _ssm
)


class SsmPatchStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ssm_ass = _ssm.CfnAssociation(
            self, 'InventoryAssociation',
            name='AWS-GatherSoftwareInventory',
            #document_version="$DEFAULT",
            association_name='InventoryAssociation',
            apply_only_at_cron_interval=False,
            schedule_expression="rate(30 minutes)",
            #compliance_severity="CRITICAL",
            targets=[
                _ssm.CfnAssociation.TargetProperty(
                    key='instanceids', values=['*']
                )
            ],
        )
        ssm_ass.add_override('Properties.Parameters.applications', ['Enabled'])
        ssm_ass.add_override('Properties.Parameters.awsComponents', ['Enabled'])
        ssm_ass.add_override('Properties.Parameters.billingInfo', ['Enabled'])
        ssm_ass.add_override('Properties.Parameters.customInventory', ['Enabled'])
        ssm_ass.add_override('Properties.Parameters.files', [''])
        ssm_ass.add_override('Properties.Parameters.instanceDetailedInformation', ['Enabled'])
        ssm_ass.add_override('Properties.Parameters.networkConfig', ['Enabled'])
        ssm_ass.add_override('Properties.Parameters.services', ['Enabled'])
        ssm_ass.add_override('Properties.Parameters.windowsRegistry', [''])
        ssm_ass.add_override('Properties.Parameters.windowsRoles', ['Enabled'])
        ssm_ass.add_override('Properties.Parameters.windowsUpdates', ['Enabled'])

        # Create association for Patch Baseline
        ssm_ass_patch = _ssm.CfnAssociation(
            self, 'PatchScanAssociation',
            name='AWS-RunPatchBaseline',
            #document_version="1",  # there is a bug when creating resource with this arg, to avoid err on creation it should be commented
            association_name='PatchScanAssociation',
            apply_only_at_cron_interval=False,
            schedule_expression="rate(30 minutes)",
            #compliance_severity="HIGH",
            targets=[
                 _ssm.CfnAssociation.TargetProperty(
                     key='InstanceIds', values=['*']
                )
            ],
            max_concurrency="1000",
            max_errors="1000"
        )
        ssm_ass_patch.add_override('Properties.Parameters.Operation', ['Scan'])
        ssm_ass_patch.add_override('Properties.Parameters.RebootOption', ['NoReboot'])
