// ================================================================ //

// simple_counter_testbench.sv
// Description: this code implements a simple counter tesbench is system verilog.
// Authors: Luiz H. A. Santos
// Date: 01/08/2025

// ================================================================ //


// ================================================================ //
// Include other important files

`include "simple_counter_module.sv"

// ================================================================ //


// ================================================================ //
// Declares the testbench module

module simple_counter_testbench();

// Declares clock and reset signals to be used in the interface
logic clk;
logic rst;

// Clock generation: 10ns period (50MHz)
initial clk = 0;
always #5 clk = ~clk;

// Reset logic: active low, asserted for first 20ns
initial begin
    rst = 1;
    #20 rst = 0;
end

// Declares the interface, using the clk and reset signals
simple_counter_interface intfc(clk, rst);

// Instantiates the module
simple_counter_module counter_module(intfc.counter_module);

// Asserts the enable signal and monitors the module's output signals
initial begin
    // ✅ CORRETO: Usando modport do testbench para controlar sinais
    intfc.counter_testbench.enable_i = 1'b0;  // Inicia desabilitado
    
    // Aguarda reset ser liberado
    wait(rst == 0);
    #10;
    
    $display("🚀 Iniciando teste do contador...");
    
    // Habilita contador usando modport
    intfc.counter_testbench.enable_i = 1'b1;
    
    // Aguarda alguns ciclos
    repeat(20) @(posedge clk);
    
    // Desabilita contador
    intfc.counter_testbench.enable_i = 1'b0;
    
    repeat(5) @(posedge clk);
    
    // Reabilita para teste de overflow
    intfc.counter_testbench.enable_i = 1'b1;
    
    repeat(250) @(posedge clk);
    
    $display("✅ Teste completo!");
    $finish;
end

// Monitor usando modport para observar sinais
initial begin
    // ✅ CORRETO: Usando modport do testbench para ler sinais
    $monitor("Time: %6t | clk=%b | rst=%b | enable=%b | count=%3d | overflow=%b",
             $time, clk, rst, 
             intfc.counter_testbench.enable_i,      // Lendo via modport
             intfc.counter_testbench.count_value_o, // Lendo via modport  
             intfc.counter_testbench.overflow_o);   // Lendo via modport
end

endmodule

// ================================================================ //