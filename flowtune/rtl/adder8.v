// 8 位带进位的加法器：组合逻辑，用来观察不同配方对加法链的影响
module adder8 (
    input  wire [7:0] a,
    input  wire [7:0] b,
    input  wire       cin,
    output wire [7:0] s,
    output wire       cout
);
    assign {cout, s} = a + b + cin;
endmodule
