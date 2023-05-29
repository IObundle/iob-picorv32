#!/usr/bin/env python3

import os
import sys

from iob_module import iob_module
from setup import setup

# Submodules
from iob_reg import iob_reg


class iob_picorv32(iob_module):
    name='iob_picorv32'
    version='V0.10'
    flows=''
    setup_dir=os.path.dirname(__file__)

    @classmethod
    def _run_setup(cls):
        # Hardware headers & modules
        iob_reg.setup()

        # Verilog modules instances
        # TODO

        cls._setup_confs()
        cls._setup_ios()
        cls._setup_block_groups()

        # Setup core using LIB function
        setup(cls)


    def _setup_confs(cls):
        super()._setup_confs([
                # Macros

                # Parameters
                {'name':'ADDR_W', 'type':'P', 'val':'32', 'min':'1', 'max':'?', 'descr':'description here'},
                {'name':'DATA_W', 'type':'P', 'val':'32', 'min':'1', 'max':'?', 'descr':'description here'},
                {'name':'V_BIT', 'type':'P', 'val':'68', 'min':'1', 'max':'?', 'descr':'description here'},
                {'name':'E_BIT', 'type':'P', 'val':'67', 'min':'1', 'max':'?', 'descr':'description here'},
                {'name':'P_BIT', 'type':'P', 'val':'66', 'min':'1', 'max':'?', 'descr':'description here'},
                {'name':'USE_COMPRESSED', 'type':'P', 'val':'1', 'min':'0', 'max':'1', 'descr':'description here'},
                {'name':'USE_MUL_DIV', 'type':'P', 'val':'1', 'min':'0', 'max':'1', 'descr':'description here'},
                {'name':'USE_EXTMEM', 'type':'P', 'val':'0', 'min':'0', 'max':'1', 'descr':'Select if configured for usage with external memory.'},
            ])

    def _setup_ios(cls):
        cls.ios += [
            {'name': 'general', 'descr':'General interface signals', 'ports': [
                {'name':"clk", 'type':"I", 'n_bits':'1', 'descr':"CPU clock input"},
                {'name':"rst", 'type':"I", 'n_bits':'1', 'descr':"CPU reset input"},
                {'name':"boot", 'type':"I", 'n_bits':'1', 'descr':"CPU boot input"},
                {'name':"trap", 'type':"O", 'n_bits':'1', 'descr':"CPU trap output"},
            ]},
            {'name': 'instruction_bus', 'descr':'Instruction bus', 'ports': [
                {'name':"ibus_req", 'type':"O", 'n_bits':'`REQ_W', 'descr':"Instruction bus request"},
                {'name':"ibus_resp", 'type':"I", 'n_bits':'`RESP_W', 'descr':"Instruction bus response"},
            ]},
            {'name': 'data_bus', 'descr':'Data bus', 'ports': [
                {'name':"dbus_req", 'type':"O", 'n_bits':'`REQ_W', 'descr':"Data bus request"},
                {'name':"dbus_resp", 'type':"I", 'n_bits':'`RESP_W', 'descr':"Data bus response"},
            ]}
        ]

    def _setup_block_groups(cls):
        cls.block_groups += []
