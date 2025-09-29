
from .base import BaseDevice

# Based on work by krzysztof1111111111
# https://www.elektroda.pl/rtvforum/topic3499254.html


class PCCO(BaseDevice):

    # PCCO sterowany jest za pomocą kontrolera PG-426-P04 i modułu wykonawczego MG-426-P04
    # Adresy rejestrów dla modułu wykonawczego MG-426-P04 a nie kontrolera PG-426-P04
    REG_MAX_ADR = 412
    REG_MAX_NUM = 30
    REG_CONFIG_START = 200

    registers = {

        # Status registers
        120: { 'type': 'date', 'name': 'date', 'desc': 'Date' },                      
        124: { 'type': 'time', 'name': 'time', 'desc': 'Time' },                                         
        130: { 'type': 'te10', 'name': 'T1', 'desc': 'T1 - temp. CWU [°C]' },                         
        132: { 'type': 'te10', 'name': 'T2', 'desc': 'T2 - temp. bufora CO [°C]' },                        
        134: { 'type': 'te10', 'name': 'T3', 'desc': 'T3 - temp. wody na wlocie do skraplacza [°C]' },                         
        136: { 'type': 'te10', 'name': 'T4', 'desc': 'T4 - temp. czynnika za skraplaczem [°C]' },                         
        138: { 'type': 'te10', 'name': 'T5', 'desc': 'T5 - temp. czynnika za skraplaczem2 [°C]' },                          
        140: { 'type': 'te10', 'name': 'T6', 'desc': 'T6 - temp. wody na wylocie ze skraplacza [°C]' },                          
        142: { 'type': 'te10', 'name': 'T7', 'desc': 'T7 - temp. powrotu z instalacji CO [°C]' },                         
        144: { 'type': 'te10', 'name': 'T8', 'desc': 'T8 - temp. wody na wylocie z pompy ciepła [°C]' },
        146: { 'type': 'te10', 'name': 'T9', 'desc': 'T9 - temp. powrotu cyrkulacji [°C]' },
        148: { 'type': 'te10', 'name': 'T10', 'desc': 'T10 - temp ??? [°C]' },
        150: { 'type': 'te10', 'name': 'T11', 'desc': 'T11 - temp. za mieszaczem CO / na wylocie z bufora [°C]' },
        152: { 'type': 'te10', 'name': 'T12', 'desc': 'T12 - temp. pokojowa obiegu CO1 [°C]' },
        154: { 'type': 'te10', 'name': 'T13', 'desc': 'T13 - temp. pokojowa obiegu CO2 [°C]' },
        156: { 'type': 'te10', 'name': 'T14', 'desc': 'T14 - temp. zewnętrzna [°C]' },
        
        # Config registers
        316: { 'type': 'temp', 'name': 'Zawor_rozprezny', 'desc': 'Stopień otwarcia zaworu rozprężnego' },
        318: { 'type': 'te10', 'name': 'I', 'desc': 'I - natezenie prądu [A]' },
        320: { 'type': 'te10', 'name': 'U', 'desc': 'U - napięcie zasilania [V]' },
        322: { 'type': 'temp', 'name': 'Hz', 'desc': 'Hz - częstotliwość pracy sprężarki [Hz]' },
        326: { 'type': 'te10', 'name': 'LP', 'desc': 'LP - ciśnienie czynnika w parowniku [bar]' },
        350: { 'type': 'te10', 'name': 'Ta', 'desc': 'Ta - temp. powietrza na wlocie do pomy ciepła [°C]' },
        352: { 'type': 'te10', 'name': 'Tp', 'desc': 'Tp - temp. czynnika w parowniku [°C]' },
        354: { 'type': 'te10', 'name': 'Td', 'desc': 'Td - temp. czynnika za sprężarką [°C]' },
        356: { 'type': 'te10', 'name': 'Ts', 'desc': 'Ts - temp. czynnika przed sprężarką [°C]' },
        380: { 'type': 'te10', 'name': 'HP', 'desc': 'Ts - temp. czynnika w skraplaczu [bar]' },
        
        408: { 'type': 'te10', 'name': 'cwu', 'desc': 'Temp. ustawiona CWU [°C]' },
        410: { 'type': 'te10', 'name': 'co1', 'desc': 'Temp. ustawiona CO1 [°C]' },
        412: { 'type': 'te10', 'name': 'co2', 'desc': 'Temp. ustawiona CO2 [°C]' }                                                       
    }

   # def disable(self, ser):
   #     return self.writeRegister(ser, 304, 0)

   # def enable(self, ser):
   #     return self.writeRegister(ser, 304, 1)
