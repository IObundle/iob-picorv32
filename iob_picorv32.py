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
        "subblocks": [
            # TODO: Add iob_cache and a way to bypass it for uncached memory region
            # {
            #     "core_name": "iob_system_cache_system",
            #     "instance_name": "cache",
            #     "instance_description": "L1 and L2 caches",
            #     "parameters": {
            #         "AXI_ADDR_W": "AXI_ADDR_W",
            #         "AXI_DATA_W": "AXI_DATA_W",
            #         "AXI_ID_W": "AXI_ID_W",
            #         "AXI_LEN_W": "AXI_LEN_W",
            #         "DDR_ADDR_W": 32, # do we need this?
            #         "FIRM_ADDR_W": 32, # do we need this?
            #     },
            #     "connect": {
            #         "clk_en_rst_s": "clk_en_rst_s",
            #         "i_bus_s": "i_bus",
            #         "d_bus_s": "d_bus",
            #         "axi_m": "d_bus_m",
            #     },
            # },
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
        ],
        "snippets": [
            {
                "verilog_code": f"""
   //picorv32 native interface wires
   wire                cpu_instr;
   wire                cpu_valid;
   wire [  AXI_ADDR_W-1:0] cpu_addr;
   wire [AXI_DATA_W/8-1:0] cpu_wstrb;
   wire [  AXI_DATA_W-1:0] cpu_wdata;
   wire [  AXI_DATA_W-1:0] cpu_rdata;
   wire                cpu_ready;

   //split cpu bus into ibus and dbus
   wire                iob_i_valid;
   wire                iob_d_valid;

   //compute the instruction bus request
   assign ibus_iob_valid = iob_i_valid;
   assign ibus_iob_addr  = cpu_addr;
   assign ibus_iob_wdata = {{AXI_DATA_W{{1'b0}}}};
   assign ibus_iob_wstrb = {{(AXI_DATA_W / 8) {{1'b0}}}};

   //compute the data bus request
   assign dbus_iob_valid = iob_d_valid;
   assign dbus_iob_addr  = cpu_addr;
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
      .mem_addr    (cpu_addr),
      .mem_wdata   (cpu_wdata),
      .mem_wstrb   (cpu_wstrb),
      .mem_rdata   (cpu_rdata),
      .mem_ready   (cpu_ready),
      //lookahead interface
      .mem_la_read (),
      .mem_la_write(),
      .mem_la_addr (),
      .mem_la_wdata(),
      .mem_la_wstrb(),
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

"""
            }
        ],
    }

    return attributes_dict
