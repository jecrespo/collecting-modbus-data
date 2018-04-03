# --------------------------------------------------------------------------- #
# Tarea básica de guardar en BBDD datos de Circutor CVM-144
# --------------------------------------------------------------------------- # 

# --------------------------------------------------------------------------- #
# Tarea programada windows segun https://blogs.esri.com/esri/arcgis/2013/07/30/scheduling-a-scrip/
# --------------------------------------------------------------------------- # 

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
# configure BBDD
# instalar como administrador: pip install mysql-connector-python
# --------------------------------------------------------------------------- # 
import mysql.connector as my_dbapi

# --------------------------------------------------------------------------- # 
# get data from modbus
# descripcion zonas memoria Circutor CVM-144 http://www.convert.com.pl/docs/instrukcje/CVM-144-ETH-TCP_en.pdf
# --------------------------------------------------------------------------- #
client = ModbusTcpClient('192.168.1.100', port=502, timeout=10)
client.connect()
log.debug("Reading Registers")
result = client.read_holding_registers(0x1e, 2)    #dirección inicio, numero bytes a leer
print(result.registers)
potencia_trifasica = ((result.registers[0]*65535) + result.registers[1])/1000
print(potencia_trifasica)
client.close()

# --------------------------------------------------------------------------- # 
# Conexión a BBDD e inserción de dato
# --------------------------------------------------------------------------- #
cnx_my = my_dbapi.connect(user='usuario', password='password', host='192.168.1.101', database='circutor')
cursor_my = cnx_my.cursor()
query_my = "INSERT INTO consumo_circutor (Consumo) VALUES ('%i')" % potencia_trifasica
cursor_my.execute(query_my)
cnx_my.commit()
cnx_my.close()
