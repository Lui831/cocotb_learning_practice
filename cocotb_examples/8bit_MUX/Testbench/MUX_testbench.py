##########################################################################################################################################################################
# MUX_testbench.py
# Author: Luiz H. A. Santos
# Desc: this file contains the cocotb testbench for the counter module
# Date: 08/01/2025
##########################################################################################################################################################################

##########################################################################################################################################################################
# Libraries

import cocotb
import random 
from cocotb.triggers import Timer
from cocotb.clock import Clock

##########################################################################################################################################################################

##########################################################################################################################################################################
# Constants

# Clock frequency
CLOCK_PERIOD = 10 # ns

# Reset ON time
RESET_TIME = 35 # ns

# Test duration
TEST_DURATION = 1000 # ns

##########################################################################################################################################################################

##########################################################################################################################################################################
# Testbench function


def mux_validation_function(dut, input_binval, selector_int):

    # Separates the binary numbers included at the input_binstr into a list, inverting its sequence
    print(input_binval.binstr)
    input_list = list(input_binval.binstr)
    input_list.reverse()

    print(input_list)
    print(selector_int)

    # Choses the input_value based on the selector
    return int(input_list[selector_int])


async def mux_stimulus_function(dut):

    # Initializes the clock cycles counter
    clk_cycles_counter = 0

    # Chooses a random value for the mux input
    dut.inpt.setimmediatevalue(cocotb.binary.BinaryValue(value=random.randint(0, 2**8 - 1), n_bits=8))

    # Chooses a random value for the selector
    dut.sel.setimmediatevalue(cocotb.binary.BinaryValue(value=random.randint(0, 7), n_bits=3))

    # Starts the reset
    dut.rst.setimmediatevalue(cocotb.binary.BinaryValue(value=1, n_bits=1))

    # Awaits for the reset time
    await Timer(RESET_TIME, units='ns')

    # Stops the reset
    dut.rst.setimmediatevalue(cocotb.binary.BinaryValue(value=0, n_bits=1))

    # Awaits for a small time to avoid any conflict
    await Timer(1, units='ps')

    # While loop for choosing random values for the mux input and selector
    while clk_cycles_counter <= (TEST_DURATION) / CLOCK_PERIOD:

        # Chooses a random value for the mux input
        dut.inpt.setimmediatevalue(cocotb.binary.BinaryValue(value=random.randint(0, 2**8 - 1), n_bits=8))

        # Chooses a random value for the selector
        dut.sel.setimmediatevalue(cocotb.binary.BinaryValue(value=random.randint(0, 7), n_bits=3))

        # Awaits for a clock period
        await Timer(CLOCK_PERIOD, units='ns')

        # Increments the clock cycles counter
        clk_cycles_counter += 1


@cocotb.test()
async def test_function(dut):

    # Initializes the stimulus function
    await cocotb.start(mux_stimulus_function(dut))

    # Initializes the clock cycles counter
    clk_cycles_counter = 0

    # Starts the test until the end of the test duration
    while clk_cycles_counter <= (RESET_TIME + TEST_DURATION) / CLOCK_PERIOD:

        # Espera sempre um período específico do timer
        await Timer(CLOCK_PERIOD, units='ns')

        # Increments the clock cycles counter
        clk_cycles_counter += 1

        # Checks if the clock cycles counter is in RESET state
        if clk_cycles_counter <= RESET_TIME / CLOCK_PERIOD:

            # Checks if the value of the mux output is 0
            assert dut.outpt.value.integer == 0, "The value of the mux output is not 0"

        # Checks if the clock cycles counter is in TEST state
        if clk_cycles_counter >= RESET_TIME / CLOCK_PERIOD and clk_cycles_counter <= (RESET_TIME + TEST_DURATION) / CLOCK_PERIOD:

            # Obtém o valor esperado para o mux output
            expected_value = mux_validation_function(dut, dut.inpt.value, dut.sel.value.integer)

            # Checks if the value of the mux output is equal to the expected value
            assert dut.outpt.value.integer == expected_value, "The value of the mux output is not equal to the expected value"

            print(f"Input value: {dut.inpt.value.binstr}")
            print(f"Selector value: {dut.sel.value.integer}")
            print(f"Expected value: {expected_value}")
            print(f"Output value: {dut.outpt.value.integer}")
            print("\n", end="")

    return


    

    


