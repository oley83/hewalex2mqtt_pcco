import os
import threading
import serial
from hewalex_geco.devices import PCCO
import paho.mqtt.client as mqtt
import logging
import sys
import json
import random

# polling interval
get_status_interval = 30.0

# Controller_odczyt (Master) - identyfikator ID tego skryptu w komunikacji do odczytu danych
conHardId = 1
conSoftId = 1

# Controller_zapis (Master) - alternatywny ID tego skryptu do zapisu danych w sterowniku pompy
conHardId2 = 1
conSoftId2 = 1

# Device ID (Slave - PCCO) - identyfikator ID pompy ciepła
devHardId = 2
devSoftId = 2

#mqtt
flag_connected_mqtt = 0
MessageCache = {}

# Read-only mode
_Read_Only_Mode = True  # Domyślnie włączony tryb read-only dla bezpieczeństwa (blokada funkcji zapisu)

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

# Start
logger.info('Starting Hewalex2Mqtt - PCCO Mono')

# Read Configs
def initConfiguration():
    logger.info("Reading config")
    # When deployed = /hewagate/hewalex2mqtt.py and /data/options.json
    config_file = os.path.join(os.path.dirname(__file__), '../data/options.json')
    config_file = os.path.normpath(config_file)

    if(os.path.isfile(config_file)) :
        file_pointer = open(config_file, 'r')
        config = json.load(file_pointer)
    else:
        logger.error("file: %s does not exist", config_file)
        sys.exit(1)
    
    # Mqtt Configuration
    global _MQTT_ip
    if (os.getenv('MQTT_ip') != None):        
        _MQTT_ip = os.getenv('MQTT_ip')
    else:
        _MQTT_ip = config['mqtt_ip']
    
    global _MQTT_port
    if (os.getenv('MQTT_port') != None):        
        _MQTT_port = int(os.getenv('MQTT_port'))
    else:
        _MQTT_port = config['mqtt_port']
    
    global _MQTT_authentication
    if (os.getenv('MQTT_authentication') != None):        
        _MQTT_authentication = os.getenv('MQTT_authentication') == "True"
    else:
        _MQTT_authentication = config['mqtt_authentication']
    
    global _MQTT_user
    if (os.getenv('MQTT_user') != None):        
        _MQTT_user = os.getenv('MQTT_user')
    else:
        _MQTT_user = config['mqtt_user']
    
    global _MQTT_pass
    if (os.getenv('MQTT_pass') != None):        
        _MQTT_pass = os.getenv('MQTT_pass')
    else:
        _MQTT_pass = config['mqtt_pass']    

    # PCCO Device Configuration
    global _Device_Pcco_Enabled
    if (os.getenv('Device_Pcco_Enabled') != None):        
        _Device_Pcco_Enabled = os.getenv('Device_Pcco_Enabled') == "True"
    else:
        _Device_Pcco_Enabled = config['Device_Pcco_Enabled']

    global _Device_Pcco_Address
    if (os.getenv('Device_Pcco_Address') != None):        
        _Device_Pcco_Address = os.getenv('Device_Pcco_Address')
    else:
        _Device_Pcco_Address = config['Device_Pcco_Address']
    
    global _Device_Pcco_Port
    if (os.getenv('Device_Pcco_Port') != None):        
        _Device_Pcco_Port = os.getenv('Device_Pcco_Port')
    else:
        _Device_Pcco_Port = config['Device_Pcco_Port']

    global _Device_Pcco_MqttTopic
    if (os.getenv('Device_Pcco_MqttTopic') != None):        
        _Device_Pcco_MqttTopic = os.getenv('Device_Pcco_MqttTopic')
    else:
        _Device_Pcco_MqttTopic = config['Device_Pcco_MqttTopic']

    # Read-only mode configuration
    global _Read_Only_Mode
    if (os.getenv('Read_Only_Mode') != None):        
        _Read_Only_Mode = os.getenv('Read_Only_Mode') == "True"
    else:
        _Read_Only_Mode = config.get('Read_only_mode', True)  # Domyślnie True
    
    logger.info(f"PCCO Configuration: Enabled={_Device_Pcco_Enabled}, Address={_Device_Pcco_Address}:{_Device_Pcco_Port}, Topic={_Device_Pcco_MqttTopic}")
    logger.info(f"Read-only mode: {_Read_Only_Mode}")  # Logowanie stanu trybu read-only

def start_mqtt():
    global client
    logger.info('Connection in progress to the Mqtt broker (IP:' + _MQTT_ip + ' PORT:' + str(_MQTT_port) + ')')
    client = mqtt.Client()
    if _MQTT_authentication:
        logger.info('Mqtt authentication enabled')
        client.username_pw_set(username=_MQTT_user, password=_MQTT_pass)
    client.on_connect = on_connect_mqtt
    client.on_disconnect = on_disconnect_mqtt
    client.on_message = on_message_mqtt        
    client.connect(_MQTT_ip, _MQTT_port)  
    
    if _Device_Pcco_Enabled:
        if not _Read_Only_Mode:  # TYLKO jeśli nie jest w trybie read-only
            logger.info('subscribed to : ' + _Device_Pcco_MqttTopic + '/Command/#')    
            client.subscribe(_Device_Pcco_MqttTopic + '/Command/#', qos=1)
        else:
            logger.info('Read-only mode: MQTT commands disabled')
        
    client.loop_start()

def on_connect_mqtt(client, userdata, flags, rc):
    logger.info("Mqtt: Connected to broker with result code " + str(rc))
    global flag_connected_mqtt
    flag_connected_mqtt = 1

