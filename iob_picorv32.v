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

module iob_picorv32 
  (
   input               clk,
   input               rst,
   output              trap,

   // instruction bus
   output [`REQ_W-1:0] ibus_req,
   input [`RESP_W-1:0] ibus_resp,

   // data bus
   output [`REQ_W-1:0] dbus_req,
   input [`RESP_W-1:0] dbus_resp
   );

   //create picorv32 native interface cat bus
   wire [1*`REQ_W-1:0]                                  cpu_req;
   wire [1*`RESP_W-1:0]                                 cpu_resp;

   //handle look ahead interface
 `ifdef USE_LA_IF
   //manual connect 
   wire                                                 la_read;
   wire                                                 la_write;
   assign                                               cpu_req[`valid(0)] = la_read | la_write;
 `endif

   //picorv32 instruction select signal
   wire                                                 cpu_instr;

   
   //
   //SPLIT MASTER BUS IN INSTRUCTION AND DATA BUSES
   //
   split
     #(
       .N_SLAVES(2)
       )
     membus_demux
       (
        // master interface
        .m_req ({cpu_req[`valid(0)], cpu_instr, cpu_req[`REQ_W-3:0]}),
        .m_resp (cpu_resp[`resp(0)]),
        
        // slaves interface
        .s_req ({ibus_req[`req(0)], dbus_req[`req(0)]}),
        .s_resp({ibus_resp[`resp(0)], dbus_resp[`resp(0)]})
        );


   //intantiate picorv32
   picorv32 #(
              //.ENABLE_PCPI(1), //enables the following 2 parameters
	      .BARREL_SHIFTER(1),
	      .ENABLE_FAST_MUL(1),
	      .ENABLE_DIV(1)
	      )
   picorv32_core (
		  .clk           (clk),
		  .resetn        (~rst),
		  .trap          (trap),
		  //memory interface
		  .mem_instr     (cpu_instr),
		  .mem_rdata     (cpu_resp[`rdata(0)]),
		  .mem_ready     (cpu_resp[`ready(0)]),
 `ifndef USE_LA_IF
		  .mem_valid     (cpu_req[`valid(0)]),
		  .mem_addr      (cpu_req[`address(0,`ADDR_W, 0)]),
		  .mem_wdata     (cpu_req[`wdata(0)]),
		  .mem_wstrb     (cpu_req[`wstrb(0)]),
`else
                  .mem_la_read   (la_read),
                  .mem_la_write  (la_write),                  
                  .mem_la_addr   (cpu_req[`address(0,`ADDR_W, 0)]),
                  .mem_la_wdata  (cpu_req[`wdata(0)]),
                  .mem_la_wstrb  (cpu_req[`wstrb(0)]),
 `endif
                  // Pico Co-Processor PCPI
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
