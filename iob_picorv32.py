#!/usr/bin/env python3

import os

from iob_module import iob_module

# Submodules
from iob_reg import iob_reg


class iob_picorv32(iob_module):
    name = 'iob_picorv32'
    version = 'V0.10'
    flows = ''
    setup_dir = os.path.dirname(__file__)

    @classmethod
    def _create_submodules_list(cls):
        ''' Create submodules list with dependencies of this module
        '''
        super()._create_submodules_list([
            iob_reg,
        ])

    @classmethod
    def _setup_confs(cls):
        super()._setup_confs([
                # Macros

                # Parameters
                {'name':'ADDR_W', 'type':'P', 'val':'32', 'min':'1', 'max':'?', 'descr':'description here'},
                {'name':'DATA_W', 'type':'P', 'val':'32', 'min':'1', 'max':'?', 'descr':'description here'},
                {'name':'USE_COMPRESSED', 'type':'P', 'val':'1', 'min':'0', 'max':'1', 'descr':'description here'},
                {'name':'USE_MUL_DIV', 'type':'P', 'val':'1', 'min':'0', 'max':'1', 'descr':'description here'},
                {'name':'USE_EXTMEM', 'type':'P', 'val':'0', 'min':'0', 'max':'1', 'descr':'Select if configured for usage with external memory.'},
            ])

    @classmethod
    def _setup_ios(cls):
        cls.ios += [
            {
                "name": "clk_rst",
                "type": "slave",
                "port_prefix": "",
                "wire_prefix": "",
                "descr": "Clock and reset",
                "ports": [],
            },
            {
                'name': 'general',
                "type": "master",
                "port_prefix": "",
                "wire_prefix": "",
                'descr':'General interface signals',
                'ports': [
                    {
                        'name':"boot_i",
                        'direction':"input",
                        'width':'1',
                        'descr':"CPU boot input"
                    },
                    {
                        'name':"trap_o",
                        'direction':"output",
                        'width':'1',
                        'descr':"CPU trap output"
                    },
                ]},
            {
                'name': 'instruction_bus',
                "type": "master",
                "port_prefix": "",
                "wire_prefix": "",
                'descr':'Instruction bus',
                'ports': [
                    {
                        'name':"ibus_req_o",
                        'direction':"output",
                        'width':'`REQ_W',
                        'descr':"Instruction bus request"},
                    {
                        'name':"ibus_resp_i",
                        'direction':"input",
                        'width':'`RESP_W',
                        'descr':"Instruction bus response"
                    },
                ]},
            {
                'name': 'data_bus',
                "type": "master",
                "port_prefix": "",
                "wire_prefix": "",
                'descr':'Data bus',
                'ports': [
                    {
                        'name':"dbus_req_o",
                        'direction':"output",
                        'width':'`REQ_W',
                        'descr':"Data bus request"
                    },
                    {
                        'name':"dbus_resp_i",
                        'direction':"input",
                        'width':'`RESP_W',
                        'descr':"Data bus response"
                    },
                ]}
        ]

    @classmethod
    def _setup_block_groups(cls):
        cls.block_groups += []
