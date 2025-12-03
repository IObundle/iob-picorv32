# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    # Each generated cpu verilog module must have a unique name due to different python parameters (can't have two differnet verilog modules with same name).
    assert "name" in py_params_dict, print(
        "Error: Missing name for generated picorv32 module."
    )

    params = {
        "reset_addr": 0x00000000,
        "uncached_start_addr": 0x00000000,
        "uncached_size": 2**32,
        "include_cache": True,
    }

    # Update params with values from py_params_dict
    for param in py_params_dict:
        if param in params:
            params[param] = py_params_dict[param]

    attributes_dict = {
        "name": py_params_dict["name"],
        "generate_hw": True,
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "P",
                "val": 0,
                "min": 0,
                "max": 32,
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "P",
                "val": 0,
                "min": 0,
                "max": 32,
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "P",
                "val": 0,
                "min": 0,
                "max": 32,
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "P",
                "val": 0,
                "min": 0,
                "max": 4,
            },
            {
                "name": "USE_COMPRESSED",
                "type": "P",
                "val": "1",
                "min": "0",
                "max": "1",
                "descr": "Use compressed instructions",
            },
            {
                "name": "USE_MUL_DIV",
                "type": "P",
                "val": "1",
                "min": "0",
                "max": "1",
                "descr": "Use multiplication and division instructions",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "signals": {"type": "iob_clk"},
            },
            {
                "name": "rst_i",
                "descr": "Synchronous reset",
                "signals": [
                    {"name": "rst_i", "descr": "CPU synchronous reset", "width": 1},
                ],
            },
            {
                "name": "i_bus_m",
                "descr": "iob-picorv32 instruction bus",
                "signals": {
                    "type": "axi",
                    "prefix": "ibus_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
            {
                "name": "d_bus_m",
                "descr": "iob-picorv32 data bus",
                "signals": {
                    "type": "axi",
                    "prefix": "dbus_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
            {
                "name": "clint_cbus_s",
                "descr": "CLINT CSRs bus",
                "signals": {
                    "type": "iob",
                    "prefix": "clint_",
                    "ADDR_W": 16,
                },
            },
            {
                "name": "plic_cbus_s",
                "descr": "PLIC CSRs bus",
                "signals": {
                    "type": "iob",
                    "prefix": "plic_",
                    "ADDR_W": 22,
                },
            },
            {
                "name": "plic_interrupts_i",
                "descr": "PLIC interrupts",
                "signals": [
                    {
                        "name": "plic_interrupts_i",
                        "descr": "PLIC interrupts",
                        "width": 32,
                    },
                ],
            },
        ],
    }

    #
    # CPU wrapper body
    #
    attributes_dict |= {
        "wires": [
            {
                "name": "cpu_reset",
                "descr": "cpu reset signal",
                "signals": [
                    {"name": "cpu_reset", "width": "1"},
                ],
            },
            {
                "name": "i_bus",
                "signals": {
                    "type": "iob",
                    "file_prefix": "iob_picorv32_ibus_",
                    "prefix": "ibus_",
                    "DATA_W": "AXI_DATA_W",
                    "ADDR_W": "AXI_ADDR_W",
                },
                "descr": "iob-picorv32 instruction bus",
            },
            {
                "name": "d_bus",
                "signals": {
                    "type": "iob",
                    "file_prefix": "iob_picorv32_dbus_",
                    "prefix": "dbus_",
                    "DATA_W": "AXI_DATA_W",
                    "ADDR_W": "AXI_ADDR_W",
                },
                "descr": "iob-picorv32 data bus",
            },
            # Ready_received register wires
            {
                "name": "ready_received_reg_en_rst",
                "descr": "Enable and reset signal for ready_received_reg",
                "signals": [
                    {"name": "ready_received_reg_en", "width": 1},
                    {"name": "ready_received_reg_rst", "width": 1},
                ],
            },
            {
                "name": "ready_received_reg_data_i",
                "descr": "Input of ready_received_reg",
                "signals": [
                    {"name": "ready_received_reg_i", "width": 1},
                ],
            },
            {
                "name": "ready_received_reg_data_o",
                "descr": "Output of ready_received_reg",
                "signals": [
                    {"name": "ready_received_reg_o", "width": 1},
                ],
            },
            # CPU reset delayed register wires
            {
                "name": "cpu_reset_delayed_rst_i",
                "signals": [
                    {"name": "cpu_reset_delayed_rst_i", "width": 1},
                ],
            },
            {
                "name": "cpu_reset_delayed_data_i",
                "signals": [
                    {"name": "cpu_reset_delayed_data_i", "width": 2},
                ],
            },
            {
                "name": "cpu_reset_delayed_data_o",
                "signals": [
                    {"name": "cpu_reset_delayed_data_o", "width": 2},
                ],
            },
        ],
    }
    attributes_dict["subblocks"] = []
    if params["include_cache"]:
        # CPU ibus -> iob_split ----+-> iob2axi -+
        #                           |            |
        #                           v            |
        # CPU dbus -> iob_split +-> iob_cache ---+-> axi_merge -> memory
        #                       |                |
        #                       +-----> iob2axi -+
        attributes_dict["wires"] += [
            {
                "name": "cache_pipeline_signals",
                "signals": [
                    {"name": "ibus_araddr_ignore_bits", "width": 2},
                    {"name": "ibus_awaddr_ignore_bits", "width": 2},
                    {"name": "inside_io_region_ibus", "width": 1},
                    {"name": "inside_io_region_dbus", "width": 1},
                ],
            },
            # Split to cache
            {
                "name": "split2cache_ibus",
                "signals": {
                    "type": "iob",
                    "prefix": "split2cache_ibus_",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            {
                "name": "split2cache_dbus",
                "signals": {
                    "type": "iob",
                    "prefix": "split2cache_dbus_",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            # Split to iob2axi
            {
                "name": "split2axi_ibus",
                "signals": {
                    "type": "iob",
                    "prefix": "split2axi_ibus_",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            {
                "name": "split2axi_dbus",
                "signals": {
                    "type": "iob",
                    "prefix": "split2axi_dbus_",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            # iob2axi to merge
            {
                "name": "axi2merge_ibus",
                "signals": {
                    "type": "axi",
                    "prefix": "axi2merge_ibus_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
            {
                "name": "axi2merge_dbus",
                "signals": {
                    "type": "axi",
                    "prefix": "axi2merge_dbus_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
            # cache to merge
            {
                "name": "cache2merge",
                "signals": {
                    "type": "axi",
                    "prefix": "cache2merge_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
        ]
        attributes_dict["subblocks"] += [
            {
                "core_name": "iob_system_cache_system",
                "instance_name": "cache",
                "instance_description": "L1 and L2 caches",
                "parameters": {
                    "AXI_ADDR_W": "AXI_ADDR_W",
                    "AXI_DATA_W": "AXI_DATA_W",
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "i_bus_s": "split2cache_ibus",
                    "d_bus_s": "split2cache_dbus",
                    "axi_m": "cache2merge",
                },
            },
            {
                "core_name": "iob_split",
                "name": "picorv32_ibus_split",
                "instance_name": "ibus_split",
                "instance_description": "Split cached/uncached ibus requests",
                "addr_w": 33,  # Each manager has -1 address bit (32 bits each). Subordinate has 33 bits (32 address + 1 selector)
                "num_managers": 2,
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "reset_i": "rst_i",
                    "s_s": (
                        "i_bus",
                        [
                            "{inside_io_region_ibus, ibus_iob_addr}",
                        ],
                    ),
                    "m_0_m": "split2cache_ibus",
                    "m_1_m": "split2axi_ibus",
                },
            },
            {
                "core_name": "iob_split",
                "name": "picorv32_dbus_split",
                "instance_name": "dbus_split",
                "instance_description": "Split cached/uncached dbus requests",
                "addr_w": 33,  # Each manager has -1 address bit (32 bits each). Subordinate has 33 bits (32 address + 1 selector)
                "num_managers": 2,
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "reset_i": "rst_i",
                    "s_s": (
                        "d_bus",
                        [
                            "{inside_io_region_dbus, dbus_iob_addr}",
                        ],
                    ),
                    "m_0_m": "split2cache_dbus",
                    "m_1_m": "split2axi_dbus",
                },
            },
            {
                "core_name": "iob_axi_merge",
                "name": "iob_picorv32_axi_merge",
                "instance_name": "axi_merge",
                "instance_description": "Merge",
                "addr_w": 34,  # Each subordinate has -1 address bit (32 bits each). Manager has 34 bits (2 ignored).
                "lock_w": 1,
                "parameters": {
                    "ID_W": "AXI_ID_W",
                    "LEN_W": "AXI_LEN_W",
                },
                "num_subordinates": 3,
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "reset_i": "rst_i",
                    "s_0_s": "axi2merge_ibus",
                    "s_1_s": "axi2merge_dbus",
                    "s_2_s": "cache2merge",
                    "m_m": (
                        "i_bus_m",
                        [
                            # Ignore most significant address bits (we only use 32 bits)
                            "{ibus_araddr_ignore_bits, ibus_axi_araddr_o}",
                            "{ibus_awaddr_ignore_bits, ibus_axi_awaddr_o}",
                        ],
                    ),
                },
            },
        ]
    # IOb to AXI converters
    attributes_dict["subblocks"] += [
        {
            "core_name": "iob_iob2axi",
            "instance_name": "ibus_iob2axi",
            "instance_description": "Convert IOb instruction bus to AXI",
            "parameters": {
                "AXI_ID_W": "AXI_ID_W",
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_LOCK_W": 1,
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "iob_s": "i_bus",
                "axi_m": "i_bus_m",
            },
        },
        {
            "core_name": "iob_iob2axi",
            "instance_name": "dbus_iob2axi",
            "instance_description": "Convert IOb data bus to AXI",
            "parameters": {
                "AXI_ID_W": "AXI_ID_W",
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_LOCK_W": 1,
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "iob_s": "d_bus",
                "axi_m": "d_bus_m",
            },
        },
    ]
    if params["include_cache"]:
        # Replace connections of iob2axi converters
        attributes_dict["subblocks"][-2]["connect"]["iob_s"] = "split2axi_ibus"
        attributes_dict["subblocks"][-2]["connect"]["axi_m"] = "axi2merge_ibus"
        attributes_dict["subblocks"][-1]["connect"]["iob_s"] = "split2axi_dbus"
        attributes_dict["subblocks"][-1]["connect"]["axi_m"] = "axi2merge_dbus"
    attributes_dict["subblocks"] += [
        {
            "core_name": "iob_reg",
            "instance_name": "ready_received_re",
            "port_params": {
                "clk_en_rst_s": "c_a_r_e",
            },
            "parameters": {
                "DATA_W": 1,
                "RST_VAL": "1'b0",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "rst_i: ready_received_reg_rst",
                        "en_i: ready_received_reg_en",
                    ],
                ),
                "data_i": "ready_received_reg_data_i",
                "data_o": "ready_received_reg_data_o",
            },
        },
        {
            "core_name": "iob_reg",
            "instance_name": "cpu_reset_delayed_reg",
            "port_params": {
                "clk_en_rst_s": "c_a_r",
            },
            "parameters": {
                "DATA_W": 2,
                "RST_VAL": "2'b11",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "rst_i: cpu_reset_delayed_rst_i",
                    ],
                ),
                "data_i": "cpu_reset_delayed_data_i",
                "data_o": "cpu_reset_delayed_data_o",
            },
        },
    ]
    attributes_dict["snippets"] = [
        {
            "verilog_code": f"""
   //picorv32 native interface wires
   wire                cpu_instr;
   wire                cpu_valid;
   wire [  AXI_ADDR_W-1:0] cpu_word_addr;
   reg  [  AXI_ADDR_W-1:0] cpu_byte_addr;
   wire [AXI_DATA_W/8-1:0] cpu_wstrb;
   wire [AXI_DATA_W/8-1:0] cpu_rstrb;
   wire [  AXI_DATA_W-1:0] cpu_wdata;
   wire [  AXI_DATA_W-1:0] cpu_rdata;
   wire                cpu_ready;

   //split cpu bus into ibus and dbus
   wire                iob_i_valid;
   wire                iob_d_valid;

   //compute the instruction bus request
   assign ibus_iob_valid = iob_i_valid;
   assign ibus_iob_addr  = cpu_byte_addr;
   assign ibus_iob_wdata = {{AXI_DATA_W{{1'b0}}}};
   assign ibus_iob_wstrb = {{(AXI_DATA_W / 8) {{1'b0}}}};

   //compute the data bus request
   assign dbus_iob_valid = iob_d_valid;
   assign dbus_iob_addr  = cpu_byte_addr;
   assign dbus_iob_wdata = cpu_wdata;
   assign dbus_iob_wstrb = cpu_wstrb;

   //split cpu bus into instruction and data buses
   wire cpu_iob_valid;

   assign iob_i_valid      = cpu_instr & cpu_iob_valid;

   assign iob_d_valid      = (~cpu_instr) & cpu_iob_valid;

   //cpu rdata and ready
   assign cpu_rdata        = cpu_instr ? ibus_iob_rdata : dbus_iob_rdata;
   assign cpu_ready        = cpu_instr ? ibus_iob_rvalid : |cpu_wstrb ? dbus_iob_ready : dbus_iob_rvalid;

   assign cpu_reset = rst_i | arst_i;

   // When reading, iob_valid must be deasserted after receiving iob_ready while waiting for iob_rvalid
   assign cpu_iob_valid = cpu_valid & ~ready_received_reg_o;

   assign ready_received_reg_i = 1'b1;
   assign ready_received_reg_en = cpu_instr ? (ibus_iob_valid & ibus_iob_ready) : (dbus_iob_valid & ibus_iob_ready);
   assign ready_received_reg_rst = cpu_ready | cpu_reset_delayed_data_o[1];

   // Delay cpu reset by 2 clocks, since outputs of cpu are not stable on the first clocks after reset
   assign cpu_reset_delayed_rst_i = cpu_reset;
   assign cpu_reset_delayed_data_i = cpu_reset_delayed_data_o<<1;

   //intantiate the PicoRV32 CPU
   picorv32 #(
      .COMPRESSED_ISA (USE_COMPRESSED),
      .ENABLE_FAST_MUL(USE_MUL_DIV),
      .ENABLE_DIV     (USE_MUL_DIV),
      .BARREL_SHIFTER (1),
      .PROGADDR_RESET (32'h{params["reset_addr"]:x})
   ) picorv32_core (
      .clk         (clk_i),
      .resetn      (~cpu_reset),
      .trap        (),
      .mem_instr   (cpu_instr),
      //memory interface
      .mem_valid   (cpu_valid),
      .mem_addr    (cpu_word_addr),
      .mem_wdata   (cpu_wdata),
      .mem_wstrb   (cpu_wstrb),
      .mem_rstrb   (cpu_rstrb),
      .mem_rdata   (cpu_rdata),
      .mem_ready   (cpu_ready),
      //lookahead interface
      .mem_la_read (),
      .mem_la_write(),
      .mem_la_addr (),
      .mem_la_wdata(),
      .mem_la_wstrb(),
      .mem_la_rstrb(),
      //co-processor interface (PCPI)
      .pcpi_valid  (),
      .pcpi_insn   (),
      .pcpi_rs1    (),
      .pcpi_rs2    (),
      .pcpi_wr     (1'b0),
      .pcpi_rd     (32'd0),
      .pcpi_wait   (1'b0),
      .pcpi_ready  (1'b0),
      // IRQ
      .irq         (plic_interrupts_i),
      .eoi         (),
      .trace_valid (),
      .trace_data  ()
   );


// Connect unused CLINT interface to zero
assign clint_iob_rvalid_o = 1'b0;
assign clint_iob_rdata_o = 20'b0;
assign clint_iob_ready_o = 1'b0;
//clint_iob_valid_i,
//clint_iob_addr_i,
//clint_iob_wdata_i,
//clint_iob_wstrb_i

// Connect unused PLIC interface to zero
assign plic_iob_rvalid_o = 1'b0;
assign plic_iob_rdata_o = 14'b0;
assign plic_iob_ready_o = 1'b0;
//plic_iob_valid_i,
//plic_iob_addr_i,
//plic_iob_wdata_i,
//plic_iob_wstrb_i,

""" + """
// Convert word aligned address to byte aligned address
always @* begin
   // Higher bits of byte address are the same
   cpu_byte_addr = cpu_word_addr;

   if (|cpu_wstrb) begin
      if (cpu_wstrb[0]) cpu_byte_addr[1:0] = 2'b00; // Byte 0
      else if (cpu_wstrb[1]) cpu_byte_addr[1:0] = 2'b01; // Byte 1
      else if (cpu_wstrb[2]) cpu_byte_addr[1:0] = 2'b10; // Byte 2
      else if (cpu_wstrb[3]) cpu_byte_addr[1:0] = 2'b11; // Byte 3
   end else begin
      if (cpu_rstrb[0]) cpu_byte_addr[1:0] = 2'b00; // Byte 0
      else if (cpu_rstrb[1]) cpu_byte_addr[1:0] = 2'b01; // Byte 1
      else if (cpu_rstrb[2]) cpu_byte_addr[1:0] = 2'b10; // Byte 2
      else if (cpu_rstrb[3]) cpu_byte_addr[1:0] = 2'b11; // Byte 3
   end
end
"""

        }
    ]
    if params["include_cache"]:
        # Connect unused d_bus_m port to zero
        attributes_dict["snippets"] += [
            {
                "verilog_code": f"""
   assign inside_io_region_ibus = ibus_iob_addr >= 32'h{params["uncached_start_addr"]:x} && ibus_iob_addr <= 32'h{(params["uncached_start_addr"]+params["uncached_size"]-1):x};
   assign inside_io_region_dbus = dbus_iob_addr >= 32'h{params["uncached_start_addr"]:x} && dbus_iob_addr <= 32'h{(params["uncached_start_addr"]+params["uncached_size"]-1):x};
"""
                + """
   // Unused dbus output signals
   assign dbus_axi_araddr_o = {AXI_ADDR_W{1'b0}};
   assign dbus_axi_arvalid_o = 1'b0;
   assign dbus_axi_rready_o = 1'b0;
   assign dbus_axi_arid_o = {AXI_ID_W{1'b0}};
   assign dbus_axi_arlen_o = {AXI_LEN_W{1'b0}};
   assign dbus_axi_arsize_o = 3'b0;
   assign dbus_axi_arburst_o = 2'b0;
   assign dbus_axi_arlock_o = 1'b0;
   assign dbus_axi_arcache_o = 4'b0;
   assign dbus_axi_arqos_o = 4'b0;
   assign dbus_axi_awaddr_o = {AXI_ADDR_W{1'b0}};
   assign dbus_axi_awvalid_o = 1'b0;
   assign dbus_axi_wdata_o = {AXI_DATA_W{1'b0}};
   assign dbus_axi_wstrb_o = {AXI_DATA_W / 8{1'b0}};
   assign dbus_axi_wvalid_o = 1'b0;
   assign dbus_axi_bready_o = 1'b0;
   assign dbus_axi_awid_o = {AXI_ID_W{1'b0}};
   assign dbus_axi_awlen_o = {AXI_LEN_W{1'b0}};
   assign dbus_axi_awsize_o = 3'b0;
   assign dbus_axi_awburst_o = 2'b0;
   assign dbus_axi_awlock_o = 1'b0;
   assign dbus_axi_awcache_o = 4'b0;
   assign dbus_axi_awqos_o = 4'b0;
   assign dbus_axi_wlast_o = 1'b0;
"""
            }
        ]

    return attributes_dict
