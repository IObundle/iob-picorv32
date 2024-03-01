#!/usr/bin/env python3

from dataclasses import dataclass

from iob_module import iob_module
from iob_reg import iob_reg
from iob_edge_detect import iob_edge_detect


@dataclass
class iob_picorv32(iob_module):
    version = 'V0.10'
    submodule_list = [
        iob_reg(),
        iob_edge_detect(),
    ]
    confs = [
        # Macros

        # Parameters
        {'name':'ADDR_W', 'type':'P', 'val':'32', 'min':'1', 'max':'?', 'descr':'description here'},
        {'name':'DATA_W', 'type':'P', 'val':'32', 'min':'1', 'max':'?', 'descr':'description here'},
        {'name':'USE_COMPRESSED', 'type':'P', 'val':'1', 'min':'0', 'max':'1', 'descr':'description here'},
        {'name':'USE_MUL_DIV', 'type':'P', 'val':'1', 'min':'0', 'max':'1', 'descr':'description here'},
        {'name':'USE_EXTMEM', 'type':'P', 'val':'0', 'min':'0', 'max':'1', 'descr':'Select if configured for usage with external memory.'},
    ]
    ios = [
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
                    'name':"boot",
                    'direction':"input",
                    'width':'1',
                    'descr':"CPU boot input"
                },
                {
                    'name':"trap",
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
                    'name':"ibus_req",
                    'direction':"output",
                    'width':'`REQ_W',
                    'descr':"Instruction bus request"},
                {
                    'name':"ibus_resp",
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
                    'name':"dbus_req",
                    'direction':"output",
                    'width':'`REQ_W',
                    'descr':"Data bus request"
                },
                {
                    'name':"dbus_resp",
                    'direction':"input",
                    'width':'`RESP_W',
                    'descr':"Data bus response"
                },
            ]}
    ]
    block_groups = []
