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
`include "iob_lib.vh"

//the look ahead interface is not working because mem_instr is unknown at request
//`define LA_IF

module iob_picorv32 
  (
   input         clk_i,
   input         rst_i,
   input         cke_i,
   output        trap,

   // instruction bus
   output        ibus_avalid,
   output        ibus_aready,
   output [31:0] ibus_address,
   input [31:0]  ibus_rdata,
   input         ibus_rvalid,

   // data bus
   output        dbus_avalid,
   output [31:0] dbus_address,
   output [31:0] dbus_wdata,
   output [3:0]  dbus_wstrb,
   input [31:0]  dbus_rdata,
   input         dbus_rvalid,
   input         dbus_ready
    );


   // cpu bus
   wire cpu_avalid;
   wire [31:0] cpu_address;
   wire [31:0] cpu_wdata;
   wire [3:0] cpu_wstrb;
   wire [31:0] cpu_rdata;
   wire cpu_ready;
   
   // write acknowledge
   wire dbus_wack;
   wire dbus_wack_nxt = cpu_avalid & cpu_ready & (| cpu_wstrb) ;
   iob_reg #(1,0) wack_reg 
     (
      .clk_i(clk_i),
      .rst_i(rst_i),
      .d_i(dbus_wack_nxt),
      .q_o(dbus_wack)
      );
      
   //split cpu bus into instruction and data buses
   wire   cpu_instr;
   assign ibus_avalid = cpu_avalid & cpu_instr;
   assign dbus_avalid = cpu_avalid & -cpu_instr;
   assign ibus_address = cpu_address;
   assign dbus_address = cpu_address;
   assign dbus_wdata = cpu_wdata;
   assign dbus_wstrb = cpu_wstrb;
   assign cpu_rdata = cpu_instr? ibus_rdata : dbus_rdata;
   assign cpu_ready = (ibus_rvalid | dbus_rvalid | iob_wack) & cpu_avalid;

   //intantiate picorv32
   picorv32 
     #(
       .COMPRESSED_ISA(1),
       .ENABLE_FAST_MUL(1),
       .ENABLE_DIV(1),
       .BARREL_SHIFTER(1),
       .PROGADDR_RESET(32'h 1000_0000)
       )
   picorv32_core 
     (
      .clk           (clk_i),
      .resetn        (~rst_i),
      .trap          (trap),
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
