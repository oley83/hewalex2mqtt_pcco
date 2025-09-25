import os
import threading
#import configparser
import serial
from hewalex_geco.devices import PCCO, ZPS
import paho.mqtt.client as mqtt
import logging
import sys
import json

# polling interval
get_status_interval = 30.0

# Controller (Master)
conHardId = 1
conSoftId = 1

# Controller2 (Master)
conHardId2 = 1
conSoftId2 = 1


# ZPS (Slave)
devHardId = 2
devSoftId = 2

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
logger.info('Starting Hewalex 2 Mqtt hvdb')

# Read Configs
def initConfiguration():
    logger.info("reading config")
    # When deployed = /hewagate/hewalex2mqtt.py and /data/options.json
    config_file = os.path.join(os.path.dirname(__file__), '../data/options.json')
    config_file= os.path.normpath(config_file)

    if(os.path.isfile(config_file)) :
        file_pointer = open(config_file, 'r')
        config = json.load(file_pointer)
    else:
        logger.error("file: %s does not exist", config_file)
    
    # Mqtt
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
    
    # ZPS Device
    global _Device_Zps_Enabled
    if (os.getenv('Device_Zps_Enabled') != None):        
        _Device_Zps_Enabled = os.getenv('Device_Zps_Enabled') == "True"
    else:
        _Device_Zps_Enabled = config['Device_Zps_Enabled']
    global _Device_Zps_Address
    if (os.getenv('_Device_Zps_Address') != None):        
        _Device_Zps_Address = os.getenv('Device_Zps_Address')
    else:
        _Device_Zps_Address = config['Device_Zps_Address']
    global _Device_Zps_Port
    if (os.getenv('Device_Zps_Port') != None):        
        _Device_Zps_Port = os.getenv('Device_Zps_Port')
    else:
        _Device_Zps_Port = config['Device_Zps_Port']

    global _Device_Zps_MqttTopic
    if (os.getenv('Device_Zps_MqttTopic') != None):        
        _Device_Zps_MqttTopic = os.getenv('Device_Zps_MqttTopic')
    else:
        _Device_Zps_MqttTopic = config['Device_Zps_MqttTopic']

    # PCCO Device
    global _Device_Pcco_Enabled
    if (os.getenv('Device_Pcco_Enabled') != None):        
        _Device_Pcco_Enabled = os.getenv('Device_Pcco_Enabled') == "True"
    else:
        _Device_Pcco_Enabled = config['Device_Pcco_Enabled']

    global _Device_Pcco_Address
    if (os.getenv('_Device_Pcco_Address') != None):        
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

# PCCO2 Device
    global _Device_Pcco2_Enabled
    if (os.getenv('Device_Pcco2_Enabled') != None):        
        _Device_Pcco2_Enabled = os.getenv('Device_Pcco2_Enabled') == "True"
    else:
        _Device_Pcco2_Enabled = config['Device_Pcco2_Enabled']

    global _Device_Pcco2_Address
    if (os.getenv('_Device_Pcco2_Address') != None):        
        _Device_Pcco2_Address = os.getenv('Device_Pcco2_Address')
    else:
        _Device_Pcco2_Address = config['Device_Pcco2_Address']

    global _Device_Pcco2_Port
    if (os.getenv('Device_Pcco2_Port') != None):        
        _Device_Pcco2_Port = os.getenv('Device_Pcco2_Port')
    else:
        _Device_Pcco2_Port = config['Device_Pcco2_Port']

    global _Device_Pcco2_MqttTopic
    if (os.getenv('Device_Pcco2_MqttTopic') != None):        
        _Device_Pcco2_MqttTopic = os.getenv('Device_Pcco2_MqttTopic')
    else:
        _Device_Pcco2_MqttTopic = config['Device_Pcco2_MqttTopic']

def start_mqtt():
    global client
    logger.info('Connection in progress to the Mqtt broker (IP:' +_MQTT_ip + ' PORT:'+str(_MQTT_port)+')')
    client = mqtt.Client()
    if _MQTT_authentication:
        logger.info('Mqtt authentication enabled')
        client.username_pw_set(username=_MQTT_user, password=_MQTT_pass)
    client.on_connect = on_connect_mqtt
    client.on_disconnect = on_disconnect_mqtt
    client.on_message = on_message_mqtt        
    client.connect(_MQTT_ip, _MQTT_port)  
    if (_Device_Pcco_Enabled):
        logger.info('subscribed to : ' + _Device_Pcco_MqttTopic + '/Command/#')    
        client.subscribe(_Device_Pcco_MqttTopic + '/Command/#', qos=1)


    if (_Device_Pcco2_Enabled):
        logger.info('subscribed to : ' + _Device_Pcco2_MqttTopic + '/Command/#')    
        client.subscribe(_Device_Pcco2_MqttTopic + '/Command/#', qos=1)
        
    client.loop_start()

