`timescale 1 ns / 1 ps
`include "iob_picorv32_conf.vh"
`include "iob_utils.vh"

module iob_picorv32 #(
    `include "iob_picorv32_params.vs"
    ) (
    input               clk_i,
    input               arst_i,
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

   //picorv32 native interface wires
   wire                 cpu_instr;
   wire                 cpu_valid;
   wire [ADDR_W-1:0]    cpu_addr;
   wire [DATA_W/8-1:0]  cpu_wstrb;
   wire [DATA_W-1:0]    cpu_wdata;
   wire [DATA_W-1:0]    cpu_rdata;
   wire                 cpu_ready;

   //split cpu bus into ibus and dbus
   wire                 cpu_i_valid;   
   wire                 cpu_d_valid;
   wire                 cpu_d_valid_int;
   wire                 cpu_d_valid_posedge;

   //iob interface wires
   wire                 iob_i_rvalid;
   wire                 iob_d_rvalid;
   wire                 iob_rvalid;
   wire                 iob_ready;
   wire                 iob_wack;
   wire                 iob_wack_nxt;

   //compute the instruction bus request
   generate
      if (USE_EXTMEM) begin: g_use_extmem
         assign ibus_req_o = {cpu_i_valid, ~boot_i, cpu_addr[ADDR_W-2:0], 36'd0};
     end else begin: g_not_use_extmem
         assign ibus_req_o = {cpu_i_valid, cpu_addr, 36'd0};
      end
   endgenerate

   //compute the data bus request
   assign dbus_req_o = {cpu_d_valid_posedge, cpu_addr, cpu_wdata, cpu_wstrb};

   //split cpu bus into instruction and data buses
   assign cpu_i_valid = cpu_instr?  cpu_valid : 1'b0;
   assign cpu_d_valid = !cpu_instr? cpu_valid : 1'b0;

   
   //extract iob interface wires from concatenated buses
   assign iob_d_rvalid = dbus_resp_i[`RVALID(0)];
   assign iob_i_rvalid = ibus_resp_i[`RVALID(0)];
   assign iob_rvalid = iob_d_rvalid | iob_i_rvalid;
   assign iob_ready  = dbus_resp_i[`READY(0)];

   //cpu rdata and ready
   assign cpu_rdata = cpu_instr? ibus_resp_i[`RDATA(0)] : dbus_resp_i[`RDATA(0)];
   assign cpu_ready = cpu_instr? iob_i_rvalid : iob_d_rvalid|iob_wack;

   //compute data read/write ack
   assign iob_wack_nxt = cpu_valid & (| cpu_wstrb) & iob_ready;
   iob_reg #(
      .DATA_W (1),
      .RST_VAL(1'b0)
   ) wack_reg (
      .clk_i (clk_i),
      .arst_i(arst_i),
      .cke_i (cke_i),
      .data_i(iob_wack_nxt),
      .data_o(iob_wack)
   );

   //the CPU valid signal must be deasserted after the ready is asserted
   //otherwise it can't be used to read and write FIFOs
   assign cpu_d_valid_int = cpu_d_valid & iob_ready;
   iob_edge_detect #(
                     .EDGE_TYPE("rising"),
                     .OUT_TYPE ("pulse")
   ) mtxswrst_posedge_detect (
      .clk_i     (clk_i),
      .cke_i     (cke_i),
      .arst_i    (arst_i),
      .rst_i     (1'b0),
      .bit_i     (cpu_d_valid_int),
      .detected_o(cpu_d_valid_posedge)
   );

   //intantiate the PicoRV32 CPU
   picorv32 #(
              .COMPRESSED_ISA(USE_COMPRESSED),
              .ENABLE_FAST_MUL(USE_MUL_DIV),
              .ENABLE_DIV(USE_MUL_DIV),
              .BARREL_SHIFTER(1)
              )
   picorv32_core (
                  .clk           (clk_i),
                  .resetn        (~arst_i),
                  .trap          (trap_o),
                  .mem_instr     (cpu_instr),
                  //memory interface
                  .mem_valid     (cpu_valid),
                  .mem_addr      (cpu_addr),
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
