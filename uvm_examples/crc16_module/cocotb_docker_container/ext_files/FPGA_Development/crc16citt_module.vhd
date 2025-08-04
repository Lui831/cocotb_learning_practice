---------------------------------------------------------------------------------------------------------
-- codec_PUS_Receiver_Transmitter_CRC16CITT_module.vhd
-- Author: Luiz H. A. Santos
-- Date: 2024-09-12
-- Description: esse arquivo contém a arquitetura do módulo CRC16CITT, responsável por calcular o CRC16
-- iterativamente de um pacote CCSDS.
---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- Libraries

library ieee;
use ieee.std_logic_1164.all;

---------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------
-- Entidade do módulo CRC16CITT

entity crc16citt_module is
    generic(

        -- CRC16 Inicial
        g_crc_init: std_logic_vector(15 downto 0) := x"FFFF"

    );
    port (

        ---- Sinais de Entrada --
        -- Clock e reset síncrono do sistema
        clk_i        : in std_logic;
        rst_sync_i   : in std_logic;

        -- Dados de entrada para cálculo do CRC16
        CRC16_data_i : in std_logic_vector(8 - 1 downto 0);

        -- Sinal de enable do CRC16
        CRC16_en_i   : in std_logic;

        ---- Sinais de Saída do CRC16 --
        -- CRC16 calculado
        CRC16_out_o  : out std_logic_vector(16 - 1 downto 0)
    );
end entity crc16citt_module;

---------------------------------------------------------------------------------------------------------

architecture rtl of crc16citt_module is


    ---- Definições de funções e procedimentos internos --
    -- Função para cálculo do CRC16CITT iterativo
    function crc16citt(data : std_logic_vector(7 downto 0); crc : std_logic_vector(15 downto 0)) return std_logic_vector is
    
        -- Variáveis locais
        variable crc_out : std_logic_vector(15 downto 0);

    begin

        crc_out(0) := crc(8) xor crc(12) xor data(0) xor data(4);
        crc_out(1) := crc(9) xor crc(13) xor data(1) xor data(5);
        crc_out(2) := crc(10) xor crc(14) xor data(2) xor data(6);
        crc_out(3) := crc(11) xor crc(15) xor data(3) xor data(7);
        crc_out(4) := crc(12) xor data(4);
        crc_out(5) := crc(8) xor crc(12) xor crc(13) xor data(0) xor data(4) xor data(5);
        crc_out(6) := crc(9) xor crc(13) xor crc(14) xor data(1) xor data(5) xor data(6);
        crc_out(7) := crc(10) xor crc(14) xor crc(15) xor data(2) xor data(6) xor data(7);
        crc_out(8) := crc(0) xor crc(11) xor crc(15) xor data(3) xor data(7);
        crc_out(9) := crc(1) xor crc(12) xor data(4);
        crc_out(10) := crc(2) xor crc(13) xor data(5);
        crc_out(11) := crc(3) xor crc(14) xor data(6);
        crc_out(12) := crc(4) xor crc(8) xor crc(12) xor crc(15) xor data(0) xor data(4) xor data(7);
        crc_out(13) := crc(5) xor crc(9) xor crc(13) xor data(1) xor data(5);
        crc_out(14) := crc(6) xor crc(10) xor crc(14) xor data(2) xor data(6);
        crc_out(15) := crc(7) xor crc(11) xor crc(15) xor data(3) xor data(7);

        return crc_out;

    end function crc16citt;


    ---- Sinais internos --
    -- Sinal de CRC16 atual
    signal s_CRC16_current_crc : std_logic_vector(15 downto 0) := g_crc_init;

begin

    ---- Declaração de processos internos --
    -- Processo para cálculo do CRC16CITT
    p_crc16citt_calculation : process(clk_i) is
    begin

        -- Verifica se o clock é de subida
        if rising_edge(clk_i) then

            -- Caso o dispositivo esteja resetado
            if rst_sync_i = '1' then

                -- Reinicializa o CRC16
                s_CRC16_current_crc <= g_crc_init;

            -- Caso contrário
            else

                -- Caso o dispositivo esteja habilitado
                if CRC16_en_i = '1' then

                    -- Atualiza
                    s_CRC16_current_crc <= crc16citt(CRC16_data_i, s_CRC16_current_crc);

                end if;
            end if;
        end if;
    end process p_crc16citt_calculation;

    ---- Ligação de sinais gerais --
    CRC16_out_o <= s_CRC16_current_crc;
    
    
end architecture rtl;