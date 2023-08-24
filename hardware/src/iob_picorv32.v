/*
 *  IObPicoRV32 -- A PicoRV32 Wrapper
 *
 *  Copyright (C) 2020 IObundle <info@iobundle.com>
 *
 *  Permission to use, copy, modify, and/or distribute this software for any
 *  purpose with or without fee is hereby granted, provided that the above
 *  copyright notice and this permission notice appear in all copies.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 *  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 *  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 *  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 *  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 *  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 *  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 */


`timescale 1 ns / 1 ps
`include "iob_picorv32_conf.vh"
`include "iob_utils.vh"

module iob_picorv32 #(
  `include "iob_picorv32_params.vs"
   ) (
   `include "iob_picorv32_io.vs"
   );

   wire         cpu_instr;

   // cpu bus
   wire         cpu_avalid;
   wire [31:0]  cpu_address;
   wire [31:0]  cpu_wdata;
   wire [4-1:0] cpu_wstrb;
   wire [31:0]  cpu_rdata;
   wire         cpu_ready;

   // Output IOb bus
   wire         out_avalid;
   wire [31:0]  out_address;
   wire [31:0]  out_wdata;
   wire [4-1:0] out_wstrb;
   wire [31:0]  in_rdata;
   wire         in_rvalid;
   wire         in_ready;

   assign ibus_avalid_o  = cpu_instr? out_avalid : 1'b0;
   assign ibus_address_o = cpu_instr? out_address : 32'0;
   assign ibus_wdata_o   = cpu_instr? out_wdata : 32'h0;
   assign ibus_wstrb_o   = cpu_instr? out_wstrb : 4'h0;

   assign dbus_avalid_o  = !cpu_instr? out_avalid : 1'b0;
   assign dbus_address_o = !cpu_instr? out_address : 32'h0;
   assign dbus_wdata_o   = !cpu_instr? out_wdata : 32'h0;
   assign dbus_wstrb_o   = !cpu_instr? out_wstrb : 4'h0;

   assign out_avalid     = cpu_avalid & ~cpu_ready;
   assign out_address    = cpu_address;
   assign out_wdata      = cpu_wdata;
   assign out_wstrb      = cpu_wstrb;

   assign in_rdata       = cpu_instr? ibus_rdata : dbus_rdata;
   assign in_rvalid      = cpu_instr? ibus_rvalid : dbus_rvalid;
   assign in_ready       = cpu_instr? ibus_ready : dbus_ready;

   assign cpu_ready      = cpu_avalid & (in_rvalid | dbus_wack);

   // write acknowledge
   wire dbus_wack;
   wire dbus_wack_nxt = cpu_avalid & cpu_ready & (| cpu_wstrb) ;
   iob_reg_r #(
      .DATA_W (1),
      .RST_VAL(0)
   ) wack_reg (
      .clk_i(clk_i),
      .arst_i(rst_i),
      .cke_i(cke_i),
      .rst_i(cpu_ready),
      .d_i(dbus_wack_nxt),
      .q_o(dbus_wack)
   );


   //intantiate picorv32
   picorv32 #(
         .COMPRESSED_ISA(USE_COMPRESSED),
         .ENABLE_FAST_MUL(USE_MUL_DIV),
         .ENABLE_DIV(USE_MUL_DIV),
         .BARREL_SHIFTER(1),
         .PROGADDR_RESET(32'h 1000_0000)
         )
   picorv32_core (
      .clk           (clk_i),
      .resetn        (~rst_i),
      .trap          (trap_o),
      .mem_instr     (cpu_instr),

      //memory interface
      .mem_valid     (cpu_avalid),
      .mem_addr      (cpu_address),
      .mem_wdata     (cpu_wdata),
      .mem_wstrb     (cpu_wstrb),
      .mem_rdata     (cpu_rdata),
      .mem_ready     (cpu_ready),

      //lookahead interface
      .mem_la_read   (),
      .mem_la_write  (),
      .mem_la_addr   (),
      .mem_la_wdata  (),
      .mem_la_wstrb  (),

      //co-processor interface (PCPI)
      .pcpi_valid    (),
      .pcpi_insn     (),
      .pcpi_rs1      (),
      .pcpi_rs2      (),
      .pcpi_wr       (1'b0),
      .pcpi_rd       (32'd0),
      .pcpi_wait     (1'b0),
      .pcpi_ready    (1'b0),

      // IRQ
      .irq           (32'd0),
      .eoi           (),
      .trace_valid   (),
      .trace_data    ()
      );

endmodule
