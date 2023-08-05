from __future__ import absolute_import
from __future__ import print_function
import veriloggen
import thread_intrinsic_embedded_code

expected_verilog = """
module test;

  reg CLK;
  reg RST;
  wire [8-1:0] LED;

  blinkled
  uut
  (
    .CLK(CLK),
    .RST(RST),
    .LED(LED)
  );


  initial begin
    $dumpfile("uut.vcd");
    $dumpvars(0, uut);
  end


  initial begin
    CLK = 0;
    forever begin
      #5 CLK = !CLK;
    end
  end


  initial begin
    RST = 0;
    #100;
    RST = 1;
    #100;
    RST = 0;
    #10000;
    $finish;
  end


endmodule



module blinkled
(
  input CLK,
  input RST,
  output reg [8-1:0] LED
);

  reg a;
  reg b;
  reg [32-1:0] th_blink;
  localparam th_blink_init = 0;
  reg signed [32-1:0] _th_blink___0;
  localparam th_blink_1 = 1;
  localparam th_blink_2 = 2;
  localparam th_blink_3 = 3;
  localparam th_blink_4 = 4;
  localparam th_blink_5 = 5;
  localparam th_blink_6 = 6;
  localparam th_blink_7 = 7;
  localparam th_blink_8 = 8;

  always @(posedge CLK) begin
    if(RST) begin
      th_blink <= th_blink_init;
      _th_blink___0 <= 0;
      LED <= 0;
    end else begin
      case(th_blink)
        th_blink_init: begin
          th_blink <= th_blink_1;
        end
        th_blink_1: begin
          a <= 0;
          b <= 1;
          th_blink <= th_blink_2;
        end
        th_blink_2: begin
          _th_blink___0 <= 0;
          th_blink <= th_blink_3;
        end
        th_blink_3: begin
          if(_th_blink___0 < 10) begin
            th_blink <= th_blink_4;
          end else begin
            th_blink <= th_blink_7;
          end
        end
        th_blink_4: begin
          LED <= a;
          th_blink <= th_blink_5;
        end
        th_blink_5: begin
          a <= b;
          b <= a;
          th_blink <= th_blink_6;
        end
        th_blink_6: begin
          _th_blink___0 <= _th_blink___0 + 1;
          th_blink <= th_blink_3;
        end
        th_blink_7: begin
          $finish;
          th_blink <= th_blink_8;
        end
      endcase
    end
  end


endmodule
"""


def test():
    veriloggen.reset()
    test_module = thread_intrinsic_embedded_code.mkTest()
    code = test_module.to_verilog()

    from pyverilog.vparser.parser import VerilogParser
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
    parser = VerilogParser()
    expected_ast = parser.parse(expected_verilog)
    codegen = ASTCodeGenerator()
    expected_code = codegen.visit(expected_ast)

    assert(expected_code == code)
