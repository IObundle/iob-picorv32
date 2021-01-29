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
`include "system.vh"
`include "interconnect.vh"

//the look ahead interface is not working because mem_instr is unknown at request
//`define LA_IF

module iob_picorv32 
  #(
    parameter ADDR_W=32,
    parameter DATA_W=32
    )
   (
    input               clk,
    input               rst,
    input               boot,
    output              trap,

    // instruction bus
    output [`REQ_W-1:0] ibus_req,
    input [`RESP_W-1:0] ibus_resp,

    // data bus
    output [`REQ_W-1:0] dbus_req,
    input [`RESP_W-1:0] dbus_resp
    );

   //create picorv32 native interface concat buses
   wire [1*`REQ_W-1:0]  cpu_req, cpu_i_req, cpu_d_req;
   wire [1*`RESP_W-1:0] cpu_resp;

   //modify addresses if DDR used according to boot status
`ifdef RUN_DDR_USE_SRAM
   assign ibus_req = {cpu_i_req[`V_BIT], ~boot, cpu_i_req[`REQ_W-3:0]};
   assign dbus_req = {cpu_d_req[`V_BIT], (cpu_d_req[`E_BIT]^~boot)&~cpu_d_req[`P_BIT], cpu_d_req[`REQ_W-3:0]};
`else
   assign ibus_req = cpu_i_req;
   assign dbus_req = cpu_d_req;
`endif

   //split cpu bus into instruction and data buses
   wire                 cpu_instr;
   assign cpu_i_req = cpu_instr?  cpu_req : {`REQ_W{1'b0}};
   assign cpu_d_req = !cpu_instr? cpu_req : {`REQ_W{1'b0}};
   assign cpu_resp = cpu_instr? ibus_resp: dbus_resp;
   
   wire                 cpu_valid;
   wire                 cpu_ready = cpu_resp[`ready(0)];
   
`ifdef LA_IF
   wire                 mem_la_read, mem_la_write;
   always @(posedge clk) cpu_valid <= mem_la_read | mem_la_write;
`else
   wire                 cpu_valid_int;
   reg                  cpu_valid_reg;
   assign cpu_req[`valid(0)] = cpu_valid & ~cpu_ready;
`endif
   

   //intantiate picorv32
   picorv32 #(
`ifdef USE_COMPRESSED
              .COMPRESSED_ISA(1),
`endif
              //.ENABLE_PCPI(1), //enables the following 2 parameters
              .BARREL_SHIFTER(1),
              .ENABLE_FAST_MUL(1),
              .ENABLE_DIV(1)
              )
   picorv32_core (
                  .clk           (clk),
                  .resetn        (~rst),
                  .trap          (trap),
                  .mem_instr     (cpu_instr),
`ifndef LA_IF
                  //memory interface
                  .mem_valid     (cpu_valid),
                  .mem_addr      (cpu_req[`address(0, `ADDR_W)]),
                  .mem_wdata     (cpu_req[`wdata(0)]),
                  .mem_wstrb     (cpu_req[`wstrb(0)]),
                  //lookahead interface
                  .mem_la_read   (),
                  .mem_la_write  (),
                  .mem_la_addr   (),
                  .mem_la_wdata  (),
                  .mem_la_wstrb  (),
`else
                  //memory interface
                  .mem_valid     (),
                  .mem_addr      (),
                  .mem_wdata     (),
                  .mem_wstrb     (),
                  //lookahead interface
                  .mem_la_read   (mem_la_read),
                  .mem_la_write  (mem_la_write),
                  .mem_la_addr   (cpu_req[`address(0, `ADDR_W)]),
                  .mem_la_wdata  (cpu_req[`wdata(0)]),
                  .mem_la_wstrb  (cpu_req[`wstrb(0)]),
`endif
                  .mem_rdata     (cpu_resp[`rdata(0)]),
                  .mem_ready     (cpu_resp[`ready(0)]),
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
