#!/usr/bin/env python3

import os, sys
sys.path.insert(0, os.getcwd()+'/submodules/LIB/scripts')
from setup import setup

top = 'iob_picorv32'
version = 'V0.10'

confs = \
[
    # Macros

    # Parameters
    {'name':'ADDR_W', 'type':'P', 'val':'32', 'min':'1', 'max':'?', 'descr':'description here'},
    {'name':'DATA_W', 'type':'P', 'val':'32', 'min':'1', 'max':'?', 'descr':'description here'},
    {'name':'V_BIT', 'type':'P', 'val':'`V_BIT', 'min':'1', 'max':'?', 'descr':'description here'},
    {'name':'E_BIT', 'type':'P', 'val':'`E_BIT', 'min':'1', 'max':'?', 'descr':'description here'},
    {'name':'P_BIT', 'type':'P', 'val':'`P_BIT', 'min':'1', 'max':'?', 'descr':'description here'},
    {'name':'USE_COMPRESSED', 'type':'P', 'val':'1', 'min':'0', 'max':'1', 'descr':'description here'},
    {'name':'USE_MUL_DIV', 'type':'P', 'val':'1', 'min':'0', 'max':'1', 'descr':'description here'},
]

ios = \
[
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

#regs = []

blocks = []

if __name__ == "__main__":
    setup(top, version, confs, ios, None, blocks)
