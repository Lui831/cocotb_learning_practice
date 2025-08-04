// ================================================================ //

// simple_counter_module.sv
// Description: this code implements a simple counter in system verilog.
// Authors: Luiz H. A. Santos
// Date: 01/08/2025

// ================================================================ //


// ================================================================ //
// Include interface from other file

`include "simple_counter_interface.sv"

// ================================================================ //


// ================================================================ //
// Module declaration

module simple_counter_module(simple_counter_interface.counter_module intfc);

    // Count process with enable, output and other signals
    always_ff @(posedge intfc.clk_i) begin

        // If the rst is active
        if (intfc.rst_sync_i == 1'b1) begin

            // Resets the output signals
            intfc.count_value_o <= '0;
            intfc.overflow_o <= 1'b0;

        end else if (intfc.enable_i == 1'b1) begin

            // Increases the count_value_o
            intfc.count_value_o <= (intfc.count_value_o + 1) % 256;

        end

        // Overflow signal logic
        if (intfc.count_value_o == 255 && intfc.rst_sync_i != 1'b1) begin

            // Activates the overflow signal
            intfc.overflow_o <= 1'b1;

        end else begin

            intfc.overflow_o <= 1'b0;

        end
    end

endmodule


// ================================================================ //