def on_connect_mqtt(client, userdata, flags, r):
    logger.info("Mqtt: Connected to broker. ")
    global flag_connected_mqtt
    flag_connected_mqtt = 1

def on_disconnect_mqtt(client, userdata, rc):
    logger.info("Mqtt: disconnected. ")
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
            logger.info('Recieved PCCO command ' + topic)
            writePccoConfig(command, payload)
        elif len(arr) == 3 and arr[0] == _Device_Pcco2_MqttTopic and arr[1] == 'Command':            
            command = arr[2]
            logger.info('Recieved PCCO2 command ' + topic)
            writePcco2Config(command, payload)
        else:
            logger.info('cannot process message on topic ' + topic)

    except Exception as e:
        logger.info('Exception in on_message_mqtt: '+ str(e))

def on_message_serial(obj, h, sh, m):
    logger.info('on_message_serial: obj:'+ str(obj))
    try:    
        if flag_connected_mqtt != 1:
            return False
        
        global MessageCache
        topic = _Device_Zps_MqttTopic
        if isinstance(obj, PCCO):
            topic = _Device_Pcco_MqttTopic
    
        if sh["FNC"] == 0x50:
            mp = obj.parseRegisters(sh["RestMessage"], sh["RegStart"], sh["RegLen"])        
            for item in mp.items():
                if isinstance(item[1], dict): # skipping dictionaries (time program) 
                    continue
                key = topic + '/' + str(item[0])
                val = str(item[1])
                if key not in MessageCache or MessageCache[key] != val:
                    MessageCache[key] = val
                    logger.info(key + " " + val)
                    client.publish(key, val)

    except Exception as e:
        logger.info('Exception in on_message_serial: '+ str(e))

def on_message_serial2(obj, h, sh, m):
    logger.info('on_message_serial2: obj:'+ str(obj))
    try:    
        if flag_connected_mqtt != 1:
            return False
        
        global MessageCache
        topic = _Device_Zps_MqttTopic
        if isinstance(obj, PCCO):
            topic = _Device_Pcco2_MqttTopic
    
        if sh["FNC"] == 0x50:
            mp = obj.parseRegisters(sh["RestMessage"], sh["RegStart"], sh["RegLen"])        
            for item in mp.items():
                if isinstance(item[1], dict): # skipping dictionaries (time program) 
                    continue
                key = topic + '/' + str(item[0])
                val = str(item[1])
                if key not in MessageCache or MessageCache[key] != val:
                    MessageCache[key] = val
                    logger.info(key + " " + val)
                    client.publish(key, val)

    except Exception as e:
        logger.info('Exception in on_message_serial2: '+ str(e))


def device_readregisters_enqueue():
    """Get device status every x seconds"""
    logger.info('Get device status')
    threading.Timer(get_status_interval, device_readregisters_enqueue).start()
    if _Device_Zps_Enabled:        
        readZPS()
        #readZPSConfig() dont care fot this ona ATM
    if _Device_Pcco_Enabled:        
        readPCCO()
        readPccoConfig()

    if _Device_Pcco2_Enabled:        
        readPCCO2()
        readPcco2Config()


def readZPS():
    ser = serial.serial_for_url("socket://%s:%s" % (_Device_Zps_Address, _Device_Zps_Port))
    dev = ZPS(conHardId, conSoftId, devHardId, devSoftId, on_message_serial)        
    dev.readStatusRegisters(ser)
    ser.close()

def readZPSConfig():
    ser = serial.serial_for_url("socket://%s:%s" % (_Device_Zps_Address, _Device_Zps_Port))
    dev = ZPS(conHardId, conSoftId, devHardId, devSoftId, on_message_serial)        
    dev.readStatusRegisters(ser)
    ser.close()

def printZPSMqttTopics():
    print('| Topic | Type | Description | ')
    print('| ----------------------- | ----------- | ---------------------------')
    dev = ZPS(conHardId, conSoftId, devHardId, devSoftId, on_message_serial)
    for k, v in dev.registers.items():
        if isinstance(v['name'] , list):
            for i in v['name']:
                if i:
                    print('| ' + _Device_Zps_MqttTopic + '/' + str(i)+ ' | ' + v['type'] + ' | ' + str(v.get('desc')))
        else:
            print('| ' + _Device_Zps_MqttTopic + '/' + str(v['name'])+ ' | ' + v['type'] + ' | ' + str(v.get('desc')))
        if k > dev.REG_CONFIG_START:          
            print('| ' + _Device_Zps_MqttTopic + '/Command/' + str(v['name'])+ ' | ' + v['type'] + ' | ' + str(v.get('desc')))

