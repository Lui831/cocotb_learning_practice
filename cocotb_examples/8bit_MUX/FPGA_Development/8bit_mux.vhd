library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity mux_8bit is
    port (
        sel   : in  std_logic_vector(2 downto 0); -- Selecionador de 3 bits
        inpt   : in  std_logic_vector(7 downto 0); -- Vetor de entrada de 8 bits
        rst : in  std_logic;                   -- Reset
        outpt  : out std_logic                    -- Saída
    );
end mux_8bit;

architecture Behavioral of mux_8bit is

    signal sel_wrst : std_logic_vector(3 downto 0); -- Selecionador com reset

begin
    
    sel_wrst <= sel & rst; -- Concatenação do selecionador com o reset

    -- SELECT para multiplexação da entrada na saída
    with sel_wrst select
        outpt <= inpt(0) when "0000",
                 inpt(1) when "0010",
                 inpt(2) when "0100",
                 inpt(3) when "0110",
                 inpt(4) when "1000",
                 inpt(5) when "1010",
                 inpt(6) when "1100",
                 inpt(7) when "1110",
                    '0' when others;

end Behavioral;