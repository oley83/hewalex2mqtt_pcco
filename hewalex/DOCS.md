# home-assistant-add-on
Home Assistant add-on for Hewalex2MQTT-hvdb-cv

### Hewalex2MQTT Home Assistant Add-on

**Overview:**
The Hewalex2MQTT add-on for Home Assistant serves as a bridge between Hewalex heat pumps and the Home Assistant platform, leveraging MQTT as the communication protocol. This add-on allows users to monitor and potentially control their Hewalex heat pump directly from the Home Assistant interface.

**Key Features:**

1. **MQTT Communication**: Utilizes MQTT, a lightweight messaging protocol, to establish real-time communication between the heat pump and Home Assistant. This ensures a reliable and timely exchange of data.
  
2. **Integration with Hewalex Heat Pumps**: Designed specifically for Hewalex systems, this add-on can interpret data from the heat pump and present it in a meaningful manner within Home Assistant.
  
3. **Compatibility with Serial-to-WiFi Converters**: The add-on works seamlessly with devices like the Elfin-EW10, which connects the RS232 port of the heat pump to a WiFi network. This is the key hardware link that enables the wireless communication between the heat pump and Home Assistant.
  
4. **Real-time Monitoring**: Users can view live data from their heat pump, such as temperature readings, operating status, and potentially other metrics, depending on the capabilities of the heat pump model.
  
5. **Remote Control Capabilities**: If supported by the heat pump model, users might be able to send commands back to the heat pump via Home Assistant, allowing for remote adjustments and control of the system.
  
6. **Enhanced Automation**: With the heat pump data integrated into Home Assistant, users can set up sophisticated automations, scenarios, and triggers based on the status and readings from the heat pump.

**Benefits**:
- **Unified Control**: Centralizes the control and monitoring of various home systems, including the Hewalex heat pump, within the Home Assistant platform.
- **Increased Visibility**: Provides a clear and real-time view of the heat pump's operation, enhancing understanding and decision-making.
- **Flexibility**: MQTT's open nature and wide acceptance allow for potential integrations with other smart home devices and platforms in the future.

### Elfin-EW10 Installation Guide for Hewalex Devices

**Introduction:**
The Elfin-EW10 device serves as a bridge between the RS485 connectors in Hewalex devices and your WiFi network, allowing the integration of Hewalex devices into smart home platforms like Home Assistant.

**Materials Needed:**
1. Elfin-EW10 (WiFi to RS485 device)
2. A 4-strand wire
3. A screwdriver
4. A device for measuring AC and ground (multimeter)

#### 1. **Preparation**:
- Ensure that the Hewalex device is powered off for safety reasons.
- Gather all necessary materials.

#### 2. **Connecting to Hewalex Heat Pumps (PCWU)**:
   
   a. **Accessing the RS485 Port**:
   - Remove the heat pump's plastic casing.
   - Open the "fuse box" inside.
   - Locate the free RS485 connector and carefully remove it.
   
   b. **Connecting the Wire**:
   - Attach one end of the 4-strand wire to the RS485 connector using a screwdriver.
   - Connect the other end of the wire to the Elfin-EW10 device, ensuring the proper alignment of wires. Refer to the manual or markings on the device to know which wire goes where.
   - **Important**: Measure the AC and ground connections to ensure proper connectivity and avoid electrical issues.
   
   c. **Heat Pump Controller Settings**:
   - Navigate to the RS485 settings in the heat pump controller, labeled "Port RS485".
   - Modify the settings as follows:
     * "Transmission speed" (Baud rate) to 38400.
     * "Physical address" (Actual address) to 2.
     * "Logical address" (Logic address) to 2.

#### 3. **Connecting to Solar Pumps (ZPS)**:

   a. **Accessing the RS485 Port**:
   - Remove the G-422 controller from its casing.
   - Find the RS485 port on the G-422 controller's backside.
   
   b. **Connection**:
   - Connect the RS485 port directly to the Elfin-EW10 device.

