#!/usr/bin/env python3

from aws_cdk import core

from config_delivery_channel.config_delivery_channel_stack import ConfigDeliveryChannelStack


app = core.App()
ConfigDeliveryChannelStack(app, "config-delivery-channel")

app.synth()
