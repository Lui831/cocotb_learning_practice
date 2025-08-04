##########################################################################################################################################################################
# crc16citt_testbench.py
# Authors: Luiz H. A. Santos.
# Date: 04/08/2025.
# Desc: this file contains the cocotb testbench functions for the crc16citt module. It will inject write and read values for the module, for development
# purposes, to verify if it is working accordingly.
##########################################################################################################################################################################


##########################################################################################################################################################################
# Libraries

import cocotb
import random
from pyuvm import *
import pyuvm
from fastcrc import crc16
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb.triggers import *
from cocotb.binary import *

##########################################################################################################################################################################


##########################################################################################################################################################################
# Constants

## Constants for the number of tests and clock cycles to be made
TEST_NUM = 100
MAX_CLK_CYCLES = 1000000000

## Constant for the RST TIME of the testbench
RST_TIME = 35

## Constant for the testbench's DUT
DUT = cocotb.top


##########################################################################################################################################################################


##########################################################################################################################################################################
# Important global variables


##########################################################################################################################################################################


##########################################################################################################################################################################
# Other functions

def generate_random_input_data():
# Description: this function generates a random byte of data to be used as input for the testbench.
# Parameters: None
# Returns: A random byte of data as an integer.

    # Returns the random byte of data
    return random.randint(0, 255)


def calculate_crc(data, previous_crc=0xFFFF):
# Description: this function calculates the CRC16-CITT of the given data.
# Parameters: data: the data to calculate the CRC for, in int value.
#             previous_crc: the previous CRC int value, default is 0xFFFF.
# Returns: None.

    # Returns the calculated CRC
    return crc16.xmodem(int.to_bytes(data, byteorder='big'), initial=previous_crc)

##########################################################################################################################################################################


##########################################################################################################################################################################
# PyUVM Relevant Classes

# UVM Sequencer for the CRC16-CITT module
class crc16citt_sequencer(uvm_sequencer):
    pass


# UVM Sequence Item for the Sequencer&Driver communication
class crc16citt_input_seq_item(uvm_sequence_item):

    # Initialization of the sequence item 
    def __init__(self, name):
        super().__init__(name)

        self.input_data = 0

    # Randomize the input data value
    def randomize(self):

        self.input_data = generate_random_input_data()


# UVM Sequence Item for the Monitor&Scoreboard communication
class crc16citt_output_seq_item(uvm_sequence_item):

    # Initialization of the sequence item 
    def __init__(self, name, dut_values=None):
        super().__init__(name)

        # Initialization of the input and output data dictionary
        self.dut_values = dut_values if dut_values is not None else {
            "input_values": {"rst_sync_i": 0, "CRC16_en_i": 0, "CRC16_data_i": 0},
            "output_values": {"CRC16_data_o": 0}
        }


# UVM Sequence to be ran by the sequencer
class crc16citt_sequence(uvm_sequence):

    # Implementation of the sequence's main logic behaviour
    async def body(self):

        # Repeat TEST_NUM times
        for _ in range(TEST_NUM):

            # Initialize the seq item
            seq_item = crc16citt_input_seq_item("crc16citt_input_seq_item")

            # Starts the transaction, randomizes the input data and finishes the item
            await self.start_item(seq_item)
            seq_item.randomize()
            await self.finish_item(seq_item)


# UVM Driver for the counter
class crc16citt_driver(uvm_driver):

    # Driver's build phase
    def build_phase(self):

        # Initializes the input data to 0
        self.input_data = 0

    
    # Driver's start_of_simulation_phase
    def start_of_simulation_phase(self):

        # Prints that the simulation is starting
        self.logger.info("[DRIVER]: The driver operation is starting, resetting the module and disabling it...")

        # Drives the enable signal to 0
        DUT.CRC16_en_i.setimmediatevalue(BinaryValue(value=0, n_bits=1))
        # Drives the reset signal to 1
        DUT.rst_sync_i.setimmediatevalue(BinaryValue(value=1, n_bits=1))


    # Driver's run_phase operation
    async def run_phase(self):

        # Awaits for the reset time
        await Timer(RST_TIME, 'ns')

        # Deasserts the reset signal
        DUT.rst_sync_i.setimmediatevalue(BinaryValue(value=0, n_bits=1))

        # Main driver loop, receiving the sequence items and driving the input data
        while True:

            # Waits for the next sequence item
            seq_item = await self.seq_item_port.get_next_item()
            self.input_data = seq_item.input_data

            # Sets the input data to the DUT and enables it
            DUT.CRC16_data_i.value = BinaryValue(value=self.input_data, n_bits=8)
            DUT.CRC16_en_i.value = BinaryValue(value=1, n_bits=1)

            # Waits for the next clock rising edge
            await RisingEdge(DUT.clk_i)

            # Deasserts the enable signal
            DUT.CRC16_en_i.value = BinaryValue(value=0, n_bits=1)

            # Waits for the next clock rising edge
            await RisingEdge(DUT.clk_i)

            # Prints the input data value
            self.logger.info("[DRIVER]: The data input is: %i" % self.input_data)

            # Finishs the item
            self.seq_item_port.item_done()


