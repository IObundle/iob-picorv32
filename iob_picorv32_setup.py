#!/usr/bin/env python3

import os, sys
sys.path.insert(0, os.getcwd()+'/submodules/LIB/scripts')
from setup import setup

meta = \
{
'name':'iob_picorv32',
'version':'V0.10',
'flows':''
}

dirs = {
'setup':os.path.dirname(__file__),
'build':f"../{meta['name']+'_'+meta['version']}",
}

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

lib_srcs = {
    'hw_setup': {
        'v_headers' : [  ],
        'hw_modules': [ 'iob_reg_a.v' ]
    },
}

# Main function to setup this core and its components
# Gen_tex and gen_makefile are created by default. However, when this system is a submodule of another, we don't want these files of this system.
# dirs_override: allows overriding some directories. This is useful when a top system wants to override the default build directory of this system.
def main(dirs_override={}, gen_tex=True, gen_makefile=True):
    #Override dirs
    dirs.update(dirs_override)
    # Setup this system
    setup(meta, confs, ios, None, blocks, lib_srcs, dirs=dirs, gen_tex=gen_tex, gen_makefile=gen_makefile)

if __name__ == "__main__":
    main()
