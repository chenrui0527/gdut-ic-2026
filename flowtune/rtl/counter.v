// 4 位带使能的加法计数器：作为前端仿真和后端综合的示例设计
module counter (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       en,
    output reg  [3:0] q
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 4'd0;
        else if (en)
            q <= q + 4'd1;
    end
endmodule
