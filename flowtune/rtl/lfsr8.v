// 8 位线性反馈移位寄存器（LFSR）：时序逻辑，含异或反馈
module lfsr8 (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       en,
    output reg  [7:0] q
);
    wire fb = q[7] ^ q[5] ^ q[4] ^ q[3];
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)      q <= 8'h01;
        else if (en)     q <= {q[6:0], fb};
    end
endmodule
