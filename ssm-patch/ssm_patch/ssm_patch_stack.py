from aws_cdk import core
from aws_cdk import (
    aws_ssm as _ssm
)


class SsmPatchStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 1 - setup SSM association
        ssm_ass = _ssm.CfnAssociation(
            self, 'inventory-all-instances',
            name='AWS-GatherSoftwareInventory',
            #document_version="1",  # there is a bug when creating resource with this arg, to avoid err on creation it should be commented
            association_name='inventory-all-instances',
            apply_only_at_cron_interval=False,
            schedule_expression="rate(30 minutes)",
            #compliance_severity="CRITICAL",
            targets=[
                 _ssm.CfnAssociation.TargetProperty(
                     key='InstanceIds', values=['*']
                )
            ]
        )
        # Workarround to apply Parameters values
        ## Ref https://github.com/aws/aws-cdk/issues/4057
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
        ssm_assPatch = _ssm.CfnAssociation(
            self, 'patch-scan-all-instances',
            name='AWS-RunPatchBaseline',
            #document_version="1",  # there is a bug when creating resource with this arg, to avoid err on creation it should be commented
            association_name='patch-scan-all-instances',
            apply_only_at_cron_interval=False,
            #schedule_expression="rate(720 minutes)",
            compliance_severity="HIGH",
            targets=[
                 _ssm.CfnAssociation.TargetProperty(
                     key='InstanceIds', values=['*']
                )
            ],
            max_concurrency="1000",
            max_errors="1000"
        )
        ssm_assPatch.add_override('Properties.Parameters.Operation', ['Scan'])
        ssm_assPatch.add_override('Properties.Parameters.RebootOption', ['NoReboot'])


        # # 2 - create maintenance window
        # # 3 - configure patching
        # # 3.1 - Configure patching group (como fazer via API?)
        # #> Select patch group: linux, windows
        # #> select schedule: every 6 hours
        # #> select operation: scan only

        # #classaws_cdk.aws_ssm.CfnMaintenanceWindow(scope, id, *, 
        # # allow_unassociated_targets, cutoff, duration, name, schedule, 
        # # description=None, end_date=None, schedule_offset=None, 
        # # schedule_timezone=None, start_date=None, tags=None)
        # ssm_win = _ssm.CfnMaintenanceWindow(

        # )

        # # classaws_cdk.aws_ssm.CfnMaintenanceWindowTarget(scope, id, *,
        # #  resource_type, targets, window_id, description=None, name=None, 
        # # owner_information=None)
        # ssm_winTg = _ssm.CfnMaintenanceWindowTarget(

        # )

        # # # classaws_cdk.aws_ssm.CfnMaintenanceWindowTask(scope, id, *, 
        # # # max_concurrency, max_errors, priority, targets, 
        # # # task_arn, task_type, window_id, description=None, 
        # # # logging_info=None, name=None, service_role_arn=None, 
        # # # task_invocation_parameters=None, task_parameters=None)
        # # ssm_winTk = _ssm.CfnMaintenanceWindowTask(

        # # )

        # classaws_cdk.aws_ssm.CfnPatchBaseline(scope, id, *, name, 
        # approval_rules=None, approved_patches=None, 
        # approved_patches_compliance_level=None, 
        # approved_patches_enable_non_security=None, description=None, 
        # global_filters=None, operating_system=None, patch_groups=None, 
        # rejected_patches=None, rejected_patches_action=None, 
        # sources=None, tags=None)
        # ssm_win = _ssm.CfnPatchBaseline(

        # )
