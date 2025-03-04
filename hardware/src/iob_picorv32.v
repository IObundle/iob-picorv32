`timescale 1 ns / 1 ps
`include "iob_picorv32_conf.vh"
`include "iob_utils.vh"

module iob_picorv32 #(
   `include "iob_picorv32_params.vs"
) (
   input  clk_i,
   input  arst_i,
   input  cke_i,
   input  boot_i,
   output trap_o,

   // instruction bus
   output [ `REQ_W-1:0] ibus_req_o,
   input  [`RESP_W-1:0] ibus_resp_i,

   // data bus
   output [ `REQ_W-1:0] dbus_req_o,
   input  [`RESP_W-1:0] dbus_resp_i
);

   //picorv32 native interface wires
   wire                cpu_instr;
   wire                cpu_valid;
   wire [  ADDR_W-1:0] cpu_addr;
   wire [DATA_W/8-1:0] cpu_wstrb;
   wire [  DATA_W-1:0] cpu_wdata;
   wire [  DATA_W-1:0] cpu_rdata;
   wire                cpu_ready;
   wire                cpu_rready;
   assign              cpu_rready = 1'b1;

   //split cpu bus into ibus and dbus
   wire                iob_i_valid;
   wire                 iob_d_valid;

   //iob interface wires
   wire                iob_i_rvalid;
   wire                iob_d_rvalid;
   wire                iob_d_ready;

   //compute the instruction bus request
   generate
      if (USE_EXTMEM) begin : g_use_extmem
         assign ibus_req_o = {cpu_rready, iob_i_valid, ~boot_i, cpu_addr[ADDR_W-2:0], 36'd0};
      end else begin : g_not_use_extmem
         assign ibus_req_o = {cpu_rready, iob_i_valid, cpu_addr, 36'd0};
      end
   endgenerate

   //compute the data bus request
   assign dbus_req_o   = {cpu_rready, iob_d_valid, cpu_addr, cpu_wdata, cpu_wstrb};

   //split cpu bus into instruction and data buses
   assign iob_i_valid  = cpu_instr & cpu_valid;

   assign iob_d_valid  = (~cpu_instr) & cpu_valid & (~iob_d_rvalid);

   //extract iob interface wires from concatenated buses
   assign iob_d_rvalid = dbus_resp_i[`RVALID(0)];
   assign iob_i_rvalid = ibus_resp_i[`RVALID(0)];
   assign iob_d_ready    = dbus_resp_i[`READY(0)];

   //cpu rdata and ready
   assign cpu_rdata    = cpu_instr ? ibus_resp_i[`RDATA(0)] : dbus_resp_i[`RDATA(0)];
   assign cpu_ready    = cpu_instr ? iob_i_rvalid : |cpu_wstrb? iob_d_ready : iob_d_rvalid;

   //intantiate the PicoRV32 CPU
   picorv32 #(
      .COMPRESSED_ISA (USE_COMPRESSED),
      .ENABLE_FAST_MUL(USE_MUL_DIV),
      .ENABLE_DIV     (USE_MUL_DIV),
      .BARREL_SHIFTER (1)
   ) picorv32_core (
      .clk         (clk_i),
      .resetn      (~arst_i),
      .trap        (trap_o),
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
      .irq         (32'd0),
      .eoi         (),
      .trace_valid (),
      .trace_data  ()
   );

endmodule
