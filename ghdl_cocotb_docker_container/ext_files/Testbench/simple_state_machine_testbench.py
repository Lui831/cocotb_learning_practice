##########################################################################################################################################################################
# simple_state_machine_testbench.py
# Author: Luiz H. A. Santos
# Desc: this file contains the cocotb testbench for a simple_state_machine module
# Date: 09/01/2025
##########################################################################################################################################################################

##########################################################################################################################################################################
# Libraries

import cocotb
import random 
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb.triggers import *
from cocotb.binary import *

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

# Function to replicate the machine state expected behaviour
async def simple_state_machine_validation_behaviour(dut):

    states_transition_table_withoutrst = {
        "IDLE"  : {"0": "IDLE", "1": "STATE1"},
        "RESET" : {"0": "RESET", "1": "IDLE"},
        "STATE1": {"0": "STATE1", "1": "STATE2"},
        "STATE2": {"0": "STATE2", "1": "STATE3"},
        "STATE3": {"0": "STATE3", "1": "IDLE"}
    }

    output_table_based_on_the_states = {
        "RESET" : "0",
        "IDLE"  : "1",
        "STATE1": "0",
        "STATE2": "1",
        "STATE3": "0"
    }

    # Initializes the clock cycles counter
    clk_cycles_counter = 0

    # Initializes the machine analogous state and output, treated as global variables
    global machine_analogous_state
    global machine_analogous_output
    machine_analogous_state = "RESET"
    machine_analogous_output = "0"

    # Initializes the behaviour of the analogous state machine
    while clk_cycles_counter <= TEST_DURATION / CLOCK_PERIOD:

        # Waits for a rising edge of the clock or any edge regarding the reset
        transition = await First(RisingEdge(dut.clk), Edge(dut.rst))

        # If the system is reseted
        if transition is Edge(dut.rst) and dut.rst.value.integer == 1:

            # Resets the system
            machine_analogous_state = "RESET"
            machine_analogous_output = "0"

        # If the system detects a rising edge of clock and its not reset
        elif transition is RisingEdge(dut.clk) and dut.rst.value.integer == 0:

            # Obtain the next state and the current output based on the estabilished tables
            machine_analogous_state = states_transition_table_withoutrst[machine_analogous_state][dut.inpt.value.binstr]
            machine_analogous_output = output_table_based_on_the_states[machine_analogous_state]

            # Increments the clock_cycles counter
            clk_cycles_counter += 1

        elif transition is RisingEdge(dut.clk) and dut.rst.value.integer == 1:

            # Resets the system
            machine_analogous_state = "RESET"
            machine_analogous_output = "0"

            # increments the clock_cycles counter
            clk_cycles_counter += 1


async def simple_state_machine_stimulus_function(dut):

    # Initializes the machine in RESET and waits a RESET time
    dut.rst.setimmediatevalue(BinaryValue(value=1, n_bits=1))
    dut.inpt.setimmediatevalue(BinaryValue(value=0, n_bits=1))

    # Initializes the clock_cycles counter
    clk_cycles_counter = 0

    # Waits for the reset time
    await Timer(RESET_TIME, units='ns')

    # Deasserts the reset signal and recalculates the clk_cycles counter
    dut.rst.setimmediatevalue(BinaryValue(value=0, n_bits=1))
    clk_cycles_counter = RESET_TIME / CLOCK_PERIOD

    # Starts the stimulus loop
    while clk_cycles_counter <= TEST_DURATION / CLOCK_PERIOD:

        # Waits for a rising edge of the clock
        await RisingEdge(dut.clk)

        # Randomly generates the input value
        dut.inpt.value = BinaryValue(value=random.randint(0, 1), n_bits=1)

        # Increments the clock_cycles counter
        clk_cycles_counter += 1


@cocotb.test()
async def test_function(dut):

    # Initializes the stimulus function and validation behaviour functions
    cocotb.start_soon(simple_state_machine_stimulus_function(dut))
    cocotb.start_soon(simple_state_machine_validation_behaviour(dut))

    # Initializes the stimulus clock
    cocotb.start_soon(Clock(dut.clk, CLOCK_PERIOD, units='ns').start())

    # Initializes the clock counter
    clk_cycles_counter = 0

    # Initializes the global variable for the machine output and machine state
    global machine_analogous_output
    global machine_analogous_state

    # Initializes the verification loop
    while clk_cycles_counter <= TEST_DURATION / CLOCK_PERIOD:

        # Waits for a rising edge of the clock
        await RisingEdge(dut.clk)

        # Prints every value regarding the system's behaviour
        print(f"Cycle {clk_cycles_counter}: Input value is {dut.inpt.value.binstr}, output value is {dut.outpt.value.binstr}, machine analogous state is {machine_analogous_state}, machine analogous output is {machine_analogous_output}, comparison is {dut.outpt.value.binstr == machine_analogous_output}")

        # Verifies if the output of the system is equal to the output of the analogous state machine
        assert dut.outpt.value == BinaryValue(value=int(machine_analogous_output), n_bits=1), f"Output value is {dut.outpt.value.binstr} and should be {machine_analogous_output}"

        # Increments the clock_cycles counter
        clk_cycles_counter += 1

    


    

    


