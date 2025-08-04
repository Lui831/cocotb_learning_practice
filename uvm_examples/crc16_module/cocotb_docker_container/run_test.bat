rem Deletando os códigos dos módulos colocados previamente...
del /Q ".\ext_files\FPGA_Development\*"

rem Movendo os arquivos atualizados para a pasta FPGA_Developments...
copy "..\crc16citt_module.vhd" ".\ext_files\FPGA_Development\"

rem Buildando o container
docker-compose build debian_service

rem Rodando o container e realizando os testes
docker rm cocotb_container
docker-compose run --name cocotb_container debian_service

rem Copia e executa o arquivo de simulação
docker cp cocotb_container:/cocotb/Testbench/simulation.ghw ./simulation.ghw
gtkwave.exe ./simulation.ghw

