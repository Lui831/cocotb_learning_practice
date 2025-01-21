library ieee;
use ieee.std_logic_1164.all;

use work.simple_state_machine_pkg.all;

entity simple_state_machine is
    port (
        
        -- State machine inputs
        rst  : in std_logic;
        clk  : in std_logic;
        inpt : in std_logic;

        -- State machine outputs
        outpt : out std_logic

    );
    
end simple_state_machine;

architecture Behavioral of simple_state_machine is

    -- Signal with state
    signal s_state : t_states := RESET;

begin
    
    p_state_machine_process : process(clk, rst) is
    begin

        if rst = '1' then

            s_state <= RESET;

        elsif rising_edge(clk) then

            -- Main case for state machine
            case s_state is

                when RESET =>
                    if inpt = '1' then
                        s_state <= IDLE;
                    else
                        s_state <= RESET;
                    end if;

                when IDLE =>
                    if inpt = '1' then
                        s_state <= STATE1;
                    else
                        s_state <= IDLE;
                    end if;

                when STATE1 =>
                    if inpt = '1' then
                        s_state <= STATE2;
                    else
                        s_state <= STATE1;
                    end if;

                when STATE2 =>
                    if inpt = '1' then
                        s_state <= STATE3;
                    else
                        s_state <= STATE2;
                    end if;

                when STATE3 =>
                    if inpt = '1' then
                        s_state <= IDLE;
                    else
                        s_state <= STATE3;
                    end if;

                when others =>
                    s_state <= RESET;

            end case;

        end if;

    end process p_state_machine_process;

    -- Output assignment process
    p_output_assignment : process(s_state) is
    begin

        case s_state is

            when RESET =>
                outpt <= '0';

            when IDLE =>
                outpt <= '1';

            when STATE1 =>
                outpt <= '0';

            when STATE2 =>
                outpt <= '1';

            when STATE3 =>
                outpt <= '0';

            when others =>
                outpt <= '0';

        end case;

    end process p_output_assignment;

end Behavioral;