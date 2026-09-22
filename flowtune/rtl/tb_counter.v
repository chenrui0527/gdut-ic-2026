// 测试平台（可选）：用 iverilog / verilator 这类仿真器跑波形时使用。
// 注意：本机没有安装仿真器，所以前端验证实际是用 flowtune/verify_equivalence.ys 里的
// 形式化等价性检查完成的（证明综合后的门级网表与这份 RTL 功能一致）。
// 以后装了 iverilog，可以用：iverilog -o tb_counter.vvp rtl/counter.v rtl/tb_counter.v && vvp tb_counter.vvp
module tb_counter;
    reg  clk = 0;
    reg  rst_n = 0;
    reg  en = 1;
    wire [3:0] q;
    reg  [3:0] cyc = 0;

    counter dut (.clk(clk), .rst_n(rst_n), .en(en), .q(q));

    always @(posedge clk) begin
        cyc <= cyc + 4'd1;
        if (cyc == 4'd1) rst_n <= 1'b1;   // 第二个周期后释放复位
        $display("cycle %0d: q = %0d", cyc, q);
    end
endmodule
