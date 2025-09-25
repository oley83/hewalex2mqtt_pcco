import os
import threading
import serial
from hewalex_geco.devices import PCCO
import paho.mqtt.client as mqtt
import logging
import sys
import json
import time

# polling interval
get_status_interval = 30.0

# Controller (Master)
conHardId = 1
conSoftId = 1

# Controller2 (Master)
conHardId2 = 1
conSoftId2 = 1

# Device ID - ZMIENIĆ NA POPRAWNY ADRES URZĄDZENIA!
# Spróbuj 16 zamiast 2, bo błąd wskazuje na adres 16
devHardId = 16  # ZMIANA: 2 → 16
devSoftId = 16  # ZMIANA: 2 → 16

#mqtt
flag_connected_mqtt = 0
MessageCache = {}

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

# Start
logger.info('Starting Hewalex 2 Mqtt hvdb - PCCO only')

# Read Configs
def initConfiguration():
    logger.info("reading config")
    config_file = os.path.join(os.path.dirname(__file__), '../data/options.json')
    config_file = os.path.normpath(config_file)

    if(os.path.isfile(config_file)):
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
    
    # Nowa opcja: timeout dla komunikacji szeregowej
    global _Serial_Timeout
    if (os.getenv('Serial_Timeout') != None):        
        _Serial_Timeout = float(os.getenv('Serial_Timeout'))
    else:
        _Serial_Timeout = config.get('serial_timeout', 5.0)
    
    logger.info(f"PCCO Configuration: Enabled={_Device_Pcco_Enabled}, Address={_Device_Pcco_Address}:{_Device_Pcco_Port}, Topic={_Device_Pcco_MqttTopic}")

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
    
    try:
        client.connect(_MQTT_ip, _MQTT_port)
        if _Device_Pcco_Enabled:
            logger.info('subscribed to : ' + _Device_Pcco_MqttTopic + '/Command/#')    
            client.subscribe(_Device_Pcco_MqttTopic + '/Command/#', qos=1)
        client.loop_start()
    except Exception as e:
        logger.error(f"MQTT connection failed: {e}")

def on_connect_mqtt(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Mqtt: Connected to broker successfully")
        global flag_connected_mqtt
        flag_connected_mqtt = 1
    else:
        logger.error(f"Mqtt: Connection failed with result code {rc}")

def on_disconnect_mqtt(client, userdata, rc):
    logger.info(f"Mqtt: disconnected with result code {rc}")
    global flag_connected_mqtt
    flag_connected_mqtt = 0

def on_message_mqtt(client, userdata, message):    
    try:        
        payload = str(message.payload.decode())
        topic = str(message.topic)
        arr = topic.split('/')
        if len(arr) == 3 and arr[0] == _Device_Pcco_MqttTopic and arr[1] == 'Command':            
            command = arr[2]
            logger.info('Received PCCO command ' + topic + ' with payload: ' + payload)
            writePccoConfig(command, payload)
        else:
            logger.warning('Cannot process message on topic ' + topic)

    except Exception as e:
        logger.error('Exception in on_message_mqtt: '+ str(e))

def on_message_serial(obj, h, sh, m):
    try:    
        if flag_connected_mqtt != 1:
            logger.debug('MQTT not connected, skipping message')
            return False
        
        global MessageCache
        topic = _Device_Pcco_MqttTopic
    
        if sh["FNC"] == 0x50:  # Odczyt rejestrów
            mp = obj.parseRegisters(sh["RestMessage"], sh["RegStart"], sh["RegLen"])        
            for item in mp.items():
                if isinstance(item[1], dict):
                    continue
                key = topic + '/' + str(item[0])
                val = str(item[1])
                if key not in MessageCache or MessageCache[key] != val:
                    MessageCache[key] = val
                    logger.info(f"Publishing: {key} = {val}")
                    client.publish(key, val, retain=True)
        elif sh["FNC"] == 0x40:  # Zapis rejestrów - to jest normalne, nie loguj jako błąd
            logger.debug(f"Write function code 0x40 acknowledged")
        else:
            logger.debug(f"Unhandled function code: {sh['FNC']} (0x{sh['FNC']:02x})")

    except Exception as e:
        logger.error('Exception in on_message_serial: '+ str(e))

def device_readregisters_enqueue():
    """Get device status every x seconds"""
    logger.debug('Polling device status')
    threading.Timer(get_status_interval, device_readregisters_enqueue).start()
    
    if _Device_Pcco_Enabled:        
        try:
            # Dodaj opóźnienie między odczytami dla stabilności
            readPCCO()
            time.sleep(1)  # Opóźnienie między status a config
            readPccoConfig()
        except Exception as e:
            logger.error(f"Error in device polling: {e}")

def safe_serial_operation(operation_name, operation_func):
    """Bezpieczna operacja na porcie szeregowym z retry"""
    max_retries = 2
    for attempt in range(max_retries):
        try:
            ser = serial.serial_for_url(f"socket://{_Device_Pcco_Address}:{_Device_Pcco_Port}", timeout=_Serial_Timeout)
            result = operation_func(ser)
            ser.close()
            return result
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed for {operation_name}: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)  # Czekaj przed retry
            else:
                raise e

def readPCCO():    
    def read_status(ser):
        dev = PCCO(conHardId, conSoftId, devHardId, devSoftId, on_message_serial)        
        dev.readStatusRegisters(ser)
        return True
    
    safe_serial_operation("PCCO status read", read_status)
    logger.debug("PCCO status registers read successfully")

def readPccoConfig():    
    def read_config(ser):
        dev = PCCO(conHardId, conSoftId, devHardId, devSoftId, on_message_serial)            
        dev.readConfigRegisters(ser)
        return True
    
    safe_serial_operation("PCCO config read", read_config)
    logger.debug("PCCO config registers read successfully")

def writePccoConfig(registerName, payload):    
    def write_config(ser):
        dev = PCCO(conHardId2, conSoftId2, devHardId, devSoftId, on_message_serial)            
        dev.write(ser, registerName, payload)
        return True
    
    safe_serial_operation("PCCO config write", write_config)
    logger.info(f"PCCO config written: {registerName} = {payload}")

if __name__ == "__main__":
    try:
        initConfiguration()
        start_mqtt()
        # Daj MQTT czas na połączenie
        time.sleep(3)
        device_readregisters_enqueue()
        logger.info("Application started successfully")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
