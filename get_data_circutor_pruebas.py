# --------------------------------------------------------------------------- # 
# Instalar pymodbus: pip install pymodbus
# get data from modbus
# --------------------------------------------------------------------------- #

from pymodbus.client.sync import ModbusTcpClient

# --------------------------------------------------------------------------- # 
# configure the client logging
# --------------------------------------------------------------------------- # 

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)	#muestra debug de la traza modbus tcp

# --------------------------------------------------------------------------- # 
# Monitor TCP2RS modbus TCP + CVM-K
# Cada dispositivo modbus RS-485 tipo CVM-K tiene un número de dispositivo modbus
# 
# TCP2RS modbus TCP:
#   - http://www.intesiscon.com/ficheros/manuales-tecnicos/73-M54032-TPC2RS-MODBUSTCP.pdf
#
# CVM-K:
#   - http://www.convert.com.pl/docs/instrukcje/CVMk-H_en.pdf
#   - http://www.convert.com.pl/docs/instrukcje/CVMk-HAR_en.pdf
#   - http://docs.circutor.com/docs/M001B01-01.pdf
#   - http://www.convert.com.pl/docs/instrukcje/CVMk-HAR_en.pdf
#   - http://lit.powerware.com/ll_download.asp?file=CVMk%20power%20analyzer%20manual%20part1.pdf
#
# CVM-144:
#   - descripcion zonas memoria Circutor CVM-144 http://www.convert.com.pl/docs/instrukcje/CVM-144-ETH-TCP_en.pdf
# --------------------------------------------------------------------------- # 

modbus_device = {'ip':'192.168.1.100','power': 0,'max_power':0}	# ejemplo dict para almacenar datos

# --------------------------------------------------------------------------- # 
# Prueba 100 lecturas seguidas consumo trifasico y máximo, en los modelos CVM-K
# --------------------------------------------------------------------------- # 

client_CG = ModbusTcpClient('192.168.1.100', port=502, timeout=10)
client_CG.connect()
log.debug("Reading Registers")

for j in range(100):
    result = client_CG.read_holding_registers(0x2a, 2, unit = 1)	# 2 bytes correspondientes a la potencia trifásica
    result_max = client_CG.read_holding_registers(0x44, 2, unit = 1)# 2 bytes correspondientes a la máxima potencia trifásica
    dato = ((result.registers[0]*65535) + result.registers[1])/1000	# conversión a W
    dato_max = ((result_max.registers[0]*65535) + result_max.registers[1])/1000	# conversión a W
    print(str(j) + " --> " + str(result.registers) + " - " + str(dato)+ " -- " + str(result_max.registers)\
          + " - " + str(dato_max))
client_CG.close()

# --------------------------------------------------------------------------- # 
# Prueba 100 lecturas seguidas consumo trifasico y máximo, en los modelos CVM-144
# --------------------------------------------------------------------------- # 

client_GS = ModbusTcpClient('192.168.1.100', port=502, timeout=10)
client_GS.connect()
log.debug("Reading Registers")

for j in range(100):
    result = client_GS.read_holding_registers(0x1e, 2)		# 2 bytes correspondientes a la potencia trifásica
    result_max = client_GS.read_holding_registers(0x7e, 2)	# 2 bytes correspondientes a la máxima potencia trifásica
    dato = ((result.registers[0]*65535) + result.registers[1])/1000	# conversión a W
    dato_max = ((result_max.registers[0]*65535) + result_max.registers[1])/1000	# conversión a W
    print(str(j) + " --> " + str(result.registers) + " - " + str(dato)+ " -- " +str(result_max.registers)\
          + " - " + str(dato_max))
client_GS.close()

# --------------------------------------------------------------------------- # 
# Prueba 1000 lecturas seguidas consumo trifasico en los modelos CVM-144
# --------------------------------------------------------------------------- # 

client_AA = ModbusTcpClient('192.168.1.100', port=502, timeout=10)
client_AA.connect()
log.debug("Reading Registers")

for j in range(1000):
    result = client_AA.read_holding_registers(0x1e, 2)
    dato = ((result.registers[0]*65535) + result.registers[1])/1000
    print(str(j) + " --> " + str(result.registers) + " - " + str(dato))
client_AA.close()

# --------------------------------------------------------------------------- # 
# Prueba scan direcciones de memoria
# --------------------------------------------------------------------------- # 

client = ModbusTcpClient(modbus_device['ip'], port=502, timeout=10)
client.connect()
log.debug("Reading Registers")

# client.read_holding_registers(0, 82) - Dirección inicio, numero bytes a leer del dispositivo 0
# Para seleccionar otro dispositivo del bus, usar la variable unit de la función read_holding_registers
# CUANDO SE USAN LOS DOS BYTES ES: PRIMER BYTE * 65535 + SEGUNDO BYTE (correspondiente a codificacion de 16 bits)
result = client.read_holding_registers(0, 82) 
print(result.registers)	#impresión de los 82 primeros bytes de memoria

# scaneo de las 600 primeras zonas de memoria tomadas de 2 en 2 bytes de la unidad 4 del bus
for i in range (0,600,2):
    try:
        result = client.read_holding_registers(i, 2, unit = 4)
        dato = ((result.registers[0]*65535) + result.registers[1])/1000
        print(str(i) + " --> " + str(result.registers) + " - " + str(dato))
    except:
        pass

# Datos concretos de varios dispositivos en el bus
modbus_device['power'] = client.read_holding_registers(42, 2, unit = 1).registers	#Potencia Trifasica W
print("Device 1 --> Power = " + str(modbus_device['power']))

modbus_device['power'] = client.read_holding_registers(42, 2, unit = 2).registers	#Potencia Trifasica W
print("Device 1 --> Power = " + str(modbus_device['power']))

modbus_device['power'] = client.read_holding_registers(42, 2, unit = 3).registers	#Potencia Trifasica W
print("Device 1 --> Power = " + str(modbus_device['power']))

modbus_device['power'] = client.read_holding_registers(42, 2, unit = 4).registers	#Potencia Trifasica W
print("Device 1 --> Power = " + str(modbus_device['power']))

client.close()