# UVM Monitor for the crc16citt_module
class crc16citt_monitor(uvm_monitor):

    # Monitor's build phase
    def build_phase(self):

        # Initializes the dictionary containing the input values and the output values
        self.dut_values = {
            "input_values": {"rst_sync_i": 0, "CRC16_en_i": 0, "CRC16_data_i": 0},
            "output_values": {"CRC16_data_o": 0}
        }

        # Initializes the analysis port
        self.analysis_port = uvm_analysis_port("analysis_port", self)


    # Monitor's run_phase operation        
    async def run_phase(self):

        # Waits for the clock signal to start
        await RisingEdge(DUT.clk_i)

        # Obtains all the signals from the DUT, emitting them to the analysis port
        while True:

            # If the DUT is not resetted, the signals are not valid
            if DUT.rst_sync_i.value != BinaryValue(value=1, n_bits=1) and DUT.CRC16_en_i.value == BinaryValue(value=1, n_bits=1):

                # Obtains the input values from the DUT
                self.dut_values["input_values"]["rst_sync_i"] = DUT.rst_sync_i.value.integer
                self.dut_values["input_values"]["CRC16_en_i"] = DUT.CRC16_en_i.value.integer
                self.dut_values["input_values"]["CRC16_data_i"] = DUT.CRC16_data_i.value.integer

                # Obtains the output values from the DUT
                self.dut_values["output_values"]["CRC16_data_o"] = DUT.CRC16_out_o.value.integer

                # Initializes the output sequence item
                output_seq_item = crc16citt_output_seq_item("crc16citt_output_seq_item", self.dut_values)

                # Writes the output sequence item to the analysis port
                self.analysis_port.write(output_seq_item)

                # Waits for the next clock rising edge
                await RisingEdge(DUT.clk_i)

            else:

                # Waits for the next clock rising edge
                await RisingEdge(DUT.clk_i)


# UVM Predictor for the crc16citt_module
class crc16citt_predictor(uvm_subscriber):

    # Initialization of the predictor
    def __init__(self, name, parent=None):
        super().__init__(name, parent)

        # Initializes the expected and observed output values
        self.expected_dut_values = {
            "input_values": {"rst_sync_i": 0, "CRC16_en_i": 0, "CRC16_data_i": 0},
            "output_values": {"CRC16_data_o": 0}
        }
        self.observed_dut_values = {
            "input_values": {"rst_sync_i": 0, "CRC16_en_i": 0, "CRC16_data_i": 0},
            "output_values": {"CRC16_data_o": 0}
        }


    # Method to predict the output values based on the input values
    def __predict_output(self):

        # Calculates the CRC16-CITT of the input data
        input_data = self.observed_dut_values["input_values"]["CRC16_data_i"]
        previous_crc = self.observed_dut_values["output_values"]["CRC16_data_o"]
        calculated_crc = calculate_crc(input_data, previous_crc)

        # Updates the expected output value
        self.expected_dut_values["output_values"]["CRC16_data_o"] = calculated_crc

        # Prints the expected output value and the observed output value
        self.logger.info("[PREDICTOR]: The previous observed output is: %s" % self.observed_dut_values["output_values"]["CRC16_data_o"])
        self.logger.info("[PREDICTOR]: The expected output is: %s" % self.expected_dut_values["output_values"]["CRC16_data_o"])
        
        # Returns the expected output value
        return self.expected_dut_values
    

    # Build phase of the predictor
    def build_phase(self):

        # Prints that the predictor is being built
        self.logger.info("[PREDICTOR]: The predictor is being built...")

        # Initializes the expected output value
        self.expected_dut_values["output_values"]["CRC16_data_o"] = 0xFFFF

    
    # Write method for the analysis export
    def write(self, item):

        # Gets the input and output values from the item
        self.observed_dut_values = item.dut_values

        # Updates the expected values based on the observed values
        self.expected_dut_values = self.__predict_output()


# UVM Env for the sequencer, driver and monitor
class crc16citt_environment(uvm_env):

    # Builds the test environment
    def build_phase(self):

        # Creates all relevant entities
        self.sequencer = crc16citt_sequencer.create("crc16citt_sequencer", self)
        self.driver    = crc16citt_driver.create("crc16citt_driver", self)
        self.monitor   = crc16citt_monitor.create("crc16citt_monitor", self)
        self.predictor = crc16citt_predictor.create("crc16citt_predictor", self)

    # Connects the environment's modules
    def connect_phase(self):

        # Connects the sequencer, driver, monitor and predictor
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
        self.monitor.analysis_port.connect(self.predictor.analysis_export)


# UVM CRC16-CITT module testbench
@pyuvm.test()
class counter_test(uvm_test):

    # Initialization of the test
    def build_phase(self):

        # Creates the environment
        self.env = crc16citt_environment.create("crc16citt_environment", self)


    def end_of_elaboration_phase(self):
        
        # Creates the sequence
        self.sequence = crc16citt_sequence.create("crc16citt_sequence")


    # Run phase
    async def run_phase(self):

        self.raise_objection()
        cocotb.start_soon(Clock(cocotb.top.clk_i, 10, 'ns').start())
        await self.sequence.start(self.env.sequencer)
        self.drop_objection()

    

    




    





        




    


    

    


