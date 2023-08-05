__copyright__ = "# Copyright (c) 2018 by cisco Systems, Inc. All rights reserved."
__author__ = "Sritej K V R <skanakad@cisco.com>"

from unicon.plugins.iosxr.settings import IOSXRSettings

class SpitfireSettings(IOSXRSettings):

    def __init__(self):
        super().__init__()
        self.HA_INIT_EXEC_COMMANDS = [
            'term length 0',
            'term width 0',
            'show version',
            'bash cat /etc/build-info.txt'
        ]
        self.ERROR_PATTERN = ['Invalid input detected at \'^\' marker']
        #self.HA_INIT_CONFIG_COMMANDS = []

