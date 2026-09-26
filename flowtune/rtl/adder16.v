// 16 位加法器：比 8 位加法器更大的组合逻辑，配方差异更明显
module adder16 (
    input  wire [15:0] a,
    input  wire [15:0] b,
    input  wire        cin,
    output wire [15:0] s,
    output wire        cout
);
    assign {cout, s} = a + b + cin;
endmodule