def readPCCO():    
    ser = serial.serial_for_url("socket://%s:%s" % (_Device_Pcco_Address, _Device_Pcco_Port))
    dev = PCCO(conHardId, conSoftId, devHardId, devSoftId, on_message_serial)        
    dev.readStatusRegisters(ser)    
    ser.close()  

def readPCCO2():  
    logger.info('READ PCCO 2')  
    ser = serial.serial_for_url("socket://%s:%s" % (_Device_Pcco2_Address, _Device_Pcco2_Port))
    dev = PCCO(conHardId2, conSoftId2, devHardId, devSoftId, on_message_serial2)        
    dev.readStatusRegisters(ser)    
    ser.close()   

def readPccoConfig():    
    ser = serial.serial_for_url("socket://%s:%s" % (_Device_Pcco_Address, _Device_Pcco_Port))
    dev = PCCO(conHardId, conSoftId, devHardId, devSoftId, on_message_serial)            
    dev.readConfigRegisters(ser)
    ser.close()

def readPcco2Config():    
    logger.info('READ PCCO CONF 2')  
    ser = serial.serial_for_url("socket://%s:%s" % (_Device_Pcco2_Address, _Device_Pcco2_Port))
    dev = PCCO(conHardId2, conSoftId2, devHardId, devSoftId, on_message_serial2)            
    dev.readConfigRegisters(ser)
    ser.close()

def writePccoConfig(registerName, payload):    
    ser = serial.serial_for_url("socket://%s:%s" % (_Device_Pcco_Address, _Device_Pcco_Port))
    dev = PCCO(conHardId2, conSoftId2, devHardId, devSoftId, on_message_serial)            
    dev.write(ser, registerName, payload)
    ser.close()

def writePcco2Config(registerName, payload):    
    ser = serial.serial_for_url("socket://%s:%s" % (_Device_Pcco2_Address, _Device_Pcco2_Port))
    dev = PCCO(conHardId2, conSoftId2, devHardId, devSoftId, on_message_serial2)            
    dev.write(ser, registerName, payload)
    ser.close()

def printPccoMqttTopics():        
    print('| Topic | Type | Description | ')
    print('| ----------------------- | ----------- | ---------------------------')
    dev = PCCO(conHardId, conSoftId, devHardId, devSoftId, on_message_serial)
    for k, v in dev.registers.items():
        if isinstance(v['name'] , list):
            for i in v['name']:
                if i:
                    print('| ' + _Device_Pcco_MqttTopic + '/' + str(i) + ' | ' + v['type'] + ' | ' + str(v.get('desc')))
        else:
            print('| ' +_Device_Pcco_MqttTopic + '/' + str(v['name'])+ ' | ' + v['type'] + ' | ' + str(v.get('desc')))
        if k > dev.REG_CONFIG_START:          
            print('| ' + _Device_Pcco_MqttTopic + '/Command/' + str(v['name']) + ' | ' + v.get('type') + ' | ' + str(v.get('desc')))

def printPcco2MqttTopics():        
    print('| Topic | Type | Description | ')
    print('| ----------------------- | ----------- | ---------------------------')
    dev = PCCO(conHardId, conSoftId, devHardId, devSoftId, on_message_serial)
    for k, v in dev.registers.items():
        if isinstance(v['name'] , list):
            for i in v['name']:
                if i:
                    print('| ' + _Device_Pcco2_MqttTopic + '/' + str(i) + ' | ' + v['type'] + ' | ' + str(v.get('desc')))
        else:
            print('| ' +_Device_Pcco2_MqttTopic + '/' + str(v['name'])+ ' | ' + v['type'] + ' | ' + str(v.get('desc')))
        if k > dev.REG_CONFIG_START:          
            print('| ' + _Device_Pcco2_MqttTopic + '/Command/' + str(v['name']) + ' | ' + v.get('type') + ' | ' + str(v.get('desc')))


if __name__ == "__main__":
    initConfiguration()
    # for generating topic list in readme
    # printPccoMqttTopics()
    # printZPSMqttTopics()
    start_mqtt()
    device_readregisters_enqueue()
