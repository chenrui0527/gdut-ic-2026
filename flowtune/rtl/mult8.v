// 8x8 位无符号乘法器：作为后端综合和配方搜索的第二个例子，规模比计数器大，不同配方差异更明显
module mult8 (
    input  wire [7:0] a,
    input  wire [7:0] b,
    output wire [15:0] p
);
    assign p = a * b;
endmodule
