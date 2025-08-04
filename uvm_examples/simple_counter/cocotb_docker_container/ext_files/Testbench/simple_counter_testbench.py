##########################################################################################################################################################################
# complex_mutex_testbench.py
# Authors: Luiz H. A. Santos, Pedro A. W. Dian, João P. Fogetti e Rafaella C. Zeron.
# Date: 19/04/2025.
# Desc: this file contains the cocotb testbench functions for the complex_mutex module. It will inject write and read values for the module, for development
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
TEST_NUM = 1000
MAX_CLK_CYCLES = 1000000000

## Constant for the RST TIME of the testbench
RST_TIME = 30


##########################################################################################################################################################################


##########################################################################################################################################################################
# Important global variables

test_is_running = True
num_tests = 0

##########################################################################################################################################################################


##########################################################################################################################################################################
# Other functions


##########################################################################################################################################################################


##########################################################################################################################################################################
# PyUVM relevant classes

# UVM Sequencer for the counter
class counter_sequencer(uvm_sequencer):
    pass


# UVM Sequence Item for the enable signal
class counter_seq_item(uvm_sequence_item):

    # Initialization of the parameters
    def __init__(self, name):
        super().__init__(name)

        self.enable_value = 0

    # Randomize the transaction
    def randomize(self):

        self.enable_value = random.randint(0, 1)


# UVM Sequence to be ran by the sequencer
class counter_sequence(uvm_sequence):

    # Reinterpretation of the body
    async def body(self):

        # Repeat 10 operations regarding the enable's changing
        for operation in range(10):

            # Initialize the seq item
            seq_item = counter_seq_item("seq_item")

            # Starts the item, randomize and finishs the item
            await self.start_item(seq_item)
            seq_item.randomize()
            await self.finish_item(seq_item)


# UVM Driver for the counter
class counter_driver(uvm_driver):

    # Driver's build phase
    def build_phase(self):

        # Initializes the enable signal to 0
        self.counter_enable = 0

    
    # Driver's start_of_simulation_phase
    def start_of_simulation_phase(self):

        # Prints that the simulation is starting
        self.logger.info("The driver operation is starting, resetting the enable signal...")

        # Drives the enable signal to 0
        cocotb.top.enable.setimmediatevalue(BinaryValue(value = 0, n_bits = 1))


    # Driver's run_phase operation
    async def run_phase(self):

        # Waits for receiving a transaction from the sequencer
        while True:

            seq_item = await self.seq_item_port.get_next_item()

            # Waits for a cycle of clock
            await RisingEdge(cocotb.top.clk)

            # Sets the enable signal based on the transaction item
            cocotb.top.enable.value = BinaryValue(value = seq_item.enable_value, n_bits = 1)

            # Prints the enable signal
            self.logger.info("The enable signal has been randomly changed into: %i..." % seq_item.enable_value)

            # Finishs the item
            self.seq_item_port.item_done()


# UVM Monitor for the counter
class counter_monitor(uvm_monitor):

    async def run_phase(self):

        # Prints all the output signals from the counter, every clock cycle
        while True:

            await RisingEdge(cocotb.top.clk)
            self.logger.info("The counter_value is: %i" % cocotb.top.count.value.integer)


# UVM Env for the sequencer, driver and monitor
class counter_environment(uvm_env):

    # Builds the environment
    def build_phase(self):

        # Creates all entities
        self.sequencer = counter_sequencer.create("counter_sequencer", self)
        self.driver    = counter_driver.create("counter_driver", self)
        self.monitor   = counter_monitor.create("counter_monitor", self)


    # Connects the environment's modules
    def connect_phase(self):
        
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)


# UVM Counter test
@pyuvm.test()
class counter_test(uvm_test):

    def build_phase(self):

        # Creates the environment
        self.env = counter_environment.create("counter_environment", self)
        
    
    def end_of_elaboration_phase(self):
        
        # Creates the sequence
        self.sequence = counter_sequence.create("counter_sequence")


    # Run phase
    async def run_phase(self):

        self.raise_objection()
        cocotb.start_soon(Clock(cocotb.top.clk, 10, 'ns').start())
        await self.sequence.start(self.env.sequencer)
        self.drop_objection()

    

    




    





        




    


    

    


