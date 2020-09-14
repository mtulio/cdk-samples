#!/usr/bin/env python3

from aws_cdk import core

from ssm_patch.ssm_patch_stack import SsmPatchStack


app = core.App()
SsmPatchStack(app, "ssm-patch")

app.synth()
