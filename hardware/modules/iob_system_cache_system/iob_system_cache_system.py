# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# Cache system structure:
#
# ibus -> L1 cache -+
#                   +-> iob_merge -> L2 cache -> axi
# dbus -> L1 cache -+
#


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "Width of id signal in axi interface",
                "type": "P",
                "val": "32",
                "min": "0",
                "max": "NA",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "Width of len signal in axi interface",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "NA",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "Width of data bus in axi interface",
                "type": "P",
                "val": "32",
                "min": "0",
                "max": "NA",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "Width of address bus in axi interface",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "NA",
            },
            {
                "name": "FE_ADDR_W",
                "descr": "Front-end address width: defines the total memory space accessible via the cache, which must be a power of two.",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "64",
            },
            {
                "name": "FE_DATA_W",
                "descr": "Front-end data width: this parameter allows supporting processing elements with various data widths.",
                "type": "P",
                "val": "32",
                "min": "32",
                "max": "64",
            },
            {
                "name": "BE_ADDR_W",
                "descr": "Back-end address width: the value of this parameter must be equal or greater than FE_ADDR_W to match the width of the back-end interface, but the address space is still dictated by ADDR_W.",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "",
            },
            {
                "name": "BE_DATA_W",
                "descr": "Back-end data width: the value of this parameter must be an integer  multiple $k \\geq 1$ of DATA_W. If $k>1$, the memory controller can operate at a frequency higher than the cache's frequency. Typically, the memory controller has an asynchronous FIFO interface, so that it can sequentially process multiple commands received in parallel from the cache's back-end interface. ",
                "type": "P",
                "val": "32",
                "min": "32",
                "max": "256",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "signals": {
                    "type": "iob_clk",
                },
            },
            {
                "name": "i_bus_s",
                "descr": "Instruction bus",
                "signals": {
                    "type": "iob",
                    "prefix": "i_",
                    "ADDR_W": "FE_ADDR_W",
                    "DATA_W": "FE_DATA_W",
                },
            },
            {
                "name": "d_bus_s",
                "descr": "Data bus",
                "signals": {
                    "type": "iob",
                    "prefix": "d_",
                    "ADDR_W": "FE_ADDR_W",
                    "DATA_W": "FE_DATA_W",
                },
            },
            {
                "name": "axi_m",
                "descr": "AXI manager interface for external memory",
                "signals": {
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
        ],
    }
    attributes_dict["wires"] = [
        {
            "name": "ibus_cache_ie",
            "descr": "Cache invalidate and write-trough buffer IO chain",
            "signals": [
                {"name": "ibus_cache_invalidate_i", "width": 1},
                {"name": "ibus_cache_invalidate_o", "width": 1},
                {"name": "ibus_cache_wtb_empty_i", "width": 1},
                {"name": "ibus_cache_wtb_empty_o", "width": 1},
            ],
        },
        {
            "name": "dbus_cache_ie",
            "descr": "Cache invalidate and write-trough buffer IO chain",
            "signals": [
                {"name": "dbus_cache_invalidate_i", "width": 1},
                {"name": "dbus_cache_invalidate_o", "width": 1},
                {"name": "dbus_cache_wtb_empty_i", "width": 1},
                {"name": "dbus_cache_wtb_empty_o", "width": 1},
            ],
        },
        {
            "name": "l2_cache_ie",
            "descr": "Cache invalidate and write-trough buffer IO chain",
            "signals": [
                {"name": "l2_cache_invalidate_i", "width": 1},
                {"name": "l2_cache_invalidate_o", "width": 1},
                {"name": "l2_cache_wtb_empty_i", "width": 1},
                {"name": "l2_cache_wtb_empty_o", "width": 1},
            ],
        },
        {
            "name": "ibus2merge",
            "descr": "ibus cache to merge",
            "signals": {
                "type": "iob",
                "prefix": "ibus2merge_",
                "ADDR_W": "FE_ADDR_W",
                "DATA_W": "FE_DATA_W",
            },
        },
        {
            "name": "dbus2merge",
            "descr": "dbus cache to merge",
            "signals": {
                "type": "iob",
                "prefix": "dbus2merge_",
                "ADDR_W": "FE_ADDR_W",
                "DATA_W": "FE_DATA_W",
            },
        },
        {
            "name": "merge2l2",
            "descr": "merge to l2 cache",
            "signals": {
                "type": "iob",
                "prefix": "merge2l2_",
                "ADDR_W": "FE_ADDR_W",
                "DATA_W": "FE_DATA_W",
            },
        },
        {
            "name": "always_low",
            "descr": "Signals always low",
            "signals": [
                {"name": "always_low", "width": 1},
            ],
        },
        {
            "name": "internal_signals",
            "descr": "Internal signals",
            "signals": [
                {"name": "addr_ignore_bit", "width": 1},
                {"name": "invalidate", "width": 1},
            ],
        },
    ]
    attributes_dict["subblocks"] = [
        {
            "core_name": "iob_cache",
            "instance_name": "ibus_iob_cache",
            "instance_description": "Instruction cache",
            "be_if": "IOb",
            "parameters": {
                "FE_ADDR_W": "AXI_ADDR_W",
                "BE_ADDR_W": "AXI_ADDR_W",
                "NWAYS_W": "1",  # Number of ways
                "NLINES_W": "7",  # Cache Line Offset (number of lines)
                "WORD_OFFSET_W": "3",  # Word Offset (number of words per line)
                "WTBUF_DEPTH_W": "5",  # FIFO's depth -- 5 minimum for BRAM implementation
                "USE_CTRL": "0",  # Cache-Control can't be accessed
                "USE_CTRL_CNT": "0",  # Remove counters
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "iob_s": "i_bus_s",
                "iob_m": "ibus2merge",
                "ie_io": "ibus_cache_ie",
            },
        },
        {
            "core_name": "iob_cache",
            "instance_name": "dbus_iob_cache",
            "instance_description": "Data cache",
            "be_if": "IOb",
            "parameters": {
                "FE_ADDR_W": "AXI_ADDR_W",
                "BE_ADDR_W": "AXI_ADDR_W",
                "NWAYS_W": "1",  # Number of ways
                "NLINES_W": "7",  # Cache Line Offset (number of lines)
                "WORD_OFFSET_W": "3",  # Word Offset (number of words per line)
                "WTBUF_DEPTH_W": "5",  # FIFO's depth -- 5 minimum for BRAM implementation
                "USE_CTRL": "0",  # Cache-Control can't be accessed
                "USE_CTRL_CNT": "0",  # Remove counters
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "iob_s": "d_bus_s",
                "iob_m": "dbus2merge",
                "ie_io": "dbus_cache_ie",
            },
        },
        {
            "core_name": "iob_cache",
            "instance_name": "l2_iob_cache",
            "instance_description": "L2 cache",
            "be_if": "AXI4",
            "parameters": {
                "FE_ADDR_W": "AXI_ADDR_W",
                "BE_ADDR_W": "AXI_ADDR_W",
                "BE_DATA_W": "AXI_DATA_W",
                "AXI_ID_W": "AXI_ID_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "NWAYS_W": "2",  # Number of ways
                "NLINES_W": "7",  # Cache Line Offset (number of lines)
                "WORD_OFFSET_W": "3",  # Word Offset (number of words per line)
                "WTBUF_DEPTH_W": "5",  # FIFO's depth -- 5 minimum for BRAM implementation
                "USE_CTRL": "0",  # Cache-Control can't be accessed
                "USE_CTRL_CNT": "0",  # Remove counters
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "iob_s": "merge2l2",
                "axi_m": "axi_m",
                "ie_io": "l2_cache_ie",
            },
        },
        {
            "core_name": "iob_merge",
            "name": "system_cache_merge",
            "instance_name": "ibus_dbus_merge",
            "addr_w": 33,  # Each subordinate has -1 address bit (32 bits each). Manager has 33 bits (1 ignored).
            "num_subordinates": 2,
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "reset_i": "always_low",
                "s_0_s": "ibus2merge",
                "s_1_s": "dbus2merge",
                "m_m": (
                    "merge2l2",
                    [
                        # Ignore most significant address bit (we only use 32 bits)
                        "{addr_ignore_bit, merge2l2_iob_addr}",
                    ],
                ),
            },
        },
    ]
    #
    # Combinatorial
    #
    attributes_dict["comb"] = {
        "code": """
   always_low = 1'b0;

   ibus_cache_invalidate_i = 1'b0;
   ibus_cache_wtb_empty_i = 1'b1;

   dbus_cache_invalidate_i = 1'b0;
   dbus_cache_wtb_empty_i = l2_cache_wtb_empty_o;

   l2_cache_invalidate_i = invalidate & ~merge2l2_iob_valid;
   l2_cache_wtb_empty_i = 1'b1;

   //Necessary logic to avoid invalidating L2 while it's being accessed by a request
   invalidate_nxt = 1'b1;
   invalidate_en = dbus_cache_invalidate_o;
   invalidate_rst = ~merge2l2_iob_valid;
"""
    }

    return attributes_dict
