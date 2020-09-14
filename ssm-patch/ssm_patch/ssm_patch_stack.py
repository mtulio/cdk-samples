from aws_cdk import core
from aws_cdk import (
    aws_ssm as _ssm
)


class SsmPatchStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 1 - setup SSM association
        # aws ssm create-association --name "AWS-GatherSoftwareInventory" --targets "Key=instanceids,Values=*"
        ssm_ass = _ssm.CfnAssociation(
            self, 'inventory-all-instances',
            name='AWS-GatherSoftwareInventory',
            document_version="$DEFAULT",
            association_name='inventory-all-instances',
            #apply_only_at_cron_interval=True,
            schedule_expression="rate(30 minutes)",
            compliance_severity="CRITICAL",
            targets=[
                 _ssm.CfnAssociation.TargetProperty(
                     key='instanceids', values=['*']
                )
            ],
            parameters={"applications": "Enabled"}
        )
            # parameters=[
            #     {
            #         "applications": "Enabled",
            #         "awsComponents": "Enabled",
            #         "billingInfo": "Enabled",
            #         "customInventory": "Enabled",
            #         "files": "-",
            #         "instanceDetailedInformation": "Enabled",
            #         "services": "Enabled",
            #         "windowsRegistry": "Enabled",
            #         "windowsRoles": "Enabled",
            #         "windowsUpdates": "Enabled"
            #     }
            # ]

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
