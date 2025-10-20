# Home-assistant-add-on
Dodatek Home Assistant Hewalex2MQTT_PCCO

### Hewalex2MQTT dodatek do Home Assistant

**Przegląd:**
Dodatek Hewalex2MQTT do Home Assistant służy jako pomost pomiędzy pompami ciepła Hewalex PCCO Mono a platformą Home Assistant, wykorzystując MQTT jako protokół komunikacyjny. Ten dodatek umożliwia użytkownikom monitorowanie i potencjalne sterowanie pompą ciepła Hewalex PCCO Mono bezpośrednio z interfejsu Home Assistant.

**Kluczowe funkcje:**

1. **Komunikacja MQTT**: Wykorzystuje lekki protokół przesyłania wiadomości MQTT w celu ustanowienia komunikacji w czasie rzeczywistym pomiędzy pompą ciepła a Home Assistant. Zapewnia to niezawodną wymianę danych.
  
2. **Integracja z pompami ciepła Hewalex PCCO Mono**: Dodatek zaprojektowany specjalnie dla pomp ciepła Hewalex, umożliwia interpretowanie danych z pompy ciepła i prezentować je w zrozumiały sposób w Home Assistant.
  
3. **Kompatybilność z konwerterami RS485 do Enthernet**: Dodatek do działania wymaga konwertera RS485 do Enthernet. Projekt bazuje na innych projektach Hewalex2MQTT które poprawnie współpracują z konwerterami RS485 do Wi-Fi (np. Elfin-EW10) to w tym przypadku współpraca prawdopoodbnie będzie poprawna. Testowano z Waveshare 23273 RS485 TO POE ETH (B).
  
4. **Monitorowanie w czasie rzeczywistym**: Użytkownicy mogą przeglądać aktualne dane ze swojej pompy ciepła, takie jak odczyty temperatury, stan pracy i inne wskaźniki.
  
5. **Możliwości zdalnego sterowania**: Dodatek po zmodyfikowaniu pliku konfiguracji rejestrów pomy ciepła (/hewalex/hewalex_geco/devices/pcco.py) umożliwia potencjalne wysłanie polecenia z powrotem do pompy ciepła za pośrednictwem Home Assistant, umożliwiając zdalną regulację i sterowanie systemem.
  
6. **Ulepszona automatyka**: Dzięki zintegrowaniu danych z pompy ciepła z Home Assistant użytkownicy mogą konfigurować wyrafinowaną automatyzację, scenariusze i wyzwalacze w oparciu o stan i odczyty pompy ciepła.

## Konfiguracja dodatku:
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
