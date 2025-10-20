# Home-assistant-add-on
Dodatek Home Assistant Hewalex2MQTT_PCCO

### Hewalex2MQTT dodatek do Home Assistant

**Przegląd:**
Dodatek Hewalex2MQTT do Home Assistant służy jako pomost pomiędzy pompami ciepła Hewalex PCCO Mono a platformą Home Assistant, wykorzystując MQTT jako protokół komunikacyjny. Ten dodatek umożliwia użytkownikom monitorowanie i potencjalne sterowanie pompą ciepła Hewalex PCCO Mono bezpośrednio z interfejsu Home Assistant. Narazie możliwy jest odczet danych tylko ze sterownika pompy ciepła. Dane z modułu zabezpieczające PZ HX nie są pobierane.

**Kluczowe funkcje:**

1. **Komunikacja MQTT**: Wykorzystuje lekki protokół przesyłania wiadomości MQTT w celu ustanowienia komunikacji w czasie rzeczywistym pomiędzy pompą ciepła a Home Assistant. Zapewnia to niezawodną wymianę danych.
  
2. **Integracja z pompami ciepła Hewalex PCCO Mono**: Dodatek zaprojektowany specjalnie dla pomp ciepła Hewalex, umożliwia interpretowanie danych z pompy ciepła i prezentować je w zrozumiały sposób w Home Assistant.
  
3. **Kompatybilność z konwerterami RS485 do Enthernet**: Dodatek do działania wymaga konwertera RS485 do Enthernet. Projekt bazuje na innych projektach Hewalex2MQTT które poprawnie współpracują z konwerterami RS485 do Wi-Fi (np. Elfin-EW10) to w tym przypadku współpraca prawdopoodbnie będzie poprawna. Testowano z Waveshare 23273 RS485 TO POE ETH (B).
  
4. **Monitorowanie w czasie rzeczywistym**: Użytkownicy mogą przeglądać aktualne dane ze swojej pompy ciepła, takie jak odczyty temperatury, stan pracy i inne wskaźniki.
  
5. **Możliwości zdalnego sterowania**: Dodatek po zmodyfikowaniu pliku konfiguracji rejestrów pomy ciepła (/hewalex/hewalex_geco/devices/pcco.py) umożliwia potencjalne wysłanie polecenia z powrotem do pompy ciepła za pośrednictwem Home Assistant, umożliwiając zdalną regulację i sterowanie systemem.
  
6. **Ulepszona automatyka**: Dzięki zintegrowaniu danych z pompy ciepła z Home Assistant użytkownicy mogą konfigurować wyrafinowaną automatyzację, scenariusze i wyzwalacze w oparciu o stan i odczyty pompy ciepła.

## Konfiguracja dodatku:
```
mqtt_ip: core-mosquitto (ip lub nazwa hosta brokera MQTT),
mqtt_port: 1883 (port brokera MQTT),
mqtt_authentication: true (autoryzacja użytkownika MQTT),
mqtt_user: mqtt (nazwa uzytkownika MQTT),
mqtt_pass: mqtt_pwd (hasło użytkownika MQTT),
Read_only_mode: true (wyłącza możliwośc wysyłania komunikatów do pompy ciepła),
Read_config_enabled: false (odczyt rejestrów konfiguracyjnych),
Print_mqtt_topics: false (dodatek listuje w logach podczas startu wszystkie dostępne tematy MQTT),
Serial_timeout": 10  (maksymalny czas odpowiedzi w sekundach konwertera RS485),
Max_retries: 2 (ilość zapytań sterownika pompy ciepła w przybadku błędu),
Polling_interval: 60 (interwał w sekundach odpytywania sterownika pompy ciepła o wymagane dane),
Device_Pcco_Enabled: true (Włączenie komunikacji z pompą ciepła PCCO Mono),
Device_Pcco_Address: 192.168.0.70 (adres ip konwertera RS485 do Enthernet),
Device_Pcco_Port: 4196 (port konwertera RS485 do Enthernet),
Device_Pcco_MqttTopic: PCCO Mono (prefix tematu MQTT dla pompy ciepła)
```

**Dodatek powstał na bazie:**
krzysztof1111111111 (https://www.elektroda.pl/rtvforum/topic3499254.html)
hvdb/hewalex2mqtt-homeassistant-add-on-cv (https://github.com/hvdb/hewalex2mqtt-homeassistant-add-on-cv/tree/main)
ratajczykmarcin/hewalex_V2 (https://github.com/ratajczykmarcin/hewalex_V2)