#### 4. **Configuring Elfin-EW10**:

   a. **Setup**:
   - Turn on the Elfin-EW10 device and connect it to your WiFi network.
   - Ensure the baud rate setting in the Elfin-EW10 matches the 38400 setting in the heat pump controller.
   - Assign a static IP address to the Elfin-EW10. This ensures consistent communication without changing addresses.
   
   b. **Integration with Home Assistant**:
   - Once the Elfin-EW10 is set up and connected, you can configure the necessary MQTT parameters in Home Assistant based on the given configuration details.
   - Ensure the MQTT settings in the Home Assistant and the Elfin-EW10 device are synchronized for smooth data flow.


**Note**: Always follow safety protocols when working with electrical devices. Ensure that the devices are turned off when making connections and that you're cautious about handling wires and connectors.
The description provided is a general guide based on the information given and may require further modifications based on specific scenarios, Elfin-EW10 device versions, or any updated instructions from the manufacturer.

### Step-by-Step Guide to Configure Home Assistant for Hewalex2MQTT

1. **Access Home Assistant Settings**:
   - Launch your Home Assistant web interface.
   - Navigate to `Instellingen` (this is Dutch for "Settings").

2. **Navigate to Add-ons**:
   - From the Settings menu, select `Add-ons`.

3. **Add Repository**:
   - In the "Add-on winkel" (Dutch for "Add-on store"), look for the three dots (ellipsis) in the upper right corner and click on them.
   - From the dropdown, select `Repositories`.
   - Here you will see an option to add a new repository. Paste the link: `https://github.com/EduardWitteveen/hewalex2mqtt-homeassistant-add-on` into the given space and confirm to add this repository.

4. **Check for Updates**:
   - Once the repository is added, again click on the three dots in the "Add-on winkel".
   - This time, select `Check for updates`. This ensures that Home Assistant recognizes any new add-ons from the recently added repository.

5. **Install Hewalex2MQTT**:
   - In the search bar of the "Add-on winkel", type in "Hewalex2MQTT".
   - You should now see the `Hewalex2MQTT` add-on from the repository you added.
   - Click on it, and you'll be taken to a detailed page about the add-on.
   - Here, you will likely find an `Install` button. Click it to install the Hewalex2MQTT add-on.
   
6. **Configuration**:
   - After installation, there might be configuration options specific to the add-on where you might have to provide details related to the Elfin-EW10 device, your MQTT broker, or other settings.
   - Ensure that you fill out any necessary fields and save the configuration.

7. **Start the Add-on**:
   - Once configured, there should be an option to start the add-on. Ensure you start it so that it can begin its operation.

8. **Monitor & Control**:
   - With the add-on running, Home Assistant should now be able to communicate with the heat pump via MQTT. You can set up entities, sensors, or other integrations based on the data being provided by the add-on.

Remember to periodically check for updates to the add-on to ensure you have the latest features and security patches. As always, before making any changes, it's a good idea to have backups of your Home Assistant configuration to easily recover in case of any unforeseen issues.


## Add-on configuration:
All options from grott are available as options in this add-on. They need to follow the naming convention of the environment variables. Eg:  
```yaml
mqtt_ip: 192.168.1.10
mqtt_port: 1883
mqtt_authentication: true
mqtt_user: mqttuser
mqtt_pass: mqttpass
Device_Zps_Enabled: false
Device_Zps_Address: 192.168.1.7
Device_Zps_Port: 8899
Device_Zps_MqttTopic: SolarBoiler
Device_Pcwu_Enabled: true
Device_Pcwu_Address: 192.168.1.93
Device_Pcwu_Port: 8899
Device_Pcwu_MqttTopic: Heatpump
Device_Pcwu2_Enabled: true
Device_Pcwu2_Address: 192.168.1.93
Device_Pcwu2_Port: 8899
Device_Pcwu2_MqttTopic: Heatpump2
```
