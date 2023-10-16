#!/usr/bin/env python3

import os

# Find python modules
if __name__ == "__main__":
    import sys

    sys.path.append("./submodules/LIB/scripts")
from iob_module import iob_module

if __name__ == "__main__":
    iob_module.find_modules()

# Submodules
from iob_reg import iob_reg


class iob_picorv32(iob_module):
    @classmethod
    def _init_attributes(cls):
        """Init module attributes"""
        cls.name = 'iob_picorv32'
        cls.version = 'V0.10'
        cls.flows = ''
        cls.setup_dir = os.path.dirname(__file__)
        cls.submodules = [
            iob_reg,
        ]

        cls.confs = [
            # Macros
            # Parameters
            {'name':'ADDR_W', 'type':'P', 'val':'32', 'min':'1', 'max':'?', 'descr':'description here'},
            {'name':'DATA_W', 'type':'P', 'val':'32', 'min':'1', 'max':'?', 'descr':'description here'},
            {'name':'USE_COMPRESSED', 'type':'P', 'val':'1', 'min':'0', 'max':'1', 'descr':'description here'},
            {'name':'USE_MUL_DIV', 'type':'P', 'val':'1', 'min':'0', 'max':'1', 'descr':'description here'},
            {'name':'USE_EXTMEM', 'type':'P', 'val':'0', 'min':'0', 'max':'1', 'descr':'Select if configured for usage with external memory.'},
        ]

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

        cls.block_groups += []


if __name__ == "__main__":
    iob_picorv32.setup_as_top_module()
