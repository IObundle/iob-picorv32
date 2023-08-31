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
            {'name': 'general', 'descr':'General interface signals', 'ports': [
                {'name':"clk_i", 'type':"I", 'n_bits':'1', 'descr':"CPU clock input"},
                {'name':"cke_i", 'type':"I", 'n_bits':'1', 'descr':"CPU clock input"},
                {'name':"rst_i", 'type':"I", 'n_bits':'1', 'descr':"CPU reset input"},
                {'name':"boot_i", 'type':"I", 'n_bits':'1', 'descr':"CPU boot input"},
                {'name':"trap_o", 'type':"O", 'n_bits':'1', 'descr':"CPU trap output"},
            ]},
            {'name': 'instruction_bus', 'descr':'Instruction bus', 'ports': [
                {'name':"ibus_avalid_o",  'type':"O", 'n_bits':'1', 'descr':"Instruction bus avalid output"},
                {'name':"ibus_addr_o",    'type':"O", 'n_bits':'ADDR_W', 'descr':"Instruction bus address output"},
                {'name':"ibus_wdata_o",   'type':"O", 'n_bits':'DATA_W', 'descr':"Instruction bus wdata output"},
                {'name':"ibus_wstrb_o",   'type':"O", 'n_bits':'DATA_W/8', 'descr':"Instruction bus wstrb output"},
                {'name':"ibus_rdata_i",   'type':"I", 'n_bits':'DATA_W', 'descr':"Instruction bus rdata input"},
                {'name':"ibus_rvalid_i",  'type':"I", 'n_bits':'1', 'descr':"Instruction bus rvalid input"},
                {'name':"ibus_ready_i",   'type':"I", 'n_bits':'1', 'descr':"Instruction bus ready input"},
            ]},
            {'name': 'data_bus', 'descr':'Data bus', 'ports': [
                {'name':"dbus_avalid_o",  'type':"O", 'n_bits':'1', 'descr':"Data bus avalid output"},
                {'name':"dbus_addr_o",    'type':"O", 'n_bits':'ADDR_W', 'descr':"Data bus address output"},
                {'name':"dbus_wdata_o",   'type':"O", 'n_bits':'DATA_W', 'descr':"Data bus wdata output"},
                {'name':"dbus_wstrb_o",   'type':"O", 'n_bits':'DATA_W/8', 'descr':"Data bus wstrb output"},
                {'name':"dbus_rdata_i",   'type':"I", 'n_bits':'DATA_W', 'descr':"Data bus rdata input"},
                {'name':"dbus_rvalid_i",  'type':"I", 'n_bits':'1', 'descr':"Data bus rvalid input"},
                {'name':"dbus_ready_i",   'type':"I", 'n_bits':'1', 'descr':"Data bus ready input"},
            ]}
        ]

    @classmethod
    def _setup_block_groups(cls):
        cls.block_groups += []