def on_disconnect_mqtt(client, userdata, rc):
    logger.info("Mqtt: disconnected with result code " + str(rc))
    global flag_connected_mqtt
    flag_connected_mqtt = 0

def on_message_mqtt(client, userdata, message):    
    try:        
        payload = str(message.payload.decode())
        topic = str(message.topic)
        arr = topic.split('/')
        # PCCO Command 
        if len(arr) == 3 and arr[0] == _Device_Pcco_MqttTopic and arr[1] == 'Command':            
            command = arr[2]
            logger.info('Received PCCO command ' + topic + ' with payload: ' + payload)
            writePccoConfig(command, payload)
        else:
            logger.info('Cannot process message on topic ' + topic)

    except Exception as e:
        logger.error('Exception in on_message_mqtt: '+ str(e))

def on_message_serial(obj, h, sh, m):
    try:    
        if flag_connected_mqtt != 1:
            logger.debug('MQTT not connected, skipping message')
            return False
        
        global MessageCache
        topic = _Device_Pcco_MqttTopic
    
        if sh["FNC"] == 0x50:
            mp = obj.parseRegisters(sh["RestMessage"], sh["RegStart"], sh["RegLen"])        
            for item in mp.items():
                if isinstance(item[1], dict): # skipping dictionaries (time program) 
                    continue
                key = topic + '/' + str(item[0])
                val = str(item[1])
               
                if key not in MessageCache or MessageCache[key] != val:    #Sprawdza czy wartość się zmieniła (unika duplikatów)
                
                    MessageCache[key] = val
                    logger.info(f"Publishing: {key} = {val}")
                    client.publish(key, val, retain=True)
        else:
            logger.debug(f"Unhandled function code: {sh['FNC']}")

    except Exception as e:
        logger.error('Exception in on_message_serial: '+ str(e))

def device_readregisters_enqueue():   #Pobiera dane z pompy co x sekund
    logger.debug('Get device status')
    random_delay = random.uniform(0, 5)    #losowe opoznienie aby unknac kolizji z ekontol
    threading.Timer(get_status_interval + random_delay, device_readregisters_enqueue).start()
    if _Device_Pcco_Enabled:        
        try:
            readPCCO()			#Odczytuje rejestry statusowe
            readPccoConfig()	#Odczytuje rejestry konfiguracyjne
        except Exception as e:
            logger.error(f"Error reading PCCO: {e}")

def readPCCO():    #Odczyt statusow z pompy
    try:
        ser = serial.serial_for_url("socket://%s:%s" % (_Device_Pcco_Address, _Device_Pcco_Port))
        dev = PCCO(conHardId, conSoftId, devHardId, devSoftId, on_message_serial)        
        dev.readStatusRegisters(ser)    
        ser.close()
        logger.debug("PCCO status registers read successfully")
    except Exception as e:
        logger.error(f"Error reading PCCO status: {e}")
        raise

def readPccoConfig():    #Odczyt konfiguracji z pompy
    try:
        ser = serial.serial_for_url("socket://%s:%s" % (_Device_Pcco_Address, _Device_Pcco_Port))
        dev = PCCO(conHardId, conSoftId, devHardId, devSoftId, on_message_serial)            
        dev.readConfigRegisters(ser)
        ser.close()
        logger.debug("PCCO config registers read successfully")
    except Exception as e:
        logger.error(f"Error reading PCCO config: {e}")
        raise

def writePccoConfig(registerName, payload):    #zapis do pompy
    if _Read_Only_Mode:  #Sprawdzanie trybu READ-ONLY
        logger.warning(f"Read-only mode enabled. Ignoring write command: {registerName} = {payload}")
        return
        
    try:
        ser = serial.serial_for_url("socket://%s:%s" % (_Device_Pcco_Address, _Device_Pcco_Port))
        dev = PCCO(conHardId2, conSoftId2, devHardId, devSoftId, on_message_serial)            
        dev.write(ser, registerName, payload)
        ser.close()
        logger.info(f"PCCO config written: {registerName} = {payload}")
    except Exception as e:
        logger.error(f"Error writing PCCO config: {e}")
        raise

def printPccoMqttTopics():       #Wyświetla listę tematów MQTT - dostepne rejestry
    print('| Topic | Type | Description | ')
    print('| ----------------------- | ----------- | ---------------------------')
    dev = PCCO(conHardId, conSoftId, devHardId, devSoftId, on_message_serial)
    for k, v in dev.registers.items():
        if isinstance(v['name'] , list):
            for i in v['name']:
                if i:
                    print('| ' + _Device_Pcco_MqttTopic + '/' + str(i) + ' | ' + v['type'] + ' | ' + str(v.get('desc')))
        else:
            print('| ' + _Device_Pcco_MqttTopic + '/' + str(v['name'])+ ' | ' + v['type'] + ' | ' + str(v.get('desc')))
        if k > dev.REG_CONFIG_START:          
            print('| ' + _Device_Pcco_MqttTopic + '/Command/' + str(v['name']) + ' | ' + v.get('type') + ' | ' + str(v.get('desc')))

if __name__ == "__main__":
    try:
        initConfiguration()
        #printPccoMqttTopics()         # Jesli odkomentowane to wyswietla dostepne rejestry
        start_mqtt()
        # Start the first polling cycle after a short delay
        threading.Timer(2.0, device_readregisters_enqueue).start()
        logger.info("Application started successfully")
        
        # Keep the main thread alive
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
