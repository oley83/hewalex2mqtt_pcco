Pompa ciepła podłaczona jest do HA za pomocą konwertera RS485 na Ethernet poprzez broker MQTT. 
Ja używam konwerter Waveshare 23273 RS485 TO POE ETH (B) ale inne też powinny działać. Konwerter powinien być ustawiony w trybie TCP Server. 
W celu redukcji zakłuceń w komunikacji pomiędzy pompą ciepła a konwerterm RS485 do podłączenia najlepeij użyć kabla sieciowego UTP. Połączenie wykonać za pomocą jednej dowolnej pary przewodów łącząc port sygnałowy A konwerstera RS485 do Eth z portem sygnałowym A modemu Eko-Lan w pompie ciepla. Port B konwertera łączymy z portem B modemu Eko-Lan.
