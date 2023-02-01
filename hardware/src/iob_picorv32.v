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

module iob_picorv32 #(
    `include "iob_picorv32_params.vh"
    ) (
    input               clk_i,
    input               rst_i,
    input               cke_i,
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
   generate
      if (RUN_EXTMEM) begin
         assign ibus_req = {cpu_i_req[V_BIT], ~boot, cpu_i_req[`REQ_W-3:0]};
         assign dbus_req = {cpu_d_req[V_BIT], (cpu_d_req[E_BIT]^~boot)&~cpu_d_req[P_BIT], cpu_d_req[`REQ_W-3:0]};
      end else begin
         assign ibus_req = cpu_i_req;
         assign dbus_req = cpu_d_req;
      end
   endgenerate

   //split cpu bus into instruction and data buses
   wire   cpu_instr;
   assign cpu_i_req = cpu_instr?  cpu_req : {`REQ_W{1'b0}};
   assign cpu_d_req = !cpu_instr? cpu_req : {`REQ_W{1'b0}};
   assign cpu_resp = cpu_instr? ibus_resp: dbus_resp;
   
   reg iob_wack;
   wire cpu_avalid;
   wire [`WSTRB_W-1:0] cpu_wstrb;
   assign cpu_req[`wstrb(0)] = cpu_wstrb;
   wire iob_rvalid = cpu_resp[`rvalid(0)];
   wire iob_ready  = cpu_resp[`ready(0)];
   wire cpu_ready  = (iob_rvalid | iob_wack) & cpu_avalid;

   wire iob_wack_nxt = cpu_avalid & (| cpu_wstrb) & iob_ready;
   iob_reg #(1,0) wack_reg (clk_i, rst_i, cke_i, iob_wack_nxt, iob_wack);

`ifdef LA_IF
   wire mem_la_read, mem_la_write;
   always @(posedge clk_i) cpu_avalid <= mem_la_read | mem_la_write;
`else
   assign cpu_req[`avalid(0)] = cpu_avalid & ~cpu_ready;
`endif
   

   //intantiate picorv32
   picorv32 #(
              .COMPRESSED_ISA(USE_COMPRESSED),
              .ENABLE_FAST_MUL(USE_MUL_DIV),
              .ENABLE_DIV(USE_MUL_DIV),
              .BARREL_SHIFTER(1)
              )
   picorv32_core (
                  .clk           (clk_i),
                  .resetn        (~rst_i),
                  .trap          (trap),
                  .mem_instr     (cpu_instr),
`ifndef LA_IF
                  //memory interface
                  .mem_valid     (cpu_avalid),
                  .mem_addr      (cpu_req[`address(0, ADDR_W)]),
                  .mem_wdata     (cpu_req[`wdata(0)]),
                  .mem_wstrb     (cpu_wstrb),
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
                  .mem_la_addr   (cpu_req[`address(0, ADDR_W)]),
                  .mem_la_wdata  (cpu_req[`wdata(0)]),
                  .mem_la_wstrb  (cpu_wstrb),
`endif
                  .mem_rdata     (cpu_resp[`rdata(0)]),
                  .mem_ready     (cpu_ready),
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
