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

//the look ahead interface is not working because mem_instr is unknown at request
//`define LA_IF

module iob_picorv32 #(
    `include "iob_picorv32_params.vs"
    ) (
    input               clk_i,
    input               rst_i,
    input               cke_i,
    input               boot_i,
    output              trap_o,

    // instruction bus
    output [`REQ_W-1:0] ibus_req_o,
    input [`RESP_W-1:0] ibus_resp_i,

    // data bus
    output [`REQ_W-1:0] dbus_req_o,
    input [`RESP_W-1:0] dbus_resp_i
    );

   localparam integer Vbit = `REQ_W-1;
   localparam integer AddrMsb = `REQ_W-2;

   //create picorv32 native interface concat buses
   wire [1*`REQ_W-1:0]  cpu_i_req;
   wire [1*`REQ_W-1:0]  cpu_d_req;
   wire [1*`REQ_W-1:0]  cpu_req;
   wire [1*`RESP_W-1:0] cpu_resp;
   wire                 cpu_i_addr_msb;
   wire                 cpu_d_addr_msb;
   wire                 cpu_instr;
   wire                 cpu_avalid;
   wire                 cpu_avalid_r;
   wire                 cpu_we_r;
   wire [`WSTRB_W-1:0]  cpu_wstrb;
   wire                 cpu_ack;
   wire                 iob_rvalid;
   wire                 iob_ready;
   wire                 iob_wack;
   wire                 iob_wack_nxt;

   //modify addresses if DDR used according to boot_i status
   generate
      if (USE_EXTMEM) begin: g_use_extmem
         assign cpu_i_addr_msb = ~boot_i;
         assign cpu_d_addr_msb = cpu_d_req[AddrMsb];
      end else begin: g_not_use_extmem
         assign cpu_i_addr_msb = 1'b0;
         assign cpu_d_addr_msb = 1'b0;
      end
   endgenerate
   assign ibus_req_o = {cpu_i_req[Vbit], cpu_i_addr_msb, cpu_i_req[AddrMsb-1:0]};
   assign dbus_req_o = {cpu_d_req[Vbit], cpu_d_addr_msb, cpu_d_req[AddrMsb-1:0]};

   //split cpu bus into instruction and data buses
   assign cpu_i_req = cpu_instr?  cpu_req : {`REQ_W{1'b0}};
   assign cpu_d_req = !cpu_instr? cpu_req : {`REQ_W{1'b0}};
   assign cpu_resp  = cpu_instr? ibus_resp_i: dbus_resp_i;

   assign cpu_req[`WSTRB(0)] = cpu_wstrb;
   assign iob_rvalid = cpu_resp[`RVALID(0)];
   assign iob_ready  = cpu_resp[`READY(0)];
   assign cpu_ack    = (iob_rvalid | iob_wack);
   assign iob_wack_nxt = cpu_avalid & (| cpu_wstrb) & iob_ready;

   iob_reg #(
      .DATA_W (1),
      .RST_VAL(1'b0)
   ) wack_reg (
      .clk_i (clk_i),
      .arst_i(rst_i),
      .cke_i (cke_i),
      .data_i(iob_wack_nxt),
      .data_o(iob_wack)
   );


   wire cpu_avalid_p;
   iob_edge_detect avalid_edge 
     (
      .clk_i (clk_i),
      .arst_i(rst_i),
      .cke_i (cke_i),
      .rst_i (1'b0),
      .bit_i (cpu_avalid & ~cpu_ack),
      .detected_o(cpu_avalid_p)
      );
   
   
`ifdef LA_IF
   wire mem_la_read, mem_la_write;
   always @(posedge clk_i) cpu_avalid <= mem_la_read | mem_la_write;
`else
   assign cpu_req[`AVALID(0)] = cpu_avalid_p;
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
                  .trap          (trap_o),
                  .mem_instr     (cpu_instr),
`ifndef LA_IF
                  //memory interface
                  .mem_valid     (cpu_avalid),
                  .mem_addr      (cpu_req[`ADDRESS(0, ADDR_W)]),
                  .mem_wdata     (cpu_req[`WDATA(0)]),
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
                  .mem_la_addr   (cpu_req[`ADDRESS(0, ADDR_W)]),
                  .mem_la_wdata  (cpu_req[`WDATA(0)]),
                  .mem_la_wstrb  (cpu_wstrb),
`endif
                  .mem_rdata     (cpu_resp[`RDATA(0)]),
                  .mem_ready     (cpu_ack),
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
